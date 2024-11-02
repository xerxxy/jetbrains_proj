# iris_classification.py

# Import necessary libraries
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Load the Iris dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
# Define the column names
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'Class']
# Read the dataset
irisdata = pd.read_csv(url, names=names)

# Separate features (X) and target labels (y)
X = irisdata.iloc[:, 0:4]
y = irisdata.select_dtypes(include=[object])

# Encode target labels as numeric values
le = preprocessing.LabelEncoder()
y = y.apply(le.fit_transform)

# Split dataset into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

# Scale features
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# Initialize and train MLP Classifier
mlp = MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=1000)
mlp.fit(X_train, y_train.values.ravel())

# Make predictions
predictions = mlp.predict(X_test)

# Print predictions
print("Predictions:", predictions)

# Evaluate model performance
print("Confusion Matrix:")
print(confusion_matrix(y_test, predictions))
print("\nClassification Report:")
print(classification_report(y_test, predictions))
