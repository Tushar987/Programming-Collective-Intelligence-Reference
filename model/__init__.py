from math import sqrt


class Model(object):
    """
    This class is responsible for the recommending algorithm.
    It depends on the data format used.
    """

    def __init__(self, data_obj):
        """
        data_obj needs to adhere to the format of data in Dataset()
        :param data_obj:
        """
        self.__data = data_obj.get_data()

    def __pearson_correlation(self, person1, person2):
        """
        Compares the similarity of 2 users based on their pearson score.
        :param person1:
        :param person2:
        :return: pearson score
        """
        shared_items = dict()
        for item in self.__data[person1]:
            if item in self.__data[person2]:
                shared_items[item] = 1
        # If there is nothing in common then return 0
        n = len(shared_items)
        if not n:
            return 0
        # Adding up the preferences
        sum1 = sum([self.__data[person1][item] for item in shared_items])
        sum2 = sum([self.__data[person2][item] for item in shared_items])
        # Adding up the squares
        sum1_square = sum([self.__data[person1][item] ** 2 for item in shared_items])
        sum2_square = sum([self.__data[person2][item] ** 2 for item in shared_items])
        # Adding up the product
        product_sum = sum([self.__data[person1][item] * self.__data[person2][item] for item in shared_items])
        numerator = product_sum - (sum1 * sum2 / n)
        denominator = sqrt((sum1_square - (sum1 ** 2) / n) * (sum2_square - (sum2 ** 2) / n))
        if not denominator:
            return 0
        return numerator / denominator

    def recommend_persons(self, person, n=3):
        """
        Best match for person from the data set.
        :param person:
        :param n:
        :return: top n matches for person
        """
        scores = [(self.__pearson_correlation(person, other), other) for other in self.__data if other != person]
        scores.sort(reverse=True)
        return scores[0:n]

    def recommend_items(self, person):
        """
        Gets recommendations using weighted average of other user's ranking.
        :param person:
        :return: ranking
        """
        totals, similarity_sums = dict(), dict()
        for other in self.__data:
            if other == person:
                continue
            similarity = self.__pearson_correlation(person, other)
            # Ignore non-positive scores
            if similarity <= 0:
                continue
            for item in self.__data[other]:
                # Only score unwatched movies
                if item not in self.__data[person] or not self.__data[person][item]:
                    totals.setdefault(item, 0)
                    totals[item] += self.__data[other][item] * similarity
                    similarity_sums.setdefault(item, 0)
                    similarity_sums[item] += similarity
        rankings = [(v / similarity_sums[k], k) for k, v in totals.items()]
        rankings.sort(reverse=True)
        return rankings
