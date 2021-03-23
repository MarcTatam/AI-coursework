from decisiontreedata import get_data, sort_data
from collections import Counter
class Attribute():
    def __init__(self, value, equailty):
        self.value = value
        self.equality = equailty
        self.under_eighteen_passed = 0
        self.eighteen_to_thirty_passed = 0
        self.thirty_to_fourty_passed = 0
        self.fourty_to_fifty_passed = 0
        self.fifty_to_sixty_passed = 0
        self.sixty_plus_passed = 0
        self.under_eighteen_failed = 0
        self.eighteen_to_thirty_failed = 0
        self.thirty_to_fourty_failed = 0
        self.fourty_to_fifty_failed = 0
        self.fifty_to_sixty_failed = 0
        self.sixty_plus_failed = 0
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

    def training_passed(self, other, classification):
        if passed(self, other):
            if classification == "age_under_18":
                self.under_eighteen_passed += 1
            elif classification == "age_18_30":
                self.eighteen_to_thirty_passed += 1
            elif classification == "age_30_40":
                self.thirty_to_fourty_passed += 1
            elif classification == "age_40_50":
                self.fourty_to_fifty_passed += 1
            elif classification == "age_50_60":
                self.fifty_to_sixty_passed +=1
            elif classification == "age_over_60":
                self.sixty_plus_passed += 1
        else:
            if classification == "age_under_18":
                self.under_eighteen_failed += 1
            elif classification == "age_18_30":
                self.eighteen_to_thirty_failed += 1
            elif classification == "age_30_40":
                self.thirty_to_fourty_failed += 1
            elif classification == "age_40_50":
                self.fourty_to_fifty_failed += 1
            elif classification == "age_50_60":
                self.fifty_to_sixty_failed +=1
            elif classification == "age_over_60":
                self.sixty_plus_failed += 1

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


