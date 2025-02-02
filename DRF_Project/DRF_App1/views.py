from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User
from .serializers import CSVSerializer
import csv
import io


def upload_view(request):
    return render(request, 'Base.html')


@api_view(['POST'])
def csv_file(request):
    file = request.FILES.get('file')

    if not file or not file.name.endswith('.csv'):
        return JsonResponse({'error': 'Invalid file format. Only CSV files are allowed.'}, status=status.HTTP_400_BAD_REQUEST)

    decoded_file = io.TextIOWrapper(file, encoding='utf-8')
    reader = csv.DictReader(decoded_file)

    success_count = 0
    error_count = 0
    errors = []
    saved_records = []

    for row in reader:
        row = {key.strip().lower(): value.strip() for key, value in row.items()}

        name = row.get('name', 'N/A')
        email = row.get('email', 'N/A')
        age = row.get('age', 'N/A')

        required_fields = ['name', 'email', 'age']
        if not all(field in row for field in required_fields):
            error_count += 1
            errors.append({'name': name, 'email': email, 'age': age, 'error': 'Missing required fields'})
            continue

        serializer = CSVSerializer(data=row)
        if serializer.is_valid():
            if not User.objects.filter(email=row['email']).exists():
                serializer.save()
                success_count += 1
                saved_records.append({'name': row['name'], 'email': row['email'], 'age': row['age']})
            else:
                error_count += 1
                errors.append({'name': name, 'email': email, 'age': age, 'error': 'User with this email already exists.'})
        else:
            error_messages = {}
            for field, message in serializer.errors.items():
                error_messages[field] = message
            error_count += 1
            errors.append({'name': name, 'email': email, 'age': age, 'error': error_messages})

    return JsonResponse({
        'total_saved': success_count,
        'total_rejected': error_count,
        'saved_records': saved_records,
        'errors': errors
    }, status=status.HTTP_201_CREATED)


def saved_records_view(request):
    saved_records = User.objects.all().order_by('-id')
    return render(request, 'Saved_records.html', {'saved_records': saved_records})


