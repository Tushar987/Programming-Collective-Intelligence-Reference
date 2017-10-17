from math import sqrt
from PIL import Image, ImageDraw


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

    def get_distance(self):
        return self.__distance


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

    def get_root(self):
        return self.__root


class Util(object):
    """
    Utility class responsible for helper functions
    """
    @staticmethod
    def read_file(file_name):
        """
        This function reads the file blogdata.txt file
        :param file_name:
        """
        lines = [line for line in file(file_name)]
        # First line is the column title
        column_names, row_names, data = lines[0].strip().split('\t')[1:], list(), list()
        for line in lines[1:]:
            temp = line.strip().split('\t')
            # First column in each row is the row name
            row_names.append(temp[0])
            # Remaining part is the data
            data.append([float(i) for i in temp[1:]])
        return row_names, column_names, data

    @staticmethod
    def pearson_correlation_score(a, b, n):
        """
        This function calculates the pearson correlation score of two vectors
        :param a: vector a
        :param b: vector b
        :param n: length of vector a or vector b
        """
        # Sum of array
        sum1, sum2 = sum(a), sum(b)
        # Square sum of array
        sum1_square, sum2_square = sum([i * i for i in a]), sum([i * i for i in b])
        # Product sum of array
        product_sum = sum([a[i] * b[i] for i in range(n)])
        # Calculate person score
        numerator = product_sum - (sum1 * sum2 / n)
        denominator = sqrt((sum1_square - pow(sum1, 2) / n) * (sum2_square - pow(sum2, 2) / n))
        if not denominator:
            return 0
        return 1.0 - numerator / denominator

    def get_height(self, cluster):
        """
        This method return the height of the dendogram
        :param cluster: root of the cluster
        :return: height of the dendogram
        """
        # For leaf nodes height is 1
        if not cluster.get_left() and not cluster.get_right():
            return 1
        return self.get_height(cluster.get_left()) + self.get_height(cluster.get_right())

    def get_depth(self, cluster):
        """
        This method return the height of the dendogram
        :param cluster: root of the cluster
        :return: height of the dendogram
        """
        # For leaf nodes depth is 0
        if not cluster.get_left() and not cluster.get_right():
            return 0
        return max(self.get_depth(cluster.get_left()), self.get_depth(cluster.get_right())) + cluster.get_distance()


class Graphics(object):
    """
    Class responsible for drawing the dendogram as a JPEG image.
    Dependency - PIL (Python Imaging Library)
    """
    def __init__(self, root, labels):
        self.__root = root
        self.__labels = labels
        self.__image = None
        self.__graphic = None
        self.__util = Util()
        self.__white = (255, 255, 255)
        self.__black = (0, 0, 0)

    def draw(self, file_name):
        """
        This method is responsible for drawing the image and saving it.
        :param file_name: name of the file where the image is to be saved
        """
        height, depth, width = self.__util.get_height(self.__root) * 20, self.__util.get_depth(self.__root), 1200
        # Width is fixed so distances are scaled accordingly
        scaling_factor = float(width - 150) / depth
        # Create a new image with white background
        self.__image = Image.new('RGB', (width, height), self.__white)
        self.__graphic = ImageDraw.Draw(self.__image)
        self.__graphic.line((0, height / 2, 10, height / 2), fill=(255, 0, 0))
        # Draw the first node
        self.__draw_node(self.__root, 10, height / 2, scaling_factor)
        self.__image.save(file_name, 'JPEG')

    def __draw_node(self, cluster, x, y, scaling_factor):
        """
        This method recursively draws the nodes of the dendogram
        :param cluster: root node
        :param x: x coordinate
        :param y: y coordinate
        :param scaling_factor: scaling factor to be used
        """
        if cluster.get_id() < 0:
            height_left = self.__util.get_height(cluster.get_left()) * 20
            height_right = self.__util.get_height(cluster.get_right()) * 20
            top, bottom = y - (height_left + height_right) / 2, y + (height_left + height_right) / 2
            line_length = cluster.get_distance() * scaling_factor
            height, width = top + height_left / 2, bottom - height_right / 2
            # Vertical line from this node to it's children
            self.__graphic.line((x, height, x, width), fill=(255, 0, 0))
            # Horizontal line from this node to it's left node
            self.__graphic.line((x, height, x + line_length, height), fill=(255, 0, 0))
            # Horizontal line from this node to it's right node
            self.__graphic.line((x, width, x + line_length, width), fill=(255, 0, 0))
            self.__draw_node(cluster.get_left(), x + line_length, height, scaling_factor)
            self.__draw_node(cluster.get_right(), x + line_length, width, scaling_factor)
        else:
            # If this is a leaf node draw the item label
            self.__graphic.text((x + 5, y - 7), self.__labels[cluster.get_id()], self.__black)
