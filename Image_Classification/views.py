from django.shortcuts import render

# Create your views here.

# now get us the data on computer vision model

import io
import os
import json

from torchvision import models, transforms
from PIL import Image
from django.conf import settings

import base64
from .forms import ImageUploadForm


# now lets get our model
model = models.densenet121(pretrained = True)
model.eval()

json_path = os.path.join(settings.STATIC_ROOT, "imagenet_class_index.json")

imagenet_mapping = json.load(open(json_path))




def transform_image(image_byte):

    transform = transforms.Compose([
        transforms.Resize(255),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            [0.485, 0.456, 0.406],
            [0.229, 0.224, 0.225]
        )
    ])


    # we use this RGB conversion as the image can be in ohter forms some have 4 color channel
    # which are not ompatable with the model input shape
    image = Image.open(io.BytesIO(image_byte)).convert('RGB')

    return transform(image).unsqueeze(0)


def get_prediction(image_byte):

    tensor = transform_image(image_byte)
    output = model.forward(tensor)
    _, y_hat = output.max(1)
    pred = str(y_hat.item())
    class_name, human_label = imagenet_mapping[pred]

    return human_label



def index(request):
    image_uri = None
    pred_lable = None

    if request.method == 'POST':

        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():

            image = form.cleaned_data['image']
            image_byte = image.file.read()

            encoded_img = base64.b64encode(image_byte).decode('ascii')
            image_uri = 'data:%s;base64,%s' % ('image/jpeg', encoded_img)

            try:
                pred_lable = get_prediction(image_byte)
            except RuntimeError as re:
                print(re)

    else:
        form = ImageUploadForm()

    
    context = {
        'form': form,
        'image_uri': image_uri,
        'predicted_label': pred_lable,
    }

    return render(request, 'Image_Classification/index.html', context)