from data import Dataset
from model import Model


temp = Dataset()
temp.clean()
obj = Model(temp)
print(obj.recommend_items('77'))
