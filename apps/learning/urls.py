# ---------- IMPORTS --------------
from django.urls import path

# -------- VIEWS --------
from .views import (
    LanguagesListApi, 
    LanguageExercisesListApi, 
    ExerciseDetailApi
)

app_name = "learning"

urlpatterns = [
    # GET: Shows minimal data about language 
    path("learn/languages", 
         LanguagesListApi.as_view(), 
         name="languages-list"),
    
    # GET: Shows list of exercises dedicated to a language
    path("learn/languages/<str:language_slug>/exercises", 
         LanguageExercisesListApi.as_view(), 
         name="exercises-list"),
    
    # GET: Shows details for specific excerise in specific language
    path(
        "learn/languages/<str:language_slug>/exercises/<str:exercise_id>",
        ExerciseDetailApi.as_view(),
        name="exercise-detail",
    ),
]
