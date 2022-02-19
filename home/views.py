from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from keras.models import model_from_json
import numpy as np
from keras.preprocessing import image
from django.core.files.storage import default_storage
from django.conf import settings
from pathlib import Path
import os
from django.contrib import messages

# Rendering the dashboard if user success
def index(request):
    if request.user.is_anonymous:
        return redirect('/login')
    return redirect('/dashboard')


# Rendering the dashboard if user success
def loginUser(request):
    if not request.user.is_anonymous:
        return redirect('/dashboard')
    if request.method == 'POST':
        user = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(username=user, password=passw)
                
        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        else:
            return render(request, 'login.html')

    return render(request, 'login.html')
        

# Rendering the login if user logouts
def logoutUser(request):
    logout(request)
    return redirect('/login')


# Rendering the dashboard if user success
def dashboard(request):
    if request.user.is_anonymous:
        return redirect('/login')
    return render(request, 'dashboard.html')


# Rendering the animal predictor if user success
def animal(request):
    if request.user.is_anonymous:
        return redirect('/login')

    if request.method == 'POST':
        if len(request.FILES) == 0:
            messages.warning(request, 'Please select an image to predict')
            return redirect('/animal')

        animal_image = request.FILES['animal']
        file_name = animal_image.name
        default_storage.delete(file_name)   # Delete already existing file from storage
        file_name_2 = default_storage.save(file_name, animal_image)

        BASE_DIR = Path(__file__).resolve().parent.parent
        file_url = os.path.join(BASE_DIR) + default_storage.url(file_name_2)

        original = image.load_img(file_url, target_size=(64, 64))
        numpy_image = image.img_to_array(original)
        numpy_image = numpy_image.reshape((1, ) + numpy_image.shape)

        # load json and create model
        json_file = open(os.path.join(BASE_DIR, "static") + r"\model\animal_model\classifier.json", 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        classifier = model_from_json(loaded_model_json)
        classifier.load_weights(os.path.join(BASE_DIR, "static") + r"\model\animal_model\classifier.h5")
        
        result = classifier.predict(numpy_image)

        if result[0][0] == 1:
            prediction = 'DOG'
        else:
            prediction = 'CAT'

        context = {
            'image_name': file_name_2,
            'prediction': prediction
        }
        
        return render(request, 'result.html', context)

    return render(request, 'animal.html')


# Creating a function to get the Digit
def getDigit(result):
    prediction = 0
    for val in range(len(result)):
        if int(result[val]) == int(1.0):
            prediction = val
        else:
            continue
            
    return prediction


# Rendering the digit predictor if user success
def digit(request):
    if request.user.is_anonymous:
        return redirect('/login')

    if request.method == 'POST':
        if len(request.FILES) == 0:
            messages.warning(request, 'Please select an image to predict')
            return redirect('/digit')

        digit_image = request.FILES['digit']
        file_name = digit_image.name
        default_storage.delete(file_name)  # Delete already existing file from storage
        file_name_2 = default_storage.save(file_name, digit_image)

        BASE_DIR = Path(__file__).resolve().parent.parent
        file_url = os.path.join(BASE_DIR) + default_storage.url(file_name_2)

        original = image.load_img(file_url, target_size=(28, 28), color_mode="grayscale")
        numpy_image = image.img_to_array(original)
        numpy_image = numpy_image.reshape(1, 784)

        # load json and create model
        json_file = open(os.path.join(BASE_DIR, "static") + r"\model\digit_model\classifier.json", 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        classifier = model_from_json(loaded_model_json)
        classifier.load_weights(os.path.join(BASE_DIR, "static") + r"\model\digit_model\classifier.h5")

        result = classifier.predict(numpy_image)    # Predicting the Digit
        result = result[0]

        prediction = getDigit(result)    # Associating the Label with the 1
        # print(prediction, '---------------------')

        context = {
            'image_name': file_url,
            'prediction': prediction
        }
        
        return render(request, 'result.html', context)

    return render(request, 'digit.html')
    