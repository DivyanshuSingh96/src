from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes, renderer_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from django.utils import timezone

from datetime import timedelta
from decouple import config as env_config

from .serializers import ImagePostSerializer
from .models import ImagePost
from .forms import ImagePostForm
from imageViewer.services import upload_image_to_cloudflare
# from .models import ImagePost

from imageViewer.services import (
    upload_image_to_cloudflare,
    get_image_url_from_cloudflare)

# Create your views here.
def tailwind_homepage(request):
    return render(request, "base.html")

def testing(request):
    return render(request, "testing.html")

# GET view for retrieving all images and regenerating URLs if expired
@api_view(["GET"])
@parser_classes([MultiPartParser, FormParser])
def image_get_view(request, pk):
    if request.method == "GET":
        image = ImagePost.objects.filter(id=pk).first()
        
        # for image in post:
            # Check if the URL has expired and regenerate it if needed
        if image.url_expiration < timezone.now():
            new_url = image.cloudflare_path
            if new_url:
                image.cloudflare_path = new_url
                image.url_expiration = timezone.now() + timedelta(seconds=3600)  # Reset expiration
                image.save()

        # Serialize the image data to return in the response
        serializer = ImagePostSerializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@parser_classes([MultiPartParser, FormParser])
def image_get_view_all(request):
    if request.method == "GET":
        images = ImagePost.objects.all()
        
        for image in images:
            if image.url_expiration < timezone.now():
                new_url = image.cloudflare_path
                if new_url:
                    image.cloudflare_path = new_url
                    image.url_expiration = timezone.now() + timedelta(seconds=3600)  # Reset expiration
                    image.save()

        # Serialize all the image data to return in the response
        serializer = ImagePostSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(["GET"])
# @parser_classes([MultiPartParser, FormParser])
# def image_get_view(request):
#     if request.method == "GET":
#         post = ImagePost.objects.all()
#         serializer = ImagePostSerializer(post, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@parser_classes([MultiPartParser, FormParser])
def image_post_view(request):
    if request.method == "POST":
        serializer = ImagePostSerializer(data=request.data)
        
        if serializer.is_valid():
            instance = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @shared_task
# def renew_image_urls():
#     # Query all expired image URLs
#     expired_images = ImagePost.objects.filter(url_expiration__lt=timezone.now())
#     for image in expired_images:
#         new_url = regenerate_signed_url(image.cloudflare_path)
#         image.cloudflare_url = new_url
#         image.save()

# def image_post_view(request):
#     if request.method == "POST":
#         form = ImagePostForm(request.POST, request.FILES)
#         # serializer = ImagePostSerializer(data=request.data)
#         if form.is_valid():
#             instance = form.save()
#             serializer = ImagePostSerializer(instance)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

# class ImagePostAPI(APIView):
#     parser_classes = [MultiPartParser, FormParser]

#     # def post(self, request, *args, **kwargs):
#     #     form = ImagePostForm(request.POST, request.FILES)
#     #     if form.is_valid():
#     #         instance = form.save(commit=False)
#     #         image_file = form.cleaned_data['image_file']
#     #         # Upload to Cloudflare and save the URL
#     #         cloudflare_id = upload_image_to_cloudflare(instance, image_file)
#     #         if cloudflare_id:
#     #             instance.image = cloudflare_id  # Assuming `image` field stores the Cloudflare URL
#     #             instance.save()
#     #             return Response({"message": "Image uploaded successfully"}, status=status.HTTP_201_CREATED)
#     #         else:
#     #             return Response({"error": "Cloudflare upload failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     #     return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

#     def post(self, request, *args, **kwargs):
#         form = ImagePostForm(request.POST, request.FILES)
#         if form.is_valid():
#             instance = form.save(commit=False)
            
#             # Access `image_file` directly from `request.FILES`
#             image_file = request.FILES.get('image_file')
            
#             if image_file:
#                 print(f"Image file received: {image_file.name}, Size: {image_file.size}")
#                 # Upload to Cloudflare and save the URL
#                 cloudflare_id = upload_image_to_cloudflare(instance, image_file)
                
#                 if cloudflare_id:
#                     instance.image = cloudflare_id  # Assuming `image` field stores the Cloudflare URL
#                     instance.save()
#                     return Response({"message": "Image uploaded successfully"}, status=status.HTTP_201_CREATED)
#                 else:
#                     return Response({"error": "Cloudflare upload failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#             else:
#                 return Response({"error": "Image file is missing"}, status=status.HTTP_400_BAD_REQUEST)
        
#         return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request, *args, **kwargs):
    #     # Fetch image posts and serialize them
    #     image_posts = ImagePost.objects.all()
    #     data = [{
    #         "id": post.id,
    #         "title": post.title,
    #         "content": post.content,
    #         "author": post.author,
    #         "cloudflare_path": post.cloudflare_path,
    #     } for post in image_posts]
    #     return Response(data, status=status.HTTP_200_OK)

# def upload_image_view(request):
#     if request.method == 'POST':
#         form = ImagePostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('homepage')
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Invalid form submission'}, status=400)
#     else:
#         form = ImagePostForm()
#     return render(request, 'Frontend/image_upload.html', {'form': form})

# def upload_image_view(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         content = request.POST.get('content')
#         author = request.POST.get('author')
#         image = request.FILES.get('image')  # Image file from the form

#         # You can now create an instance of the model manually
#         instance = ImagePost.objects.create(
#             title=title,
#             content=content,
#             author=author,
#             image=image
#         )
#         return redirect('homepage')
#     return render(request, 'Frontend/image_upload.html')

# def upload_image_view(request):
#     if request.method == 'POST':
#         form = ImagePostForm(request.POST, request.FILES)
        
#         if form.is_valid():
#             # Save the instance, including the image and encrypted key
#             instance = form.save()

#             # Redirect or provide a success response
#             return redirect('success_url')  # Replace with your actual success URL
#         else:
#             # If the form is invalid, return an error response
#             return JsonResponse({'status': 'error', 'message': 'Invalid form submission'}, status=400)
    
#     else:
#         # GET request: Initialize an empty form to be displayed
#         form = ImagePostForm()

#     return render(request, 'Frontend/image_upload.html', {'form': form})