from django.contrib.auth import get_user_model
from django.views.generic import DetailView

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import UserSerializer, CreditCardSerializer


class UserProfile(DetailView):
    model = get_user_model()
    template_name = 'account/profile.html'


class MeView(generics.RetrieveUpdateDestroyAPIView):
    model = get_user_model()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class MeCreditCardsViewSet(viewsets.ViewSet):
    def list(self, request):
        credit_cards = request.user.get_credit_cards()

        serializer = CreditCardSerializer(credit_cards, many=True)

        return Response(serializer.data)
