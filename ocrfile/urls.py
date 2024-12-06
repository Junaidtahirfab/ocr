from django.urls import path
from ocrfile.views import *

urlpatterns = [
    path("folder/",                      FolderApiView.as_view(),             name='folder-create-list'),
    path("companyfile/",                 CompanyFileApiView.as_view(),        name='companyfile-create-list'),
    
    
    ]