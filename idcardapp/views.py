import os
import cv2
import pytesseract
import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import ScannedIDCard
from .serializers import ScannedIDCardSerializer
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser
from PIL import Image
from io import BytesIO
import base64
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout




def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # After successful registration, redirect to the login page
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with the URL of your home page
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Replace 'login' with the URL of your login page




def extract_pakistani_id_card_info(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply image preprocessing techniques (e.g., denoising, thresholding)
    # ...

    

    # Set the path to Tesseract executable (change if necessary)
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # Perform OCR on the preprocessed image
    text = pytesseract.image_to_string(gray, lang='eng')

    # Extract ID card number using regular expressions
    id_card_match = re.search(r"\d{5}-\d{7}-\d{1,2}", text)
    id_card_number = id_card_match.group(0) if id_card_match else None

    # Extract name using regular expressions
    name_match = re.search(r"(?i)Name[:\s]*([\w\s]+)", text)
    name = name_match.group(1) if name_match else None

    # Extract father's name using regular expressions
    father_name_match = re.search(r"(?i)Husband Name[:\s]*([\w\s]+)", text)
    father_name = father_name_match.group(1) if father_name_match else None

    # Extract date of birth using regular expressions
    dob_match = re.search(r"\d{2}\.\d{2}\.\d{4}", text)
    date_of_birth_str = dob_match.group(0) if dob_match else None

    # Convert date of birth to the correct format (YYYY-MM-DD)
    if date_of_birth_str:
        day, month, year = date_of_birth_str.split('.')
        date_of_birth = f"{year}-{month}-{day}"
    else:
        date_of_birth = None

    return id_card_number, name, father_name, date_of_birth

@api_view(['POST'])
def extract_id_card_info(request):
    if request.method == 'POST':
        image_data = request.data.get('image_base64')

        if image_data:
            # Remove the data:image/jpeg;base64, prefix
            image_data = image_data.split(';base64,')[1]

            # Convert the base64 string to an image
            image = Image.open(BytesIO(base64.b64decode(image_data)))

            # Save the image to a temporary file
            image_path = os.path.join(settings.MEDIA_ROOT, 'temp_image.jpg')
            image.save(image_path)

            id_card_number, name, father_name, date_of_birth = extract_pakistani_id_card_info(image_path)

            # Delete the temporary image file
            os.remove(image_path)

            return Response({
                'id_card_number': id_card_number,
                'name': name,
                'father_name': father_name,
                'date_of_birth': date_of_birth,
            }, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

class ScannedIDCardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScannedIDCard.objects.all()
    serializer_class = ScannedIDCardSerializer

def home(request):
    id_card_number = None
    name = None
    father_name = None
    date_of_birth = None
    image_url = None

    if request.method == 'POST':
        image = request.FILES.get('image')
        image_path = os.path.join(settings.MEDIA_ROOT, image.name)

        with open(image_path, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # Extract ID card information from the uploaded image
        id_card_number, name, father_name, date_of_birth = extract_pakistani_id_card_info(image_path)

        # Assuming 'image_url' is the URL of the uploaded image
        # You should set the 'image_url' to the actual URL where the image is served
        image_url = os.path.join(settings.MEDIA_URL, image.name)

    # Retrieve previously scanned ID card information from the database
    scanned_id_cards = ScannedIDCard.objects.all()

    context = {
        'id_card_number': id_card_number,
        'name': name,
        'father_name': father_name,
        'date_of_birth': date_of_birth,
        'image_url': image_url,
        'scanned_id_cards': scanned_id_cards,
    }
    return render(request, 'index.html', context)

# Rest of your views and URL patterns...
