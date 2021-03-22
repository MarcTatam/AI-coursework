from sklearn.datasets import load_digits
from sklearn.cluster import KMeans
from collections import Counter
import matplotlib.pyplot as plt

#Load data
digits = load_digits()
#Perform K-Means
kmeans = KMeans(n_clusters=10, max_iter=1000, n_init=20)
kmeans.fit(digits.data)

#Get prediction data
prediction = kmeans.fit_predict(digits.data)
#Get actual values
target = digits.target
#Intialise dictionary which will contain a list of target values for each prediction cluster
indexes_dict = {0 : [], 1 : [], 2 : [], 3 : [], 4 : [], 5 : [], 6 : [], 7 : [], 8 : [], 9 : []}
#Init number of incorrectly classified digits dictionary
incorrect_dict = {0 : 0, 1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0, 8 : 0, 9 : 0}
#Init total number of digits classified as this digit dict
total_dict = {0 : 0, 1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0, 8 : 0, 9 : 0}
incorrect = 0
names = []
values = []

#For each data item add target value to associated cluster list
for i in range(0, 1797):
    indexes_dict[prediction[i]] = indexes_dict[prediction[i]] + [target[i]]

#For each cluster
for i in range(0,10):
    #Get associated target list
    this_list = indexes_dict[i]
    #Count frequency of each item in list
    counted_list = Counter(this_list)
    #Get most common item and set it as the current true value
    for target_value, count in counted_list.most_common(1):
        current_true_value = target_value
        #Add to total for this digit
        total_dict[current_true_value] = count
    #For each item in counted list
    for target_value, count in counted_list.most_common(10):
        current_incorrect_value = target_value
        #If true value do nothing
        if current_incorrect_value == current_true_value:
            continue
        #Else add to incorrect count and total count
        else:
            incorrect += 1
            incorrect_dict[current_true_value] = incorrect_dict[current_true_value] + count
            total_dict[current_true_value] = total_dict[current_true_value] + count

for i in range(0,10):
    #Add digit to names list
    names.append(i)
    #Calculate incorrectly classified digits percentage and add to values list
    percent_accuracy = (incorrect_dict[i]/total_dict[i])*100
    values.append(percent_accuracy)

#Plot chart
plt.bar(names,values)
plt.xticks(range(10))
plt.ylabel("Percentage Inaccuracy")
plt.xlabel("Estimated Digit")
plt.title("Innaccuracy of K-Means Classification")
plt.show()
