import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split

# Task 2.2
drugfile = pd.read_csv('drug200.csv')

# Task 2.3
drug_array = np.array(drugfile["Drug"])

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
