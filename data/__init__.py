from os import path, getcwd


class Dataset(object):
    """
    This class is responsible for data oriented operations like data cleaning, dataset change.
    """
    def __init__(self):
        """
        __data_set : dataset represented as dictionary of dictionaries.
        """
        self.__data_set = dict()

    def clean(self):
        """
        Cleans the data source, and gives the predefined structure to it.
        """
        # Get movie titles
        movies = dict()
        for line in open('data/movies.csv'):
            movie_id, title = line.split(',')[0:2]
            movies[movie_id] = title
        # Load data
        for line in open('data/ratings.csv'):
            user_id, movie_id, ratings, timestamp = line.split(',')
            if ratings == 'rating':
                continue
            self.__data_set.setdefault(user_id, dict())
            self.__data_set[user_id][movies[movie_id]] = float(ratings)

    def get_data(self):
        """
        This method returns the dataset
        :return: __data_set
        """
        return self.__data_set
