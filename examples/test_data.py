import sqlite3
from collections import defaultdict


def get_data():
    # Подключение к базе данных
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Извлечение данных из базы данных
    cursor.execute(''' SELECT id FROM Vehicle''')
    vehicles_id = cursor.fetchall()

    # Создаем словарь для хранения сгруппированных данных
    grouped_data_by_vehicle = {}

    # Обработка данных для каждой машины
    for vehicle_id in vehicles_id:
        # Получаем данные из таблицы TripCard для данной машины
        cursor.execute("SELECT date, mileage FROM TripCard WHERE vehicle_id = ?", (vehicle_id[0],))
        trip_card_data = cursor.fetchall()

        # Получаем данные из таблицы Telematics для данной машины
        cursor.execute("SELECT date, mileage FROM Telematics WHERE vehicle_id = ?", (vehicle_id[0],))
        telematics_data = cursor.fetchall()

        # Создаем словарь для хранения данных по датам
        grouped_data_by_date = defaultdict(list)

        # Объединяем данные из TripCard и Telematics по дате
        for date, mileage_trip in trip_card_data:
            # Ищем соответствующие данные в Telematics
            telematics_mileage = next((mileage_telematics for telematics_date, mileage_telematics in telematics_data if
                                       telematics_date == date), -1)
            # Добавляем данные в словарь
            grouped_data_by_date[date].append([date, mileage_trip, telematics_mileage])

        # Добавляем отдельные данные из Telematics, которых нет в TripCard
        for date, mileage_telematics in telematics_data:
            if date not in grouped_data_by_date:
                grouped_data_by_date[date].append([date, -1, mileage_telematics])

        # Добавляем данные в словарь по идентификатору машины
        grouped_data_by_vehicle[vehicle_id[0]] = dict(grouped_data_by_date)

    # Здесь можно обрабатывать grouped_data_by_vehicle по вашему усмотрению
    for vehicle_id, data_by_date in grouped_data_by_vehicle.items():
        print("Vehicle ID:", vehicle_id)
        for date, data_list in data_by_date.items():
            print("Date:", date)
            print("Data:", data_list)

    # Закрываем соединение с базой данных
    conn.close()
