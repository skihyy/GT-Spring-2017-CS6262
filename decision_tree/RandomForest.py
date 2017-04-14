import csv
import numpy as np  # http://www.numpy.org
import ast
import operator
import random
import math


class RandomForest(object):
    class __DecisionTree(object):
        tree = {}

        def learn(self, data, data_label):
            # Train decision tree and store it in self.tree
            # data_set is like XX containing both data and data label
            data_set = []
            num_of_rows = len(data)
            repeat_range = range(num_of_rows)

            for i in repeat_range:
                row = data[i]
                row.append(data_label[i])
                data_set.append(row)

            self.tree = self.create_tree(data_set)
            # self.tree = self.create_tree(data_set)
            pass

        def create_tree(self, data_set, count=None, iteration_limit=None):
            """
            Given a data set, create a tree.
            NOTE: Except final value, all other numbers should be in float format
            :param data_set: data set, the last column is the data label
            :param count: iterations
            :param iteration_limit: iterations for stop
            :return: dictionary of trees
            """
            data_label = [row[-1] for row in data_set]

            # depth control
            if count is not None and iteration_limit is not None:
                if count >= iteration_limit:
                    return self.majority_count(data_label)

            # if all the data labels are the same, return it
            if data_label.count(data_label[0]) == len(data_label):
                return data_label[0]

            # after go through all features, and now there are only 1 data attribute left,
            # if I still cannot get a classification, using majority rule
            if 1 == len(data_set[0]):
                return self.majority_count(data_label)

            best_fit_position, best_info_gain = self.choose_best_feature_to_split(data_set)
            best_fit_position_float = float(best_fit_position)  # use as key to handle exceptions

            current_tree = {best_fit_position_float: {}}
            # all values at the best fir position
            fit_value = [row[best_fit_position] for row in data_set]
            # delete duplicated values
            unique_value = set(fit_value)
            for value in unique_value:
                value = float(value)
                # if there is depth control
                if count is not None and iteration_limit is not None:
                    current_tree[best_fit_position_float][value] = self.create_tree(
                        self.split_data_set(data_set, best_fit_position, value),
                        count=count + 1, iteration_limit=iteration_limit)
                else:
                    current_tree[best_fit_position_float][value] = self.create_tree(
                        self.split_data_set(data_set, best_fit_position, value))

            return current_tree

        '''     # this is the binary classification
                def classify(self, record):
                    # TODO: return predicted label for a single record using self.tree
                    # a temporary variable for the tree
                    current_tree = self.tree

                    while dict == type(current_tree):
                        index = current_tree.keys()[0]

                        if record[index] <= current_tree[index]:
                            current_tree = current_tree[index][0]
                        else:
                            current_tree = current_tree[index][1]

                    return current_tree
        '''

        def classify(self, record):
            # Return predicted label for a single record using self.tree
            # print(self.tree)

            current_tree = self.tree

            while isinstance(current_tree, dict):
                # record[current_best_feature_position] would be the fit value at this level (best split feature)
                initial_position_float = current_tree.keys()[0]
                current_best_feature_position = int(initial_position_float)
                # go into the tree
                current_tree = current_tree[initial_position_float]
                # check
                if not isinstance(current_tree, dict):
                    return current_tree

                # value of best split feature
                current_feature_point = float(record[current_best_feature_position])
                # not sure whether this point will be in the tree, find closest one
                keys = current_tree.keys()
                closest_point = self.find_closest_point(current_feature_point, keys)
                # go to next level
                # print("Current keys: " + str(keys))
                # print("Current chosen key:" + str(closest_point))
                current_tree = current_tree[closest_point]

            return current_tree

        def choose_best_feature_to_split(self, data_set):
            """
            Given a set of data, find out the best feature for splitting the nodes
            :param data_set: data set, the last column is the data label
            :return: the position of this best feature, and best information gain
            """
            num_of_features = len(data_set[0]) - 1
            # calculate entropy
            base_entropy = self.cal_shannon_entropy(data_set)

            best_info_gain = 0.0
            best_feature_position = -1

            repeat_range = range(num_of_features)
            for i in repeat_range:
                # create a list of all data_set in this feature
                feature_list = [row[i] for row in data_set]
                # delete duplicated data_set for unique tag for classification
                classifier_value = set(feature_list)
                new_entropy = 0.0

                # calculate the new entropy to compare with the old one
                for value in classifier_value:
                    sub_data_set = self.split_data_set(data_set, i, value)
                    probability = len(sub_data_set) / float(len(data_set))
                    new_entropy += probability * self.cal_shannon_entropy(data_set)

                info_gain = base_entropy - new_entropy

                # only find out the best info gain
                if info_gain > best_info_gain:
                    best_info_gain = info_gain
                    best_feature_position = i

            return best_feature_position, best_info_gain

        def split_data_set(self, data_set, split_point, value):
            """
            Split data set into sub data set.
            :param data_set: the set of data to split
            :param split_point: the position of split
            :param value: the value used for matching split point value
            :return: a splitted sub data set
            """
            sub_data_set = []

            for row in data_set:
                if value == row[split_point]:
                    # get all values except the split_point value
                    sub_data_row = row[:split_point]
                    sub_data_row.extend(row[split_point + 1:])
                    sub_data_set.append(sub_data_row)

            return sub_data_set

        def cal_shannon_entropy(self, data_set):
            """
            Calculate Shannon entropy for a given data.
            :param data_set: data set, the last column is the data label
            :return: Shannon entropy
            """
            num_of_rows = len(data_set)

            if 0 == num_of_rows:
                return 0

            # a dictionary with key = data label, value = the number of current label shows
            label_count = {}

            # go through every row of data_set
            for row in data_set:
                current_label = row[-1]

                if current_label not in label_count.keys():
                    label_count[current_label] = 0
                label_count[current_label] += 1

            entropy = 0.0

            for key in label_count:
                probability = float(label_count[key]) / num_of_rows
                entropy -= probability * math.log(probability, 2)

            return entropy

        def majority_count(self, data_label):
            """
            Return the label in data label that appears most.
            :param data_label: data label list
            :return: label that appears most
            """
            label_count = {}

            for label in data_label:
                if label not in label_count.keys():
                    label_count[label] = 0
                label_count[label] += 1

            sorted_label_count = sorted(label_count.iteritems(), key=operator.itemgetter(1), reverse=True)
            return sorted_label_count[0][0]

        def find_closest_point(self, point, num_list):
            """
            Given a list of unsorted numbers, return the one which is the closest to point.
            This can be used to split a leaf, especially when there is requirement of the
            number of leaves.
            :param point: a point for finding the closest position
            :param num_list: a list of unsorted numbers
            :return: num in the list which is the closest to point
            """
            current_index = num_list[0]
            compare_list = num_list[1:]
            minimum_difference = point

            for num in compare_list:
                temp_difference = math.fabs(num - point)
                if minimum_difference > temp_difference:
                    minimum_difference = temp_difference
                    current_index = num

            return current_index

    num_trees = 0
    decision_trees = []
    bootstraps_datasets = []  # the bootstrapping data set for trees
    bootstraps_labels = []  # the true class labels,

    # corresponding to records in the bootstrapping data set

    def __init__(self, num_trees):
        # TODO: do initialization here.
        self.num_trees = num_trees
        self.decision_trees = [self.__DecisionTree() for i in range(num_trees)]

    # def _bootstrapping(self, data_set, n):
    def _bootstrapping(self, data_set, good_data, n, percentage=0.05):
        """
        Return sample data and sample data label from a given data set by using bootstrapping method.
        :type percentage: the percentage of good data that must be throw into the training set
        :param data_set: data set, the last column is the data label
        :param n: the number of rows in the data set
        :return: sample data and sample data label
        """
        # Create a sample data set with replacement of size n
        # Reference: https://en.wikipedia.org/wiki/Bootstrapping_(statistics)

        sample_data = []
        sample_label = []

        repeat_times = range(n)
        # at least 5% data should be good data
        good_data_number = n * percentage
        # the length of good data set
        good_data_length = len(good_data)

        for i in repeat_times:
            if i < good_data_number:
                random_pick_index = random.randint(0, good_data_length - 1)
                row = good_data[random_pick_index]
            else:
                random_pick_index = random.randint(0, n - 1)
                row = data_set[random_pick_index]
            sample_data.append(row[:-1])
            sample_label.append(row[-1])

        return sample_data, sample_label
        pass

    def bootstrapping(self, data_set, percentage=0.05):
        # Separate good and bad data set
        good_data = self.get_good_data(data_set)

        # Initialize the bootstrap data sets for each tree.
        for i in range(self.num_trees):
            # data_sample, data_label = self._bootstrapping(data_set, len(data_set))
            data_sample, data_label = self._bootstrapping(data_set, good_data, len(data_set), percentage)
            self.bootstraps_datasets.append(data_sample)
            self.bootstraps_labels.append(data_label)

    def get_good_data(self, data_set):
        good_data = []
        for line in data_set:
            if 1 == line[-1]:
                good_data.append(line)
        return good_data

    def fitting(self):
        # Train `num_trees` decision trees using the bootstraps datasets and labels
        repeat_range = range(self.num_trees)

        for i in repeat_range:
            print("Current building tree#: " + str(i))
            self.decision_trees[i].learn(self.bootstraps_datasets[i], self.bootstraps_labels[i])
        pass

    def voting(self, X):
        """
        M-fold cross validation. M depends on the number of trees set in the first place.
        :param X: X is the whole data set, which will be handled later.
        :return: y, where is a list with the result.
        """
        y = np.array([], dtype=int)
        count = 0

        for record in X:
            print("Current predicting: #" + str(count))
            count += 1

            votes = []
            for i in range(len(self.bootstraps_datasets)):
                dataset = self.bootstraps_datasets[i]
                if record not in dataset:
                    # Since we are doing cross validation,
                    # only the data that are not used for training
                    # can be used to test for the current tree
                    OOB_tree = self.decision_trees[i]
                    effective_vote = OOB_tree.classify(record)
                    votes.append(effective_vote)

            # pick the majority vote of M trees
            counts = np.bincount(votes)
            y = np.append(y, np.argmax(counts))

        return y


def main(percentage=0.05, forest_size=10):
    """
    Here, X is assumed to be a matrix with n rows and d columns
    where n is the number of total records
    and d is the number of features of each record
    Also, y is assumed to be a vector of d labels

    XX is similar to X, except that XX also contains the data label for
    each record.
    :param percentage: The training set good data percentage
    :param forest_size: The number of decision trees in the forest
    :return: 
    """
    print('Good percentage: %f' % percentage)
    X = list()
    y = list()
    XX = list()  # Contains data features and data labels

    # Load data set
    with open("data-set.csv") as f:
        # skip the first line
        # first line is attribute and label name
        next(f, None)

        for line in csv.reader(f, delimiter=","):
            X.append(line[:-1])
            y.append(line[-1])
            xline = [ast.literal_eval(i) for i in line]
            XX.append(xline[:])

    forest_size = 10

    # Initialize a random forest
    randomForest = RandomForest(forest_size)

    # Create the bootstrapping data sets
    randomForest.bootstrapping(XX, percentage)

    # Build trees in the forest
    randomForest.fitting()

    # Provide an unbiased error estimation of the random forest
    # based on out-of-bag (OOB) error estimate.
    y_truth = np.array(y, dtype=int)
    X = np.array(X, dtype=float)
    y_predicted = randomForest.voting(X)

    # results = [prediction == truth for prediction, truth in zip(y_predicted, y_test)]
    results = [prediction == truth for prediction, truth in zip(y_predicted, y_truth)]
    true_positive = [prediction == truth and 1 == truth for prediction, truth in zip(y_predicted, y_truth)]
    true_negative = [prediction == truth and 0 == truth for prediction, truth in zip(y_predicted, y_truth)]
    false_positive = [prediction != truth and 1 == prediction for prediction, truth in zip(y_predicted, y_truth)]
    false_negative = [prediction != truth and 0 == prediction for prediction, truth in zip(y_predicted, y_truth)]

    # Accuracy
    accuracy = float(results.count(True)) / float(len(results))
    true_positive_rate = float(true_positive.count(True)) / float(len(true_positive))
    true_negative_rate = float(true_negative.count(True)) / float(len(true_negative))
    false_positive_rate = float(false_positive.count(True)) / float(len(false_positive))
    false_negative_rate = float(false_negative.count(True)) / float(len(false_negative))

    print('--------------')
    print('Good percentage: %f' % percentage)
    print ("Accuracy: %.4f" % accuracy)
    print ("True positive rate: %.4f" % true_positive_rate)
    print ("True negative rate: %.4f" % true_negative_rate)
    print ("False positive rate: %.4f" % false_positive_rate)
    print ("False negative rate: %.4f" % false_negative_rate)
    print('--------------')


main(percentage=0.45)
