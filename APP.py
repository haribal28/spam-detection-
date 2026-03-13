# Install libraries
!pip install pandas scikit-learn tensorflow

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Download dataset
!wget https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv

# Load dataset
data = pd.read_csv("sms.tsv", sep="\t", names=["label","message"])

# Convert spam/ham to numbers
encoder = LabelEncoder()
data["label"] = encoder.fit_transform(data["label"])

# Tokenize messages
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(data["message"])

X = tokenizer.texts_to_sequences(data["message"])
X = pad_sequences(X, maxlen=50)

y = data["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Build RNN model
model = tf.keras.Sequential()

model.add(tf.keras.layers.Embedding(5000,64,input_length=50))
model.add(tf.keras.layers.LSTM(64))
model.add(tf.keras.layers.Dense(1,activation="sigmoid"))

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

print("Training model...")

model.fit(
    X_train,
    y_train,
    epochs=40,
    batch_size=32,
    validation_data=(X_test,y_test)
)

# Evaluate
loss,acc = model.evaluate(X_test,y_test)
print("Model Accuracy:",acc)

# ---- USER INPUT PART ----

while True:

    user_msg = input("\nEnter a message (type 'exit' to stop): ")

    if user_msg.lower() == "exit":
        break

    seq = tokenizer.texts_to_sequences([user_msg])
    seq = pad_sequences(seq,maxlen=50)

    prediction = model.predict(seq)

    if prediction > 0.5:
        print("Prediction: 🚨 Spam Message")
    else:
        print("Prediction: ✅ Normal Message")