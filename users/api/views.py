from django.contrib.auth import get_user_model
from users.models import Profile
from django.db.models import Q
from rest_framework.generics import (
    RetrieveAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404
)


from rest_framework.permissions import (
    AllowAny,

)
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

User = get_user_model()

from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
    UserProfileUpdateSerializer,
    # UserProfileCreateSerializer,
)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

# class UserProfileCreateAPIView(CreateAPIView):
#     serializer_class = UserProfileCreateSerializer
#     queryset = Profile.objects.all()
#     permission_classes = [AllowAny]


class UserLoginAOIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        # print(f"DATA= {data}")
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):  # other wise raise exception
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserProfileUpdateAPIView(RetrieveUpdateAPIView):
    # queryset = Profile.objects.all()
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'user_id'

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj

    def get_queryset(self):

        queryset = Profile.objects.filter(user=self.request.user)
        print(f'CURRENT USER= {queryset}')
        return queryset

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

