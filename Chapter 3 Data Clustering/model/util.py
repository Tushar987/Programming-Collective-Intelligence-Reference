from math import sqrt


class Util(object):
    """
    Utility class responsible for helper functions
    """
    @staticmethod
    def read_file(file_name):
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
