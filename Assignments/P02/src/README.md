# Data Structure Performance Analysis

Comparison of **BST**, **Linked List**, **Hash Table**, and **Sorted Array** 
across four workload types (A–D) and four sizes (1K, 5K, 10K, 20K).

All charts are grouped by workload type. Each section contains:

- **Scaling line charts** — how each metric grows as n increases
- **Per-size bar charts** — side-by-side comparison at each workload size

---

## Table of Contents

- [Understanding the Counter Values](#understanding-the-counter-values)
- [Workload A](#workload-a)
- [Workload B](#workload-b)
- [Workload C](#workload-c)
- [Workload D](#workload-d)

---

## Understanding the Counter Values

When you first look at the results, the counter numbers can seem shockingly large. A BST with 1,000,000+ comparisons, a hash table with millions of comparisons, or a sorted array with 90,000,000+ structural operations can all look like bugs. They are not. This section explains exactly why each structure produces the numbers it does.

---

### 1. The Most Important Concept: Total Cost vs. Per-Operation Cost

Big-O notation like O(log n) or O(1) describes the cost of a **single operation**. The counters in these results record the **cumulative total** across every single operation in the entire workload. These are two very different things.

For a workload of n = 10,000 that runs 20,000 operations (10,000 inserts + 10,000 lookups), even a perfectly efficient O(log n) structure accumulates a large total:

```
Each lookup on a 10,000-element BST costs ~log2(10,000) ≈ 13 comparisons
10,000 lookups × 13 comparisons each = 130,000 total comparisons

Inserts also accumulate as the tree grows:
  insert #1     → tree has 1 node     → ~1  comparison
  insert #1000  → tree has 1000 nodes  → ~10 comparisons
  insert #10000 → tree has 10000 nodes → ~13 comparisons
  Total insert comparisons ≈ sum of log(1) + log(2) + ... + log(10000)
                           ≈ 10,000 × log(10,000) / 2
                           ≈ 65,000 comparisons

Grand total ≈ 65,000 (inserts) + 130,000 (lookups) = ~195,000 comparisons
```

A raw counter of 195,000 is exactly what O(log n) predicts — it is not a bug. To recover the per-operation average and verify complexity, always divide:

```
avg comparisons per op = total_comparisons / (inserts + lookups + deletes)

Example: 195,000 / 20,000 = ~9.75 comparisons per op
         log2(10,000) ≈ 13  →  reasonable for an unbalanced BST
```

### 2. Why BST Comparisons Exceed Pure log(n)

A plain unbalanced BST has no rotations or rebalancing. Its depth depends entirely on the order elements are inserted. In the best case (random order) depth ≈ log(n). In the worst case (sorted or nearly sorted input) the tree degenerates into a linked list with depth = n, making every operation O(n) instead of O(log n).

```
Perfectly balanced BST with 10,000 nodes:
  depth = log2(10,000) ≈ 13
  avg comparisons per lookup ≈ 13

Skewed BST (partially sorted input) with 10,000 nodes:
  depth can reach 30, 40, or even hundreds
  avg comparisons per lookup grows well above 13
  total comparisons across all ops grows proportionally
```

This is why you may see BST comparison counts that are 2–5× higher than the O(n log n) theoretical minimum. The fix would be a self-balancing tree (AVL, Red-Black) which guarantees depth stays at log(n) regardless of insertion order.

### 3. Why Sorted Array Has High Structural Ops but Fast Lookups

The sorted array has a split personality — lookups are very fast but inserts and deletes are very expensive.

**Lookups — O(log n) via binary search:**

```
contains(42) on an array of 10,000 elements:
  step 1: check index 5000  → too high, search left half
  step 2: check index 2500  → too low,  search right half
  step 3: check index 3750  → too high, search left half
  ...
  found in ~13 steps regardless of where 42 lives in the array
```

This is why sorted array lookup beats linked list — a linked list has no index access and must scan from the head one node at a time (O(n)), while the sorted array can halve the search space on every step (O(log n)).

**Inserts — O(n) due to shifting:**

```
insert(42) into a sorted array of 10,000 elements:
  step 1: binary search finds insertion point at index 3750  → 13 comparisons
  step 2: shift elements 3750..9999 one position to the right → 6,250 structural ops
  step 3: place 42 at index 3750                              → 1  structural op

Across 10,000 inserts into a growing array:
  insert #1    → shift ~0    elements
  insert #5000 → shift ~2500 elements on average
  insert #10000→ shift ~5000 elements on average
  Total structural ops ≈ n²/4 ≈ 25,000,000 for n=10,000
```

This O(n²) growth in structural ops is real and correct — it is not a counter bug. It shows exactly why sorted arrays are impractical for insert-heavy workloads at large n.

### 4. Why Hash Table Lookup Can Be Worse Than Expected

A hash table promises O(1) average lookup — but that guarantee only holds when the table is properly sized relative to the number of elements stored in it. The ratio of elements to buckets is called the **load factor**:

```
load factor = number of elements / number of buckets

This implementation uses chaining (each bucket is a list).
When load factor is high, each bucket holds many elements,
and every lookup must scan that entire chain linearly.

Example — HashTable initialized with 101 buckets:
  1,000  elements →  ~10 elements per bucket  → ~10  comparisons per lookup
  5,000  elements →  ~50 elements per bucket  → ~50  comparisons per lookup
  10,000 elements →  ~99 elements per bucket  → ~99  comparisons per lookup
  20,000 elements → ~198 elements per bucket  → ~198 comparisons per lookup

Compare to a properly sized table (capacity ≈ n):
  20,000 elements in 20,011 buckets → ~1 element per bucket → ~1 comparison per lookup
```

This is why the hash table comparison counts balloon at larger workload sizes. The structure itself is not broken — it is simply undersized. To fix this, pass a capacity close to the expected element count when constructing the table:

```cpp
// Instead of: HashTable hashTable;  (defaults to 101 buckets)
HashTable hashTable(20011);  // prime number close to max expected elements
```

### 5. Why Linked List Shows 2× More Lookups Than Other Structures

The linked list `insert` method checks for duplicates by calling the public `contains()` method. Since `contains()` increments the `lookups` counter, every insert silently costs one extra lookup on top of whatever explicit `contains` calls exist in the workload:

```
Workload A with n=10,000 (10,000 inserts + 10,000 explicit lookups):

  10,000 inserts each call contains() internally → +10,000 lookups
  10,000 explicit contains() calls from workload → +10,000 lookups
  ─────────────────────────────────────────────────────────────────
  Total lookups counter = 20,000

BST / Hash Table / Sorted Array do duplicate checks inline
without calling their public contains(), so their lookup
counter only reflects the 10,000 explicit workload calls.
```

This is not necessarily wrong — the linked list genuinely does perform that extra scan on every insert. It is an accurate reflection of the real work being done, and it highlights another hidden cost of the linked list's design.

---

## Workload A

_Insert-heavy workload — primarily insertions and lookups, no deletions._

### Scaling Charts — Workload A

These charts show how each data structure scales as the workload size grows from 1,000 to 20,000 elements.

#### Comparisons — Workload A Scaling

![Comparisons scaling for Workload A](charts/line_A_comparisons.png)

#### Structural Operations — Workload A Scaling

![Structural Operations scaling for Workload A](charts/line_A_structural_ops.png)

#### Inserts — Workload A Scaling

![Inserts scaling for Workload A](charts/line_A_inserts.png)

#### Lookups — Workload A Scaling

![Lookups scaling for Workload A](charts/line_A_lookups.png)

---

### Per-Size Bar Charts — Workload A

Side-by-side comparison of all four data structures at each workload size.

#### n = 1,000

**Comparisons**

![Comparisons for Workload A n=1,000](charts/bar_A_1000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload A n=1,000](charts/bar_A_1000_structural_ops.png)

**Inserts**

![Inserts for Workload A n=1,000](charts/bar_A_1000_inserts.png)

**Lookups**

![Lookups for Workload A n=1,000](charts/bar_A_1000_lookups.png)

#### n = 5,000

**Comparisons**

![Comparisons for Workload A n=5,000](charts/bar_A_5000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload A n=5,000](charts/bar_A_5000_structural_ops.png)

**Inserts**

![Inserts for Workload A n=5,000](charts/bar_A_5000_inserts.png)

**Lookups**

![Lookups for Workload A n=5,000](charts/bar_A_5000_lookups.png)

#### n = 10,000

**Comparisons**

![Comparisons for Workload A n=10,000](charts/bar_A_10000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload A n=10,000](charts/bar_A_10000_structural_ops.png)

**Inserts**

![Inserts for Workload A n=10,000](charts/bar_A_10000_inserts.png)

**Lookups**

![Lookups for Workload A n=10,000](charts/bar_A_10000_lookups.png)

#### n = 20,000

**Comparisons**

![Comparisons for Workload A n=20,000](charts/bar_A_20000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload A n=20,000](charts/bar_A_20000_structural_ops.png)

**Inserts**

![Inserts for Workload A n=20,000](charts/bar_A_20000_inserts.png)

**Lookups**

![Lookups for Workload A n=20,000](charts/bar_A_20000_lookups.png)

---

## Workload B

_Balanced workload — mix of inserts, lookups, and deletes._

### Scaling Charts — Workload B

These charts show how each data structure scales as the workload size grows from 1,000 to 20,000 elements.

#### Comparisons — Workload B Scaling

![Comparisons scaling for Workload B](charts/line_B_comparisons.png)

#### Structural Operations — Workload B Scaling

![Structural Operations scaling for Workload B](charts/line_B_structural_ops.png)

#### Inserts — Workload B Scaling

![Inserts scaling for Workload B](charts/line_B_inserts.png)

#### Lookups — Workload B Scaling

![Lookups scaling for Workload B](charts/line_B_lookups.png)

---

### Per-Size Bar Charts — Workload B

Side-by-side comparison of all four data structures at each workload size.

#### n = 1,000

**Comparisons**

![Comparisons for Workload B n=1,000](charts/bar_B_1000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload B n=1,000](charts/bar_B_1000_structural_ops.png)

**Inserts**

![Inserts for Workload B n=1,000](charts/bar_B_1000_inserts.png)

**Lookups**

![Lookups for Workload B n=1,000](charts/bar_B_1000_lookups.png)

#### n = 5,000

**Comparisons**

![Comparisons for Workload B n=5,000](charts/bar_B_5000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload B n=5,000](charts/bar_B_5000_structural_ops.png)

**Inserts**

![Inserts for Workload B n=5,000](charts/bar_B_5000_inserts.png)

**Lookups**

![Lookups for Workload B n=5,000](charts/bar_B_5000_lookups.png)

#### n = 10,000

**Comparisons**

![Comparisons for Workload B n=10,000](charts/bar_B_10000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload B n=10,000](charts/bar_B_10000_structural_ops.png)

**Inserts**

![Inserts for Workload B n=10,000](charts/bar_B_10000_inserts.png)

**Lookups**

![Lookups for Workload B n=10,000](charts/bar_B_10000_lookups.png)

#### n = 20,000

**Comparisons**

![Comparisons for Workload B n=20,000](charts/bar_B_20000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload B n=20,000](charts/bar_B_20000_structural_ops.png)

**Inserts**

![Inserts for Workload B n=20,000](charts/bar_B_20000_inserts.png)

**Lookups**

![Lookups for Workload B n=20,000](charts/bar_B_20000_lookups.png)

---

## Workload C

_Delete-heavy workload — high proportion of deletions after insertions._

### Scaling Charts — Workload C

These charts show how each data structure scales as the workload size grows from 1,000 to 20,000 elements.

#### Comparisons — Workload C Scaling

![Comparisons scaling for Workload C](charts/line_C_comparisons.png)

#### Structural Operations — Workload C Scaling

![Structural Operations scaling for Workload C](charts/line_C_structural_ops.png)

#### Inserts — Workload C Scaling

![Inserts scaling for Workload C](charts/line_C_inserts.png)

#### Deletes — Workload C Scaling

![Deletes scaling for Workload C](charts/line_C_deletes.png)

#### Lookups — Workload C Scaling

![Lookups scaling for Workload C](charts/line_C_lookups.png)

---

### Per-Size Bar Charts — Workload C

Side-by-side comparison of all four data structures at each workload size.

#### n = 1,000

**Comparisons**

![Comparisons for Workload C n=1,000](charts/bar_C_1000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload C n=1,000](charts/bar_C_1000_structural_ops.png)

**Inserts**

![Inserts for Workload C n=1,000](charts/bar_C_1000_inserts.png)

**Deletes**

![Deletes for Workload C n=1,000](charts/bar_C_1000_deletes.png)

**Lookups**

![Lookups for Workload C n=1,000](charts/bar_C_1000_lookups.png)

#### n = 5,000

**Comparisons**

![Comparisons for Workload C n=5,000](charts/bar_C_5000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload C n=5,000](charts/bar_C_5000_structural_ops.png)

**Inserts**

![Inserts for Workload C n=5,000](charts/bar_C_5000_inserts.png)

**Deletes**

![Deletes for Workload C n=5,000](charts/bar_C_5000_deletes.png)

**Lookups**

![Lookups for Workload C n=5,000](charts/bar_C_5000_lookups.png)

#### n = 10,000

**Comparisons**

![Comparisons for Workload C n=10,000](charts/bar_C_10000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload C n=10,000](charts/bar_C_10000_structural_ops.png)

**Inserts**

![Inserts for Workload C n=10,000](charts/bar_C_10000_inserts.png)

**Deletes**

![Deletes for Workload C n=10,000](charts/bar_C_10000_deletes.png)

**Lookups**

![Lookups for Workload C n=10,000](charts/bar_C_10000_lookups.png)

#### n = 20,000

**Comparisons**

![Comparisons for Workload C n=20,000](charts/bar_C_20000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload C n=20,000](charts/bar_C_20000_structural_ops.png)

**Inserts**

![Inserts for Workload C n=20,000](charts/bar_C_20000_inserts.png)

**Deletes**

![Deletes for Workload C n=20,000](charts/bar_C_20000_deletes.png)

**Lookups**

![Lookups for Workload C n=20,000](charts/bar_C_20000_lookups.png)

---

## Workload D

_Lookup-heavy workload — many lookups relative to inserts, no deletions._

### Scaling Charts — Workload D

These charts show how each data structure scales as the workload size grows from 1,000 to 20,000 elements.

#### Comparisons — Workload D Scaling

![Comparisons scaling for Workload D](charts/line_D_comparisons.png)

#### Structural Operations — Workload D Scaling

![Structural Operations scaling for Workload D](charts/line_D_structural_ops.png)

#### Inserts — Workload D Scaling

![Inserts scaling for Workload D](charts/line_D_inserts.png)

#### Lookups — Workload D Scaling

![Lookups scaling for Workload D](charts/line_D_lookups.png)

---

### Per-Size Bar Charts — Workload D

Side-by-side comparison of all four data structures at each workload size.

#### n = 1,000

**Comparisons**

![Comparisons for Workload D n=1,000](charts/bar_D_1000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload D n=1,000](charts/bar_D_1000_structural_ops.png)

**Inserts**

![Inserts for Workload D n=1,000](charts/bar_D_1000_inserts.png)

**Lookups**

![Lookups for Workload D n=1,000](charts/bar_D_1000_lookups.png)

#### n = 5,000

**Comparisons**

![Comparisons for Workload D n=5,000](charts/bar_D_5000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload D n=5,000](charts/bar_D_5000_structural_ops.png)

**Inserts**

![Inserts for Workload D n=5,000](charts/bar_D_5000_inserts.png)

**Lookups**

![Lookups for Workload D n=5,000](charts/bar_D_5000_lookups.png)

#### n = 10,000

**Comparisons**

![Comparisons for Workload D n=10,000](charts/bar_D_10000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload D n=10,000](charts/bar_D_10000_structural_ops.png)

**Inserts**

![Inserts for Workload D n=10,000](charts/bar_D_10000_inserts.png)

**Lookups**

![Lookups for Workload D n=10,000](charts/bar_D_10000_lookups.png)

#### n = 20,000

**Comparisons**

![Comparisons for Workload D n=20,000](charts/bar_D_20000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload D n=20,000](charts/bar_D_20000_structural_ops.png)

**Inserts**

![Inserts for Workload D n=20,000](charts/bar_D_20000_inserts.png)

**Lookups**

![Lookups for Workload D n=20,000](charts/bar_D_20000_lookups.png)

---

## Data Structure Summary

The table below shows the Big-O complexity for each operation and rates each structure across the metrics tracked by the counters. 🟢 = good, 🟡 = acceptable, 🔴 = poor.

### Complexity by Operation

| Structure | Insert | Lookup | Delete | Structural Ops (per insert) | Resize Events |
|---|---|---|---|---|---|
| **BST** | O(log n) avg | O(log n) avg | O(log n) avg | O(1) — one node allocated | None |
| **Linked List** | O(n) — duplicate scan | O(n) — linear scan | O(n) — linear scan | O(1) — one node allocated/freed | None |
| **Hash Table** | O(1) avg | O(1) avg if sized correctly | O(1) avg | O(1) — one push/pop | None |
| **Sorted Array** | O(n) — shifts elements right | O(log n) — binary search | O(n) — shifts elements left | O(n) per insert → O(n²) total | O(log n) doublings |

### Strengths and Weaknesses by Metric

| Structure | Comparisons | Structural Ops | Lookup Speed | Insert Speed | Delete Speed | Memory Overhead | Scales Well? |
|---|---|---|---|---|---|---|---|
| **BST** | 🟡 O(n log n) total, higher if unbalanced | 🟢 O(1) per insert — one node created | 🟢 O(log n) per op | 🟢 O(log n) per op | 🟢 O(log n) per op | 🟡 Pointer overhead per node | 🟡 Yes if balanced, degrades if skewed |
| **Linked List** | 🔴 O(n²) total — every op scans from head | 🟢 O(1) per insert/delete — one node created/freed | 🔴 O(n) per op — no random access | 🔴 O(n) per op — duplicate scan | 🔴 O(n) per op — must find node first | 🟡 Pointer overhead per node | 🔴 No — all ops degrade linearly |
| **Hash Table** | 🟢 O(1) avg if load factor low — 🔴 O(n) if undersized | 🟢 O(1) — simple push/pop on bucket chain | 🟢 O(1) avg if properly sized | 🟢 O(1) avg if properly sized | 🟢 O(1) avg if properly sized | 🟡 Wasted bucket memory if oversized | 🟢 Yes — if capacity grows with n |
| **Sorted Array** | 🟢 O(n log n) total — binary search keeps comparisons low | 🔴 O(n²) total — every insert shifts elements | 🟢 O(log n) per op — binary search | 🔴 O(n) per op — must shift elements | 🔴 O(n) per op — must shift elements | 🟢 Compact — no pointer overhead | 🔴 No — insert/delete cost grows quadratically |

### When to Use Each Structure

| Structure | Best Used When | Avoid When |
|---|---|---|
| **BST** | You need ordered traversal and balanced insert/lookup/delete performance | Input is sorted or nearly sorted — causes skew and degrades to O(n) |
| **Linked List** | Workload is tiny or you need frequent front insertions/deletions | n is large — all ops are O(n) and comparisons grow quadratically |
| **Hash Table** | You need the fastest possible average-case lookup and insert | You need ordered data, or capacity is much smaller than n |
| **Sorted Array** | Workload is lookup-heavy and insert/delete are rare | Insert or delete frequency is high — structural ops grow as O(n²) |
