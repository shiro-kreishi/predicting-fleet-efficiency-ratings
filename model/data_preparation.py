import sqlite3
from collections import defaultdict

if __name__ == '__main__':
    data = []
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT Vehicle.id FROM Vehicle''')
    vehicles = cursor.fetchall()

    for vehicle in vehicles:
        vehicle_id = vehicle[0]

        cursor.execute(
            '''
            SELECT TC.mileage, TC.date
            FROM Vehicle
            JOIN TripCard TC ON TC.vehicle_id = Vehicle.id
            WHERE Vehicle.id = ?
            ''', (vehicle_id,)
        )
        trips = cursor.fetchall()

        cursor.execute(
            '''
            SELECT TM.mileage, TM.date
            FROM Vehicle
            JOIN Telematics TM ON TM.vehicle_id = Vehicle.id
            WHERE Vehicle.id = ?
            ''', (vehicle_id,)
        )
        telematics = cursor.fetchall()

        cursor.execute(
            '''
            SELECT DS.value
            FROM Vehicle
            JOIN DrivingStyle DS ON DS.vehicle_id = Vehicle.id
            WHERE Vehicle.id = ?
            ''', (vehicle_id,)
        )
        driving_styles = cursor.fetchall()

        # Создаем словарь для хранения данных по дате
        combined_data = defaultdict(lambda: {'trip_mileage': -1, 'telematics_mileage': -1})

        # Заполняем данные из trips
        for mileage, date in trips:
            combined_data[date]['trip_mileage'] = mileage

        # Заполняем данные из telematics
        for mileage, date in telematics:
            combined_data[date]['telematics_mileage'] = mileage

        # Формируем итоговый список данных
        for date, mileages in combined_data.items():
            data.append((vehicle_id, date, mileages['trip_mileage'], mileages['telematics_mileage']))

    conn.close()

    # Вывод данных для проверки
    for record in data:
        print(record)
    print(len(data))