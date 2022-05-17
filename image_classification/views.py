import base64
import io
import urllib

import requests
import torch
from PIL import Image
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .forms import ImageUploadForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.


# load pretrained DenseNet and go straight to evaluation mode for inference
# load as global variable here, to avoid expensive reloads with each request
model = model = torch.hub.load(
         "ultralytics/yolov5", "custom", path="last.pt", force_reload=True)
model.eval()

predicted_result = "null"

def get_prediction(image_bytes):
    """For given image bytes, predict the label using the pretrained DenseNet"""
    img = Image.open(io.BytesIO(image_bytes))
    results = model(img, size=640)
    data = results.pandas().xyxy[0].to_json(orient="records")
    return data


@method_decorator(csrf_exempt)
def index(request):
    global predicted_result
    image_uri = None
    predicted_label = None
    if request.method == 'POST':
        if request.FILES.get("image"):
            image = request.FILES.get("image")
            image_bytes = image.read()
            # convert and pass the image as base64 string to avoid storing it to DB or filesystem
            encoded_img = base64.b64encode(image_bytes).decode('utf-8')
            image_uri = 'data:%s;base64,%s' % ('image/jpeg', encoded_img)
            # get predicted label with previously implemented PyTorch function
            try:
                predicted_result = get_prediction(image_bytes)
            except RuntimeError as re:
                print(re)
            return HttpResponse(predicted_result)
        if request.POST.get("url"):
            url = request.POST.get("url")
            image_bytes = urllib.request.urlopen(url).read()

            # convert and pass the image as base64 string to avoid storing it to DB or filesystem
            encoded_img = base64.b64encode(image_bytes).decode('utf-8')
            image_uri = 'data:%s;base64,%s' % ('image/jpeg', encoded_img)
            # get predicted label with previously implemented PyTorch function
            try:
                predicted_result = get_prediction(image_bytes)
            except RuntimeError as re:
                print(re)
            return HttpResponse(predicted_result)

    else:
        # in case of GET: simply show the empty form for uploading images
        form = ImageUploadForm()

    return render(request, 'image_classification/index.html')

