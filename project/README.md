# EE5333 Introduction to Physical Design Automation - End sem project
# installation of parser
bash 
``` 
pip install wheels/lefdefparser-0.1-cp312-cp312-win_amd64.whl
```
# Generate solution file

Create a sample def file containing solutions for three nets of `add5`.
```
python src/detailed_router.py --lef data/lef/sky130.lef --def data/def/add5.def --guide data/gr/add5.guide --output output/add5_out.def
```
This should create a `add5_out.def` in the same directory.

# Running the checker

The script `checker.py` does (a) spacing DRC check and (b) connectivity check for all nets.
It requires the package `rtree`, which can be installed using `pip install rtree`.
```
python src/checker.py --lef data/lef/sky130.lef --def output/add5_out.def --guide data/gr/add5.guide
```
Total number of open (disconnected) nets and the number of spacing violations are reported on console.


There is an optional visualizer for the placement, which can be invoked using the `-p` argument.
```
python3 checker.py -i ../def/c17.def -o ./c17_out.def -l ../lef/sky130.lef -p
```

