from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from os.path import splitext
import pandas as pd
import logging
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Polygon, Vehicle, Fines, Telematics, TripCard, DrivingStyle
from .parser.parse import excel_to_db

logger = logging.getLogger(__name__)

def post_list(request):
    return render(request, 'rzd/upload_file.html', {})

def upload_file(request):
    if request.method == 'POST' and 'myfile' in request.FILES:
        myfile = request.FILES['myfile']
        MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
        if myfile.size > MAX_FILE_SIZE:
            error_message = f"Ошибка: Размер файла '{myfile.name}' превышает максимально допустимый размер ({MAX_FILE_SIZE / (1024 * 1024)} MB)."
            logger.error(error_message)
            return render(request, 'rzd/upload_file.html', {
                'error_message': error_message
            })

        _, file_extension = splitext(myfile.name)
        if file_extension.lower() == '.xlsx':
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = os.path.join(settings.MEDIA_URL, filename)
            logger.info(f"Загруженный файл: {uploaded_file_url}")
            print(filename)
            excel_to_db(filename)
            data_frame = pd.read_excel(os.path.join(settings.MEDIA_ROOT, filename))
            data = data_frame.head(2).to_html(index=False)

            return render(request, 'rzd/upload_file.html', {
                'uploaded_file_url': uploaded_file_url,
                'data': data
            })
        else:
            error_message = f"Ошибка: Только файлы с расширением .xlsx допускаются, а не '{file_extension}'"
            logger.error(error_message)
            return render(request, 'rzd/upload_file.html', {
                'error_message': error_message
            })

    return render(request, 'rzd/upload_file.html')

def view_data(request, model_name):
    models = {
        'polygon': Polygon,
        'vehicle': Vehicle,
        'fines': Fines,
        'telematics': Telematics,
        'tripcard': TripCard,
        'drivingstyle': DrivingStyle,
    }

    model = models.get(model_name)

    if not model:
        return render(request, '404.html', status=404)

    items_list = model.objects.all()
    paginator = Paginator(items_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'rzd/upload_file.html', {'page_obj': page_obj, 'model_name': model_name})

def view_all_data(request):
    vehicles = Vehicle.objects.all()
    fines = Fines.objects.all()
    telematics = Telematics.objects.all()
    trip_cards = TripCard.objects.all()
    driving_styles = DrivingStyle.objects.all()

    return render(request, 'rzd/upload_file.html', {
        'vehicles': vehicles,
        'fines': fines,
        'telematics': telematics,
        'trip_cards': trip_cards,
        'driving_styles': driving_styles,
    })