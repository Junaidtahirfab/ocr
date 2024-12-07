from django.urls import path
from ocrfile.views import *

urlpatterns = [
    path("folder/",                                 FolderApiView.as_view(),             name='folder-create-list'),
    path("folder/<int:pk>/",                        FolderApiView.as_view(),             name='folder-create-list'),
    path("companyfile/",                            CompanyFileApiView.as_view(),        name='companyfile-create-list'),
    path('companyfile/<int:pk>/add-shared-user/',   AddSharedUserView.as_view(),         name='add-shared-user'),
    path('companyfile/<int:pk>/remove-shared-user/',RemoveSharedUserView.as_view(),      name='remove-shared-user'),
    
    
    ]