import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import MultiLabelBinarizer

from ExtractData import parse_orders

file_path = 'CsvReaderOutput.txt'
orders = parse_orders(file_path)

def preprocess_orders(orders):
    all_items = set(item for order in orders for item in order['items'])
    item_list = list(all_items)
    item_index = {item: idx for idx, item in enumerate(item_list)}
    
    X, y = [], []
    for order in orders:
        cart_vector = [0] * len(item_list)
        for item in order['items']:
            cart_vector[item_index[item]] = 1
        
        for item in order['items']:
            target_vector = [0] * len(item_list)
            target_vector[item_index[item]] = 1
            X.append(cart_vector)
            y.append(target_vector)
    
    return np.array(X), np.array(y), item_list

def build_model(input_size):
    model = Sequential([
        Dense(128, activation='relu', input_shape=(input_size,)),
        Dense(64, activation='relu'),
        Dense(input_size, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

X, y, item_list = preprocess_orders(orders)

model = build_model(input_size=len(item_list))
model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2)

def predict_next_item(cart, model, item_list):
    cart_vector = np.array([[1 if item in cart else 0 for item in item_list]])
    prediction = model.predict(cart_vector)
    predicted_item_index = np.argmax(prediction)
    return item_list[predicted_item_index]

cart = ["GREAT NTHN ORIGINAL STUB CTN", "GREAT NTHN MID CAN 6PK"]
predicted_item = predict_next_item(cart, model, item_list)
print(f"Predicted next item: {predicted_item}")