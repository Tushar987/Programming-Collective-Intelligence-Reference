# Data Clustering

### ABOUT
___
This project develops a  data clustering algorithm using hierarchial clustering.
It consists of 2 modules ```data``` and ```model```
#### ```data```
This module consists of classes responsible for operations on dataset like data cleaning, data structuring etc.
Currently it uses the Movie lens dataset but it can be used on various other dataset as long as the structure remains the same for the given ```model```
#### ```model```
This module consists of our model that is responsible for converting the data into various clusters.

### USAGE
___
```
from data import Generator


obj = Generator('data/feedlist.txt')
obj.parse()
obj.filter()
obj.write()
```


### TODO
___
+ Ability to take on different metrics instead of the hardcoded one i.e. ```pearson correlation```
+ A ***minimalist*** web end to this project so the service can be consumed.