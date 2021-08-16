from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/',views.signup),
    # path('check-user/', views.checkUser),

    path('consent-agreed/', views.consentAgreed),
    path('instruction-read/', views.instructionRead),
    path('practice-done/', views.startTask),
    path('annotation-done/', views.annotationDone),
    path('review-done/', views.reviewDone),
    path('submit-survey/', views.submitSurvey),

    path('get-cats/',views.getCats),

    path('get-suggestions/', views.getSuggestions),

    path('get-image-id/', views.getImageID),

    path('get-annotations/',views.getAnnotations),
    path('save-annotation/', views.saveAnnotation),
    path('delete-annotation/', views.deleteAnnotation),
    path('delete-all-annotations/', views.deleteAllAnnotations),

    path('update-status/', views.updateStatus),
    path('get-status/', views.getStatus),


    path('get-random-suggestions-to-review/', views.getRandomSuggestionsToReview),
    path('save-similarity/', views.saveSimilarity),
]