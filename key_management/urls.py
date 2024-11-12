from django.urls import path
from . import views

# urlpatterns = [
#     # path('upload-key/', views.UploadKey.as_view(), name='upload-key'),
#     # path('get-key/', views.GetKey.as_view(), name='get-key'),
#     path("", views.apiOverview, name="api-overview"),
#     path("api/task-create/", views.taskCreate, name="task-create"),
# ]

urlpatterns = [
    # path("", views.apiOverview, name="api-overview"),
    # path("task-list/", views.taskList, name="task-list"),
    # path("task-detail/<str:pk>/", views.taskDetail, name="task-detail"),
    # path("task-create/", views.taskCreate, name="task-create"),
    # path("task-update/<str:pk>/", views.taskUpdate, name="task-update"),
    # path("task-delete/<str:pk>/", views.taskDelete, name="task-delete"),

    path("apiPost/", views.UploadKey.as_view(), name="upload-key"),
    path("apiGet/", views.GetKey.as_view(), name="get-key"),
    path("apiEncrypt/", views.upload_encrypted_image, name="encrypt-upload"),
    path("display-images/<str:pk>/", views.display_image_view, name="display-image-view"),
]