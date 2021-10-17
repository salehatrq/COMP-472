import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import Perceptron
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV


# Task 2.2
drug_file = pd.read_csv('MP1/drug200.csv')

# Task 2.3
drug_array = np.array(drug_file["Drug"])

(unique_drug, frequency) = np.unique(drug_array, return_counts=True)

#Creates a bar chart showing the frequencing of the drugs
plt.bar(unique_drug, frequency, width = 0.8)

plt.xlabel("Drug")
plt.ylabel("Frequency")

plt.title("Drug distribution")

#Saves the figure to a PDF file
plt.savefig("drug-distribution.pdf")

# Task 2.4
drug_file["BP"] = pd.Categorical(drug_file["BP"], ['LOW', 'NORMAL', 'HIGH'], ordered=True)
drug_file["Cholesterol"] = pd.Categorical(drug_file["Cholesterol"], ['NORMAL', 'HIGH'], ordered=True)

numerical_data = pd.get_dummies(drug_file, columns=['Sex', 'BP', 'Cholesterol'])

#Task 2.5
X_data = numerical_data[['Age', 'Na_to_K', 'Sex_F', 'Sex_M', 'BP_LOW', 'BP_NORMAL', 'BP_HIGH', 'Cholesterol_NORMAL', 'Cholesterol_HIGH']]

X_train, X_test, y_train, y_test = train_test_split(X_data, drug_array)

# Task 2.6
#a) Gaussian Naive Bayes Classifier with default parameters
gnb_classifier = GaussianNB()
gnb_classifier.fit(X_train, y_train)

#b) Decision Tree with default parameters
base_dt_classifier = DecisionTreeClassifier()
base_dt_classifier.fit(X_train, y_train)

#c) Better performing Decision Tree
hyper_params = {'criterion':['gini', 'entropy'], 'max_depth': [2,10,20], 'min_samples_split': [2, 20, 50]}

top_dt_classifier = GridSearchCV(DecisionTreeClassifier(), hyper_params)
top_dt_classifier.fit(X_train, y_train)

#d) Perceptron with default parameters
perceptron_classifier = Perceptron()
perceptron_classifier.fit(X_train, y_train)

#e) Multi-Layered Perceptron with the provided parameters -- RETURNS A WARNING 
base_ml_perceptron_classifier = MLPClassifier(hidden_layer_sizes=(100,1), activation='logistic', solver='sgd')
base_ml_perceptron_classifier.fit(X_train, y_train)

#f) Better performing Multi-Layered Perceptron -- RETURNS A WARNING
params = {'activation':['identity', 'logistic', 'tanh', 'relu'], 'solver': ['sgd', 'adam'], 'hidden_layer_sizes': [[10,10,10], [50,30]]} 

top_ml_perceptron_classifier = GridSearchCV(MLPClassifier(), params)
top_ml_perceptron_classifier.fit(X_train, y_train)

# Task 2.7
separator = '----------------------------------------------\n\n'
class_arr = ['DrugA', 'DrugB', 'DrugC', 'DrugX', 'DrugY']

performance_file = open('drugs-performance.txt', 'w')

def dostepseven(classifier_obj):
	cf_matrix = confusion_matrix(y_test, classifier_obj.predict(X_test))
	np.savetxt(performance_file, cf_matrix, fmt='%.0f', delimiter='|')

	precision = precision_score(y_test, classifier_obj.predict(X_test), average=None)
	performance_file.write("Precision Measures by Class\n")

	for i in range(len(class_arr)):
		performance_file.write(class_arr[i] + ':' + format(precision[i], '.2f') + '\t\n')

	recall = recall_score(y_test, classifier_obj.predict(X_test), average=None)
	performance_file.write("Recall Measures by Class\n")

	for i in range(len(class_arr)):
		performance_file.write(class_arr[i] + ':' + format(recall[i], '.2f') + '\t\n')

	f1 = f1_score(y_test, classifier_obj.predict(X_test), average=None)
	performance_file.write("F1 Measures by Class\n")

	for i in range(len(class_arr)):
		performance_file.write(class_arr[i] + ':' + format(f1[i], '.2f') + '\t\n')

	accuracy = accuracy_score(y_test, classifier_obj.predict(X_test))
	performance_file.write("\nAccuracy of the model: " + str(accuracy) + "\n")

	f1_macroavg = f1_score(y_test, classifier_obj.predict(X_test), average='macro')
	performance_file.write("Macro-average F1 of the model: " + str(f1_macroavg) + "\n")

	f1_weightedavg = f1_score(y_test, classifier_obj.predict(X_test), average='weighted')
	performance_file.write("Weighted-average F1 of the model: " + str(f1_weightedavg) + "\n")

# NB
performance_file.write("Gaussian Naive Bayes Classifier\na)\n")
dostepseven(gnb_classifier)
performance_file.write(separator)

# Base-DT
performance_file.write("Base Decision Tree Classifier\nb)\n")
dostepseven(base_dt_classifier)
performance_file.write(separator)

# Top-DT
performance_file.write("Top Decision Tree Classifier\nc)\n")
dostepseven(top_dt_classifier)
performance_file.write(separator)

# PER
performance_file.write("Perceptron Classifier\nd)\n")
dostepseven(perceptron_classifier)
performance_file.write(separator)

# Base-MLP
performance_file.write("Base Multi-Layered Perceptron Classifier\ne)\n")
dostepseven(perceptron_classifier)
performance_file.write(separator)

# Top-MLP
performance_file.write("Top Multi-Layered Perceptron Classifier\nf)\n")
dostepseven(top_ml_perceptron_classifier)
performance_file.write(separator)
