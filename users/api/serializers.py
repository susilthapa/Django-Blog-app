from django.contrib.auth import get_user_model

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
