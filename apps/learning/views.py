# ----------- IMPORTS -------------
from django.shortcuts import render
from pathlib import Path
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.responses import success_response, error_response

# ------ SERIALIZERS --------
from .serializers import (
    LanguageOutSerializer,
    ExerciseListOutSerializer,
    ExerciseDetailOutSerializer,
)

import json

# ------------ HELPERS (Private functions) --------------

# ----- HELPER 1: Load the json content ------
def _load_learning_content() -> dict:
    """
    Reads and parses the learning content from a local JSON file.

    Returns:
        dict: The full dictionary containing all languages and exercises.
    """
    # Resolve the path of the JSON file
    base_dir = Path(__file__).resolve().parent
    path = base_dir / "learning_content.json"

    # Open and load the json content
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
    
# ----- HELPER 2: Get the language object from the JSON  ------
def _get_language(content: dict, language_slug: str) -> dict | None:
    """
    Searches for a specific language dictionary within the loaded content.

    Args:
        content (dict): The full learning content dictionary.
        language_slug (str): The unique string identifier for the language (e.g., 'python').

    Returns:
        dict | None: The language dictionary if found, otherwise None.
    """
    for lang in content.get("languages", []):
        if lang.get("slug") == language_slug:
            return lang
    return None

# ----- HELPER 3: Return full exercise details ------
def _get_exercise(language: dict, exercise_id: str) -> dict | None:
    """
    Retrieves a specific exercise from a given language based on its ID.

    Args:
        language (dict): The dictionary representing a specific language.
        exercise_id (str): The unique identifier for the exercise.

    Returns:
        dict | None: The exercise detail dictionary if found, otherwise None.
    """
    for ex in language.get("exercises", []):
        if ex.get("id") == exercise_id:
            return ex
    return None


# ------------- VIEWS --------------

# --- View 1: Get the list of languages ---
class LanguagesListApi(APIView):
    """
    Endpoint: GET /learn/languages
    
    List all available programming languages.

    Returns:
        A list of language objects containing name, slug, and version.
    """
    
    authentication_classes = []
    
    # Override the get method
    def get(self, request):
        content = _load_learning_content()  # Load the content
        languages = content.get("languages", []) # Get the languages object
        
        # Pass the data to the serializer 
        # `many=True` means I am giving you a list of dictionaries. 
        # Please loop through them and apply the serializer rules to each one.
        # `.data` will trigger the actual serialization process
        data = LanguageOutSerializer(languages, many=True).data 
        return success_response(
            data=data, 
            message="Successfully retrieved the list of supported languages."
        )
        
# --- View 2: Get the list of exercises for specific langauge---
class LanguageExercisesListApi(APIView):
    """
    Endpoint: GET /learn/languages/{language_slug}/exercises
    
    Retrieve all exercises for a specific language slug.
    """
    
    authentication_classes = []
        
    def get(self, request, language_slug: str):
        content = _load_learning_content() # Load the content
        language = _get_language(content, language_slug) # Get teh specified language object

        # In case no language was found
        if not language:
            return error_response(
                message=f"Language '{language_slug}' was not found.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        # Get the list of excerises dedicated for the specified language
        exercises = language.get("exercises", [])
        # Return list-only shape (id/title/difficulty)
        data = ExerciseListOutSerializer(exercises, many=True).data # Call the serializer
        
        # Return the list of language's excerises
        return success_response(
            data=data, 
            message=f"Successfully retrieved all exercises for {language_slug.capitalize()}."
        )
        
# --- View 3: Get details for single exercise ---
class ExerciseDetailApi(APIView):
    """
    Endpoint: GET /learn/languages/{language_slug}/exercises/{exercise_id}
    
    Retrieve specific details for a single exercise.
    """
    authentication_classes = []
    
    def get(self, request, language_slug: str, exercise_id: str):
        content = _load_learning_content() # Load the content
        language = _get_language(content, language_slug) 

        # If no language was found
        if not language:
            return error_response(
                message="Language not found.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        # Get the specific exercise details from the JSON
        exercise = _get_exercise(language, exercise_id)
        if not exercise:
            return error_response(
                message=f"Exercise with ID '{exercise_id}' does not exist.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        # Return list-only shape (title, difficulty, prompt, starter_code, hints)
        data = ExerciseDetailOutSerializer(exercise).data
        
        # Specific message for a single object detail
        return success_response(
            data=data, 
            message=f"Exercise '{data.get('title')}' details retrieved successfully."
        )