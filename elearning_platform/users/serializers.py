# from rest_framework import serializers
# from .models import User

# class UserRegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, min_length=6)

#     class Meta:
#         model = User
#         fields = ['email', 'name', 'password', 'role']

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             email=validated_data['email'],
#             password=validated_data['password'],
#             name=validated_data['name'],
#             role=validated_data['role']
#         )
#         return user

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email', 'name', 'bio', 'profile_picture', 'social_links', 'role']
#         read_only_fields = ['email', 'role']


from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import AccessToken

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'role']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            token = AccessToken.for_user(user)
            return {"access": str(token)}
        raise serializers.ValidationError("Invalid credentials")

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'bio', 'profile_pic', 'social_links', 'role']
        read_only_fields = ['email', 'role']
