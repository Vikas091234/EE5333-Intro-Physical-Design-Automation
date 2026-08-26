# EE5333 Introduction to Physical Design Automation - End Sem Project

## 1. Project Overview

This project implements a detailed routing flow for the supplied physical-design benchmarks using:

- LEF files for technology and cell information
- DEF files for the placed design
- GUIDE files for routing regions
- A detailed router to generate routed DEF files
- `checker.py` for connectivity and spacing checks
- An optional layout visualizer available through the checker `-p` option

The final implementation was evaluated on the following benchmarks:

```text
add5
c17
c432
c499
c6288
c7552
spm
```

See [`REPORT.md`](REPORT.md) for the experimental results and observations.

---

## 2. Repository Structure

The important directories/files are:

```text
project/
│
├── scr/
│   ├── detailed_router.py
│   ├── checker.py
│   └── ...
│
├── data/
│   ├── def/
│   │   ├── add5.def
│   │   ├── c17.def
│   │   ├── c432.def
│   │   ├── c499.def
│   │   ├── c6288.def
│   │   ├── c7552.def
│   │   └── spm.def
│   │
│   ├── lef/
│   │   └── sky130.lef
│   │
│   └── gr/
│       ├── add5.guide
│       ├── c17.guide
│       ├── c432.guide
│       ├── c499.guide
│       ├── c6288.guide
│       ├── c7552.guide
│       └── spm.guide
│
├── output/
│   └── <generated routed DEF files>
│
├── wheels/
│   └── lefdefparser-0.1-cp312-cp312-win_amd64.whl
│
├── README.md
└── REPORT.md
```

---

## 3. Requirements

The current tested environment is:

```text
Windows
Python 3.12
```

Check Python:

```bat
python --version
```

The tested Python version was:

```text
Python 3.12.9
```

Check pip:

```bat
python -m pip --version
```

---

## 4. Install the LEFDEFParser Package

The router and checker require the course-provided `LEFDEFParser` package.

The repository contains the course wheel:

```text
wheels\lefdefparser-0.1-cp312-cp312-win_amd64.whl
```

Install it from the project root:

```bat
python -m pip install .\wheels\lefdefparser-0.1-cp312-cp312-win_amd64.whl
```

If pip reports that the same version is already installed but Python still gives:

```text
ModuleNotFoundError: No module named 'LEFDEFParser'
```

force reinstall the wheel:

```bat
python -m pip install --force-reinstall .\wheels\lefdefparser-0.1-cp312-cp312-win_amd64.whl
```

Verify the installation:

```bat
python -m pip show -f lefdefparser
```

The package is a compiled Windows/Python 3.12 extension, so the supplied wheel must match the Python version and platform.

---

## 5. Install `rtree`

The checker requires the `rtree` package.

Install it using:

```bat
python -m pip install rtree
```

Verify it:

```bat
python -c "import rtree; print('rtree OK')"
```

Expected output:

```text
rtree OK
```

If the repository contains a `requirements.txt`, the normal Python dependencies can also be installed using:

```bat
python -m pip install -r requirements.txt
```

The course-provided `LEFDEFParser` wheel should still be installed separately as described above.

---

# 6. Running the Detailed Router

Run commands from the **project root**.

The general command is:

```bat
python scr\detailed_router.py -i <DEF> -l <LEF> -g <GUIDE> -o <OUTPUT_DEF>
```

For example, for `add5`:

```bat
python scr\detailed_router.py -i data\def\add5.def -l data\lef\sky130.lef -g data\gr\add5.guide -o output\add5_out.def
```

A successful run prints information similar to:

```text
[DR] LEF  : data\lef\sky130.lef
[DR] DEF  : data\def\add5.def
[DR] GUIDE: data\gr\add5.guide
[DR] Building track grid ...
[DR] Collecting pin shapes ...
[DR] Loading cell obstructions ...
[DR] Routing ...
[DR] Routed=...
[DR] Writing: output\add5_out.def
[DR] Finished in ...s
```

The generated routed DEF is written to the `output` directory.

---

# 7. Run All Benchmarks

The following commands reproduce the final benchmark runs.

### add5

```bat
python scr\detailed_router.py -i data\def\add5.def -l data\lef\sky130.lef -g data\gr\add5.guide -o output\add5_out.def
```

### c17

```bat
python scr\detailed_router.py -i data\def\c17.def -l data\lef\sky130.lef -g data\gr\c17.guide -o output\c17_out.def
```

### c432

```bat
python scr\detailed_router.py -i data\def\c432.def -l data\lef\sky130.lef -g data\gr\c432.guide -o output\c432_out.def
```

### c499

```bat
python scr\detailed_router.py -i data\def\c499.def -l data\lef\sky130.lef -g data\gr\c499.guide -o output\c499_out.def
```

### c6288

```bat
python scr\detailed_router.py -i data\def\c6288.def -l data\lef\sky130.lef -g data\gr\c6288.guide -o output\c6288_out.def
```

### c7552

```bat
python scr\detailed_router.py -i data\def\c7552.def -l data\lef\sky130.lef -g data\gr\c7552.guide -o output\c7552_out.def
```

### spm

```bat
python scr\detailed_router.py -i data\def\spm.def -l data\lef\sky130.lef -g data\gr\spm.guide -o output\spm_out.def
```

---

# 8. Running the Checker

The checker performs:

1. Connectivity checking
2. Spacing DRC checking

The general command is:

```bat
python scr\checker.py -i <INPUT_DEF> -o <OUTPUT_DEF> -l <LEF>
```

For example:

```bat
python scr\checker.py -i data\def\add5.def -o output\add5_out.def -l data\lef\sky130.lef
```

The checker reports:

```text
Total number of spacing violations : ...
Total number of nets : ...
Total number of open nets : ...
```

`Total number of open nets : 0` means that all nets considered by the checker are connected in the generated routed DEF.

---

# 9. Run the Checker for All Benchmarks

### add5

```bat
python scr\checker.py -i data\def\add5.def -o output\add5_out.def -l data\lef\sky130.lef
```

### c17

```bat
python scr\checker.py -i data\def\c17.def -o output\c17_out.def -l data\lef\sky130.lef
```

### c432

```bat
python scr\checker.py -i data\def\c432.def -o output\c432_out.def -l data\lef\sky130.lef
```

### c499

```bat
python scr\checker.py -i data\def\c499.def -o output\c499_out.def -l data\lef\sky130.lef
```

### c6288

```bat
python scr\checker.py -i data\def\c6288.def -o output\c6288_out.def -l data\lef\sky130.lef
```

### c7552

```bat
python scr\checker.py -i data\def\c7552.def -o output\c7552_out.def -l data\lef\sky130.lef
```

### spm

```bat
python scr\checker.py -i data\def\spm.def -o output\spm_out.def -l data\lef\sky130.lef
```

---

# 10. Layout Visualization

The checker has an optional visualization mode enabled using the `-p` option.

From the project root, for example:

```bat
python scr\checker.py -i data\def\c17.def -o output\c17_out.def -l data\lef\sky130.lef -p
```

This is the updated form of the visualization command because the current repository keeps `checker.py` under `scr\` and the input/output files under `data\` and `output\`.

The `-p` option can be used with other benchmarks in the same way. For example:

```bat
python scr\checker.py -i data\def\c7552.def -o output\c7552_out.def -l data\lef\sky130.lef -p
```

---

# 11. Final Experimental Results

The final/best benchmark results obtained from the implementation are:

| Benchmark | Guide Nets | Routed Nets | Open Nets | Routing Time (s) | Spacing Violations |
|---|---:|---:|---:|---:|---:|
| add5 | 61 | 60 | 0 | 0.29 | 52 |
| c17 | 23 | 22 | 0 | 0.22 | 20 |
| c432 | 198 | 197 | 0 | 0.63 | 291 |
| c499 | 363 | 362 | 0 | 1.48 | 564 |
| c6288 | 1526 | 1525 | 0 | 4.08 | 3236 |
| c7552 | 1592 | 1591 | 0 | 11.77 | 3991 |
| spm | 308 | 307 | 0 | 1.09 | 873 |

### Connectivity

All seven benchmarks achieved:

```text
Open nets = 0
```

Therefore, all nets considered routable by the implementation were successfully connected.

### Runtime

The measured routing time ranged from:

```text
0.22 s  →  11.77 s
```

The largest benchmark, `c7552`, contained 1591 routed nets and completed routing in 11.77 seconds.

### Spacing

The checker still reports spacing violations. These include both:

- net-to-net spacing violations
- net-to-obstruction spacing violations

Therefore, the current implementation should not be considered completely DRC-clean.

For detailed analysis and observations, see:

```text
REPORT.md
```

---

# 12. Reproducing the Complete Flow

For a benchmark, the complete flow is:

```text
DEF + LEF + GUIDE
        |
        v
detailed_router.py
        |
        v
generated routed DEF
        |
        v
checker.py
        |
        +----> connectivity result
        |
        +----> spacing DRC result
        |
        +----> optional visualization (-p)
```

Example:

```bat
python scr\detailed_router.py -i data\def\c17.def -l data\lef\sky130.lef -g data\gr\c17.guide -o output\c17_out.def

python scr\checker.py -i data\def\c17.def -o output\c17_out.def -l data\lef\sky130.lef

python scr\checker.py -i data\def\c17.def -o output\c17_out.def -l data\lef\sky130.lef -p
```

---

# 13. Project Report

A detailed discussion of the implementation, experimental results, observations, limitations, and conclusions is provided in:

```text
REPORT.md
```

---

# 14. Known Limitations

The current implementation successfully establishes connectivity on all seven supplied benchmarks, but spacing violations remain.

The reported spacing violations increase substantially for some of the larger designs. This indicates that congestion handling and geometric spacing enforcement remain areas for improvement.

The results should therefore be interpreted as:

- successful connectivity routing across the supplied benchmark suite;
- practical routing runtime;
- remaining spacing-rule violations requiring further improvement.

