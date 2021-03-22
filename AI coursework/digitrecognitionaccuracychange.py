from sklearn.datasets import load_digits
from sklearn.cluster import KMeans
from collections import Counter
import matplotlib.pyplot as plt
#Load data
digits = load_digits()
names = []
values = []

#For a repition with max_iter of 1-40
for i in range(0, 41):
    #Set current max iteration count
    current_iter = i+1
    #Add current max iteration count to names list
    names.append(current_iter)
    #Init inertia
    inertia = 0
    #Repeat K-Means 20 times
    for j in range(0,21):
        #Perform K-Means
        kmeans = KMeans(n_clusters=10, max_iter=current_iter, n_init=20)
        kmeans.fit(digits.data)
        inertia += kmeans.inertia_
    #Average inertia value for current max_iteration
    values.append(inertia/20)
#Plot
plt.plot(names,values)
plt.ylabel("inertia")
plt.xlabel("Number of Iterations")
plt.title("Innaccuracy of K-Means Classification")
plt.show()
