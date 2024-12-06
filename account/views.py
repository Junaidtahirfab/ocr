from .serializers import (SendOTPSerializer,OtpverifySerializer,UserRegisterSerializer,
                        UserSerializer,LoginSerializer,RoleSerializer,ShareUserSerializer,
                        UserListSerializer,ChangePasswordSerializer,
                        ProfileSerializer,ResetPasswordStep1,ResetPasswordStep2)
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.exceptions import PermissionDenied
from rest_framework import status,generics,permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import Role,User,Company





class SendOTPView(GenericAPIView):
    permission_classes = []
    serializer_class = SendOTPSerializer
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({"success": "OTP successfully sent"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class VerifyOTPView(GenericAPIView):
    permission_classes = []
    serializer_class = OtpverifySerializer
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({"success": "Email successfully verified", "email" :serializer.validated_data['email']}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserView(GenericAPIView):
    permission_classes = []
    serializer_class = UserRegisterSerializer
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        # Validate and create the user if valid
        if serializer.is_valid():
            user = serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class UserLoginView(GenericAPIView):
    permission_classes = []
    serializer_class = LoginSerializer
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        # Serialize the incoming data
        serializer = self.serializer_class(data=request.data)
        # Validate the data (credentials)
        if serializer.is_valid():
            # On successful validation, return the user data with tokens
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoleListView(generics.ListAPIView):
    permission_classes = []
    serializer_class = RoleSerializer
    authentication_classes = []
    queryset = Role.objects.all()  # Query all Role objects
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)




class UserListView(generics.ListAPIView, generics.CreateAPIView):
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated] # Ensure the user is authenticated

    def get_queryset(self):
        user = self.request.user  # Get the authenticated user
        # Check if the user has 'Admin' role
        if user.role and user.role.name == 'Admin':
            # Return users who belong to the same company as the authenticated admin
            return User.objects.filter(company=user.company)
        else:
            # If the user is not an Admin, raise a permission error
            raise PermissionDenied("You do not have permission to access this resource.")
        
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ChangePasswordView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(context={"request": request}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
class ProfileApiView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer
    
    def get_queryset(self):
        # Retrieves the currently authenticated user from the request
        user = self.request.user
        # Returns a queryset of the User model filtered by the authenticated user's ID
        return User.objects.filter(id=int(user.id))

    def get_object(self):
        # Retrieves the currently authenticated user from the request
        user = self.request.user
        # Returns a single user object matching the authenticated user's ID from the queryset
        return self.get_queryset().get(id=user.id)

    def get(self, request, *args, **kwargs):
        # Handles GET requests using the parent's implementation, returning the user's profile data
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # Handles PUT requests using the parent's implementation, allowing full update of the user's profile
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # Handles PATCH requests using the parent's implementation, allowing partial update of the user's profile
        return super().patch(request, *args, **kwargs)
    
class ResetPasswordStep1View(GenericAPIView):
    permission_classes = [HasAPIKey]
    serializer_class = ResetPasswordStep1
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({"success": "successfully send OTP "}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ResetPasswordStep2View(GenericAPIView):
    permission_classes = [HasAPIKey]
    serializer_class = ResetPasswordStep2
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({"success": "successfully set New Password"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class SharedUserListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ShareUserSerializer

    def get_queryset(self):
        return User.objects.filter(company=self.request.user.company)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    
    
    
    