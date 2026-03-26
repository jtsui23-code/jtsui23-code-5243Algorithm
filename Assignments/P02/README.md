## Program 2 - Comparing Lookup Type Data Structures

### Provided to You

There are c++ implementations for:

- Binary Search Tree
- Hash Table
- Linked List
- Ordered Dynamic Array

with all necessary basic functionality and small tests to show how to use each of them.
There is no additional code added to count any of the stats we want to collect for comparing different data structures and how they handle certain types of behaviors (insert, find, delete). Below is the new folder structure:

### Deliverable

|  #  |  Link |  Description |
| :-: | ----------- | ---------------------- |
|  1  | — | Made driver scripts for Hash Table, Linked List, and Ordered Dynamic Array |
|  2  | — | Updated BST, Hash Table, Linked List, and Ordered Dynamic Array to include `runJobFiles()` and Counters |
|  3  | [makework.py](https://github.com/jtsui23-code/jtsui23-code-5243Algorithm/blob/main/Assignments/P02/src/makework.py) | Python script that creates workloads using the compiled workload generator |
|  4  | [count_json.py](https://github.com/jtsui23-code/jtsui23-code-5243Algorithm/blob/main/Assignments/P02/src/count_json.py) | Compiled workload generator used to produce workload data |
|  5  | [runexperiments.sh](https://github.com/jtsui23-code/jtsui23-code-5243Algorithm/blob/main/Assignments/P02/src/runexperiments.sh) | Bash script that runs the driver files with generated workloads |
|  6  | — | From `./jtsui23-code-5243Algorithm/Assignments/P02/src/`, run `./runexperiments.sh` to generate comparison JSON files |
|  7  | [charts](https://github.com/jtsui23-code/jtsui23-code-5243Algorithm/tree/main/Assignments/P02/src/charts) | Contains charts comparing data structures |
|  8  | [results](https://github.com/jtsui23-code/jtsui23-code-5243Algorithm/tree/main/Assignments/P02/src/results) | Contains JSON results comparing data structures |


# Data Structure Performance Analysis

Comparison of **BST**, **Linked List**, **Hash Table**, and **Sorted Array** 
across four workload types (A–D) and four sizes (1K, 5K, 10K, 20K).

All charts are grouped by workload type. Each section contains:

- **Scaling line charts** — how each metric grows as n increases
- **Per-size bar charts** — side-by-side comparison at each workload size

---



### When to Use Each Structure

| Structure | Best Used When | Avoid When |
|---|---|---|
| **BST** | You need ordered traversal and balanced insert/lookup/delete performance | Input is sorted or nearly sorted — causes skew and degrades to O(n) |
| **Linked List** | Workload is tiny or you need frequent front insertions/deletions | n is large — all ops are O(n) and comparisons grow quadratically |
| **Hash Table** | You need the fastest possible average-case lookup and insert | You need ordered data, or capacity is much smaller than n |
| **Sorted Array** | Workload is lookup-heavy and insert/delete are rare | Insert or delete frequency is high — structural ops grow as O(n²) |

## Table of Contents

- [Understanding the Counter Values](#understanding-the-counter-values)
- [Workload A](#workload-a)
- [Workload B](#workload-b)
- [Workload C](#workload-c)
- [Workload D](#workload-d)

---

## Understanding the Counter Values

The counter numbers can seem large like a BST with 1,000,000+ comparisons, a hash table with millions of comparisons, or a sorted array with 90,000,000+ structural operations can all look like bugs. This section explains exactly why each structure produces the numbers it does.

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

This is why you may see BST comparison counts that are 2–5× higher than the O(n log n) theoretical minimum. The fix would be a self-balancing tree (AVL, Red-Black) which guarantees depth stays at log(n) regardless of insertion order.

### 3. Why Sorted Array Has High Structural Ops but Fast Lookups

Lookups are very fast, but inserts and deletes are very expensive.

**Lookups — O(log n) using binary search:**


This is why sorted array lookup beats linked list — a linked list has no index access and must scan from the head one node at a time (O(n)), while the sorted array can halve the search space on every step (O(log n)).

**Inserts — O(n) due to shifting:**

```

Across 10,000 inserts into a growing array:
  insert #1    → shift ~0    elements
  insert #5000 → shift ~2500 elements on average
  insert #10000→ shift ~5000 elements on average
  Total structural ops ≈ n²/4 ≈ 25,000,000 for n=10,000
```


### 4. Why Hash Table Lookup Can Be Worse Than Expected

A hash table promises O(1) average lookup — but that guarantee only holds when the table is properly sized relative to the number of elements stored in it. 

This is why the hash table comparison counts balloon at larger workload sizes because it is simply undersized. 

### 5. Why Linked List Shows 2× More Lookups Than Other Structures

The linked list `insert` method checks for duplicates by calling the public `contains()` method. Since `contains()` increments the `lookups` counter, every insert silently costs one extra lookup on top of whatever explicit `contains` calls exist in the workload:


---

## Data Structure Summary

| Structure | Insert | Lookup | Delete | Notes |
|---|---|---|---|---|
| BST | O(log n) avg | O(log n) avg | O(log n) avg | Degrades to O(n) if unbalanced |
| Linked List | O(n) | O(n) | O(n) | Simple but slow at scale |
| Hash Table | O(1) avg | O(1) avg | O(1) avg | Performance depends on load factor |
| Sorted Array | O(n) | O(log n) | O(n) | Fast lookup, expensive insert/delete |

---
## Workload A

_Insert-heavy workload — primarily insertions and lookups, no deletions._

### Scaling Charts — Workload A

These charts show how each data structure scales as the workload size grows from 1,000 to 20,000 elements.

#### Comparisons — Workload A Scaling

![Comparisons scaling for Workload A](src/charts/line_A_comparisons.png)

#### Structural Operations — Workload A Scaling

![Structural Operations scaling for Workload A](src/charts/line_A_structural_ops.png)

#### Inserts — Workload A Scaling

![Inserts scaling for Workload A](src/charts/line_A_inserts.png)

#### Lookups — Workload A Scaling

![Lookups scaling for Workload A](src/charts/line_A_lookups.png)

---

### Per-Size Bar Charts — Workload A

Side-by-side comparison of all four data structures at each workload size.

#### n = 1,000

**Comparisons**

![Comparisons for Workload A n=1,000](src/charts/bar_A_1000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload A n=1,000](src/charts/bar_A_1000_structural_ops.png)

**Inserts**

![Inserts for Workload A n=1,000](src/charts/bar_A_1000_inserts.png)

**Lookups**

![Lookups for Workload A n=1,000](src/charts/bar_A_1000_lookups.png)

#### n = 5,000

**Comparisons**

![Comparisons for Workload A n=5,000](src/charts/bar_A_5000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload A n=5,000](src/charts/bar_A_5000_structural_ops.png)

**Inserts**

![Inserts for Workload A n=5,000](src/charts/bar_A_5000_inserts.png)

**Lookups**

![Lookups for Workload A n=5,000](src/charts/bar_A_5000_lookups.png)

#### n = 10,000

**Comparisons**

![Comparisons for Workload A n=10,000](src/charts/bar_A_10000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload A n=10,000](src/charts/bar_A_10000_structural_ops.png)

**Inserts**

![Inserts for Workload A n=10,000](src/charts/bar_A_10000_inserts.png)

**Lookups**

![Lookups for Workload A n=10,000](src/charts/bar_A_10000_lookups.png)

#### n = 20,000

**Comparisons**

![Comparisons for Workload A n=20,000](src/charts/bar_A_20000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload A n=20,000](src/charts/bar_A_20000_structural_ops.png)

**Inserts**

![Inserts for Workload A n=20,000](src/charts/bar_A_20000_inserts.png)

**Lookups**

![Lookups for Workload A n=20,000](src/charts/bar_A_20000_lookups.png)

---

## Workload B

_Balanced workload — mix of inserts, lookups, and deletes._

### Scaling Charts — Workload B

These charts show how each data structure scales as the workload size grows from 1,000 to 20,000 elements.

#### Comparisons — Workload B Scaling

![Comparisons scaling for Workload B](src/charts/line_B_comparisons.png)

#### Structural Operations — Workload B Scaling

![Structural Operations scaling for Workload B](src/charts/line_B_structural_ops.png)

#### Inserts — Workload B Scaling

![Inserts scaling for Workload B](src/charts/line_B_inserts.png)

#### Lookups — Workload B Scaling

![Lookups scaling for Workload B](src/charts/line_B_lookups.png)

---

### Per-Size Bar Charts — Workload B

Side-by-side comparison of all four data structures at each workload size.

#### n = 1,000

**Comparisons**

![Comparisons for Workload B n=1,000](src/charts/bar_B_1000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload B n=1,000](src/charts/bar_B_1000_structural_ops.png)

**Inserts**

![Inserts for Workload B n=1,000](src/charts/bar_B_1000_inserts.png)

**Lookups**

![Lookups for Workload B n=1,000](src/charts/bar_B_1000_lookups.png)

#### n = 5,000

**Comparisons**

![Comparisons for Workload B n=5,000](src/charts/bar_B_5000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload B n=5,000](src/charts/bar_B_5000_structural_ops.png)

**Inserts**

![Inserts for Workload B n=5,000](src/charts/bar_B_5000_inserts.png)

**Lookups**

![Lookups for Workload B n=5,000](src/charts/bar_B_5000_lookups.png)

#### n = 10,000

**Comparisons**

![Comparisons for Workload B n=10,000](src/charts/bar_B_10000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload B n=10,000](src/charts/bar_B_10000_structural_ops.png)

**Inserts**

![Inserts for Workload B n=10,000](src/charts/bar_B_10000_inserts.png)

**Lookups**

![Lookups for Workload B n=10,000](src/charts/bar_B_10000_lookups.png)

#### n = 20,000

**Comparisons**

![Comparisons for Workload B n=20,000](src/charts/bar_B_20000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload B n=20,000](src/charts/bar_B_20000_structural_ops.png)

**Inserts**

![Inserts for Workload B n=20,000](src/charts/bar_B_20000_inserts.png)

**Lookups**

![Lookups for Workload B n=20,000](src/charts/bar_B_20000_lookups.png)

---

## Workload C

_Delete-heavy workload — high proportion of deletions after insertions._

### Scaling Charts — Workload C

These charts show how each data structure scales as the workload size grows from 1,000 to 20,000 elements.

#### Comparisons — Workload C Scaling

![Comparisons scaling for Workload C](src/charts/line_C_comparisons.png)

#### Structural Operations — Workload C Scaling

![Structural Operations scaling for Workload C](src/charts/line_C_structural_ops.png)

#### Inserts — Workload C Scaling

![Inserts scaling for Workload C](src/charts/line_C_inserts.png)

#### Deletes — Workload C Scaling

![Deletes scaling for Workload C](src/charts/line_C_deletes.png)

#### Lookups — Workload C Scaling

![Lookups scaling for Workload C](src/charts/line_C_lookups.png)

---

### Per-Size Bar Charts — Workload C

Side-by-side comparison of all four data structures at each workload size.

#### n = 1,000

**Comparisons**

![Comparisons for Workload C n=1,000](src/charts/bar_C_1000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload C n=1,000](src/charts/bar_C_1000_structural_ops.png)

**Inserts**

![Inserts for Workload C n=1,000](src/charts/bar_C_1000_inserts.png)

**Deletes**

![Deletes for Workload C n=1,000](src/charts/bar_C_1000_deletes.png)

**Lookups**

![Lookups for Workload C n=1,000](src/charts/bar_C_1000_lookups.png)

#### n = 5,000

**Comparisons**

![Comparisons for Workload C n=5,000](src/charts/bar_C_5000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload C n=5,000](src/charts/bar_C_5000_structural_ops.png)

**Inserts**

![Inserts for Workload C n=5,000](src/charts/bar_C_5000_inserts.png)

**Deletes**

![Deletes for Workload C n=5,000](src/charts/bar_C_5000_deletes.png)

**Lookups**

![Lookups for Workload C n=5,000](src/charts/bar_C_5000_lookups.png)

#### n = 10,000

**Comparisons**

![Comparisons for Workload C n=10,000](src/charts/bar_C_10000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload C n=10,000](src/charts/bar_C_10000_structural_ops.png)

**Inserts**

![Inserts for Workload C n=10,000](src/charts/bar_C_10000_inserts.png)

**Deletes**

![Deletes for Workload C n=10,000](src/charts/bar_C_10000_deletes.png)

**Lookups**

![Lookups for Workload C n=10,000](src/charts/bar_C_10000_lookups.png)

#### n = 20,000

**Comparisons**

![Comparisons for Workload C n=20,000](src/charts/bar_C_20000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload C n=20,000](src/charts/bar_C_20000_structural_ops.png)

**Inserts**

![Inserts for Workload C n=20,000](src/charts/bar_C_20000_inserts.png)

**Deletes**

![Deletes for Workload C n=20,000](src/charts/bar_C_20000_deletes.png)

**Lookups**

![Lookups for Workload C n=20,000](src/charts/bar_C_20000_lookups.png)

---

## Workload D

_Lookup-heavy workload — many lookups relative to inserts, no deletions._

### Scaling Charts — Workload D

These charts show how each data structure scales as the workload size grows from 1,000 to 20,000 elements.

#### Comparisons — Workload D Scaling

![Comparisons scaling for Workload D](src/charts/line_D_comparisons.png)

#### Structural Operations — Workload D Scaling

![Structural Operations scaling for Workload D](src/charts/line_D_structural_ops.png)

#### Inserts — Workload D Scaling

![Inserts scaling for Workload D](src/charts/line_D_inserts.png)

#### Lookups — Workload D Scaling

![Lookups scaling for Workload D](src/charts/line_D_lookups.png)

---

### Per-Size Bar Charts — Workload D

Side-by-side comparison of all four data structures at each workload size.

#### n = 1,000

**Comparisons**

![Comparisons for Workload D n=1,000](src/charts/bar_D_1000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload D n=1,000](src/charts/bar_D_1000_structural_ops.png)

**Inserts**

![Inserts for Workload D n=1,000](src/charts/bar_D_1000_inserts.png)

**Lookups**

![Lookups for Workload D n=1,000](src/charts/bar_D_1000_lookups.png)

#### n = 5,000

**Comparisons**

![Comparisons for Workload D n=5,000](src/charts/bar_D_5000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload D n=5,000](src/charts/bar_D_5000_structural_ops.png)

**Inserts**

![Inserts for Workload D n=5,000](src/charts/bar_D_5000_inserts.png)

**Lookups**

![Lookups for Workload D n=5,000](src/charts/bar_D_5000_lookups.png)

#### n = 10,000

**Comparisons**

![Comparisons for Workload D n=10,000](src/charts/bar_D_10000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload D n=10,000](src/charts/bar_D_10000_structural_ops.png)

**Inserts**

![Inserts for Workload D n=10,000](src/charts/bar_D_10000_inserts.png)

**Lookups**

![Lookups for Workload D n=10,000](src/charts/bar_D_10000_lookups.png)

#### n = 20,000

**Comparisons**

![Comparisons for Workload D n=20,000](src/charts/bar_D_20000_comparisons.png)

**Structural Operations**

![Structural Operations for Workload D n=20,000](src/charts/bar_D_20000_structural_ops.png)

**Inserts**

![Inserts for Workload D n=20,000](src/charts/bar_D_20000_inserts.png)

**Lookups**

![Lookups for Workload D n=20,000](src/charts/bar_D_20000_lookups.png)

---


