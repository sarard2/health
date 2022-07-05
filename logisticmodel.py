#Importing Needed Libraries
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, ConfusionMatrixDisplay,RocCurveDisplay, precision_score, recall_score, f1_score, classification_report, roc_curve, plot_roc_curve, auc, precision_recall_curve, plot_precision_recall_curve, average_precision_score
from sklearn.model_selection import cross_val_score


#Reading data
data=pd.read_csv("https://raw.githubusercontent.com/sarard2/health/main/healthdata.csv")
#Inspecting the data
print(data.head())
print(data.info())
#Dropping the ID column as it doesn't represent a feature
data.drop(columns=['id'],inplace=True)
print(data.head())
#Missing values check
print(data.isna().sum().plot(kind="bar",rot=45))
plt.show()

#Defining the features X and the target variable y
X=data.drop('stroke', axis=1)
y=data['stroke']

#Split into training and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.25, random_state= 0)

#For the dimensions of train and test data
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

# Impute with the mean of the training and the test data
BMI_train = X_train['bmi'].mean()
BMI_test = X_test['bmi'].mean()
X_train = X_train.fillna(value=BMI_train)
X_test = X_test.fillna(value=BMI_test)

#Double check for missing values
print(X_train.isna().sum().plot(kind="bar",rot=45))
plt.show()
print(X_test.isna().sum().plot(kind="bar",rot=45))
plt.show()

#Before modeling, categorical variables need to be changed
#Converting Categorical Features into numerical form using LabelEncoder()
le = LabelEncoder()

#For the train dataset

#Gender
print(X_train["gender"].value_counts())
X_train["gender"]=le.fit_transform(X_train["gender"])
print(X_train["gender"].value_counts())
#Thus Female is 0, Male is 1, and Other is 2

#Marriage
print(X_train["ever_married"].value_counts())
X_train["ever_married"]=le.fit_transform(X_train["ever_married"])
print(X_train["ever_married"].value_counts())
#Thus Yes is 1 (married) and No is 0 (not married)

#Work Type
print(X_train["work_type"].value_counts())
X_train["work_type"] = le.fit_transform(X_train["work_type"])
print(X_train["work_type"].value_counts())
#Thus gov job is 0, Never worked is 1, Private is 2, self employed is 3, children is 4.

#Residence Type
print(X_train["residence_type"].value_counts())
X_train["residence_type"] = le.fit_transform(X_train["residence_type"])
print(X_train["residence_type"].value_counts())
#Thus Rural is 0, and Urban is 1

#Smoking Status
print(X_train["smoking_status"].value_counts())
X_train["smoking_status"]=le.fit_transform(X_train["smoking_status"])
print(X_train["smoking_status"].value_counts())
#Thus Unknown is 0, formerly smoked is 1, never smoked is 2, and smokes is 3


#For the test data

X_test["gender"]=le.fit_transform(X_test["gender"])
X_test["ever_married"]=le.fit_transform(X_test["ever_married"])
X_test["work_type"] = le.fit_transform(X_test["work_type"])
X_test["residence_type"] = le.fit_transform(X_test["residence_type"])
X_test["smoking_status"]=le.fit_transform(X_test["smoking_status"])

#Modeling Stage
lr = LogisticRegression()
lr.fit(X_train,y_train)
y_pred = lr.predict(X_test)

#Checking Accuracy of the model
acc_score_lr=accuracy_score(y_test,y_pred)*100
print("accuracy score: ",accuracy_score(y_train,lr.predict(X_train))*100)
print("accuracy score: ",acc_score_lr)
print(f"Confusion Matrix :- \n {confusion_matrix(y_test,y_pred)}")
print(f"Classification Report : -\n {classification_report(y_test, y_pred)}")


#Moving it into pickle file to be used in streamlit
import pickle
file = open(r"C:\Users\Sara\Desktop\logisticmodel.pkl", "wb")
pickle.dump(lr , file)
file.close()
model = open(r"C:\Users\Sara\Desktop\logisticmodel.pkl", "rb")
forest = pickle.load(model)
