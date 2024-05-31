import sqlite3

import numpy as np
import tensorflow as tf
keras = tf.keras
KL = keras.layers
KM = keras.models

Sequential, Dense = KM.Sequential, KL.Dense


if __name__ == '__main__':
    # Подключение к базе данных
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Извлечение данных из базы данных
    cursor.execute('''
    SELECT 
        TripCard.mileage AS mileage_trip, 
        Telematics.mileage AS mileage_telematics, 
        Fines.value AS fines, 
        DrivingStyle.value AS driving_style
    FROM 
        Vehicle
    JOIN 
        TripCard ON Vehicle.id = TripCard.vehicle_id
    JOIN 
        Telematics ON Vehicle.id = Telematics.vehicle_id
    JOIN 
        Fines ON Vehicle.id = Fines.vehicle_id
    JOIN 
        DrivingStyle ON Vehicle.id = DrivingStyle.vehicle_id
    ''')

    data = cursor.fetchall()
    conn.close()

    # Предварительная обработка данных
    cleaned_data = []
    for row in data:
        try:
            cleaned_row = [float(value) for value in row]
            cleaned_data.append(cleaned_row)
        except ValueError:
            # Игнорируем строки, которые не могут быть преобразованы в float
            continue

    cleaned_data = np.array(cleaned_data)

    # Формирование входных данных X_train
    X_train = cleaned_data[:, :4]

    # Создание меток на основе критериев
    y_train = np.array([
        1 if (mileage_trip == mileage_telematics and fines <= 3 and driving_style >= 4) else 0
        for mileage_trip, mileage_telematics, fines, driving_style in X_train
    ])

    # Создание модели нейронной сети
    model = Sequential([
        Dense(4, activation='relu', input_shape=(1,)),
        Dense(3, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    print(model.summary())

    # Компиляция модели
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    # Обучение модели
    model.fit(X_train, y_train, epochs=5, batch_size=1)

    # Предсказание эффективности транспортного средства для новых данных
    X_new = np.array([[100, 100, 3, 0], [200, 200, 0, 6], [150, 150, 5, 0]])
    predictions = model.predict(X_new)
    for i, pred in enumerate(predictions):
        print(f'Транспортное средство {i + 1}: вероятность эффективности = {pred[0]:.2f}')