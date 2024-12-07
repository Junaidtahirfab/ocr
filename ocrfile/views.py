from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Folder,CompanyFile
from account.models import User
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import FolderSerializer,CompanyFileSerializer
from django.db.models import Q


class FolderApiView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if user.role.name == "Admin":
            return Folder.objects.filter(company__id=user.company.id)
        elif user.role.name == "viewer":
            return Folder.objects.filter(shared_with=user)
        else:
            return Folder.objects.filter(Q(created_by=user) | Q(shared_with=user)).distinct()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            folder = serializer.save(created_by=request.user, company=request.user.company)
            return Response(
                {"success": f"Folder '{folder.name}' created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, *args, **kwargs):
            # Fetch the filtered folders
        folders = self.get_queryset()

        # Prepare the response format
        response_data = []
        for folder in folders:
            # Get all files related to the folder
            files = CompanyFile.objects.filter(folder=folder)
            print("files",files)
            shared_users= ''
            shared_user_count= 0
            for file in files:
                shared_user_count = file.shared_with.count()
                if file.shared_with:
                    shared_users = file.shared_with.all().values_list('email','first_name')
            folder_data = {
                "folder_id": folder.id,
                "folder_name": folder.name,
                "created_by": folder.created_by.email,
                "shared_user_count": shared_user_count,
                "shared_users": shared_users,
                "files": [
                    {
                        "id": file.id,
                        "file_name": file.file.name,
                        "uploaded_by": file.uploaded_by.email,
                        "uploaded_at": file.uploaded_at,
                    }
                    for file in files
                ],
            }
            response_data.append(folder_data)

        return Response(response_data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class CompanyFileApiView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CompanyFileSerializer
    queryset = CompanyFile.objects.all()

    

        
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file = serializer.save(uploaded_by=request.user, company=request.user.company)
            return Response(
                {"success": f"File '{file.file.name}' uploaded successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddSharedUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        print("here")
        company_file = get_object_or_404(CompanyFile, pk=pk)
        # Retrieve the new user ID from the request
        shared_user_id = request.data.get("shared_with")
        if not shared_user_id:
            return Response({"error": "'shared_with' field is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            new_user = User.objects.get(pk=shared_user_id)
            company_file.shared_with.add(new_user)
            company_file.save()
            return Response({"message": f"User {new_user.first_name} added successfully to the shared list."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User with the given ID does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RemoveSharedUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        company_file = get_object_or_404(CompanyFile, pk=pk)
        # Retrieve the user ID to be removed from the request
        shared_user_id = request.data.get("shared_with")
        if not shared_user_id:
            return Response({"error": "'shared_with' field is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Get the user instance
            user_to_remove = User.objects.get(pk=shared_user_id)
            # Remove the user from the shared_with field
            if user_to_remove in company_file.shared_with.all():
                company_file.shared_with.remove(user_to_remove)
                company_file.save()
                return Response({"message": f"User {user_to_remove.username} removed successfully from the shared list."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User is not in the shared list."}, status=status.HTTP_404_NOT_FOUND)

        except User.DoesNotExist:
            return Response({"error": "User with the given ID does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
# from rest_framework.parsers import MultiPartParser, FormParser

# class BulkFileUploadApiView(APIView):
#     """
#     Handles uploading multiple files at once.
#     """
#     permission_classes = [permissions.IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]

#     def post(self, request, *args, **kwargs):
#         files = request.FILES.getlist('files')
#         folder_id = request.data.get("folder")

#         folder = Folder.objects.filter(pk=folder_id).first()
#         company = self.request.user.company

#         if not company:
#             return Response({"error": "Company not found."}, status=status.HTTP_400_BAD_REQUEST)

#         created_files = []
#         for file in files:
#             created_file = CompanyFile.objects.create(
#                 file=file,
#                 company=company,
#                 folder=folder,
#                 uploaded_by=request.user,
#             )
#             created_files.append({"id": created_file.id, "file": created_file.file.name})

#         return Response(
#             {"success": "Files uploaded successfully", "files": created_files},
#             status=status.HTTP_201_CREATED,
#         )