import random
from datetime import timedelta, date
from rzd.models import Polygon, Vehicle, Fines, Telematics, TripCard, DrivingStyle

# Случайная дата в заданном промежутке
def rand_date(start, end):
    return start + timedelta(
        days=random.randint(0, int((end - start).days)))

# Создаем полигоны
for i in range(1, 11):  # Допустим, у нас будет 10 полигонов
    Polygon.objects.create(
        name=f'Полигон {i}',
        short_name=f'P{i}',
        polygon=f'Геоданные полигона {i}'
    )

# Создаем транспортные средства
for i in range(1, 41):
    Vehicle.objects.create(
        number=f'А{i:03}BC',
        polygon_id=random.randint(1, 10),  # Случайно выбираем один из созданных полигонов
        structural_unit=f'Отдел {random.randint(1, 5)}'
    )

# Создаем штрафы
for i in range(1, 41):
    Fines.objects.create(
        vehicle_id=random.randint(1, 40),
        value=random.uniform(100.0, 1000.0)  # Случайная величина штрафа
    )

# Добавляем телематику
start_date = date(2021, 1, 1)
end_date = date(2021, 12, 31)

for i in range(1, 41):
    Telematics.objects.create(
        date=rand_date(start_date, end_date),
        mileage=random.uniform(50.0, 500.0),  # Случайный пробег
        vehicle_id=random.randint(1, 40)
    )

# Путевые карты
for i in range(1, 41):
    TripCard.objects.create(
        date=rand_date(start_date, end_date),
        mileage=random.uniform(50.0, 500.0),  # Случайный пробег
        vehicle_id=random.randint(1, 40)
    )

# Стиль вождения
styles = ['Осторожный', 'Агрессивный', 'Экономичный']
for i in range(1, 41):
    DrivingStyle.objects.create(
        vehicle_id=random.randint(1, 40),
        value=random.choice(styles)  # Случайная стилистика вождения
    )