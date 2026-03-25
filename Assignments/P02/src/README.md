# Data Structure Performance Analysis

Comparison of **BST**, **Linked List**, **Hash Table**, and **Sorted Array** 
across four workload types (A–D) and four sizes (1K, 5K, 10K, 20K).

All charts are grouped by workload type. Each section contains:

- **Scaling line charts** — how each metric grows as n increases
- **Per-size bar charts** — side-by-side comparison at each workload size

---

## Table of Contents

- [Workload A](#workload-a)
- [Workload B](#workload-b)
- [Workload C](#workload-c)
- [Workload D](#workload-d)

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

| Structure | Insert | Lookup | Delete | Notes |
|---|---|---|---|---|
| BST | O(log n) avg | O(log n) avg | O(log n) avg | Degrades to O(n) if unbalanced |
| Linked List | O(n) | O(n) | O(n) | Simple but slow at scale |
| Hash Table | O(1) avg | O(1) avg | O(1) avg | Performance depends on load factor |
| Sorted Array | O(n) | O(log n) | O(n) | Fast lookup, expensive insert/delete |
