from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
import numpy as np
from tensorflow.keras.layers import LeakyReLU # type: ignore
from django.conf import settings
# Load your pre-trained model
model = load_model(os.path.join('static', 'model_saver1', 'modelleg.h5'),
custom_objects = {'LeakyReLU':LeakyReLU})  # Adjust the path


def predict_image(img_path, model, confidence_threshold=0.7):
    # Load and preprocess the image
    img = image.load_img(img_path, target_size=(120, 120))  # Match model input size
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0  # Normalize to [0, 1]
    img_array = np.expand_dims(img_array, axis=0)
    
    # Make predictions
    prediction = model.predict(img_array)
    
    # Get probabilities for both classes
    pneumonia_confidence = prediction[0][0]  # Confidence for Pneumonia class
    healthy_confidence = 1 - pneumonia_confidence  # Confidence for Healthy class
    
    # Log the predictions (optional, for debugging)
    print(f"Predictions - Pneumonia: {pneumonia_confidence:.2f}, Healthy: {healthy_confidence:.2f}")
    
    # Enhanced OOD detection: check the spread of probabilities
    total_confidence = pneumonia_confidence + healthy_confidence
    if total_confidence < 1.0:  # Adjust this threshold as needed
        return {
            'result': 'Unknown',
            'medication': 'Invalid Image',
            'message': 'The image is not a valid medical image. Please ensure it is relevant.'
        }
    
    # Classify based on confidence thresholds
    if pneumonia_confidence > confidence_threshold:
        return {
            'result': 'Pneumonia Detected',
            'medication': 'Antibiotics (e.g., Amoxicillin, Azithromycin)',
            'message': 'Consult a doctor for proper dosage and duration of treatment.'
        }
    elif healthy_confidence > confidence_threshold:
        return {
            'result': 'Healthy',
            'medication': 'None',
            'message': 'No medication required. Maintain a healthy lifestyle.'
        }
    else:
        # Default to 'Unknown' if no class is confident enough
        return {
            'result': 'Unknown',
            'medication': 'Invalid Image',
            'message': 'The image is not a valid medical image. Please ensure it is relevant.'
        }

# View to handle form submission and prediction
def home(request):
    if request.method == 'POST' and request.FILES['image']:
        img = request.FILES['image']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
        filename = fs.save(img.name, img)
        img_path = fs.url(filename)

        # Get prediction result with additional details
        prediction_data = predict_image(os.path.join(settings.MEDIA_ROOT, 'uploads', filename),model)
        img_full_path = settings.MEDIA_URL + 'uploads/' + filename

        # Debugging: Print prediction data
        print(prediction_data)

        return render(request, 'results.html', {
            'result': prediction_data['result'],
            'medication': prediction_data['medication'],
            'message': prediction_data['message'],
            'img_path': img_full_path,
        })
    
    return render(request, 'index.html')


