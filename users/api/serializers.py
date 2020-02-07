from django.contrib.auth import get_user_model
from django.db.models import Q
from users.models import Profile

from rest_framework.serializers import (
    CharField,
    EmailField,
    ValidationError,
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class UserCreateSerializer(ModelSerializer):
    password2 = CharField(label='Confirm Password', write_only=True)
    email = EmailField(label='Email Address', validators=[UniqueValidator(queryset=User.objects.all())])  # also place required when not inserted email instead of blank by default

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
        ]
        extra_kwargs = {
                        'password': {'write_only': True}
                        }

    # def validate(self, data):
    #     email = data['email']
    #     user_qs = User.objects.filter(email=email)
    #     if user_qs.exists():
    #         raise ValidationError("User with this email already exists!")

    def validate_password(self, value):
        data = self.get_initial()
        # print(f"INITIAL VALUE = {value}")
        password1 = data.get("password2")
        email = data.get('email')
        # print(f"Password 2 = {password1}")
        password2 = value
        if password1 != password2:
            raise ValidationError("Password must match!")
        return value

    def validate_password2(self, value):  # two validation function because for two password fields to show error
        data = self.get_initial()
        print(f"INITIAL VALUE = {value}")
        password1 = data.get("password")
        password2 = value
        print(value)
        if password1 != password2:
            raise ValidationError("Password must match!")
        return value

    def create(self, validated_data):
        # print(validated_data)
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(read_only=True, allow_blank=True)
    username = CharField(required=False, allow_blank=True)
    email = EmailField(label='Email Address', required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',
        ]
        extra_kwargs = {
                        'password': {'write_only': True}
                        }

    def validate(self, data):
        user_obj = None
        email = data.get('email')  # if email is not entered 'None' will be as default
        username = data.get('username')
        password = data.get('password')
        if not email and not username:
            raise ValidationError("A username or email is required to login")
        user = User.objects.filter(
            Q(username=username) |
            Q(email=email)
        ).distinct()  # if there two of them then get one of them
        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        print(user)
        if user.exists() and user.count() == 1:
            user_obj = user.first()  # ??
            # print(f'User OBJECT ={user_obj}')
        else:
            raise ValidationError("This username/email is not valid")

        if user_obj:
            if not user_obj.check_password(password): # checks whether password is correct or if password key is not there
                raise ValidationError('Incorrect Credentials please try again!')
        data["token"] = "SOME RANDOM TOKEN"
        return data


class UserProfileUpdateSerializer(ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = Profile
        fields = [
            'image',
            'user',
        ]


