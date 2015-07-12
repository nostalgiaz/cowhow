import braintree

from django.contrib.auth import get_user_model
from django.views.generic import DetailView

from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework.views import APIView

from .serializers import (
    UserSerializer, CreditCardSerializer, AddCreditCardSerializer, MerchantAccountSerializer
)


class UserProfile(DetailView):
    model = get_user_model()
    template_name = 'account/profile.html'


class MeView(generics.RetrieveUpdateDestroyAPIView):
    model = get_user_model()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class TokenView(APIView):
    def get(self, request):
        return Response({
            'token': braintree.ClientToken.generate()
        })


class MerchantViewSet(viewsets.ViewSet):
    # def list(self, request):
    #     pass

    def create(self, request):
        user = request.user

        serializer = MerchantAccountSerializer(data=request.DATA)

        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        return Response(status=status.HTTP_201_CREATED)


class MeCreditCardsViewSet(viewsets.ViewSet):
    def list(self, request):
        credit_cards = request.user.get_credit_cards()

        serializer = CreditCardSerializer(credit_cards, many=True)

        return Response(serializer.data)

    def create(self, request):
        user = request.user

        serializer = AddCreditCardSerializer(data=request.DATA)

        serializer.is_valid(raise_exception=True)
        result = serializer.save(user=user)

        serializer = CreditCardSerializer(result)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
