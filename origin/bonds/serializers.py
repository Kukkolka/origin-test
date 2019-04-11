from rest_framework import serializers
from .models import Bonds


class BondSerializer(serializers.ModelSerializer):
    legal_name = serializers.CharField(read_only=True)
    class Meta:
        model = Bonds
        fields = ("isin", "size", "currency", "maturity", "lei","legal_name")
