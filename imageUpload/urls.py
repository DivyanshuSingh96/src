from django.urls import path
from . import views

urlpatterns = [
    path("tailwind-homepage/", views.tailwind_homepage, name="homepage"),
    path("testing-page/", views.testing, name="testing-page"),
    # path("upload-data/", views.upload_image_view, name="upload-data"),
    path("apiGET-Image/<str:pk>", views.image_get_view, name="api-get-image"),
    path("apiPOST-Image/", views.image_post_view, name="api-post-image"),
    path("apiGET-Images", views.image_get_view_all, name="api-get-images"),
    # path("apiPOST-Img/", views.ImagePostAPI.as_view(), name="Image-API"),
]