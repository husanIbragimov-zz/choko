from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from apps.base.models import Profile
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class AdminCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'email', 'first_name', 'last_name', 'is_staff', 'is_active'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        is_staff = validated_data.pop('is_staff', None)
        is_active = validated_data.pop('is_active', None)
        username = validated_data.pop('username', None)

        validate_password(password)
        password = make_password(password)

        user = User.objects.filter(username=username)
        if user:
            raise serializers.ValidationError({"message": "User already exists!"})
        else:
            user = User.objects.create(username=username, password=password, is_staff=is_staff, is_active=is_active,
                                       **validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        phone_number = validated_data.pop('username', None)
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)
        is_staff = validated_data.pop('is_staff', None)
        is_active = validated_data.pop('is_active', None)

        user = User.objects.filter(id=instance.id).first()

        if instance.username != phone_number:
            user.username = phone_number

        if password:
            validate_password(password)
            password = make_password(password)
            user.set_password(password)

        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        if is_staff:
            user.is_staff = is_staff

        if is_active:
            user.is_active = is_active
        user.save()
        return user


class AdminListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ClientCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'email', 'first_name', 'last_name', 'is_active'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        is_active = validated_data.pop('is_active', None)
        username = validated_data.pop('username', None)

        validate_password(password)
        password = make_password(password)

        user = User.objects.filter(username=username)
        if user:
            raise serializers.ValidationError({"message": "User already exists!"})
        else:
            user = User.objects.create(username=username, password=password, is_active=is_active, **validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        phone_number = validated_data.pop('username', None)
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)
        is_active = validated_data.pop('is_active', None)

        user = User.objects.filter(id=instance.id).first()

        if instance.username != phone_number:
            user.username = phone_number

        if password:
            validate_password(password)
            password = make_password(password)
            user.set_password(password)

        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        if is_active:
            user.is_active = is_active
        user.save()
        return user


class AdminLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=13, required=True)
    password = serializers.CharField(max_length=16, write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)
    role = serializers.SerializerMethodField()

    @staticmethod
    def get_role(obj):
        user = User.objects.filter(username=obj.get('username')).first()
        admin = Profile.objects.filter(user=user).first()        
        if admin:
            return admin.role
        return None
    

    @staticmethod
    def get_tokens(obj):
        user = User.objects.filter(username=obj.get('username')).first()
        return get_tokens_for_user(user)


    class Meta:
        model = User
        fields = ('username', 'password', 'role', 'tokens')

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        admin = Profile.objects.filter(user=user).first()


        if not user:
            raise AuthenticationFailed({'success': False, 'message': 'User not found'})
        

        data = {
            'success': True,
            'username': user.username,
            'role': admin.role,
            'tokens': get_tokens_for_user(user=user)
        }
        return data


class ClientListSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'


    def get_role(self, obj):
        user_role = Profile.objects.filter(user_id=obj.id).first()
        if user_role is not None:
            return user_role.role
        return None
    
