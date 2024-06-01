# import sqlite3
import openpyxl
from django_backend.rzd.models import Polygon, Vehicle, Fines, Telematics, TripCard, DrivingStyle


# conn = sqlite3.connect("../../../../parsexlsx/database.db")
# cursor = conn.cursor()
def excel_to_db(filename):
    workbook = openpyxl.load_workbook(filename=f"django_backend/{filename}")
    sheet = workbook.active
    last_index_polygon = cursor.lastrowid  # DELETE FROM имя_таблицы;
    last_index_vehicle = cursor.lastrowid  # DELETE FROM sqlite_sequence WHERE name='имя_таблицы';
    for i in sheet.iter_rows(min_row=2):
        if not sheet[f"A{i[0].row}"].value is None:
            cursor.execute("SELECT name FROM Polygon")
            result = cursor.fetchall()
            if result is not None and (sheet[f"A{i[0].row}"].value,) not in result:
                cursor.execute("INSERT INTO Polygon (name, short_name, polygon) VALUES (?, ?, ?)",
                               (sheet[f"A{i[0].row}"].value, sheet[f"B{i[0].row}"].value, sheet[f"C{i[0].row}"].value))
                last_index_polygon = cursor.lastrowid
            elif result is None:
                cursor.execute("INSERT INTO Polygon (name, short_name, polygon) VALUES (?, ?, ?)",
                               (sheet[f"A{i[0].row}"].value, sheet[f"B{i[0].row}"].value, sheet[f"C{i[0].row}"].value))
                last_index_polygon = cursor.lastrowid
            cursor.execute("INSERT INTO Vehicle (number, polygon_id, structural_unit) VALUES (?, ?, ?)",
                           (sheet[f"D{i[0].row}"].value, last_index_polygon, sheet[f"E{i[0].row}"].value))
            last_index_vehicle = cursor.lastrowid
            if "=RANDBETWEEN(" not in str(sheet[f"M{i[0].row}"].value):
                cursor.execute("INSERT INTO Fines (vehicle_id, value) VALUES (?, ?)",
                               (last_index_vehicle, sheet[f"M{i[0].row}"].value))
            else:
                cursor.execute("INSERT INTO Fines (vehicle_id, value) VALUES (?, ?)",
                               (last_index_vehicle, 0))
            cursor.execute("INSERT INTO DrivingStyle (vehicle_id, value) VALUES (?, ?)",
                           (last_index_vehicle, sheet[f"N{i[0].row}"].value))
        else:
            if not sheet[f"K{i[0].row}"].value is None and not sheet[f"L{i[0].row}"].value is None:
                cursor.execute("INSERT INTO Telematics (date, mileage, vehicle_id) VALUES (?, ?, ?)",
                               (sheet[f"K{i[0].row}"].value, sheet[f"L{i[0].row}"].value, last_index_vehicle))
            elif not sheet[f"K{i[0].row}"].value is None and sheet[f"L{i[0].row}"].value is None:
                cursor.execute("INSERT INTO Telematics (date, mileage, vehicle_id) VALUES (?, ?, ?)",
                               (sheet[f"K{i[0].row}"].value, '', last_index_vehicle))
            elif sheet[f"K{i[0].row}"].value is None and not sheet[f"L{i[0].row}"].value is None:
                cursor.execute("INSERT INTO Telematics (date, mileage, vehicle_id) VALUES (?, ?, ?)",
                               ('', sheet[f"L{i[0].row}"].value, last_index_vehicle))
            if not sheet[f"I{i[0].row}"].value is None and not sheet[f"J{i[0].row}"].value is None:
                cursor.execute("INSERT INTO TripCard (date, mileage, vehicle_id) VALUES (?, ?, ?)",
                               (sheet[f"I{i[0].row}"].value, sheet[f"J{i[0].row}"].value, last_index_vehicle))
            elif not sheet[f"I{i[0].row}"].value is None and not sheet[f"J{i[0].row}"].value is None:
                cursor.execute("INSERT INTO TripCard (date, mileage, vehicle_id) VALUES (?, ?, ?)",
                               (sheet[f"I{i[0].row}"].value, '', last_index_vehicle))
            elif sheet[f"I{i[0].row}"].value is None and not sheet[f"J{i[0].row}"].value is None:
                cursor.execute("INSERT INTO TripCard (date, mileage, vehicle_id) VALUES (?, ?, ?)",
                               ('', sheet[f"J{i[0].row}"].value, last_index_vehicle))
    workbook.close()
    conn.commit()
    cursor.close()
    conn.close()
