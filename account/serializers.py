
import django.contrib.auth.password_validation as validators
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User,OtpVerify,Company,Role
from rest_framework import serializers,status
from django.core import exceptions
from .utils import send_otp
# from .tasks import emailsend



class SendOTPSerializer(serializers.Serializer):
    # Email field that is required for the serializer
    email = serializers.EmailField(required=True)
    def validate(self, attrs):
        # Extract email from the validated data
        email = attrs.get("email")
        user_obj = None
        # Check if email is provided
        if not email:
            raise serializers.ValidationError("Email is required", "email", status_code=status.HTTP_400_BAD_REQUEST)
        try:
            # Attempt to retrieve the user associated with the provided email
            user_obj = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            pass
        # Remove any existing OTPs for this user
        if  user_obj:
            OtpVerify.objects.filter(user=user_obj).delete()
        else:
            OtpVerify.objects.filter(email=email).delete()
        # Generate a new OTP
        email_body = "Enter this OTP to Verify your Email\n"
        send_otp(email, email_body)
        # Return the validated data
        return attrs
    
    
class OtpverifySerializer(serializers.Serializer):
    # Email field, required for OTP verification
    email = serializers.CharField(required=True)
    # OTP field, required for verification
    otp = serializers.CharField(required=True)
    def validate(self, attrs):
        # Extract the email from the input attributes
        email = attrs['email']
    
        otp = attrs.get("otp")
        if not otp:
            # If OTP is not provided, raise a custom validation error
            raise serializers.ValidationError("OTP is required", "otp", status_code=status.HTTP_400_BAD_REQUEST)
        try:
            # Attempt to find an OTP record that matches the given OTP and user
            otp_obj = OtpVerify.objects.get(otp=otp, email=email)
        except OtpVerify.DoesNotExist:
            # If no OTP record is found, raise a custom validation error
            raise serializers.ValidationError("Invalid OTP", "otp", status_code=status.HTTP_400_BAD_REQUEST)
        # Delete the OTP record after successful verification
        otp_obj.delete()
        # Return the validated attributes
        return attrs


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'category', 'address_line_1', 'address_line_2', 'city', 'zip_code', 'country', 'state']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    # Nested CompanySerializer
    company = CompanySerializer()
    role_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'password', 'company',"role_name"]

    def create(self, validated_data):
        admin_role = Role.objects.filter(name="Admin").first()
        # Extract company data from validated_data
        company_data = validated_data.pop('company', None)
        password = validated_data.pop("password")
        # Create the company if provided in the request
        if company_data:
            company = Company.objects.create(**company_data)
        else:
            company = None

        # Create the user and assign the company to the user
        user = User.objects.create(company=company, **validated_data)
        user.set_password(password)
        user.role = admin_role
        user.is_admin = True
        user.save()
        return user
    def get_role_name(self, obj):
        # Return the role name for the user
        return obj.role.name if obj.role else None



class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        # Check if the user exists
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email", code='email')

        # Check if the password is correct
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect Password", code='password')

        # Generate the JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Prepare the response data
        company_data = CompanySerializer(user.company).data if user.company else None
        role_name = user.role.name if user.role else None

        # Return the user data with tokens
        return {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'company': company_data,
            'role_name': role_name,
            'access_token': str(access_token),
            'refresh_token': str(refresh),
        }


class UserListSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()  # To display company name instead of ID
    role = serializers.StringRelatedField()  # To display role name instead of ID

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'company', 'role']  # Include role and company




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone',
                'password', 'company', 'role', 'address_1',
                'address_2', 'city', 'zip_code', 'country', 'state', 'gender', 'date_of_birth']
        extra_kwargs = {'password': {'write_only': True}}  # Ensure password is write-only

    def create(self, validated_data):

        # Get the authenticated user (admin) making the request
        admin_user = self.context['request'].user

        # Ensure the user is an Admin
        if admin_user.role.name != 'Admin':
            raise serializers.ValidationError("Only admins can create users.")

        # Assign the company of the admin to the new user
        company = admin_user.company
        print("company.....",company)

        # Pop the password and role fields from validated data
        password = validated_data.pop('password')
        role = validated_data.pop('role')

        # Create the new user and assign the company and selected role
        user = User.objects.create(role=role, **validated_data)
        user.set_password(password)  # Hash the password before saving
        user.company = company
        user.save()

        return user




class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        new_password = attrs.get("new_password", None)
        old_password = attrs.get("old_password", None)
        try:
            user = self.context["request"].user
        except Exception as ex:
            raise serializers.ValidationError({"invalid ": "Please contact admin {}".format(ex)})
        if not user.check_password(old_password):
            raise serializers.ValidationError({"old_password": "Incorrect Password"})
        if user.check_password(new_password):
            raise serializers.ValidationError({"new_password": "New password should not be same as old_password"})
        try:
            # validate the password and catch the exception
            validators.validate_password(password=new_password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        user.set_password(validated_data.get("new_password"))
        user.save()
        return validated_data

    def save(self, **kwargs):
        return super().save(**kwargs)




class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone',
                'company', 'role', 'address_1',
                'address_2', 'city', 'zip_code', 'country', 'state', 'gender', 'date_of_birth']

    def validate(self, attrs):
        email = attrs.get("email", None)
        
        if email and email != None:
            raise serializers.ValidationError({"User ": "Please contact admin For change the email"})

        return attrs


class ResetPasswordStep1(serializers.Serializer):
    # Email field that is required for the serializer
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        # Extract email from the validated data
        email = attrs.get("email")
        # Check if email is provided
        if not email:
            raise serializers.ValidationError("Email is required", "email", status_code=status.HTTP_400_BAD_REQUEST)
        try:
            # Attempt to retrieve the user associated with the provided email
            user_obj = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            # Raise a validation error if the user does not exist
            raise serializers.ValidationError("Valid email is required", "email", status_code=status.HTTP_400_BAD_REQUEST)
        # Remove any existing OTPs for this user
        OtpVerify.objects.filter(user=user_obj).delete()
        # Generate and send a new OTP
        email_body = "Enter this OTP to reset your password\n"
        send_otp(user_obj.id, email_body)
        # Return the validated data
        return attrs


class ResetPasswordStep2(serializers.Serializer):
    otp = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        otp = attrs.get("otp", None)
        password = attrs.get("password", None)
        # Check if OTP is provided
        if otp:
            try:
                # Fetch the OTP object using the OTP code
                otpobj = OtpVerify.objects.filter(otp=otp).first()
                # Check if OTP exists
                if otpobj:
                    # Use the is_valid method to check if OTP is still valid
                    if not otpobj.is_valid():
                        raise serializers.ValidationError({"otp": "The OTP has expired."})
                    # Validate the password and catch the exception
                    try:
                        validators.validate_password(password=password, user=otpobj.user)
                    except exceptions.ValidationError as e:
                        raise serializers.ValidationError({'password': list(e.messages)})
                    # Set the new password, delete the OTP, and save the user
                    otpobj.user.set_password(password)
                    otpobj.delete()
                    otpobj.user.save()
                else:
                    raise OtpVerify.DoesNotExist
            except OtpVerify.DoesNotExist:
                raise serializers.ValidationError({"otp": "Valid OTP is required."})
        else:
            raise serializers.ValidationError({"otp": "OTP is required."})
        return attrs
    
    
