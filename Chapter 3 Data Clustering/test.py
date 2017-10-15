from data import Generator


obj = Generator('data/feedlist.txt')
obj.parse()
obj.filter()
obj.write()
