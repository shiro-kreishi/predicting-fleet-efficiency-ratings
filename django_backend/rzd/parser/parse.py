import openpyxl
from ..models import Polygon, Vehicle, Fines, Telematics, TripCard, DrivingStyle
from django.db import transaction


def excel_to_db(filename):
    workbook = openpyxl.load_workbook(filename=filename)
    sheet = workbook.active

    with transaction.atomic():  # Группируем операции в одной транзакции
        for row in sheet.iter_rows(min_row=2):
            # Присваиваем значения переменным для удобства чтения
            name = row[0].value
            short_name = row[1].value
            polygon_data = row[2].value
            number = row[3].value
            structural_unit = row[4].value
            fine_value = row[12].value
            driving_style_value = row[13].value
            date_telematics = row[10].value
            mileage_telematics = row[11].value
            date_trip_card = row[8].value
            mileage_trip_card = row[9].value

            # Создаем или получаем polygon
            polygon, created = Polygon.objects.get_or_create(
                name=name,
                defaults={
                    'short_name': short_name,
                    'polygon': polygon_data
                }
            ) if name else (None, False)

            # Создаем vehicle, если указан номер
            vehicle = Vehicle.objects.create(
                number=number,
                polygon=polygon,
                structural_unit=structural_unit
            ) if number and polygon else None

            # Если vehicle создан, то добавляем штрафы, стиль вождения, телематику и трип-карты
            if vehicle:
                if fine_value and "=RANDBETWEEN(" not in str(fine_value):
                    Fines.objects.create(vehicle=vehicle, value=fine_value)
                if driving_style_value:
                    DrivingStyle.objects.create(vehicle=vehicle, value=driving_style_value)
                if date_telematics or mileage_telematics:
                    Telematics.objects.create(
                        vehicle=vehicle,
                        date=date_telematics or '',
                        mileage=mileage_telematics if mileage_telematics is not None else 0
                    )
                if date_trip_card or mileage_trip_card:
                    TripCard.objects.create(
                        vehicle=vehicle,
                        date=date_trip_card or '',
                        mileage=mileage_trip_card if mileage_trip_card is not None else 0
                    )

    workbook.close()