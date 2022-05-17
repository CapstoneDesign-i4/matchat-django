import base64
import io
import urllib

import requests
import torch
from PIL import Image
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from .forms import ImageUploadForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from matchat.models import Product


# Create your views here.


# load pretrained DenseNet and go straight to evaluation mode for inference
# load as global variable here, to avoid expensive reloads with each request
model = model = torch.hub.load(
         "ultralytics/yolov5", "custom", path="last.pt", force_reload=True)
model.eval()

predicted_result = "null"

def get_prediction(image_bytes):
    """For given image bytes, predict the label using the pretrained DenseNet"""
    product = get_object_or_404(Product, pk=9)
    img = Image.open(io.BytesIO(image_bytes))
    product.web_result = "debug1"
    product.save()
    results = model(img, size=640)
    product.web_result = "debug2"
    product.save()
    data = results.pandas().xyxy[0].to_json(orient="records")
    product.web_result = "debug3"
    product.save()
    return data


@method_decorator(csrf_exempt)
def index(request):
    global predicted_result
    product = get_object_or_404(Product, pk=9)
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
        product.web_result = "debug4"
        product.web_result = request.POST.get("url")
        product.save()
        if request.POST.get("url"):
            product.web_result = "debug5"
            product.save()
            url = request.POST.get("url")
            product.web_result = "debug6"
            product.save()
            image_bytes = urllib.request.urlopen(url, timeout=40).read()
            product.web_result = "debug7"
            product.save()

            # convert and pass the image as base64 string to avoid storing it to DB or filesystem
            encoded_img = base64.b64encode(image_bytes).decode('utf-8')
            product.web_result = "debug8"
            product.save()
            image_uri = 'data:%s;base64,%s' % ('image/jpeg', encoded_img)
            product.web_result = "debug9"
            product.save()
            # get predicted label with previously implemented PyTorch function
            try:
                product.web_result = "debug10"
                product.save()
                predicted_result = get_prediction(image_bytes)
                product.web_result = "debug11"
                product.save()
            except RuntimeError as re:
                product.web_result = "debug12"
                product.save()
                print(re)
                product.web_result = "debug13"
                product.save()
            return HttpResponse("test")

    else:
        # in case of GET: simply show the empty form for uploading images
        form = ImageUploadForm()

    return render(request, 'image_classification/index.html')

