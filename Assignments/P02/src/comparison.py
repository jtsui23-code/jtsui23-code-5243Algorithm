import json
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ── Config ────────────────────────────────────────────────────────────────────

RESULTS_DIR = "results"
CHARTS_DIR  = "charts"

STRUCTURES = {
    "bst":         "BST",
    "linkedlist":  "Linked List",
    "hashtable":   "Hash Table",
    "sortedarray": "Sorted Array",
}

WORKLOAD_TYPES = ["A", "B", "C", "D"]
SIZES          = [1000, 5000, 10000, 20000]

METRICS = ["comparisons", "structural_ops", "inserts", "deletes", "lookups"]

COLORS = {
    "bst":         "#4C72B0",
    "linkedlist":  "#DD8452",
    "hashtable":   "#55A868",
    "sortedarray": "#C44E52",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_result(struct_key: str, wtype: str, size: int) -> dict | None:
    fname = f"{struct_key}_results_{wtype}_{size}.json"
    path  = os.path.join(RESULTS_DIR, fname)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def fmt_number(n: float) -> str:
    """Human-readable axis labels: 1.2M, 45K, etc."""
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.0f}K"
    return str(int(n))


def make_bar_chart(title: str, metric: str, labels: list[str],
                   values: dict[str, float], save_path: str) -> None:
    """Single grouped bar chart: one group per structure for one workload."""
    structs  = list(STRUCTURES.keys())
    x        = np.arange(len(structs))
    bar_vals = [values.get(s, 0) for s in structs]
    colors   = [COLORS[s] for s in structs]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(x, bar_vals, color=colors, width=0.5, edgecolor="white", linewidth=0.8)

    # Value labels on top of bars
    for bar, val in zip(bars, bar_vals):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() * 1.02,
                    fmt_number(val),
                    ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels([STRUCTURES[s] for s in structs], fontsize=11)
    ax.set_ylabel(metric.replace("_", " ").title(), fontsize=11)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: fmt_number(v)))
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_ylim(0, max(bar_vals) * 1.15 if max(bar_vals) > 0 else 1)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


def make_line_chart(title: str, metric: str, wtype: str,
                    data: dict[str, dict[int, float]], save_path: str) -> None:
    """Line chart: one line per structure, x-axis = sizes."""
    fig, ax = plt.subplots(figsize=(9, 5))

    for struct_key, size_map in data.items():
        xs = sorted(size_map.keys())
        ys = [size_map[x] for x in xs]
        ax.plot(xs, ys,
                marker="o", linewidth=2, markersize=6,
                label=STRUCTURES[struct_key],
                color=COLORS[struct_key])

    ax.set_xlabel("Workload Size (n)", fontsize=11)
    ax.set_ylabel(metric.replace("_", " ").title(), fontsize=11)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: fmt_number(v)))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: fmt_number(v)))
    ax.legend(fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(CHARTS_DIR, exist_ok=True)
    generated = 0

    # ── 1. Per-workload bar charts (one chart per type+size+metric) ────────────
    for wtype in WORKLOAD_TYPES:
        for size in SIZES:
            # Load all four structures for this workload
            results = {}
            for sk in STRUCTURES:
                r = load_result(sk, wtype, size)
                if r:
                    results[sk] = r

            if not results:
                print(f"  No data for workload {wtype}_{size}, skipping.")
                continue

            for metric in METRICS:
                values = {sk: r.get(metric, 0) for sk, r in results.items()}

                # Skip charts where all values are zero (e.g. no deletes in type A)
                if all(v == 0 for v in values.values()):
                    continue

                title     = f"Workload {wtype} — n={size:,}  |  {metric.replace('_',' ').title()}"
                save_path = os.path.join(CHARTS_DIR, f"bar_{wtype}_{size}_{metric}.png")
                make_bar_chart(title, metric, list(STRUCTURES.keys()), values, save_path)
                generated += 1
                print(f"  Saved {save_path}")

    # ── 2. Scaling line charts (one per type+metric, x = size) ────────────────
    for wtype in WORKLOAD_TYPES:
        for metric in METRICS:
            # Build {struct -> {size -> value}}
            data: dict[str, dict[int, float]] = {sk: {} for sk in STRUCTURES}
            any_data = False

            for size in SIZES:
                for sk in STRUCTURES:
                    r = load_result(sk, wtype, size)
                    if r and metric in r:
                        data[sk][size] = r[metric]
                        any_data = True

            if not any_data:
                continue

            # Drop structures with no data points
            data = {sk: v for sk, v in data.items() if v}

            # Skip if all values across all sizes are zero
            all_zero = all(v == 0 for sm in data.values() for v in sm.values())
            if all_zero:
                continue

            title     = f"Workload {wtype} — Scaling  |  {metric.replace('_',' ').title()}"
            save_path = os.path.join(CHARTS_DIR, f"line_{wtype}_{metric}.png")
            make_line_chart(title, metric, wtype, data, save_path)
            generated += 1
            print(f"  Saved {save_path}")

    print(f"\nDone — {generated} charts saved to '{CHARTS_DIR}/'")


if __name__ == "__main__":
    main()