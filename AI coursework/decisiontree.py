from decisiontreedata import get_data, sort_data
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