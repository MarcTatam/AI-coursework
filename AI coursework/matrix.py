from sklearn.datasets import load_digits
from sklearn.cluster import KMeans
from collections import Counter
import matplotlib.pyplot as plt

#Get data set
digits = load_digits()

#Make K means plot
kmeans = KMeans(n_clusters=10, max_iter=1000, n_init=20)
kmeans.fit(digits.data)

#Get prediction for each item in data set
prediction = kmeans.fit_predict(digits.data)

#Get actual value for each item in dataset
target = digits.target

#Intialise dictionary which will contain a list of target values for each prediction cluster
indexes_dict = {0 : [], 1 : [], 2 : [], 3 : [], 4 : [], 5 : [], 6 : [], 7 : [], 8 : [], 9 : []}

#Matrix to store data to be plotted
matrix = [[0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0]]

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
        current_true = target_value
    #Map each count to the matrix. Counter.most_common returns 0 for non existent indecies
    for target_value, count in counted_list.most_common(10):
        matrix[current_true][target_value] = count

#Plot heat map and labels
plt.imshow(matrix)
plt.xticks(range(10))
plt.yticks(range(10))
plt.colorbar()
plt.ylabel("Classification")
plt.xlabel("Actual Value")
plt.title("Innaccuracy of K-Means Classification")
plt.show()
