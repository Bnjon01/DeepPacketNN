from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, MaxPooling1D, Conv1D, Flatten
from tensorflow.keras import metrics
from keras.utils import np_utils
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Data file input, comment/uncomment the given csv file or replace the name
#data = pd.read_csv("TrafficData.csv", header=None, delimiter=',', skiprows=2)
data = pd.read_csv("ApplicationData.csv", header=None, delimiter=',', skiprows=2)
# Amount of categories in preprocessed data
# Provided sample data settings: 10 for TrafficData.csv and 14 for ApplicationData.csv
CATEGORY_NUM = 0

# Split data into X and Y, cutting off column 1501 for Y
X_data = data.iloc[:,:1500]
y_data = data.iloc[:,1500:]
# Encode Y into an array, 10 for traffic classification, 14 for application classification
y_data = np_utils.to_categorical(y_data, CATEGORY_NUM)

# 64% training data, 20% test data, 16% validation data
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size = 0.2)
X_train, X_val, y_train, y_val = train_test_split(X_data, y_data, test_size = 0.2)

#SAE
SAE = Sequential()
SAE.add(Dense(400, input_shape=(1500,), activation="relu"))
SAE.add(Dropout(0.05))
SAE.add(Dense(300, activation="relu"))
SAE.add(Dropout(0.05))
SAE.add(Dense(200, activation="relu"))
SAE.add(Dropout(0.05))
SAE.add(Dense(100, activation="relu"))
SAE.add(Dropout(0.05))
SAE.add(Dense(50, activation="relu"))
SAE.add(Dropout(0.05))
SAE.add(Dense(CATEGORY_NUM, activation="softmax"))
# Training with MSE loss function
SAE.compile(loss="mean_squared_error", optimizer="adam")
SAE.fit(X_train, y_train, epochs=200, verbose=1)
# Training with CCE loss function
SAE.compile(loss="categorical_crossentropy", optimizer="adam", metrics=[metrics.Precision(), metrics.Recall()])
SAE.fit(X_train, y_train, epochs=200, verbose=1)

y_pred = np.argmax(SAE.predict(X_test), axis=-1)
y_pred = np_utils.to_categorical(y_pred, CATEGORY_NUM)
print(classification_report(y_test, y_pred))

#CNN
CNN = Sequential()
#Application classification layers
CNN.add(Conv1D(200, input_shape=(1500,1), activation="relu", kernel_size=4, strides=3))
CNN.add(Conv1D(200, activation="relu", kernel_size=5, strides=1))

##Traffic classification
#CNN.add(Conv1D(200, input_shape=(1500,1), activation="relu", kernel_size=5, strides=3))
#CNN.add(Conv1D(200, activation="relu", kernel_size=4, strides=3))

CNN.add(MaxPooling1D())
CNN.add(Flatten())
CNN.add(Dense(200, activation="relu"))
CNN.add(Dropout(0.05))
CNN.add(Dense(200, activation="relu"))
CNN.add(Dropout(0.05))
CNN.add(Dense(200, activation="relu"))
CNN.add(Dropout(0.05))
CNN.add(Dense(CATEGORY_NUM, activation="softmax"))
CNN.compile(loss="categorical_crossentropy", optimizer="adam", metrics=[metrics.Precision(), metrics.Recall()])
CNN.fit(X_train, y_train, epochs=300, verbose=1)

y_pred = np.argmax(CNN.predict(X_test), axis=-1)
y_pred = np_utils.to_categorical(y_pred, CATEGORY_NUM)
print(classification_report(y_test, y_pred))


















