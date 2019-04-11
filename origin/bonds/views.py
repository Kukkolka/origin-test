from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import generics
from .models import Bonds
from .serializers import BondSerializer
from .permissions import UserIsOwnerBond
import pdb

class GetBond(ListCreateAPIView):
    serializer_class = BondSerializer
    model = Bonds
    permission_classes = (IsAuthenticated, UserIsOwnerBond)

    def get_queryset(self):
        return Bonds.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        new_bond = self.model(**serializer.validated_data)
        new_bond.user = self.request.user
        new_bond.apply_legal_name()
        new_bond.save()
