from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/',views.signup),
    path('check-user/', views.checkUser),

    path('consent-agreed/', views.consentAgreed),
    path('instruction-read/', views.instructionRead),
    path('practice-done/', views.startTask),
    #views.startTask),

    path('get-doctypes/', views.getDocTypes),
    path('get-cats/',views.getCats),

    path('get-suggestions/', views.getSuggestions),
   # path('save-suggestion/', views.saveSuggestions),


    path('add-cat/', views.addCat),
    path('add-subcat/', views.addSubcat),

    path('get-image-id/', views.getImageID),

    path('get-annotations/',views.getAnnotations),
    path('save-annotation/', views.saveAnnotation),
    path('delete-annotation/', views.deleteAnnotation),
    path('delete-all-annotations/', views.deleteAllAnnotations),

    path('update-status/', views.updateStatus),
    path('get-status/', views.getStatus),

    path('record-annotation-done/', views.recordAnnotationDone),

 #   path('get-suggestions-to-review/', views.getSuggestionsToReview),
 #   path('get-issues-with-random-suggestions/', views.getIssuesWithRandomSuggestions),

    path('get-random-suggestions-to-review/', views.getRandomSuggestionsToReview),
#    path('get-unreviewed-issues/', views.getUnreviewedIssues),
    path('save-similarity/', views.saveSimilarity),

    path('submit/', views.submit),
    path('submit-survey/', views.submitSurvey),


    path('get-annotations-by-image', views.getAnnotationsByImage),
    path('get-workers', views.getWorkers),
    path('get-every-annotations', views.getEveryAnnotations),
    path('get-annotations-by-worker', views.getAnnotationsByWorker),
    path(r'image/<image_id>/', views.getImage, name='image_id'),
    path(r'upload_image/', views.uploadImage),
    path(r'json/<json_id>/', views.getJson, name='json_id'),
    path(r'upload_json/', views.uploadJson),
]