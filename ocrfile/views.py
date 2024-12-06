from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Folder
from .serializers import FolderSerializer
from django.db.models import Q


class FolderApiView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.role.name == "Admin":
            return Folder.objects.filter(company__id = user.company.id)
        if user.role.name == "viewer":
            # Folders created by the user or shared with the user
            return Folder.objects.filter(shared_with=user)
        else:
            return Folder.objects.filter(Q(created_by=user) | Q(shared_with=user)).distinct()
        
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            folder = serializer.save(created_by=request.user)
            return Response(
                {"success": f"Folder '{folder.name}' created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)