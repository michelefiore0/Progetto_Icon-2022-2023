import pandas as pd
import numpy as np
import seaborn as sns
import psutil
import matplotlib
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import validation_curve

df = pd.read_csv('Cleaned-Data2.csv')

X = df.drop(['Fever'], axis=1)
y = df['Fever']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors=1,metric='euclidean')
classifier.fit(X_train,y_train)
y_pred = classifier.predict(X_test)
print("Accuratezza:",metrics.accuracy_score(y_test, y_pred))

pred_y_df=pd.DataFrame({'Valore corrente':y_test, 'Valore predetto':y_pred})
pred_y_df[0:20]

print(classification_report(y_test,y_pred))



from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=120, max_depth=40)
rfc.fit(X_train,y_train)
y_rfc_pred = rfc.predict(X_test)
print("Accuratezza:",metrics.accuracy_score(y_test, y_rfc_pred))

pred_y_df=pd.DataFrame({'Valore corrente':y_test, 'Valore predetto':y_rfc_pred})
pred_y_df[0:20]

print(classification_report(y_test,y_rfc_pred))



from sklearn.tree import DecisionTreeClassifier
dtc = DecisionTreeClassifier(max_depth=40)
dtc.fit(X_train,y_train)
y_dtc_pred = dtc.predict(X_test)
print("Accuratezza:",metrics.accuracy_score(y_test, y_dtc_pred))

pred_y_df=pd.DataFrame({'Valore corrente':y_test, 'Valore predetto':y_dtc_pred})
pred_y_df[0:20]

print(classification_report(y_test,y_dtc_pred))


from sklearn import ensemble
gb_clf = ensemble.GradientBoostingClassifier(learning_rate=0.05, max_depth=20)
gb_clf.fit(X_train, y_train)
y_gb_pred=gb_clf.predict(X_test)
print("Accuratezza:",metrics.accuracy_score(y_test, y_gb_pred))

pred_y_df=pd.DataFrame({'Valore corrente':y_test, 'Valore predetto':y_gb_pred})
pred_y_df[0:20]

print(classification_report(y_test,y_gb_pred))

confusion_matrix = metrics.confusion_matrix(y_test, y_pred)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = [False, True])
cm_display.plot()
plt.show()


confusion_matrix = metrics.confusion_matrix(y_test, y_dtc_pred)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = [False, True])
cm_display.plot()
plt.show()


confusion_matrix = metrics.confusion_matrix(y_test, y_rfc_pred)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = [False, True])
cm_display.plot()
plt.show()


confusion_matrix = metrics.confusion_matrix(y_test, y_gb_pred)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = [False, True])
cm_display.plot()
plt.show()


from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_validate
from sklearn.model_selection import KFold, cross_val_score


clf = DecisionTreeClassifier(random_state=42)
k_folds = KFold(n_splits = 5)
scores = cross_val_score(clf, X, y, cv = k_folds)
print("Decision Tree Cross Validation Scores: ", scores)
print("Average CV Score: ", scores.mean())
print("Number of CV Scores used in Average: ", len(scores))



param_range = np.arange(1, 40, 2)
train_scores, test_scores = validation_curve(
    DecisionTreeClassifier(class_weight='balanced'), X, y, param_name="max_depth", cv=10,
    param_range=param_range,n_jobs=psutil.cpu_count(),
    scoring="accuracy")
train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)
plt.figure(figsize=(10,10))
plt.title("Validation Curve with DecisionTree")
plt.xlabel("max_depth")
plt.ylabel("Score")
plt.ylim(0.0, 1.1)

plt.plot(param_range, train_scores_mean, label="Training score",
             color="r")

plt.plot(param_range, test_scores_mean, label="Cross-validation score",
             color="g")

plt.legend(loc="best")
plt.xticks(param_range)
plt.show()


clf = RandomForestClassifier(random_state=42)
k_folds = KFold(n_splits = 5)
scores = cross_val_score(clf, X, y, cv = k_folds)
print("Random Forest Cross Validation Scores: ", scores)
print("Average CV Score: ", scores.mean())
print("Number of CV Scores used in Average: ", len(scores))


param_range = np.arange(1, 250, 2)
train_scores, test_scores = validation_curve(RandomForestClassifier(),
                                             X,
                                             y,
                                             param_name="n_estimators",
                                             param_range=param_range,
                                             cv=3,
                                             scoring="accuracy",
                                             n_jobs=-1)
train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)
test_std = np.std(test_scores, axis=1)
plt.plot(param_range, train_mean, label="Training score", color="black")
plt.plot(param_range, test_mean, label="Cross-validation score", color="dimgrey")
plt.fill_between(param_range, train_mean - train_std, train_mean + train_std, color="gray")
plt.fill_between(param_range, test_mean - test_std, test_mean + test_std, color="gainsboro")
plt.title("Validation Curve With Random Forest")
plt.xlabel("Number Of Trees")
plt.ylabel("Accuracy Score")
plt.tight_layout()
plt.legend(loc="best")
plt.show()

