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
    lines.append("- [Understanding the Counter Values](#understanding-the-counter-values)")
    for wtype in WORKLOAD_TYPES:
        lines.append(f"- [Workload {wtype}](#{f'workload-{wtype.lower()}'})")
    lines.append("")
    lines.append("---\n")

    # ── In-depth Explanation ──────────────────────────────────────────────────
    lines.append("## Understanding the Counter Values\n")
    lines.append(
        "When you first look at the results, the counter numbers can seem shockingly large. "
        "A BST with 1,000,000+ comparisons, a hash table with millions of comparisons, or a sorted array "
        "with 90,000,000+ structural operations can all look like bugs. They are not. "
        "This section explains exactly why each structure produces the numbers it does.\n"
    )

    lines.append("---\n")

    # 1. Total vs per-op
    lines.append("### 1. The Most Important Concept: Total Cost vs. Per-Operation Cost\n")
    lines.append(
        "Big-O notation like O(log n) or O(1) describes the cost of a **single operation**. "
        "The counters in these results record the **cumulative total** across every single operation "
        "in the entire workload. These are two very different things.\n"
    )
    lines.append(
        "For a workload of n = 10,000 that runs 20,000 operations (10,000 inserts + 10,000 lookups), "
        "even a perfectly efficient O(log n) structure accumulates a large total:\n"
    )
    lines.append("```")
    lines.append("Each lookup on a 10,000-element BST costs ~log2(10,000) ≈ 13 comparisons")
    lines.append("10,000 lookups × 13 comparisons each = 130,000 total comparisons")
    lines.append("")
    lines.append("Inserts also accumulate as the tree grows:")
    lines.append("  insert #1     → tree has 1 node     → ~1  comparison")
    lines.append("  insert #1000  → tree has 1000 nodes  → ~10 comparisons")
    lines.append("  insert #10000 → tree has 10000 nodes → ~13 comparisons")
    lines.append("  Total insert comparisons ≈ sum of log(1) + log(2) + ... + log(10000)")
    lines.append("                           ≈ 10,000 × log(10,000) / 2")
    lines.append("                           ≈ 65,000 comparisons")
    lines.append("")
    lines.append("Grand total ≈ 65,000 (inserts) + 130,000 (lookups) = ~195,000 comparisons")
    lines.append("```\n")
    lines.append(
        "A raw counter of 195,000 is exactly what O(log n) predicts — it is not a bug. "
        "To recover the per-operation average and verify complexity, always divide:\n"
    )
    lines.append("```")
    lines.append("avg comparisons per op = total_comparisons / (inserts + lookups + deletes)")
    lines.append("")
    lines.append("Example: 195,000 / 20,000 = ~9.75 comparisons per op")
    lines.append("         log2(10,000) ≈ 13  →  reasonable for an unbalanced BST")
    lines.append("```\n")

    # 2. BST
    lines.append("### 2. Why BST Comparisons Exceed Pure log(n)\n")
    lines.append(
        "A plain unbalanced BST has no rotations or rebalancing. Its depth depends entirely on "
        "the order elements are inserted. In the best case (random order) depth ≈ log(n). "
        "In the worst case (sorted or nearly sorted input) the tree degenerates into a linked list "
        "with depth = n, making every operation O(n) instead of O(log n).\n"
    )
    lines.append("```")
    lines.append("Perfectly balanced BST with 10,000 nodes:")
    lines.append("  depth = log2(10,000) ≈ 13")
    lines.append("  avg comparisons per lookup ≈ 13")
    lines.append("")
    lines.append("Skewed BST (partially sorted input) with 10,000 nodes:")
    lines.append("  depth can reach 30, 40, or even hundreds")
    lines.append("  avg comparisons per lookup grows well above 13")
    lines.append("  total comparisons across all ops grows proportionally")
    lines.append("```\n")
    lines.append(
        "This is why you may see BST comparison counts that are 2–5× higher than the O(n log n) "
        "theoretical minimum. The fix would be a self-balancing tree (AVL, Red-Black) which "
        "guarantees depth stays at log(n) regardless of insertion order.\n"
    )

    # 3. Sorted Array
    lines.append("### 3. Why Sorted Array Has High Structural Ops but Fast Lookups\n")
    lines.append(
        "The sorted array has a split personality — lookups are very fast but inserts and deletes are very expensive.\n"
    )
    lines.append("**Lookups — O(log n) via binary search:**\n")
    lines.append("```")
    lines.append("contains(42) on an array of 10,000 elements:")
    lines.append("  step 1: check index 5000  → too high, search left half")
    lines.append("  step 2: check index 2500  → too low,  search right half")
    lines.append("  step 3: check index 3750  → too high, search left half")
    lines.append("  ...")
    lines.append("  found in ~13 steps regardless of where 42 lives in the array")
    lines.append("```\n")
    lines.append(
        "This is why sorted array lookup beats linked list — a linked list has no index access "
        "and must scan from the head one node at a time (O(n)), while the sorted array can "
        "halve the search space on every step (O(log n)).\n"
    )
    lines.append("**Inserts — O(n) due to shifting:**\n")
    lines.append("```")
    lines.append("insert(42) into a sorted array of 10,000 elements:")
    lines.append("  step 1: binary search finds insertion point at index 3750  → 13 comparisons")
    lines.append("  step 2: shift elements 3750..9999 one position to the right → 6,250 structural ops")
    lines.append("  step 3: place 42 at index 3750                              → 1  structural op")
    lines.append("")
    lines.append("Across 10,000 inserts into a growing array:")
    lines.append("  insert #1    → shift ~0    elements")
    lines.append("  insert #5000 → shift ~2500 elements on average")
    lines.append("  insert #10000→ shift ~5000 elements on average")
    lines.append("  Total structural ops ≈ n²/4 ≈ 25,000,000 for n=10,000")
    lines.append("```\n")
    lines.append(
        "This O(n²) growth in structural ops is real and correct — it is not a counter bug. "
        "It shows exactly why sorted arrays are impractical for insert-heavy workloads at large n.\n"
    )

    # 4. Hash Table
    lines.append("### 4. Why Hash Table Lookup Can Be Worse Than Expected\n")
    lines.append(
        "A hash table promises O(1) average lookup — but that guarantee only holds when the "
        "table is properly sized relative to the number of elements stored in it. "
        "The ratio of elements to buckets is called the **load factor**:\n"
    )
    lines.append("```")
    lines.append("load factor = number of elements / number of buckets")
    lines.append("")
    lines.append("This implementation uses chaining (each bucket is a list).")
    lines.append("When load factor is high, each bucket holds many elements,")
    lines.append("and every lookup must scan that entire chain linearly.")
    lines.append("")
    lines.append("Example — HashTable initialized with 101 buckets:")
    lines.append("  1,000  elements →  ~10 elements per bucket  → ~10  comparisons per lookup")
    lines.append("  5,000  elements →  ~50 elements per bucket  → ~50  comparisons per lookup")
    lines.append("  10,000 elements →  ~99 elements per bucket  → ~99  comparisons per lookup")
    lines.append("  20,000 elements → ~198 elements per bucket  → ~198 comparisons per lookup")
    lines.append("")
    lines.append("Compare to a properly sized table (capacity ≈ n):")
    lines.append("  20,000 elements in 20,011 buckets → ~1 element per bucket → ~1 comparison per lookup")
    lines.append("```\n")
    lines.append(
        "This is why the hash table comparison counts balloon at larger workload sizes. "
        "The structure itself is not broken — it is simply undersized. "
        "To fix this, pass a capacity close to the expected element count when constructing the table:\n"
    )
    lines.append("```cpp")
    lines.append("// Instead of: HashTable hashTable;  (defaults to 101 buckets)")
    lines.append("HashTable hashTable(20011);  // prime number close to max expected elements")
    lines.append("```\n")

    # 5. Linked List double-counting
    lines.append("### 5. Why Linked List Shows 2× More Lookups Than Other Structures\n")
    lines.append(
        "The linked list `insert` method checks for duplicates by calling the public `contains()` method. "
        "Since `contains()` increments the `lookups` counter, every insert silently costs one extra lookup "
        "on top of whatever explicit `contains` calls exist in the workload:\n"
    )
    lines.append("```")
    lines.append("Workload A with n=10,000 (10,000 inserts + 10,000 explicit lookups):")
    lines.append("")
    lines.append("  10,000 inserts each call contains() internally → +10,000 lookups")
    lines.append("  10,000 explicit contains() calls from workload → +10,000 lookups")
    lines.append("  ─────────────────────────────────────────────────────────────────")
    lines.append("  Total lookups counter = 20,000")
    lines.append("")
    lines.append("BST / Hash Table / Sorted Array do duplicate checks inline")
    lines.append("without calling their public contains(), so their lookup")
    lines.append("counter only reflects the 10,000 explicit workload calls.")
    lines.append("```\n")
    lines.append(
        "This is not necessarily wrong — the linked list genuinely does perform that extra scan "
        "on every insert. It is an accurate reflection of the real work being done, and it "
        "highlights another hidden cost of the linked list's design.\n"
    )

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
    lines.append(
        "The table below shows the Big-O complexity for each operation and rates each structure "
        "across the metrics tracked by the counters. "
        "🟢 = good, 🟡 = acceptable, 🔴 = poor.\n"
    )

    # Complexity table
    lines.append("### Complexity by Operation\n")
    lines.append("| Structure | Insert | Lookup | Delete | Structural Ops (per insert) | Resize Events |")
    lines.append("|---|---|---|---|---|---|")
    lines.append("| **BST** | O(log n) avg | O(log n) avg | O(log n) avg | O(1) — one node allocated | None |")
    lines.append("| **Linked List** | O(n) — duplicate scan | O(n) — linear scan | O(n) — linear scan | O(1) — one node allocated/freed | None |")
    lines.append("| **Hash Table** | O(1) avg | O(1) avg if sized correctly | O(1) avg | O(1) — one push/pop | None |")
    lines.append("| **Sorted Array** | O(n) — shifts elements right | O(log n) — binary search | O(n) — shifts elements left | O(n) per insert → O(n²) total | O(log n) doublings |")
    lines.append("")

    # Strengths and weaknesses ratings table
    lines.append("### Strengths and Weaknesses by Metric\n")
    lines.append("| Structure | Comparisons | Structural Ops | Lookup Speed | Insert Speed | Delete Speed | Memory Overhead | Scales Well? |")
    lines.append("|---|---|---|---|---|---|---|---|")
    lines.append("| **BST** | 🟡 O(n log n) total, higher if unbalanced | 🟢 O(1) per insert — one node created | 🟢 O(log n) per op | 🟢 O(log n) per op | 🟢 O(log n) per op | 🟡 Pointer overhead per node | 🟡 Yes if balanced, degrades if skewed |")
    lines.append("| **Linked List** | 🔴 O(n²) total — every op scans from head | 🟢 O(1) per insert/delete — one node created/freed | 🔴 O(n) per op — no random access | 🔴 O(n) per op — duplicate scan | 🔴 O(n) per op — must find node first | 🟡 Pointer overhead per node | 🔴 No — all ops degrade linearly |")
    lines.append("| **Hash Table** | 🟢 O(1) avg if load factor low — 🔴 O(n) if undersized | 🟢 O(1) — simple push/pop on bucket chain | 🟢 O(1) avg if properly sized | 🟢 O(1) avg if properly sized | 🟢 O(1) avg if properly sized | 🟡 Wasted bucket memory if oversized | 🟢 Yes — if capacity grows with n |")
    lines.append("| **Sorted Array** | 🟢 O(n log n) total — binary search keeps comparisons low | 🔴 O(n²) total — every insert shifts elements | 🟢 O(log n) per op — binary search | 🔴 O(n) per op — must shift elements | 🔴 O(n) per op — must shift elements | 🟢 Compact — no pointer overhead | 🔴 No — insert/delete cost grows quadratically |")
    lines.append("")

    # Best use case summary
    lines.append("### When to Use Each Structure\n")
    lines.append("| Structure | Best Used When | Avoid When |")
    lines.append("|---|---|---|")
    lines.append("| **BST** | You need ordered traversal and balanced insert/lookup/delete performance | Input is sorted or nearly sorted — causes skew and degrades to O(n) |")
    lines.append("| **Linked List** | Workload is tiny or you need frequent front insertions/deletions | n is large — all ops are O(n) and comparisons grow quadratically |")
    lines.append("| **Hash Table** | You need the fastest possible average-case lookup and insert | You need ordered data, or capacity is much smaller than n |")
    lines.append("| **Sorted Array** | Workload is lookup-heavy and insert/delete are rare | Insert or delete frequency is high — structural ops grow as O(n²) |")
    lines.append("")

    # ── Write file ────────────────────────────────────────────────────────────
    with open(README_PATH, "w") as f:
        f.write("\n".join(lines))

    print(f"README.md generated at '{README_PATH}'")


if __name__ == "__main__":
    main()