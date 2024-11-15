from rest_framework import serializers
from .models import Book
import re

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['creation_date', 'user']  # Mark creation_date as read-only


    def validate_isbn(self, value):
        # Remove "ISBN " prefix if present
        clean_value = value.upper().replace("ISBN ", "").strip() if value else value

        if value and not re.match(r'^\d{10}(\d{3})?$', clean_value):  # Allow 10 or 13 digit ISBN
            raise serializers.ValidationError("ISBN must be either a 10 or 13-digit number.")
        return value
