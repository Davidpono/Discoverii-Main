
from django.shortcuts import render
import openai, os, requests
from dotenv import load_dotenv
from django.core.files.base import ContentFile
from images.models import Image
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY", None)
client = OpenAI(api_key=api_key)
def dnd_view(request):
    chatbot_response = None
    obj = None

    if api_key is not None and request.method == 'POST':
        OpenAI.api_key = api_key
        Name = request.POST.get('Name')
        Pronoun = request.POST.get('Pronoun')
        Age = request.POST.get('Age')
        Species = request.POST.get('Species')
        Class = request.POST.get('Class')
        details = request.POST.get('details')

        prompt = f"make me a dungeons and dragons back-story for Species {Species} Named {Name} that is a {Pronoun} is {Age} old, and is a {Class} and is {details}"
        prompt2 = f"make an realistic pciture with dungeons and dragons style with a dungeons and style background where it portrays a {Species} Named {Name} that is a {Pronoun} is {Age} old, and is a {Class} and is {details} make sure it has fitting background not picture with white background make it as detailed as you can"


        response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt
        )

        response_img = client.images.generate(
            model="dall-e-3",
            prompt=prompt2,
            size="1024x1024",
            quality="standard",
             n=1,
        )

        img_url = response_img.data[0].url
        response_img_content = requests.get(img_url).content
       
        chatbot_response = response.choices[0].text
          
        chatbot_response = chatbot_response


        # Save image to Django model
        img_file = ContentFile(response_img_content)
        count = Image.objects.count() + 1
        fname = f"image-{count}.jpg"
        obj = Image(phrase=Name)
        obj.ai_image.save(fname, img_file)
        obj.save()

    return render(request, "DND/base.html", {"response": chatbot_response, "object": obj})