from django.urls import path, include
from . import views

urlpatterns = [
    # path(r'image/', views.selectedImage),
    # path(r'image/box_info/', views.selectedImageBox)
    path('signup/',views.signup),
    #path('start-task/', views.startTask),
    path('get-cats/',views.getCats),

    path('get-raw-distribution/', views.getRawDistribution),
    path('get-curr-distribution/', views.getCurrDistribution),

    path('get-na-suggestions/', views.getNASuggestions),
    path('get-closeto-suggestions/', views.getCloseToSuggestions),

    path('save-na-approve/', views.saveNAApprove),
    path('save-na-new/', views.saveNANew),
    path('save-na-existing/', views.saveNAExisting),

    path('save-close-to-approve/', views.saveCloseToApprove),
    path('save-close-to-new/', views.saveCloseToNew),
    path('save-close-to-ignore/', views.saveCloseToIgnore),
]