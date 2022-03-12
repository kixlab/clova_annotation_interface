from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/',views.signup),
    path('get-cats/',views.getCats),
    path('get-final-cats/',views.getFinalCats),


    path('get-raw-distribution/', views.getRawDistribution),
    path('get-curr-distribution/', views.getCurrDistribution),

    path('get-na-suggestions/', views.getNASuggestions),
    path('get-closeto-suggestions/', views.getCloseToSuggestions),

    path('save-na-approve/', views.saveNAApprove),
    path('save-na-new/', views.saveNANew),
    path('save-na-existing/', views.saveNAExisting),
    path('save-na-ignore/', views.saveNAIgnore),

    path('save-close-to-approve/', views.saveCloseToApprove),
    path('save-close-to-new/', views.saveCloseToNew),
    path('save-close-to-existing/', views.saveCloseToExisting),
    path('save-close-to-ignore/', views.saveCloseToIgnore),

    path('change-cat-text/', views.changeCatText),
    path('change-subcat-text/', views.changeSubCatText),
    path('change-subcat-description/', views.changeSubCatDescription),
    path('move-subcat/', views.moveSubCat),
    path('get-all-memo/', views.getMemo),

    path('get-examples/', views.getExamples),
    
    path('add-cat/', views.addCat),
    path('merge-cats/', views.mergeCats),
    path('merge-subcats/', views.mergeSubCats)

]