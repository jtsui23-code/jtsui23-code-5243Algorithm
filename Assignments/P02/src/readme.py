import os

CHARTS_DIR = "charts"
README_PATH = "README.md"

WORKLOAD_TYPES = ["A", "B", "C", "D"]
SIZES = [1000, 5000, 10000, 20000]
METRICS = ["comparisons", "structural_ops", "inserts", "deletes", "lookups"]

METRIC_LABELS = {
    "comparisons":   "Comparisons",
    "structural_ops": "Structural Operations",
    "inserts":       "Inserts",
    "deletes":       "Deletes",
    "lookups":       "Lookups",
}

WORKLOAD_DESCRIPTIONS = {
    "A": "Insert-heavy workload — primarily insertions and lookups, no deletions.",
    "B": "Balanced workload — mix of inserts, lookups, and deletes.",
    "C": "Delete-heavy workload — high proportion of deletions after insertions.",
    "D": "Lookup-heavy workload — many lookups relative to inserts, no deletions.",
}

STRUCTURE_LABELS = {
    "bst":         "BST",
    "linkedlist":  "Linked List",
    "hashtable":   "Hash Table",
    "sortedarray": "Sorted Array",
}


def chart_exists(filename: str) -> bool:
    return os.path.exists(os.path.join(CHARTS_DIR, filename))


def main():
    lines = []

    # ── Title & Overview ──────────────────────────────────────────────────────
    lines.append("# Data Structure Performance Analysis\n")
    lines.append("Comparison of **BST**, **Linked List**, **Hash Table**, and **Sorted Array** ")
    lines.append("across four workload types (A–D) and four sizes (1K, 5K, 10K, 20K).\n")
    lines.append("All charts are grouped by workload type. Each section contains:\n")
    lines.append("- **Scaling line charts** — how each metric grows as n increases")
    lines.append("- **Per-size bar charts** — side-by-side comparison at each workload size\n")

    lines.append("---\n")

    # ── Table of Contents ─────────────────────────────────────────────────────
    lines.append("## Table of Contents\n")
    for wtype in WORKLOAD_TYPES:
        lines.append(f"- [Workload {wtype}](#{f'workload-{wtype.lower()}'})")
    lines.append("")
    lines.append("---\n")

    # ── Per Workload Section ──────────────────────────────────────────────────
    for wtype in WORKLOAD_TYPES:
        lines.append(f"## Workload {wtype}\n")
        lines.append(f"_{WORKLOAD_DESCRIPTIONS[wtype]}_\n")

        # ── Scaling Line Charts ───────────────────────────────────────────────
        lines.append(f"### Scaling Charts — Workload {wtype}\n")
        lines.append("These charts show how each data structure scales as the workload size grows from 1,000 to 20,000 elements.\n")

        has_line_charts = False
        for metric in METRICS:
            fname = f"line_{wtype}_{metric}.png"
            if chart_exists(fname):
                has_line_charts = True
                lines.append(f"#### {METRIC_LABELS[metric]} — Workload {wtype} Scaling\n")
                lines.append(f"![{METRIC_LABELS[metric]} scaling for Workload {wtype}]({CHARTS_DIR}/{fname})\n")

        if not has_line_charts:
            lines.append("_No scaling charts found for this workload._\n")

        lines.append("---\n")

        # ── Per Size Bar Charts ───────────────────────────────────────────────
        lines.append(f"### Per-Size Bar Charts — Workload {wtype}\n")
        lines.append("Side-by-side comparison of all four data structures at each workload size.\n")

        for size in SIZES:
            size_label = f"{size:,}"
            has_charts_for_size = any(
                chart_exists(f"bar_{wtype}_{size}_{metric}.png")
                for metric in METRICS
            )

            if not has_charts_for_size:
                continue

            lines.append(f"#### n = {size_label}\n")

            for metric in METRICS:
                fname = f"bar_{wtype}_{size}_{metric}.png"
                if chart_exists(fname):
                    lines.append(f"**{METRIC_LABELS[metric]}**\n")
                    lines.append(f"![{METRIC_LABELS[metric]} for Workload {wtype} n={size_label}]({CHARTS_DIR}/{fname})\n")

        lines.append("---\n")

    # ── Structure Summary ─────────────────────────────────────────────────────
    lines.append("## Data Structure Summary\n")
    lines.append("| Structure | Insert | Lookup | Delete | Notes |")
    lines.append("|---|---|---|---|---|")
    lines.append("| BST | O(log n) avg | O(log n) avg | O(log n) avg | Degrades to O(n) if unbalanced |")
    lines.append("| Linked List | O(n) | O(n) | O(n) | Simple but slow at scale |")
    lines.append("| Hash Table | O(1) avg | O(1) avg | O(1) avg | Performance depends on load factor |")
    lines.append("| Sorted Array | O(n) | O(log n) | O(n) | Fast lookup, expensive insert/delete |")
    lines.append("")

    # ── Write file ────────────────────────────────────────────────────────────
    with open(README_PATH, "w") as f:
        f.write("\n".join(lines))

    print(f"README.md generated at '{README_PATH}'")


if __name__ == "__main__":
    main()