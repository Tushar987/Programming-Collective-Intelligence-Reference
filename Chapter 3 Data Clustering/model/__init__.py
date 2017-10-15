from .util import Util


class Node(object):
    """
    Class representing the node of the cluster
    """
    def __init__(self, vector, left=None, right=None, distance=0.0, id=None):
        self.__vector = vector
        self.__left = left
        self.__right = right
        self.__distance = distance
        self.__id = id

    def get_vector(self):
        return self.__vector

    def get_id(self):
        return self.__id

    def get_left(self):
        return self.__left

    def get_right(self):
        return self.__right


class HierarchialCluster(object):
    """
    Class representing the dendogram by hierarchial clustering of the vector
    """
    def __init__(self):
        self.__root = None

    def generate(self, rows):
        """
        Responsible for generating the dendogram
        """
        distances, current_cluster_id = dict(), -1
        # Initialize the clusters as the rows
        cluster = [Node(rows[i], id=i) for i in range(len(rows))]
        while len(cluster) > 1:
            lowest_pair = (0, 1)
            n = len(cluster[1].get_vector())
            closest = Util.pearson_correlation_score(cluster[0].get_vector(), cluster[1].get_vector(), n)
            # Loop through all pairs to find the smallest distance
            for i in range(len(cluster)):
                for j in range(i + 1, len(cluster)):
                    key = (cluster[i].get_id(), cluster[j].get_id())
                    if key not in distances:
                        n = len(cluster[0].get_vector())
                        value = Util.pearson_correlation_score(cluster[i].get_vector(), cluster[j].get_vector(), n)
                        distances[key] = value
                    d = distances[key]
                    if d < closest:
                        closest = d
                        lowest_pair = (i, j)
            # Calculate average of 2 clusters
            a, b, n = cluster[lowest_pair[0]], cluster[lowest_pair[1]], len(cluster[0].get_vector())
            merged_vector = [(a.get_vector()[i] + b.get_vector()[i]) / 2.0 for i in range(n)]
            # Create the new cluster
            new_cluster = Node(merged_vector, left=a, right=b, distance=closest, id=current_cluster_id)
            # Cluster with id that were not in the original sets are discarded
            current_cluster_id -= 1
            del cluster[lowest_pair[1]]
            del cluster[lowest_pair[0]]
            cluster.append(new_cluster)
        self.__root = cluster[0]

    def traverse(self, labels=None, n=0):
        temp = self.__root
        self.__traverse(temp, labels, n)

    def __traverse(self, root, labels, n):
        # Indent the output
        for i in range(n):
            print ' ',
        if root.get_id() < 0:
            # It represents a branch
            print('-')
        else:
            # It represents a node
            print(root.get_id() if not labels else labels[root.get_id()])
        # Recursively print right and left branches
        if root.get_left():
            self.__traverse(root.get_left(), labels, n + 1)
        if root.get_right():
            self.__traverse(root.get_right(), labels, n + 1)
