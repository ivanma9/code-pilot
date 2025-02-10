from rest_framework import serializers
from .models import Suggestion, Composition

class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = ['text', 'context', 'language']

class CompositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composition
        fields = ['message', 'context', 'code', 'response', 'language']