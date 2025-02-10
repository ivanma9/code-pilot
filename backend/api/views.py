from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SuggestionSerializer, CompositionSerializer
from .models import Suggestion
from django.views.decorators.csrf import csrf_exempt
import logging
from .ai_service import AIService

# Create your views here.

@csrf_exempt
@api_view(['POST'])
def suggestions(request):
    logger = logging.getLogger(__name__)
    logger.info(f"[{__name__}] suggestions request received - Request ID: {id(request)}")
    logger.info(f"[{__name__}] Serializer data: {request.data}")
    serializer = SuggestionSerializer(data=request.data)
    if serializer.is_valid():
        # Save the suggestion to database
        suggestion = serializer.save()
        
        # Create AI service instance and get suggestions
        logger.info(f"[{__name__}] Processing suggestion - Text: {suggestion.text}, Context: {suggestion.context}, Language: {suggestion.language}")
        ai_service = AIService()
        ai_suggestions = ai_service.generate_suggestions(
            text=suggestion.text,
            context=suggestion.context,
            language=suggestion.language
        )
        
        # Save these AI suggestions to database
        for ai_suggestion in ai_suggestions.get("suggestions", []):
            Suggestion.objects.create(
                text=ai_suggestion["text"],
                context=suggestion.context,
                language=suggestion.language
            )
            
        return Response(ai_suggestions)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def composer(request):
    serializer = CompositionSerializer(data=request.data)
    if serializer.is_valid():
        # Save the composition request
        composition = serializer.save()
        
        # Generate AI response
        ai_response = "AI generated response based on the input"
        
        # Update the composition with the response
        composition.response = ai_response
        composition.save()
        
        return Response({"response": ai_response})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
