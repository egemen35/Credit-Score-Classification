# -*- coding: utf-8 -*-
"""Bitirme

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-wT9Vv1ANXvpJdgx5atLI8rQNpQnsWxw

# Kütüphaneler
"""

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
drive.mount('/gdrive')
# %cd /gdrive/MyDrive/Bitirme

#1.kutuphaneler
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import seaborn as sbn
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from google.colab import files

!pip install catboost
!pip install category_encoders

"""# Yeni Veriseti"""

from category_encoders.cat_boost import CatBoostEncoder
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
ohe = preprocessing.OneHotEncoder()
#2.veri onisleme
#2.1.veri yukleme
Train = pd.read_csv('trainc.csv')
Test = pd.read_csv('testc.csv')
Trainorjinal = pd.read_csv('train.csv')
Testorjinal = pd.read_csv('test.csv')

#test
TrainCols = list(Trainorjinal.columns.values)
TrainCols2 = list(Train.columns.values)

#Eksik veriler
c28 = Trainorjinal['Amount_invested_monthly']
c28 = pd.DataFrame(c28)
print(c28.dtypes)
rc28 = c28.replace('__10000__', 'NaN')
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
imputer = imputer.fit(rc28)
c30 = imputer.transform(rc28)
c30 = pd.DataFrame(c30, columns=['Amount invested monthly'])

#bağımlıdeğişken
bagımlı = Train.iloc[:,-1]
bagımlı= pd.DataFrame(bagımlı)
bagımlı= le.fit_transform(bagımlı).ravel()
bagımlı = pd.DataFrame(bagımlı, columns=['bagımlı'])

CBE = CatBoostEncoder()

#ENCODE EDİLMESİ GEREKENLER

#MESLEK
meslek = Train.iloc[:,6]
meslek = pd.DataFrame(meslek)
meslek = CBE.fit_transform(meslek, bagımlı)


#creditmix
Creditmix = Train.iloc[:,18]
Creditmix = pd.DataFrame(Creditmix)
Creditmix = CBE.fit_transform(Creditmix, bagımlı)


#PaymentofMinAmount

Pofa = Train.iloc[:,-6]
Pofa = pd.DataFrame(Pofa)
Pofa = CBE.fit_transform(Pofa, bagımlı)

#PaymentBehavior
PaymentBehavior = Train.iloc[:,-3]
PaymentBehavior = pd.DataFrame(PaymentBehavior)
PaymentBehavior = CBE.fit_transform(PaymentBehavior, bagımlı)


#Veri setinin ML e hazırlanması
Train = Train.drop(['ID','Customer_ID','Month','Name','Age','SSN','Occupation','Credit_Mix','Type_of_Loan','Payment_of_Min_Amount','Amount_invested_monthly', 'Payment_Behaviour'], axis=1)

#verilerin bağımlı ve bağımsız olarak ayrılması
bagımsız = Train.iloc[:,:15]

#birleştirme işlemleri
A = pd.concat([c30,meslek,Creditmix,Pofa,PaymentBehavior,bagımsız], axis=1)
B = bagımlı
from sklearn.model_selection import train_test_split
x_train, x_test,y_train,y_test = train_test_split(A,B,test_size=0.33, random_state=0)

"""
#verilerin olceklenmesi
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
X_train = sc.fit_transform(x_train)
X_test = sc.transform(x_test)
"""
#verilerin olceklenmesi
from sklearn.preprocessing import RobustScaler
sc=RobustScaler()
X_train = sc.fit_transform(x_train)
X_test = sc.transform(x_test)

X = np.append(arr = np.ones((100000,43)).astype(int), values=A, axis=1)
x_train = pd.DataFrame(X_train)

"""#Veri görselleştirmeleri"""

print(A.columns.tolist())
column_count = len(A.columns.tolist())
print("Sütun sayısı:", column_count)

print(Trainorjinal.columns.tolist())

plt.figure(figsize=(12,8))
sbn.distplot(A['Amount invested monthly'], bins=int(180/4), color = 'r')
plt.title('Amount İnvested Monthly Distribution')
plt.xlabel('Amount invested monthly')
plt.ylabel('Proportional')
plt.show()

"""Bağımsız değişkenlerin özellikleri"""

sbn.countplot(x='Credit_Score',data=Trainorjinal)
value_counts = Trainorjinal['Credit_Score'].value_counts()
print(value_counts)

"""Veriseti hakkında bilgi"""

Trainorjinal.info()
Train.isna().sum()

"""kaç adet NaN değer var"""

Train.isna().sum()

pd.set_option('display.max_columns', None)
Trainorjinal.head()

print(Trainorjinal.apply(lambda col : col.unique()))

Trainorjinal['Annual_Income'] = Trainorjinal['Annual_Income'].astype(str)
Trainorjinal['Annual_Income'] = Trainorjinal['Annual_Income'].str.replace('_', '')
Trainorjinal['Annual_Income'] = Trainorjinal['Annual_Income'].str.strip()
Trainorjinal['Annual_Income'] = Trainorjinal['Annual_Income'].astype(float)
import seaborn as sns
import matplotlib.pyplot as plt

sbn.countplot(x='Occupation',data=Trainorjinal)
plt.xticks(rotation=90)

"""#ModelDeneme"""

#Method to evaluate the performance of the model
def evaluate_model(y_test,y_pred):
    print("Classification Report")
    print(classification_report(y_test, y_pred))

    print("\n---------------------------------------------\n")
    # Compute confusion matrix
    cm = confusion_matrix(y_test, y_pred)

    # Create a heatmap of the confusion matrix using Seaborn
    sns.heatmap(cm, annot=True, cmap='Greens',fmt='.0f')

    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.title('Confusion Matrix')

    plt.show()

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.model_selection import cross_validate
from sklearn.preprocessing import StandardScaler
import numpy as np

# List of classifiers to test
classifiers = [
    ('Decision Tree', DecisionTreeClassifier()),
    ('Random Forest', RandomForestClassifier(n_jobs=-1)),
    ('KNN', KNeighborsClassifier(n_neighbors=5, n_jobs=-1)),
    ('Gaussian NB', GaussianNB())
]

# Apply data transformation
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Reshape y_train to a 1D array
y_train_reshaped = np.ravel(y_train)

# Iterate over each classifier and evaluate performance
for clf_name, clf in classifiers:
    # Perform cross-validation and calculate multiple scores
    scoring = ['accuracy', 'precision_macro', 'recall_macro']
    scores = cross_validate(clf, X_train_scaled, y_train_reshaped, cv=5, scoring=scoring)

    # Calculate average performance metrics
    avg_accuracy = np.mean(scores['test_accuracy'])
    avg_precision = np.mean(scores['test_precision_macro'])
    avg_recall = np.mean(scores['test_recall_macro'])

    # Print the performance metrics
    print(f'Classifier: {clf_name}')
    print(f'Average Accuracy: {avg_accuracy:.4f}')
    print(f'Average Precision: {avg_precision:.4f}')
    print(f'Average Recall: {avg_recall:.4f}')
    print('-----------------------')

# List of classifiers to test
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
classifiers = [
    ('Decision Tree', DecisionTreeClassifier()),
    ('Random Forest', RandomForestClassifier()),
    ('KNN', KNeighborsClassifier(n_neighbors=5)),
    ('Gaussion NB',GaussianNB()),
    ('SVC', SVC(kernel='poly'))

]

# Iterate over each classifier and evaluate performance
for clf_name, clf in classifiers:
    # Perform cross-validation
    scores = cross_val_score(clf, X_train, y_train, cv=5, scoring='accuracy')

    # Calculate average performance metrics
    avg_accuracy = scores.mean()
    avg_precision = cross_val_score(clf, X_train, y_train, cv=5, scoring='precision_macro').mean()
    avg_recall = cross_val_score(clf, X_train, y_train, cv=5, scoring='recall_macro').mean()

    # Print the performance metrics
    print(f'Classifier: {clf_name}')
    print(f'Average Accuracy: {avg_accuracy:.4f}')
    print(f'Average Precision: {avg_precision:.4f}')
    print(f'Average Recall: {avg_recall:.4f}')
    print('-----------------------')

"""# Orjinal Düzenleme"""

#2.veri onisleme
#2.1.veri yukleme
Train = pd.read_csv('trainc.csv')
Test = pd.read_csv('testc.csv')
Trainorjinal = pd.read_csv('train.csv')
Testorjinal = pd.read_csv('test.csv')
#pd.read_csv("veriler.csv")


#test
TrainCols = list(Trainorjinal.columns.values)
TrainCols2 = list(Train.columns.values)

#Eksik veriler
c28 = Trainorjinal['Amount_invested_monthly']
c28 = pd.DataFrame(c28)
print(c28.dtypes)
rc28 = c28.replace('__10000__', 'NaN')
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
imputer = imputer.fit(rc28)
c30 = imputer.transform(rc28)
c30 = pd.DataFrame(c30, columns=['Amount invested monthly'])

#ENCODE EDİLMESİ GEREKENLER

from sklearn import preprocessing
le = preprocessing.LabelEncoder()
ohe = preprocessing.OneHotEncoder()

#MESLEK
meslek = Train.iloc[:,6]
meslek = pd.DataFrame(meslek)
meslek = ohe.fit_transform(meslek).toarray()
meslek = pd.DataFrame(meslek, columns=['m1','m2','m3','m4','m5','m6','m7','m8','m9','m10','m11','m12','m13','m14','m15'])


#creditmix
Creditmix = Train.iloc[:,18]
Creditmix = pd.DataFrame(Creditmix)
Creditmix = ohe.fit_transform(Creditmix).toarray()
Creditmix = pd.DataFrame(Creditmix, columns=['poorc','goodc','standartc'])


#PaymentofMinAmount

Pofa = Train.iloc[:,-6]
Pofa = pd.DataFrame(Pofa)
Pofa = ohe.fit_transform(Pofa).toarray()
Pofa = pd.DataFrame(Pofa, columns=['nan','no','yes'])

#PaymentBehavior
PaymentBehavior = Train.iloc[:,-3]
PaymentBehavior = pd.DataFrame(PaymentBehavior)
PaymentBehavior = ohe.fit_transform(PaymentBehavior).toarray()
PaymentBehavior = pd.DataFrame(PaymentBehavior, columns=['b1','b2','b3','b4','b5','b6'])


#Veri setinin ML e hazırlanması
Train = Train.drop(['ID','Customer_ID','Month','Name','Age','SSN','Occupation','Credit_Mix','Type_of_Loan','Payment_of_Min_Amount','Amount_invested_monthly', 'Payment_Behaviour'], axis=1)

#verilerin bağımlı ve bağımsız olarak ayrılması
bagımsız = Train.iloc[:,:15]

#bağımlıdeğişken
bagımlı = Train.iloc[:,-1]
bagımlı= pd.DataFrame(bagımlı)
bagımlı= le.fit_transform(bagımlı).ravel()
bagımlı = pd.DataFrame(bagımlı, columns=['bagımlı'])
#birleştirme işlemleri
A = pd.concat([c30,meslek,Creditmix,Pofa,PaymentBehavior,bagımsız], axis=1)
B = bagımlı

from sklearn.model_selection import train_test_split

x_train, x_test,y_train,y_test = train_test_split(A,B,test_size=0.33, random_state=0)

#verilerin olceklenmesi
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
X_train = sc.fit_transform(x_train)
X_test = sc.transform(x_test)

X = np.append(arr = np.ones((100000,43)).astype(int), values=A, axis=1)

"""#RandomForestClassifier"""

#RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=151, criterion = 'gini', max_features='sqrt', max_depth=148, min_samples_split=2,
                             verbose=1, bootstrap= False)

rfc.fit(X_train,y_train)
y_pred = rfc.predict(X_test)
y_proba = rfc.predict_proba(X_test)
cm = confusion_matrix(y_test,y_pred)
print(cm)

display_labels = ["İYİ","KÖTÜ","STANDART"]
cm_display = metrics.ConfusionMatrixDisplay(cm, display_labels = display_labels)
cm_display.plot()
plt.show()
Accuracy = metrics.accuracy_score(y_test,y_pred)
Sensitivity_recall = metrics.recall_score(y_test,y_pred, average = 'macro')
Precision = metrics.precision_score(y_test,y_pred,average= 'macro')
Specificity = metrics.recall_score(y_test,y_pred, pos_label=0, average = 'macro')
F1_score = metrics.f1_score(y_test,y_pred,average='macro')

print(Accuracy)
print(Sensitivity_recall)
print(Precision)
print(Specificity)
print(F1_score)
scores = {"accuracy": Accuracy,
          "sensitivity_recall": Sensitivity_recall,
          "precision": Precision,
          "specificity": Specificity,
          "f1_score": F1_score}

from sklearn.metrics import classification_report
Rapor = classification_report(y_test,y_pred)
print(Rapor)

#Handle Imbalance Data
from imblearn.over_sampling import SMOTE

smote = SMOTE()
X_sm, y_sm = smote.fit_resample(A, B)

y_sm.value_counts()

#Split data
X_train, X_test, y_train, y_test = train_test_split(X_sm, y_sm, test_size=0.2, random_state=15, stratify=y_sm)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

#RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=151, criterion = 'gini', max_features='sqrt', max_depth=148, min_samples_split=2,
                             verbose=1, bootstrap= False)

rfc.fit(X_train,y_train)
y_pred = rfc.predict(X_test)
y_proba = rfc.predict_proba(X_test)
cm = confusion_matrix(y_test,y_pred)
display_labels = ["İYİ","KÖTÜ","STANDART"]
cm_display = metrics.ConfusionMatrixDisplay(cm, display_labels = display_labels)
cm_display.plot()
plt.show()
Accuracy = metrics.accuracy_score(y_test,y_pred)
Sensitivity_recall = metrics.recall_score(y_test,y_pred, average = 'macro')
Precision = metrics.precision_score(y_test,y_pred,average= 'macro')
Specificity = metrics.recall_score(y_test,y_pred, pos_label=0, average = 'macro')
F1_score = metrics.f1_score(y_test,y_pred,average='macro')

print(Accuracy)
print(Sensitivity_recall)
print(Precision)
print(Specificity)
print(F1_score)
scores = {"accuracy": Accuracy,
          "sensitivity_recall": Sensitivity_recall,
          "precision": Precision,
          "specificity": Specificity,
          "f1_score": F1_score}

from sklearn.metrics import classification_report
Rapor = classification_report(y_test,y_pred)
print(Rapor)

"""#DecisionTreeClassifier

"""

#DecisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
dtc = DecisionTreeClassifier(criterion = 'entropy')
dtc.fit(X_train,y_train)
y_pred = dtc.predict(X_test)
cm = confusion_matrix(y_test,y_pred)

plt.figure(figsize=(50,30))
tree.plot_tree(dtc, max_depth=1, filled=True)
plt.show()
display_labels = ["İYİ","KÖTÜ","STANDART"]
cm_display = metrics.ConfusionMatrixDisplay(cm, display_labels = display_labels)
cm_display.plot()
plt.show()
Accuracy = metrics.accuracy_score(y_test,y_pred)
Sensitivity_recall = metrics.recall_score(y_test,y_pred, average = 'macro')
Precision = metrics.precision_score(y_test,y_pred,average= 'macro')
Specificity = metrics.recall_score(y_test,y_pred, pos_label=0, average = 'macro')
F1_score = metrics.f1_score(y_test,y_pred,average='macro')

print(Accuracy)
print(Sensitivity_recall)
print(Precision)
print(Specificity)
print(F1_score)
scores = {"accuracy": Accuracy,
          "sensitivity_recall": Sensitivity_recall,
          "precision": Precision,
          "specificity": Specificity,
          "f1_score": F1_score}

from sklearn.metrics import classification_report
Rapor = classification_report(y_test,y_pred)
print(Rapor)

"""#Gaussian Naive Bayes

"""

from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(X_train, y_train)
y_pred = gnb.predict(X_test)
cm = confusion_matrix(y_test,y_pred)
display_labels = ["İYİ","KÖTÜ","STANDART"]
cm_display = metrics.ConfusionMatrixDisplay(cm, display_labels = display_labels)
cm_display.plot()
plt.show()
Accuracy = metrics.accuracy_score(y_test,y_pred)
Sensitivity_recall = metrics.recall_score(y_test,y_pred, average = 'macro')
Precision = metrics.precision_score(y_test,y_pred,average= 'macro')
Specificity = metrics.recall_score(y_test,y_pred, pos_label=0, average = 'macro')
F1_score = metrics.f1_score(y_test,y_pred,average='macro')

print(Accuracy)
print(Sensitivity_recall)
print(Precision)
print(Specificity)
print(F1_score)
scores = {"accuracy": Accuracy,
          "sensitivity_recall": Sensitivity_recall,
          "precision": Precision,
          "specificity": Specificity,
          "f1_score": F1_score}

from sklearn.metrics import classification_report
Rapor = classification_report(y_test,y_pred)
print(Rapor)

"""#SVC

"""

from sklearn.svm import SVC
svc = SVC(kernel='poly')
svc.fit(X_train,y_train)
y_pred = svc.predict(X_test)
cm = confusion_matrix(y_test,y_pred)
display_labels = ["İYİ","KÖTÜ","STANDART"]
cm_display = metrics.ConfusionMatrixDisplay(cm, display_labels = display_labels)
cm_display.plot()
plt.show()
Accuracy = metrics.accuracy_score(y_test,y_pred)
Sensitivity_recall = metrics.recall_score(y_test,y_pred, average = 'macro')
Precision = metrics.precision_score(y_test,y_pred,average= 'macro')
Specificity = metrics.recall_score(y_test,y_pred, pos_label=0, average = 'macro')
F1_score = metrics.f1_score(y_test,y_pred,average='macro')

print(Accuracy)
print(Sensitivity_recall)
print(Precision)
print(Specificity)
print(F1_score)
scores = {"accuracy": Accuracy,
          "sensitivity_recall": Sensitivity_recall,
          "precision": Precision,
          "specificity": Specificity,
          "f1_score": F1_score}

from sklearn.metrics import classification_report
Rapor = classification_report(y_test,y_pred)
print(Rapor)

"""#KNN

"""

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=1, metric='minkowski')
knn.fit(X_train,y_train)
y_pred = knn.predict(X_test)
cm = confusion_matrix(y_test,y_pred)
display_labels = ["İYİ","KÖTÜ","STANDART"]
cm_display = metrics.ConfusionMatrixDisplay(cm, display_labels = display_labels)
cm_display.plot()
plt.show()
Accuracy = metrics.accuracy_score(y_test,y_pred)
Sensitivity_recall = metrics.recall_score(y_test,y_pred, average = 'macro')
Precision = metrics.precision_score(y_test,y_pred,average= 'macro')
Specificity = metrics.recall_score(y_test,y_pred, pos_label=0, average = 'macro')
F1_score = metrics.f1_score(y_test,y_pred,average='macro')

print(Accuracy)
print(Sensitivity_recall)
print(Precision)
print(Specificity)
print(F1_score)
scores = {"accuracy": Accuracy,
          "sensitivity_recall": Sensitivity_recall,
          "precision": Precision,
          "specificity": Specificity,
          "f1_score": F1_score}

from sklearn.metrics import classification_report
Rapor = classification_report(y_test,y_pred)
print(Rapor)

"""#Linear Regression

"""

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(x_train,y_train)
y_pred = regressor.predict(x_test)
cm = confusion_matrix(y_test,y_pred)

"""#LogisticRegression

"""

from sklearn.linear_model import LogisticRegression
logr = LogisticRegression(random_state=0)
logr.fit(X_train,y_train)
y_pred = logr.predict(X_test)
cm = confusion_matrix(y_test,y_pred)

"""#ConfusionMatrix çıktıları

"""

display_labels = ["İYİ","KÖTÜ","STANDART"]
cm_display = metrics.ConfusionMatrixDisplay(cm, display_labels = display_labels)
cm_display.plot()
plt.show()
Accuracy = metrics.accuracy_score(y_test,y_pred)
Sensitivity_recall = metrics.recall_score(y_test,y_pred, average = 'macro')
Precision = metrics.precision_score(y_test,y_pred,average= 'macro')
Specificity = metrics.recall_score(y_test,y_pred, pos_label=0, average = 'macro')
F1_score = metrics.f1_score(y_test,y_pred,average='macro')

print(Accuracy)
print(Sensitivity_recall)
print(Precision)
print(Specificity)
print(F1_score)
scores = {"accuracy": Accuracy,
          "sensitivity_recall": Sensitivity_recall,
          "precision": Precision,
          "specificity": Specificity,
          "f1_score": F1_score}

from sklearn.metrics import classification_report
Rapor = classification_report(y_test,y_pred)
print(Rapor)

"""#özelliklerin model üzerinde ne kadar etkisi olduğunu göstermek için kullanılan bir görselleştirme

['Occupation', 'Payment_of_Min_Amount', 'Payment_Behaviour']
"""

print(x_train)
print(A)

import pandas as pd

column_mapping = {
    0: 'Amount invested monthly',
    1: 'Occupation',
    2: 'Credit_Mix',
    3: 'Payment_of_Min_Amount',
    4: 'Payment_Behaviour',
    5: 'Annual_Income',
    6: 'Monthly_Inhand_Salary',
    7: 'Num_Bank_Accounts',
    8: 'Num_Credit_Card',
    9: 'Interest_Rate',
    10: 'Num_of_Loan',
    11: 'Delay_from_due_date',
    12: 'Num_of_Delayed_Payment',
    13: 'Changed_Credit_Limit',
    14: 'Num_Credit_Inquiries',
    15: 'Outstanding_Debt',
    16: 'Credit_Utilization_Ratio',
    17: 'Credit_History_Age',
    18: 'Total_EMI_per_month',
    19: 'Monthly_Balance'
}

feat_importances = pd.Series(rfc.feature_importances_, index=x_train.columns)
feat_importances_mapped = feat_importances.rename(index=column_mapping)
print(feat_importances_mapped)
feat_importances_mapped.nlargest(20).plot(kind='barh')
plt.show()

"""#SVC İÇİN HİPERPARAMETRİ OPTİMİZASYONU

"""

from sklearn.model_selection import GridSearchCV



param_grid = {'C': [0.1, 1],

}

grid_search = GridSearchCV(estimator=rfc, param_grid=param_grid, cv=5, n_jobs=-1)
grid_search.fit(X_train, y_train)

# y_train ve y_test verilerini yeniden şekillendirin

y_train = np.array(y_train)
y_test = np.array(y_test)

y_train = y_train.ravel()
y_test = y_test.ravel()



grid_search.fit(X_train, y_train)

# En iyi parametreleri yazdırın ve modelinizi eğitin.
print("Best parameters found:", grid_search.best_params_)
best_model = grid_search.best_estimator_
best_model.fit(X_train, y_train)

# Test seti üzerinde model performansını değerlendirin.
y_pred = best_model.predict(X_test)
y_proba = best_model.predict_proba(X_test)
cmGrid = confusion_matrix(y_test, y_pred)

cm_display2 = metrics.ConfusionMatrixDisplay(cmGrid, display_labels = display_labels)
cm_display2.plot()
plt.show()

Rapor2 = classification_report(y_test,y_pred)

"""#Hiperparametri Optimizasyonu RandomForestİÇİN

"""

from sklearn.model_selection import GridSearchCV

from sklearn.ensemble import RandomForestClassifier

# Verileri yükleyin ve özellikleri ve hedefleri belirleyin

# GridSearchCV kullanarak modelinizin hiperparametrelerini belirleyin
param_grid = {
    'n_estimators': [151],
    'max_depth': [148],
    'min_samples_split': [2],
    'max_features': ['sqrt'],
    'min_impurity_decrease': [0.0],
    'bootstrap': [True, False],
    'oob_score': [True, False],
    'max_samples': [None, 0.5, 0.8],
    'class_weight': [None, 'balanced']
}
model = RandomForestClassifier()
grid_search = GridSearchCV(model, param_grid, cv=5, n_jobs=-1)

# y_train ve y_test verilerini yeniden şekillendirin

y_train = np.array(y_train)
y_test = np.array(y_test)

y_train = y_train.ravel()
y_test = y_test.ravel()

grid_search.fit(X_train, y_train)

# En iyi parametreleri yazdırın ve modelinizi eğitin.
print("Best parameters found:", grid_search.best_params_)
best_model = grid_search.best_estimator_
best_model.fit(X_train, y_train)

# Test seti üzerinde model performansını değerlendirin.
y_pred = best_model.predict(X_test)
y_proba = best_model.predict_proba(X_test)
cmGrid = confusion_matrix(y_test, y_pred)

cm_display2 = metrics.ConfusionMatrixDisplay(cmGrid, display_labels = display_labels)
cm_display2.plot()
plt.show()

Rapor2 = classification_report(y_test,y_pred)