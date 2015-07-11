from django.contrib.auth import get_user_model
from django.views.generic import DetailView

from rest_framework import generics

from .serializers import UserSerializer


class UserProfile(DetailView):
    model = get_user_model()
    template_name = 'account/profile.html'


class MeView(generics.RetrieveUpdateDestroyAPIView):
    model = get_user_model()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
