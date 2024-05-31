import sqlite3
from collections import defaultdict


def get_data():
    # Подключение к базе данных
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Извлечение данных из базы данных
    cursor.execute('''SELECT id FROM Vehicle''')
    vehicles_id = cursor.fetchall()

    # Создаем словарь для хранения сгруппированных данных
    grouped_data_by_vehicle = {}

    # Обработка данных для каждой машины
    for vehicle_id in vehicles_id:
        vehicle_id = vehicle_id[0]

        # Получаем данные из таблицы TripCard для данной машины
        cursor.execute("SELECT date, mileage FROM TripCard WHERE vehicle_id = ?", (vehicle_id,))
        trip_card_data = cursor.fetchall()

        # Получаем данные из таблицы Telematics для данной машины
        cursor.execute("SELECT date, mileage FROM Telematics WHERE vehicle_id = ?", (vehicle_id,))
        telematics_data = cursor.fetchall()

        # Создаем словарь для хранения данных по датам
        grouped_data_by_date = defaultdict(lambda: [-1, -1])

        # Обрабатываем данные из TripCard
        for date, mileage_trip in trip_card_data:
            grouped_data_by_date[date][0] = mileage_trip

        # Обрабатываем данные из Telematics
        for date, mileage_telematics in telematics_data:
            grouped_data_by_date[date][1] = mileage_telematics

        # Получаем данные из таблицы Fines для данной машины
        cursor.execute("SELECT value FROM Fines WHERE vehicle_id = ?", (vehicle_id,))
        fines_data = cursor.fetchall()

        # Получаем данные из таблицы DrivingStyle для данной машины
        cursor.execute("SELECT value FROM DrivingStyle WHERE vehicle_id = ?", (vehicle_id,))
        driving_style_data = cursor.fetchall()

        # Добавляем данные в итоговый словарь
        grouped_data_by_vehicle[vehicle_id] = {
            'dates': dict(grouped_data_by_date),
            'fines': [fine[0] for fine in fines_data],  # Извлекаем только значения штрафов
            'driving_style': [style[0] for style in driving_style_data]  # Извлекаем только значения стиля вождения
        }

    # Закрываем соединение с базой данных
    conn.close()

    return grouped_data_by_vehicle