import numpy as np                                  #per la gestione dei dati
import pandas as pd                                 #per la gestione dei dati
import seaborn as sns                               #per la visualizzazione dati e per pairplot()
import matplotlib.pyplot as plt                     #per la visualizzazione dati
import sklearn
from sklearn import datasets                        #per importare il campione di dati
from sklearn.preprocessing import StandardScaler    #per trasformare il dataset
from sklearn.cluster import KMeans                  #per istanziare, lavorare e usare il modello
from sklearn.cluster import Birch                   #per istanziare, lavorare e usare il modello
from sklearn import metrics                         #per la valutazione del modello
import plotly.graph_objects as go
import plotly.express as px
from yellowbrick.cluster import KElbowVisualizer
from sklearn.model_selection import train_test_split
from yellowbrick.cluster import SilhouetteVisualizer
from plotly.offline import init_notebook_mode ,iplot
from sklearn.metrics import silhouette_score

df=pd.read_csv("C:/Users/matte/OneDrive/Desktop/Cleaned-Data2.csv")
print(df)

df.corr()
print(df.corr())

X = df.drop(['Fever'], axis=1)
y = df['Fever']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

plt.figure(figsize = (15,6))
sns.heatmap( df.corr(), annot=True)
plt.show()

plt.figure(figsize = (15,4))
sns.boxplot(data = df, orient = "h")
plt.show()

scaler = StandardScaler()
scaled_array = scaler.fit_transform(df)
scaled_df = pd.DataFrame(scaled_array, columns=df.columns)

plt.figure(figsize = (15,4))
sns.boxplot(data = scaled_df, orient = "h")
plt.show()

scaled_df.describe()

kmeans_model = KMeans(n_clusters=5)
kmeans_model.fit(scaled_df)
centroids = kmeans_model.cluster_centers_
centroids

kmeans_model.cluster_centers_.shape

kmeans_model.labels_
df["cluster"] = kmeans_model.labels_
print(df)

plt.figure(figsize = (15,4))
sns.boxplot(data = centroids, orient = "h")
plt.show()

plt.figure(figsize = (15,4))
fig = px.histogram(centroids, title='Istogramma Centroidi', log_y=True, text_auto=True)
fig.update_layout(bargap=0.2)
fig.show()

km = KMeans(random_state=42)
visualizer = KElbowVisualizer(km, k=(2, 10))
visualizer.fit(X)  # Adatta i dati al visualizzatore
visualizer.show()

model=kmeans_model.fit(X_train)
pred_test = model.predict(X_test)
pred_train = model.predict(X_train)
print(pred_test)
print(pred_train)


plt.rcParams["figure.figsize"] = (15, 8)
df.hist()
plt.show()

plt.figure(figsize = (15,4))
fig = px.histogram(df, title='Istogramma Generale', log_y=True, text_auto=True)
fig.update_layout(bargap=0.2)
fig.show()


score_silhouette_train = silhouette_score (X_train, pred_train)
score_silhouette_test = silhouette_score (X_test, pred_test)
print("--> TRAIN : For n_clusters = 5, silhouette score is {}".format(score_silhouette_train))
print("--> TEST : For n_clusters = 5, silhouette score is {}".format(score_silhouette_test))

score_davies_train = metrics.davies_bouldin_score(X_train, pred_train)
score_davies_test = metrics.davies_bouldin_score(X_test, pred_test)
print("--> TRAIN : For n_clusters = 5, davies_bouldin score is {}".format(score_davies_train))
print("--> TEST : For n_clusters = 5, davies_bouldin score is {}".format(score_davies_test))



