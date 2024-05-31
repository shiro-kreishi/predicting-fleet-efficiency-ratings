import sqlite3
from get_data import get_data
import numpy as np
import tensorflow as tf

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

keras = tf.keras
KL = keras.layers
KM = keras.models

Sequential, Dense, Input = KM.Sequential, KL.Dense, KL.Input

data = get_data()

# Создание меток на основе критериев
y_train = np.array([
    1 if (mileage_trip == mileage_telematics and fines <= 3 and driving_style >= 4) else 0
    for mileage_trip, mileage_telematics, fines, driving_style in X_train
])

# Создание модели нейронной сети
model = Sequential([
    Input(shape=(4,)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Компиляция модели
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Обучение модели
model.fit(X_train, y_train, epochs=10, batch_size=1)

# Предсказание эффективности транспортного средства для новых данных
X_new = np.array([[100, 100, 3, 0], [200, 200, 0, 6], [150, 150, 5, 0]])
predictions = model.predict(X_new)
for i, pred in enumerate(predictions):
    print(f'Транспортное средство {i + 1}: вероятность эффективности = {pred[0]:.2f}')