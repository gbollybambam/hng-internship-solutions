from rest_framework import serializers
from .models import AnalyzedString

class AnalyzedStringSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()
    id = serializers.CharField(source='pk', read_only=True)

    class Meta:
        model = AnalyzedString
        fields = ['id', 'value', 'properties', 'created_at']

    def get_properties(self, obj):
        return {
            "length": obj.length,
            "is_palindrome": obj.is_palindrome,
            "unique_characters": obj.unique_characters,
            "word_count": obj.word_count,
            "sha256_hash": obj.id,
            "character_frequency_map": obj.character_frequency_map,
        }
    
class StringValueSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=5000)