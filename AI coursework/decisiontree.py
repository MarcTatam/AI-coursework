from decisiontreedata import get_data, sort_data
from collections import Counter
from math import log2
class Attribute():
    def __init__(self, value, equailty):
        self.value = value
        self.equality = equailty
        self.childTrue = None
        self.childFalse = None
        self.parent = None
        self.index = 0

    def passed(self, other):
        if self.equality == "equal to":
            return self.value == other
        if self.equality == "less than":
            return self.value > other
        if self.equality == "greater than":
            return self.value < other
        return False

    def __eq__(self, other):
        return self.value == other.value and self.equality == other.equality

class DecisionTree():
    def __init__(self, root:Attribute):
        self.root = root

def get_mode(examples:list)->str:
    classifications_list = []
    for item in examples:
        classification_list.append(item[21])
    counted_classifications = Counter(classification_list)
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
    current_best_ig = 0
    current_best_index = 0
    for i in range(0,len(attributes)):
        current_true = []
        current_false = []
        current_attribute = attributes[i]
        for item in examples:
            if current_attribute.passed(item[current_attribute.index]):
                current_true.append(item[21])
            else:
                current_fales.append(item[21])
        temp_ig = calculate_ig(examples, current_true, current_false)
        if temp_ig > current_best_ig:
            current_best_ig = temp_ig
            current_best_index = i
    return attributes[current_best_index]

def DTL(examples:list, attributes:list, default:str)->DecisionTree:
    if len(examples == 0):
        return default
    classification_unifrom == True
    for item in examples:
        if item[21] != examples[0][21]:
            classification_uniform = False
    if classification_uniform:
        return examples[0][21]
    if len(attributes) == 0:
        return get_mode(examples)
    best_attribute = choose_attribute(examples, attributes)
    passed_examples = []
    failed_examples = []
    for item in examples:
        if best_attribute.passed(item):
            passed_examples.append(item)
        else:
            failed_examples.append(item)
    attributes_copy = []
    for attribute in attributes:
        if attribute != best_attribute:
            attributes_copy.append(attribute)
    true_tree = DTL(passed_examples, attributes_copy, get_mode(examples))
    false_tree = DTL(failed_examples, attributes_copy, get_mode(examples))
    if isinstance(true_tree, DecisionTree):
        true_tree.root.parent = best_attribute
        best_attribute.childTrue = true_tree.root
    else:
        best_attribute.childTrue = true_tree
    if isinstance(false_tree, DecisionTree):
        false_tree.root.parent = best_attribute
        best_attribute.childTrue = false_tree.root
    else:
        best_attribute.childTrue = false_tree
    tree = DecisionTree(best_attribute)
    return tree

def setup_attributes()->list:
    """Function which creates the list of attributes. Created to make code more readable
    
    Returns
    A list of all the attributes to use in the decision tree"""
    R_intersections  = Attribute(0, "greater than")
    R_


if __name__ == "__main__":
    print(entropy_calculation(["b","b","b","b","b","g","g","g","g","g"]))
    print(calculate_ig(["b","b","b","b","b","g","g","g","g","g"],["b","g","g","g","g","g"],["b","b","b","b"]))