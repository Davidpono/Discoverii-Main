from django.shortcuts import render
from dotenv import load_dotenv
import openai, os, requests
from django.core.files.base import ContentFile
from images.models import Image
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

def dnd_view(request):
    chatbot_response = None
    obj = None

    # Access the OpenAI API key from environment variables
    api_key = os.getenv("OPENAI_API_KEY", None)

    # Check if API key is available and the request method is POST
    if api_key is not None and request.method == 'POST':
        # Initialize OpenAI client with the API key
        client = OpenAI(api_key=api_key)

        Name = request.POST.get('Name')
        Pronoun = request.POST.get('Pronoun')
        Age = request.POST.get('Age')
        Species = request.POST.get('Species')
        Class = request.POST.get('Class')
        details = request.POST.get('details')

        prompt = f"make me a dungeons and dragons back-story for Species {Species} Named {Name} that is a {Pronoun} is {Age} old, and is a {Class} and is {details}"
        prompt2 = f"make an realistic pciture with dungeons and dragons style with a dungeons and style background where it portrays a {Species} Named {Name} that is a {Pronoun} is {Age} old, and is a {Class} and is {details} make sure it has fitting background not picture with white background make it as detailed as you can"

        try:
            # Call OpenAI API to generate text
            response = client.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt
            )

            # Call OpenAI API to generate image
            response_img = client.images.generate(
                model="dall-e-3",
                prompt=prompt2,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            # Get image URL and content
            img_url = response_img.data[0].url
            response_img_content = requests.get(img_url).content

            # Get the generated text response
            chatbot_response = response.choices[0].text

            # Save image to Django model
            img_file = ContentFile(response_img_content)
            count = Image.objects.count() + 1
            fname = f"image-{count}.jpg"
            obj = Image(phrase=Name)
            obj.ai_image.save(fname, img_file)
            obj.save()

        except Exception as e:
            # Handle any errors that occur during API calls
            chatbot_response = f"Error occurred: {str(e)}"

    # Render the template with the response and image object
    return render(request, "DND/base.html", {"response": chatbot_response, "object": obj})
