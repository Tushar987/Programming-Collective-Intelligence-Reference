from .util import Util


class BinaryCluster(object):
    """
    Class representing the Binary cluster
    """
    def __init__(self, vector, left=None, right=None, distance=0.0, value=None):
        self.__vector = vector
        self.__left = left
        self.__right = right
        self.__distance = distance
        self.__id = value
