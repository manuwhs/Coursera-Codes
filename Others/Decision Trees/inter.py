import numpy as np
import scipy.stats as st


from sklearn import preprocessing
le_sex = preprocessing.LabelEncoder()

#to convert into numbers

train.Sex = le_sex.fit_transform(train.Sex)

#to convert back

train.Sex = le_sex.inverse_transform(train.Sex)








def get_count_dict(data):
    """
    Return the unique values and their frequencies as a dictionary
    :param data: a 1-D numpy array
    :return:
    """
    data_values, data_freqs = np.unique(data, return_counts=True)
    return dict(zip(data_values, data_freqs))


def hypothesis_test(attribute_data, labels, p_threshold=None, return_p_value=False):
    """
    Perform a chi-square test on the values for an attribute and their corresponding labels
    :param attribute_data:
    :param labels:
    :param p_threshold:
    :param return_p_value:
    :return: True/False for p value exceeding threshold and optionally the p value tested
    """
    # Get label frequencies
    label_counts = get_count_dict(labels)
    # Get attribute value frequencies
    attr_val_counts = get_count_dict(attribute_data)
    # Calculate length of data (outside of loops below)
    total_count = len(labels)

    # k and m will be used for degrees of freedom in chi-squared call
    # k unique classes
    k = len(label_counts)
    # m unique attribute values
    m = len(attr_val_counts)

    statistic = 0.0
    for attr_val, attr_val_count in attr_val_counts.items():
        attr_val_ratio = attr_val_count / total_count
        # Get corresponding label frequencies within this attribute value
        label_counts_attr_val = get_count_dict(labels[attribute_data == attr_val])
        for label_attr_val, label_count_attr_val in label_counts_attr_val.items():
            # Expected label count is the probability of the attribute value by the
            # probability of the label within the attribute
            exp_label_count_attr_val = attr_val_ratio * label_counts[label_attr_val]
            # Calculate the Chi-square statistic
            statistic += (label_count_attr_val - exp_label_count_attr_val)**2 / exp_label_count_attr_val

    # Calculate the p value from the chi-square distribution CDF
    p_value = 1 - st.chi2.cdf(statistic, df=(m-1)*(k-1))

    if return_p_value:
        return p_value < p_threshold, p_value
    else:
        return p_value < p_threshold


# Main decision tree class. There'll be one instance of the class per node.
class DecisionTree:
    # Main prediction at this node
    label = None
    
    # Split attribute for the children
    attribute = None
    
    # Attribute value (where attribute has been set by parent)
    attribute_value = None
    
    # A list of child nodes (DecisionTree)
    children = None
    
    # p value for hypothesis testing
    p_value = None
    
    # Threshold to test p value against
    p_threshold = None
    # the parent node (DecisionTree)
    parent = None
    # level down the tree. 1 is top level
    level = None
    # max depth, for pruning
    max_level = 10000000

    def __init__(self, dataTr, labels, attributes, fitness_func=info_gain, value=None, parent=None, p_threshold=1.0, max_level=None, old_level=0):
        """
        Create a Decision tree node
        :param Itr: Index of the training samples that fall into this node
        :param attributes: Attribute column references
        :param fitness_func: A function to test goodness of fit
        :param value: Value of the parent's split attribute
        
        :param parent: Parent of the current node
        :param p_threshold: threshold for hypothesis test
        :param level: Level of depth on the tree
        
        ### Design parameters 
        :param fitness_func: A function to test goodness of fit
        :param d_func: The function to split the data
        :return:
        """
        self.level = old_level + 1
        self.p_threshold = p_threshold

        if max_level is not None:
            self.max_level = max_level

        if value is not None:
            self.attribute_value = value

        if parent is not None:
            self.parent = parent

        # If data or remaining attributes are empty or we've reached max depth then set the node label to the most
        # common one and return
        if data.size == 0 or not attributes or self.level == self.max_level:
            try:
                # self.label = st.mode(labels)[0][0][0]
                self.label = st.mode(labels)[0][0]
            except:
                self.label = labels[len(labels) - 1]
            return

        # If labels are all the same, set label and return
        if np.all(labels[:] == labels[0]):
            self.label = labels[0]
            return

        # If corresponding attribute values are the same on every example just pick the last label and return
        # Implemented as a loop so we can stop checking as soon as we find a mismatch
        examples_all_same = True
        for i in range(1, data.shape[0]):
            for j in range(data.shape[1]):
                if data[0, j] != data[i, j]:
                    examples_all_same = False
                    break
            if not examples_all_same:
                break
        if examples_all_same:
            # Choose the last label
            self.label = labels[len(labels) - 1]
            return

        # Build the tree by splitting the data and adding child trees
        self.build(data, labels, attributes, fitness_func)
        return

    def __repr__(self):
        if self.children is None:
            return "x[{0}]={1}, y={2}".format(self.parent.attribute, self.attribute_value, self.label)
        else:
            if self.parent is not None:
                return "x[{0}]={1}, p={2}".format(self.parent.attribute, self.attribute_value, self.p_value)
            else:
                return "p={0}".format(self.p_value)




    def classify(self, data):
        """
        Make predictions for the rows passed in data
        :param data: rows of attribute values
        :return: a numpy array of labels
        """
        if data.size == 0:
            return

        # If we're down to one record then convert it back to a 2-D array
        if len(data.shape) == 1:
            data = np.reshape(data, (1,len(data)))

        if self.children is None:
            # If we're at the bottom of the tree then return the labels for all records as the tree node label
            labels = np.ones(len(data)) * self.label
            return labels

        labels = np.zeros(len(data))

        for child in self.children:
            # Get the array indexes where the split attibute value  = child attribute value
            child_attr_val_idx = data[:,self.attribute] == child.attribute_value
            # pass the array subsets to child trees for classification
            labels[child_attr_val_idx] = child.classify(data[child_attr_val_idx])

        return labels