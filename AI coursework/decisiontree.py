from decisiontreedata import get_tree_data, sort_data
from collections import Counter
from math import log2
import matplotlib.pyplot as plt
class Attribute():
    """Class which represents a attribute"""
    def __init__(self, value, equailty):
        self.value = value
        self.equality = equailty
        self.childTrue = None
        self.childFalse = None
        self.parent = None
        self.index = 0

    def passed(self, other):
        """Method to check if a datapoint passes this attribute
        
        Args
        self - this object
        other - datapoint to compare to
        
        Returns
        Boolean of if the datapoint passes or not"""
        if self.equality == "equal to":
            return self.value == float(other)
        if self.equality == "less than":
            return self.value > float(other)
        if self.equality == "greater than":
            return self.value < float(other)
        return False

    def __eq__(self, other):
        """Comparison function"""
        if other == None:
            return False
        return self.value == other.value and self.equality == other.equality

class DecisionTree():
    """Class to represent the decision tree"""
    def __init__(self, root:Attribute, nodes:list):
        self.root = root
        self.nodes = nodes


def get_mode(data:list)->str:
    """Gets modal value from list

    Args
    data - data to get mode from

    Returns
    modal value string"""
    
    classifications_list = []
    for item in data:
        classifications_list.append(item[21])
    counted_classifications = Counter(classifications_list)
    return counted_classifications.most_common(1)[0][0]

def entropy_calculation(dataset:list)->float:
    """Calculates the entropy of a given list

    Args
    dataset - List of dataset to calculate entropy for

    Returns
    float - float value of the entropy of list"""
    list_length = len(dataset)
    counted_list = Counter(dataset)
    entropy = 0
    for count in counted_list.most_common(5):
        if count[1] != 0:
            entropy += (count[1]/list_length)*log2(count[1]/list_length)
    return -entropy

def calculate_ig(start_list:list, true_list:list, false_list:list)->float:
    """Calculates the information gain from a set of data

    Args
    start_list - list before it is split
    true_lsit - list of items that ended up being true
    false_list - list of items that ended up being false
    
    Returns
    float - float representing information gain of this data"""
    start_entropy = entropy_calculation(start_list)
    true_entropy = entropy_calculation(true_list)
    false_entropy = entropy_calculation(false_list)
    ig = start_entropy - ((len(true_list)/len(start_list))*true_entropy+(len(false_list)/len(start_list))*false_entropy)
    return ig

def choose_attribute(examples, attributes):
    """Chooses the best attribute from a list
    
    Args
    examples - training data
    attributes - attributes list to select best from
    
    Returns
    attribute which is the best attribute from the list"""
    current_best_ig = 0
    current_best_index = 0
    current_for_entropy = []
    for item in examples:
        current_for_entropy.append(item[21])
    for i in range(0,len(attributes)):
        current_true = []
        current_false = []
        current_attribute = attributes[i]
        for item in examples:
            if current_attribute.passed(item[current_attribute.index]):
                current_true.append(item[21])
            else:
                current_false.append(item[21])
        temp_ig = calculate_ig(current_for_entropy, current_true, current_false)
        if temp_ig > current_best_ig:
            current_best_ig = temp_ig
            current_best_index = i
    return attributes[current_best_index]

def DTL(examples:list, attributes:list, default:str)->DecisionTree:
    """Produces the decision tree for a set of attributes and a set of training data
    
    Args
    examples - training data
    attributes - list of attributes for the decision tree
    default - default value to assign to a data point
    
    Returns
    decision tree for the data or a classification"""
    #Check there is still training data left
    if len(examples) == 0:
        return default
    #Check that classifications are not uniform
    classification_uniform = True
    for item in examples:
        if item[21] != examples[0][21]:
            classification_uniform = False
    if classification_uniform:
        return examples[0][21]
    #Check if there are attributes to select
    if len(attributes) == 0:
        return get_mode(examples)
    #choose best attribute
    best_attribute = choose_attribute(examples, attributes)
    #sort into passed data and failed data lists
    passed_examples = []
    failed_examples = []
    for item in examples:
        if best_attribute.passed(item[best_attribute.index]):
            passed_examples.append(item)
        else:
            failed_examples.append(item)
    #make copies of attributes due to them being passed by reference in python
    attributes_copy = list(attributes)
    attributes_true = []
    attributes_false = []
    temp_index = attributes_copy.index(best_attribute)
    del attributes_copy[temp_index]
    for item in attributes_copy:
        temp_attribute_1 = Attribute(item.value, item.equality)
        temp_attribute_1.index = item.index
        temp_attribute_2 = Attribute(item.value, item.equality)
        temp_attribute_2.index = item.index
        attributes_true.append(temp_attribute_1)
        attributes_false.append(temp_attribute_2)
    #Get sub trees
    true_tree = DTL(passed_examples, attributes_true, get_mode(examples))
    false_tree = DTL(failed_examples, attributes_false, get_mode(examples))
    #Check whether sub trees are trees or strings
    if isinstance(true_tree, DecisionTree):
        true_tree.root.parent = best_attribute
        best_attribute.childTrue = true_tree.root
    elif true_tree == None:
        best_attribute.childTrue = get_mode(examples)
    else:
        best_attribute.childTrue = true_tree
    if isinstance(false_tree, DecisionTree):
        false_tree.root.parent = best_attribute
        best_attribute.childFalse = false_tree.root
    elif false_tree == None:
        best_attribute.childFalse = get_mode(examples)
    else:
        best_attribute.childTrue = false_tree
    #Catch if false somehow gets assigned a none value
    if best_attribute.childFalse == None:
        best_attribute.childFalse = get_mode(examples)
    tree = DecisionTree(best_attribute, attributes)
    return tree

def depth_limited_DTL(examples:list, attributes:list, default:str, depth:int)->DecisionTree:
    """Produces a decision tree with a limit on the tree depth
    
    Args
    examples - training data
    attributes - list of attributes for the decision tree
    default - default value to assign to a data point
    depth - depth limit of the tree
    
    Returns
    decision tree for the data or a classification"""
    #Check there is still training data left
    if len(examples) == 0:
        return default
    #Check that classifications are not uniform
    classification_uniform = True
    for item in examples:
        if item[21] != examples[0][21]:
            classification_uniform = False
    if classification_uniform:
        return examples[0][21]
    #Check if there are attributes to select
    if len(attributes) == 0:
        return get_mode(examples)
    #Check depth limit has not been reached
    if depth == 0:
        return get_mode(examples)
    #choose best attribute
    best_attribute = choose_attribute(examples, attributes)
    #sort into passed data and failed data lists
    passed_examples = []
    failed_examples = []
    for item in examples:
        if best_attribute.passed(item[best_attribute.index]):
            passed_examples.append(item)
        else:
            failed_examples.append(item)
    #make copies of attributes due to them being passed by reference in python
    attributes_copy = list(attributes)
    attributes_true = []
    attributes_false = []
    temp_index = attributes_copy.index(best_attribute)
    del attributes_copy[temp_index]
    for item in attributes_copy:
        temp_attribute_1 = Attribute(item.value, item.equality)
        temp_attribute_1.index = item.index
        temp_attribute_2 = Attribute(item.value, item.equality)
        temp_attribute_2.index = item.index
        attributes_true.append(temp_attribute_1)
        attributes_false.append(temp_attribute_2)
    #Get subtrees
    true_tree = depth_limited_DTL(passed_examples, attributes_true, get_mode(examples), depth-1)
    false_tree = depth_limited_DTL(failed_examples, attributes_false, get_mode(examples), depth -1)
    if isinstance(true_tree, DecisionTree):
        true_tree.root.parent = best_attribute
        best_attribute.childTrue = true_tree.root
    elif true_tree == None:
        best_attribute.childTrue = get_mode(examples)
    else:
        best_attribute.childTrue = true_tree
    #Check whether sub trees are trees or strings
    if isinstance(false_tree, DecisionTree):
        false_tree.root.parent = best_attribute
        best_attribute.childFalse = false_tree.root
    elif false_tree == None:
        best_attribute.childFalse = get_mode(examples)
    else:
        best_attribute.childTrue = false_tree
    #Catch if false somehow gets assigned a none value
    if best_attribute.childFalse == None:
        best_attribute.childFalse = get_mode(examples)
    tree = DecisionTree(best_attribute, attributes)
    return tree

def DTL_chart():
    """Function to plot a chart of accuracy against decision tree depth"""
    names = []
    values = []
    data = get_tree_data()
    attributes_list = setup_attributes()
    for i in range(1,21):
        count = 0
        names.append(i)
        temp_tree = depth_limited_DTL(data, attributes_list, get_mode(data), i)
        values.append(accuracy_test(temp_tree))
    plt.plot(names, values)
    plt.ylabel("Precent Accuracy")
    plt.xlabel("Recursion Depth")
    plt.show()


def setup_attributes()->list:
    """Function which creates the list of attributes. Created to make code more readable
    
    Returns
    A list of all the attributes to use in the decision tree"""
    #Give each attribute its average
    R_intersections  = Attribute(3.7845574768348187, "greater than")
    R_diversity = Attribute(1.318174459765588,"greater than")
    R_total = Attribute(5.983660185122511,"greater than")
    B_diversity = Attribute(0.8464037529991364,"greater than")
    B_total = Attribute(0.22528549504967743,"greater than")
    LU_mix = Attribute(8.496650140012384e-10,"greater than")
    TP_crossing = Attribute(0.2399348003134439,"greater than")
    pois_park = Attribute(6.022228757995691e-08,"greater than")
    pois_pitch = Attribute(5.579459327021355e-09,"greater than")
    pois_diversity = Attribute(3.0087034204951686,"greater than")
    pois_total = Attribute(1.0858132798012943,"greater than")
    TP_oa_count = Attribute(0.09198721614749146,"greater than")
    TP_edt_count = Attribute(0.2636865402264445,"greater than")
    TP_out_count = Attribute(0.10025112844124064,"greater than")
    TP_cv_count = Attribute(0.2224524164110635,"greater than")
    TP_diverstiy = Attribute(0.020769924644401888,"greater than")
    TP_total = Attribute(0.6783773012062729,"greater than")
    V_density = Attribute(2.8972394101055436,"greater than")
    B_age = Attribute(52.712325278083874,"greater than")
    B_age_diversity = Attribute(1.382932767676439,"greater than")

    #give each attribute its column index
    R_intersections.index = 1
    R_diversity.index = 2
    R_total.index = 3
    B_diversity.index = 4
    B_total.index = 5
    LU_mix.index = 6
    TP_crossing.index = 7
    pois_park.index = 8
    pois_pitch.index = 9
    pois_diversity.index = 10
    pois_total.index = 11
    TP_oa_count.index = 12
    TP_edt_count.index = 13
    TP_out_count.index = 14
    TP_cv_count.index = 15
    TP_diverstiy.index = 16
    TP_total.index = 17
    V_density.index = 18
    B_age.index = 19
    B_age_diversity.index = 20

    return_list =[R_intersections, R_diversity, R_total, B_diversity, B_total,
                  LU_mix, TP_crossing, pois_park, pois_pitch, pois_diversity,pois_total,
                  TP_oa_count, TP_edt_count, TP_out_count, TP_cv_count,
                  TP_diverstiy, TP_total, V_density, B_age, B_age_diversity]
    return return_list

def accuracy_test(tree: DecisionTree)->float:
    """Calculates the accuracy percentage
    
    Args
    tree - decision tree to calculate accuracy for
    
    Returns
    float representing percentage accuracy"""
    test_data = get_tree_data()
    root = tree.root
    correct = 0
    for item in test_data:
        current_node = root
        classified = False
        while not classified:
            if current_node.passed(item[current_node.index]):
                current_node = current_node.childTrue
            else:
                current_node = current_node.childFalse
            if isinstance(current_node, str):
                classified = True
                if current_node == item[21]:
                    correct += 1
    return correct/len(test_data)

if __name__ == "__main__":
    #training_data = get_tree_data()
    #attributes_list = setup_attributes()
    #tree = DTL(training_data, attributes_list, get_mode(training_data))
    DTL_chart()