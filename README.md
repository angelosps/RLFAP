# Radio Link Frequency Assignment Problem (RLFAP)

The Radio Link Frequency Assignment Problem is a Constraint Satisfaction Problem (CSP) which consists of assigning frequencies to a set of radio links defined between pairs of sites in order to avoid interferences.  
Extensive description of the problem can be found [here](https://miat.inrae.fr/schiex/rlfap.shtml).  

## Search methods used:
* Backtracking with Forward Checking (FC)
* Backtracking with Maintaining Arc Consistency (MAC)
* Forward Checking with Conflict directed BackJumping hybrid (FC-CBJ)
* Min Conflicts

## Use of heuristics:
In order to speed up the search, I am using a conflict directed variable ordering heuristic such as is the *dom/wdeg heuristic*. Due to the difficulty of the instances, the search time takes several hours, but, with the help of *dom/wdeg heuristic* the search time takes only a few seconds. The heuristic it is used in all of the above methods while searching.   
Reference to the related paper about *dom/wdeg heuristic* below.

## Experimental results:

### Method: Forward Checking (FC) with dom/wdeg heuristic

| Instance | Result | Time(s)| Assignments | Constraint checks |
| --- | --- | --- | --- | --- | 
| 11 | SAT | ~9 | 13855 | 2829739 |
| 2-f24 | SAT | ~0.05 | 254 | 22384 |
| 2-f25 | UNSAT | ~41 | 198551 | 37282795 |
| 3-f10 | SAT | ~1.1 | 4304 | 777626 |
| 3-f11 | UNSAT | ~49 | 210370 | 38962375 |
| 8-f10 | SAT | ~630 | 2512599 | 325083064 |
| 8-f11 | UNSAT | ~204 | 638778 | 86488684 |
| 14-f27 | SAT | ~36 | 99915 | 5052782 |
| 14-f28 | UNSAT | ~180 | 318864 | 19178933 |
| 6-w2 | UNSAT | ~0.05 | 250 | 46258 |
| 7-w1-f4 | SAT | ~0.2 | 2308 | 106877 |

### Method: Maintaining Arc Consistency (MAC with AC3) with dom/wdeg heuristic

| Instance | Result | Time(s)| Assignments | Constraint checks |
| --- | --- | --- | --- | --- | 
| 11 | SAT | ~11 | 4560  | 9261742 |
| 2-f24 | SAT | ~0.1 | 228 | 165964 |
| 2-f25 | UNSAT | ~145 | 52330 | 100095447 |
| 3-f10 | SAT | ~2 | 852 | 1269090 |
| 3-f11 | UNSAT | ~36 | 8292 | 25501966 |
| 8-f10 | SAT | ~46 | 14149 | 30407876 |
| 8-f11 | UNSAT | ~6 | 1979 | 4608720 |
| 14-f27 | SAT | ~18 | 15389 | 4337430 |
| 14-f28 | UNSAT | ~22 | 8874 | 8185280 |
| 6-w2 | UNSAT | ~0.08 | 44 | 93186 |
| 7-w1-f4 | SAT | ~0.2 | 442 | 277559 |

### Method: FC-CBJ hybrid with dom/wdeg heuristic

| Instance | Result | Time(s)| Assignments | Constraint checks |
| --- | --- | --- | --- | --- | 
| 11 | SAT | ~4 | 5576 | 1185589 |
| 2-f24 | SAT | ~0.5 | 250 | 22287 |
| 2-f25 | UNSAT | ~11 | 44875 | 8899233 |
| 3-f10 | SAT | ~0.8 | 2697 | 480205 |
| 3-f11 | UNSAT | ~25 | 85283 | 15145162 |
| 8-f10 | SAT | ~130 | 334057 | 48612625 |
| 8-f11 | UNSAT | ~30 | 64408 | 9435454 |
| 14-f27 | SAT | ~25 | 50859 | 2615605 |
| 14-f28 | UNSAT | ~20 | 29178 | 2012526 |
| 6-w2 | UNSAT | ~0.05 | 250 | 46258 |
| 7-w1-f4 | SAT | ~0.3 | 2120 | 96116 |

### Method: Min Conflicts with maximum steps = 1000 (average of 5 executions)

| Instance | Result | Time(s)| Assignments | Constraint checks | Constraints violated |
| --- | --- | --- | --- | --- | --- |
| 11 | UNSAT | ~6.3 | 1680  | 9529708 | 10 |
| 2-f24 | UNSAT | ~1.8 | 1200 | 3022859 | 12 |
| 2-f25 | UNSAT | ~1.7 | 1200  | 2963507 | 18 |
| 3-f10 | UNSAT | ~3.9 | 1400 | 6183665 | 39 |
| 3-f11 | UNSAT | ~3.8 | 1400 | 6147748 | 42 |
| 8-f10 | UNSAT | ~5.9 | 1680 | 8005154 | 215 | 
| 8-f11 | UNSAT | ~6.4 | 1680 | 7995665 | 262 |
| 14-f27 | UNSAT | ~7 | 1916 | 9540495 | 338 |
| 14-f28 | UNSAT | ~6.9 | 1916  | 9524215 | 439 |
| 6-w2 | UNSAT | ~1.1 | 1200 | 1641059 | 82 |
| 7-w1-f4 | UNSAT | ~1.2 | 1400 | 1499578 | 64 |

## Run instructions

```bash
  $ python3 rlfap.py <instance> <method>
```  

*i.e., for the instance "11" run each of the methods (FC/MAC/FC-CBJ/Min-Conflicts) as follows:*

```bash
  $ python3 rlfap.py 11 FC              
  $ python3 rlfap.py 11 MAC             
  $ python3 rlfap.py 11 FC-CBJ          
  $ python3 rlfap.py 11 Min-Conflicts  
```

#### CODE CITATION
I use _csp.py_, _search.py_ & _utils.py_ from https://github.com/aimacode/aima-python.

#### REFERENCES
Boussemart, F., Hemery, F., Lecoutre, C., & Sais, L. (2004). Boosting systematic search by weighting constraints. In ECAI (Vol. 16, pp. 146-150) (http://www.frontiersinai.com/ecai/ecai2004/ecai04/pdf/p0146.pdf)
