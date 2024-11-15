from rest_framework import serializers
from .models import Book
import re

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        # Mark creation_date as read-only
        read_only_fields = ['creation_date', 'user']  


    def validate_isbn(self, value):
        # Regex that check if the value is only 10 or 13 integer long
        if value and not re.match(r'^\d{10}(\d{3})?$', value):  
            raise serializers.ValidationError("ISBN must be a 10 or 13 digit integer")
        return value
