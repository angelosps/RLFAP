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



#### REFERENCES
Boussemart, F., Hemery, F., Lecoutre, C., & Sais, L. (2004). Boosting systematic search by weighting constraints. In ECAI (Vol. 16, pp. 146-150) (http://www.frontiersinai.com/ecai/ecai2004/ecai04/pdf/p0146.pdf)

