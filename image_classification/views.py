import base64
import io
import urllib

import requests
import torch
from PIL import Image
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .forms import ImageUploadForm

# Create your views here.


# load pretrained DenseNet and go straight to evaluation mode for inference
# load as global variable here, to avoid expensive reloads with each request
model = model = torch.hub.load(
    "ultralytics/yolov5", "custom", path="last.pt", force_reload=True)
model.eval()


def get_prediction(image_bytes):
    """For given image bytes, predict the label using the pretrained DenseNet"""
    img = Image.open(io.BytesIO(image_bytes))
    results = model(img, size=640)
    data = results.pandas().xyxy[0].to_json(orient="records")
    return data


@method_decorator(csrf_exempt)
def index(request):
    predicted_result = None
    image_uri = None
    predicted_label = None

    if request.method == 'POST':
        if request.FILES.get("image"):
            image = request.FILES.get("image")
            image_bytes = image.read()
            try:
                predicted_result = get_prediction(image_bytes)
            except RuntimeError as re:
                print(re)
            return HttpResponse(predicted_result)
        if request.POST.get("url"):
            url = request.POST.get("url")
            image_bytes = urllib.request.urlopen(url).read()
            try:
                predicted_result = get_prediction(image_bytes)
            except RuntimeError as re:
                print(re)
            return HttpResponse(predicted_result)
    else:
        # in case of GET: simply show the empty form for uploading images
        form = ImageUploadForm()

    return render(request, 'image_classification/index.html')


