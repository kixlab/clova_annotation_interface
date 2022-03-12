import csv
from api.models import *
from django.db.models import Count

doctype=DocType.objects.get(doctype='event')

SimScore.objects.filter(doctype=doctype).delete()
FinalSuggestion.objects.filter(subcat__initcat__doctype=doctype).delete()
GroupedAnnotation.objects.filter(document__doctype=doctype).delete()

print("is_similar clicked", len(Similarity.objects.filter(mine__annotation__document__doctype=doctype, is_similar=True)))

for similarity in Similarity.objects.filter(mine__annotation__document__doctype=doctype):
    user=similarity.user
    profile=Profile.objects.get(user=user)
    mine=similarity.mine
    others=similarity.others
    mysuggestion=mine.suggestion
    othersuggestion=others.suggestion
    if(mysuggestion is not othersuggestion):
        if(mine.annotation.is_alive and others.annotation.is_alive):
            if(mysuggestion.pk<othersuggestion.pk):
                first_sugg=mysuggestion
                second_sugg=othersuggestion
            else:
                first_sugg=othersuggestion
                second_sugg=mysuggestion
            if(len(SimScore.objects.filter(doctype=doctype,first_sugg=first_sugg, second_sugg=second_sugg))==0):
                if(similarity.is_similar):
                    SimScore(doctype=doctype, first_sugg=first_sugg, second_sugg=second_sugg, similar=1, not_similar=0).save()
                else:
                    SimScore(doctype=doctype, first_sugg=first_sugg, second_sugg=second_sugg, similar=0, not_similar=1).save()
            else: #existing pair
                simScore=SimScore.objects.get(doctype=doctype, first_sugg=first_sugg, second_sugg=second_sugg)
                if(similarity.is_similar):
                    simScore.similar=simScore.similar+1
                    if(simScore.similar>=2): # and (simScore.not_similar==0 or simScore.similar/simScore.not_similar>=2)):
                        simScore.is_valid=True
                    else:
                        simScore.is_valid=False
                else:
                    simScore.not_similar=simScore.not_similar+1
                    if(simScore.similar>=2): # and (simScore.not_similar==0 or simScore.similar/simScore.not_similar>=2)):
                        simScore.is_valid=True 
                    else:
                        simScore.is_valid=False
                simScore.save()

print("valid sim score",len(SimScore.objects.filter(doctype=doctype, is_valid=True)))
candsuggs=[ sugg for sugg in UserSuggestion.objects.filter(subcat__initcat__doctype=doctype)]
while len(candsuggs)>0:
    cursugg=candsuggs[0] #snowball
    members=[]
    new_members=[cursugg]
    while(len(members) < len(new_members)): 
        members=new_members
        right_simscores=[]
        left_simscores=[]
        for sugg in members: 
            right_simscores=right_simscores+[score for score in SimScore.objects.filter(doctype=doctype,first_sugg=sugg, is_valid=True)]
        right_matches=list(set([simscore.second_sugg for simscore in right_simscores]))
        for sugg in members: 
            left_simscores=left_simscores+[score for score in SimScore.objects.filter(doctype=doctype,second_sugg=sugg, is_valid=True)]
        left_matches=list(set([simscore.first_sugg for simscore in left_simscores]))
        new_members=list(set(members+left_matches+right_matches))
    count=0
    maxmem=new_members[0]
    for mem in new_members:
        new_count=len(SelectedSuggestion.objects.filter(suggestion=mem))
        if(new_count>count):
            count=new_count
            maxmem=mem
    thisFS=FinalSuggestion(subcat=maxmem.subcat, suggested_subcat=maxmem.suggested_subcat)
    thisFS.save()
    for member in members: 
        selections=SelectedSuggestion.objects.filter(suggestion=member, annotation__is_alive=True)
        for selection in selections: 
            if(selection.annotation.subcat.subcat_text=='n/a'):
                annot_type='n/a'
            else:
                annot_type='ct'
            GroupedAnnotation(user=selection.user, document=selection.annotation.document, 
            boxes_id=selection.annotation.boxes_id, annot_type=annot_type, final_suggestion=thisFS, 
            reason=selection.reason, subcat=selection.suggestion.subcat).save()
    candsuggs=[sugg for sugg in candsuggs if sugg not in members]