# Recommendation-System

### ABOUT
___
This project develops a recommendation system engine that can be used to predict the favourable output from a given dataset.

It consists of 2 modules ```data``` and ```model```
#### ```data```
This module consists of classes responsible for operations on dataset like data cleaning, data structuring etc.
Currently it uses the Movie lens dataset but it can be used on various other dataset as long as the structure remains the same for the given ```model```
#### ```model```
This module consists of our model that learns from the given dataset, and provides the output in test phase. Currently it is using ```pearson correlation``` metric.


### USAGE
___
```
from data import Dataset
from model import Model


temp = Dataset()
temp.clean()
obj = Model(temp)
print(obj.recommend_items('77'))
```


### TODO
___
+ Ability to take on different metrics instead of the hardcoded one i.e. ```pearson correlation```
+ A ***minimalist*** web end to this project so the service can be consumed.