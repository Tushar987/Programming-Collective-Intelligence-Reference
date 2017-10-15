from data import Generator
from model import *


obj = Generator('data/feedlist.txt')
obj.parse()
obj.filter()
obj.write()
blog_names, word, data = Util.read_file('data/blogdata.txt')
obj = HierarchialCluster()
obj.generate(data)
obj.traverse(labels=blog_names)
