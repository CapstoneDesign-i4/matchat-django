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

test = "start"

def get_prediction(image_bytes):
    """For given image bytes, predict the label using the pretrained DenseNet"""
    global test
    test = "debug8"
    img = Image.open(io.BytesIO(image_bytes))
    test = "debug9"
    results = model(img, size=640)
    test = "debug10"
    data = results.pandas().xyxy[0].to_json(orient="records")
    test = "debug11"
    return data


@method_decorator(csrf_exempt)
def index(request):
    image_uri = None
    predicted_label = None
    global test
    if request.method == 'POST':
        if request.FILES.get("image"):
            image = request.FILES.get("image")
            image_bytes = image.read()
            # convert and pass the image as base64 string to avoid storing it to DB or filesystem
            encoded_img = base64.b64encode(image_bytes).decode('ascii')
            image_uri = 'data:%s;base64,%s' % ('image/jpeg', encoded_img)
            # get predicted label with previously implemented PyTorch function
            try:
                predicted_result = get_prediction(image_bytes)
            except RuntimeError as re:
                print(re)
            return HttpResponse(predicted_result)
        if request.POST.get("url"):
            test = "debug1"
            url = request.POST.get("url")
            test = "debug2"
            image_bytes = urllib.request.urlopen(url).read()
            test = "debug3"

            # convert and pass the image as base64 string to avoid storing it to DB or filesystem
            encoded_img = base64.b64encode(image_bytes).decode('ascii')
            test = "debug4"
            image_uri = 'data:%s;base64,%s' % ('image/jpeg', encoded_img)
            test = "debug5"
            # get predicted label with previously implemented PyTorch function
            try:
                predicted_result = get_prediction(image_bytes)
                test = "debug6"
            except RuntimeError as re:
                print(re)
                test = "debug7"
            return HttpResponse(test)

    else:
        # in case of GET: simply show the empty form for uploading images
        form = ImageUploadForm()

    return render(request, 'image_classification/index.html')

