import matplotlib.pyplot as plt
import os
from sklearn.datasets import  load_files
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from tabulate import tabulate
from sklearn.pipeline import make_pipeline


# Task 1.2

business = 'MP1/BBC/business'
entertainment = 'MP1/BBC/entertainment'
politics = 'MP1/BBC/politics'
sport = 'MP1/BBC/sport'
tech = 'MP1/BBC/tech'

totalBusinessFiles = 0
totalEntertainmentFiles = 0
totalPoliticsFiles = 0
totalSportFiles = 0
totalTechFiles = 0

for base, dirs, files in os.walk(business):
    for Files in files:
        totalBusinessFiles += 1

for base, dirs, files in os.walk(entertainment):
    for Files in files:
        totalEntertainmentFiles += 1

for base, dirs, files in os.walk(politics):
    for Files in files:
        totalPoliticsFiles += 1

for base, dirs, files in os.walk(sport):
    for Files in files:
        totalSportFiles += 1

for base, dirs, files in os.walk(tech):
    for Files in files:
        totalTechFiles += 1

x = range(5)
x_labels = ['Business', 'Entertainment', 'Politics', 'Sport', 'Tech']
y = [totalBusinessFiles, totalEntertainmentFiles, totalPoliticsFiles, totalSportFiles, totalTechFiles]


plt.bar(x, y, color=['black', 'red', 'green', 'blue', 'yellow'], align='center')
plt.title('BBC Distribution')
plt.ylabel("Total number of instances per class", fontsize = 10)
plt.xticks(x, x_labels)
plt.grid(True)

for index,data in enumerate(y):
    plt.text(x=index , y =data+1 , s=f"{data}" , fontdict=dict(fontsize=12, color = 'maroon'))

#plt.savefig('BBC-distribution.pdf')

 
 # Task 1.3

bbc_data = load_files('MP1/BBC',load_content=True, encoding = 'latin1')


# Task 1.4

vectorizer = CountVectorizer()
vectorizer.fit(bbc_data.data)

vectorizer.get_feature_names_out()

#X_train
bbc_data_transformed = vectorizer.transform(bbc_data.data)

bbc_data_transformed.toarray()

# print(pd.DataFrame(bbc_data_transformed.toarray(), columns=vectorizer.get_feature_names_out()))

# print("\nSparse matrix\n" , bbc_data_transformed)

# print ("\nDense matrix\n", bbc_data_transformed.toarray())


# Task 1.5

# y_train
BBC_Y = bbc_data.target

X_train, X_test, y_train, y_test  = train_test_split(bbc_data_transformed, BBC_Y,  test_size=0.20, train_size=0.8, random_state=None)


# Task 1.6 

classifier_MNB = MultinomialNB()
classifier_MNB.fit(X_train, y_train)
prediction = classifier_MNB.predict(X_test)


# Task 1.7
f = open("bbc-performance.txt", "w")
f.write("(a) ======= MultinomialNB default values, try 1 =======\n\n(b)\n")
cm = confusion_matrix(y_test, prediction)
confusion_matrix = pd.DataFrame(cm, index=x_labels)
f.write(tabulate(confusion_matrix, x_labels))
f.close()