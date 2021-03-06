from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .models import *

import string
import random
import json
from datetime import datetime, timedelta
from django.db.models import Max, Count, Q


n_documents=800
workers_per_image=5
images_per_worker=20

window = images_per_worker / workers_per_image 
n_annotators=n_documents/window # now = 50 
workers_per_group=images_per_worker/window # 20 / 4 = 5


@csrf_exempt
@api_view(['POST','GET'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data['mturk_id']
    password = username
    if len(User.objects.filter(username=username))==0:
        new_user=User(username=username, password=password)
        new_user.save()
        login(request, new_user)        
        response = {
            'step': 'new',
            'doctype': 'event',
            'username': username
        }
    else: # if already signed up 
        user=User.objects.get(username=username)
        profile=Profile.objects.get(user=user)
        if (profile.annotation_done):
        
            username_new = username + "-#" + str(len(User.objects.filter(username__contains=username.split("-#")[0])))
            password = username_new

            new_user=User(username=username_new, password=password)
            new_user.save()
            login(request, new_user)        
            response = {
                'step': 'new',
                'doctype': 'event',
                'username': username_new,
                'new_user': 'yes'
            }
        elif not profile.consent_agreed:
            step='consent'
            response = {
                'step': step,
                'doctype':profile.doctype.doctype,
                'username': username
            } 
        else:
            if(not profile.practice_done):
                step='instruction'
            else:
                step='annotation'
            response = {
                'step': step,
                'doctype':profile.doctype.doctype,
                'username': username
            } 
    return JsonResponse(response)
    
@csrf_exempt
def startTask(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        username = query_json['mturk_id']
        user = User.objects.get(username=username)
        recordPracticeDone(user)
        
        profile=Profile.objects.get(user=user)
        if(len(Status.objects.filter(user=user))==0):
        # assign task by assigning start image number 
        ## get smallest available user_order 
        # check if there is a user order taken but not completed
            remaining_dropouts=Profile.objects.filter(practice_done=True, doctype=profile.doctype, done=False, practice_endtime=(datetime.now()-timedelta(hours=1, minutes=50)), dropout=False)
            
            if(len(remaining_dropouts)==0):
                active_profiles=Profile.objects.filter(practice_done=True,doctype=profile.doctype, dropout=False)
                if(len(active_profiles)==0):
                    order=0
                else:
                    last_order= active_profiles.order_by('-user_order')[0].user_order  #aggregate(Max('user_order'))
                    order=last_order+1 
            else:
                # drop out exist, take those in dropout list
                dropout=remaining_dropouts[0]
                dropout.dropout = True
                # remove this profile from dropout list 
                dropout.save()
                order=dropout.user_order

            profile.starttime=datetime.now()
            profile.user_order=order
            mod_order = (order % n_annotators)
            profile.mod_order=mod_order        
            profile.save()

            if(mod_order<=(n_annotators-workers_per_group)): # now: 50 -5 = 45 --> 45*4 ~ 45*4 + 20
                # assign documents 
                documents=Document.objects.filter(doctype=profile.doctype, doc_no__gte=(mod_order*window), doc_no__lt=(mod_order*window+images_per_worker))
                
            else: 
                # assign documents 
                end_docs=Document.objects.filter(doctype=profile.doctype, doc_no__gte=mod_order*window) # now: 184: 188: 192: 196:  
                start_docs=Document.objects.filter(doctype=profile.doctype, doc_no__lt=int((workers_per_group - (n_annotators-mod_order))*window)) # 46 --> 4*(5-(50-46)), 49 --> 4*(5-(50-49)) 
                documents=start_docs + end_docs 
    
            # initialize status 
            for document in documents:
                Status(user=user, document=document, status=False).save()
        else: 
            statuses=Status.objects.filter(user=user)
            documents=[status.document for status in statuses]

        response={
            'assigned_images': [doc.doc_no for doc in documents]
        }
        return JsonResponse(response)

@csrf_exempt
def consentAgreed(request):
    if request.method =='POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        user = User.objects.get(username=username)
        recordConsentAgreed(user)
        return HttpResponse('')

@csrf_exempt
def instructionRead(request):
    if request.method =='POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        user = User.objects.get(username=username)
        recordInstructionDone(user)
        return HttpResponse('')

@csrf_exempt
def annotationDone(request):
    if request.method =='POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        user = User.objects.get(username=username)
        recordAnnotationDone(user)
        return HttpResponse('')

@csrf_exempt
def reviewDone(request):
    if request.method =='POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        user = User.objects.get(username=username)
        recordReviewDone(user)
        return HttpResponse('')

@csrf_exempt
def submitSurvey(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        username = query_json['mturk_id']
        user = User.objects.get(username=username)
        recordSurveyDone(user)
        
        profile=Profile.objects.get(user=user)
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        profile.token=token
        profile.done=True
        profile.save()

        response={
            'token': token
        }
        return JsonResponse(response)

def recordConsentAgreed(user):
    profile=Profile.objects.get(user=user)
    profile.consent_agreed=True
    profile.save()

def recordInstructionDone(user):
    profile=Profile.objects.get(user=user)
    profile.instr_done=True
    profile.practice_starttime=datetime.now()
    profile.save()

def recordPracticeDone(user):
    profile=Profile.objects.get(user=user)
    profile.practice_done=True
    profile.practice_endtime=datetime.now()
    profile.save()

def recordAnnotationDone(user):
    profile=Profile.objects.get(user=user)
    profile.annotation_done=True
    profile.annot_endtime=datetime.now()
    profile.save()

def recordReviewDone(user):
    profile=Profile.objects.get(user=user)
    profile.review_done=True
    profile.review_endtime=datetime.now()
    profile.save()

def recordSurveyDone(user):
    profile=Profile.objects.get(user=user)
    profile.survey_done=True
    profile.survey_endtime=datetime.now()
    profile.save()

@csrf_exempt
def getImageID(request):
    if request.method == 'GET':
        username = request.GET['mturk_id']        
        user = User.objects.get(username=username)
        profile=Profile.objects.get(user=user)

        #get least unannotated document
        startdoc=Status.objects.filter(user=user, document__doctype=profile.doctype)[0]
        startno=startdoc.document.doc_no
        response = {
            
        }
        return JsonResponse(response)

@csrf_exempt
def getCats(request):
    if request.method == 'GET':
        username = request.GET['mturk_id']
        user = User.objects.get(username=username)
        profile=Profile.objects.get(user=user)
        initcats=InitCat.objects.filter(doctype=profile.doctype)
        subcats=[]
        cats=[]
        for cat in initcats:
            cats.append({'cat': cat.cat_text, 'pk': cat.pk})
            for subcat in InitSubCat.objects.filter(initcat=cat):
                subcats.append({'cat': subcat.initcat.cat_text, 'subcat':subcat.subcat_text, 'description':subcat.subcat_description, 'pk':subcat.pk, 'catpk':subcat.initcat.pk, 'suggestion': False})
        response = {
            'cats': cats,
            'subcats': subcats
        }
        return JsonResponse(response)

@csrf_exempt
def getAnnotations(request):
    if request.method=='GET':
        username = request.GET['mturk_id']
        user = User.objects.get(username=username)
        #user=request.user
        doctypetext=request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        image_id =request.GET['image_id']
        document=Document.objects.get(doctype=doctype, doc_no=int(image_id))
        annots=Annotation.objects.filter(user=user, document=document,is_alive=True)
        
        annotations=[]
        for annot in annots: 
            thisSuggestion= SelectedSuggestion.objects.filter(user=user, annotation=annot)
            suggestion=''
            if(len(thisSuggestion)>0):
                suggestion=thisSuggestion[0].suggestion.suggested_subcat
            if(annot.subcat==None):
                annotations.append({'group_id':annot.pk, 'boxes_id': annot.boxes_id, 'cat': annot.cat.cat_text, 'subcat':None, 'subcatpk': None, 'catpk':annot.cat.pk, 'confidence': None, 'suggestion': suggestion})
            else:
                if(annot.subcat.subcat_text=="N/A"):
                    annotations.append({'group_id':annot.pk, 'boxes_id': annot.boxes_id, 'cat': annot.cat.cat_text, 'subcat':annot.subcat.subcat_text, 'subcatpk':annot.subcat.pk, 'catpk':annot.cat.pk, 'confidence': None,  'suggestion': suggestion})
                else:
                    annotations.append({'group_id':annot.pk, 'boxes_id': annot.boxes_id, 'cat': annot.cat.cat_text, 'subcat':annot.subcat.subcat_text, 'subcatpk':annot.subcat.pk, 'catpk':annot.cat.pk, 'confidence': annot.confidence,  'suggestion': suggestion})
        response={
            'annotations':annotations
        }
        return JsonResponse(response)


def getSuggestions(request):
    if request.method=='GET':
        username = request.GET['mturk_id']
        user = User.objects.get(username=username)
        #user=request.user
        doctypetext=request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)

        subcatpk=request.GET['subcatpk']
        subcat=InitSubCat.objects.get(pk=subcatpk)

        candSuggestions=UserSuggestion.objects.annotate(nselection=Count('selectedsuggestion')).filter(subcat=subcat, nselection__gte=1).order_by('-nselection')

        mysuggestions=[]
        othersuggestions=[]
        for sug in candSuggestions:
            thisSelection = SelectedSuggestion.objects.filter(suggestion=sug, user=user)
            if(len(thisSelection)>0):
                mysuggestions.append(sug)
            else:
                othersuggestions.append(sug)

        response={
            'mysuggestions': [i.suggested_subcat for i in mysuggestions],
            'othersuggestions': [i.suggested_subcat for i in othersuggestions]
        }

        return JsonResponse(response)

@csrf_exempt
def saveAnnotation(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        user = User.objects.get(username=username)
        #user=request.user
        profile=Profile.objects.get(user=user)
        image_id =query_json['image_id']
        document=Document.objects.get(doctype=profile.doctype, doc_no=int(image_id))
        boxes = query_json['boxes_id']
        subcatpk = query_json['subcatpk']
        catpk = query_json['catpk']
        confidence=query_json['confidence']
        suggestion=query_json['suggestion']
        reason=query_json['reason']

        thisSubcat=InitSubCat.objects.get(pk=subcatpk)
        thisCat=InitCat.objects.get(pk=catpk)

        if(thisSubcat.subcat_text=='n/a'):
            newAnnot=Annotation(user=user, document=document, boxes_id = boxes, cat=thisCat, subcat=thisSubcat, confidence=False, is_alive=True)
        else:
            newAnnot=Annotation(user=user, document=document, boxes_id = boxes, cat=thisCat, subcat=thisSubcat, confidence=confidence, is_alive=True)
        newAnnot.save()

        if(confidence!=1):
            thisSuggestions=UserSuggestion.objects.filter(subcat=thisSubcat, suggested_subcat=suggestion)
            if(len(thisSuggestions)==0): # new suggestion
                newSuggestion = UserSuggestion(user=user, subcat=thisSubcat, suggested_subcat=suggestion)
                newSuggestion.save()
                # add selection count 
                newSelection = SelectedSuggestion(suggestion=newSuggestion, user=user, annotation=newAnnot, reason=reason)
                newSelection.save()
            else: #existing suggestion 
                thisSuggestion=thisSuggestions[0]
                newSelection = SelectedSuggestion(suggestion=thisSuggestion, user=user, annotation=newAnnot, reason=reason)
                newSelection.save()
        response={
            'annot_pk': newAnnot.pk
        }
        return JsonResponse(response)

@csrf_exempt
def deleteAnnotation(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        user = User.objects.get(username=username)
        #user=request.user
        doctypetext=query_json['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        image_id =query_json['image_id']
        document=Document.objects.get(doctype=doctype, doc_no=int(image_id))
        annot_pk = query_json['annot_pk']
        thisAnnot=Annotation.objects.get(user=user, pk=annot_pk)
        thisAnnot.is_alive=False
        thisAnnot.save()
        response={
            'annot_pk': annot_pk
        }
        return JsonResponse(response)

@csrf_exempt
def deleteAllAnnotations(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        user = User.objects.get(username=username)
        #user=request.user
        doctypetext=query_json['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        image_id =query_json['image_id']
        document=Document.objects.get(doctype=doctype, doc_no=int(image_id))

        thisAnnots=Annotation.objects.filter(user=user, document=document)
        for annot in thisAnnots: 
            annot.is_alive=False 
            annot.save()
        return HttpResponse('')

@csrf_exempt
def saveMemo(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        user = User.objects.get(username=username)
        doctypetext=query_json['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        memo_text=query_json['memo']
        my_memos=Memo.objects.filter(user=user, doctype=doctype)
        if(len(my_memos)==0):
            new_memo=Memo(user=user, doctype=doctype, text=memo_text)
            new_memo.save()
        else: 
            my_memo=my_memos[0]
            my_memo.text=memo_text 
            my_memo.save()
        return HttpResponse('')


def getMemo(request):
    if request.method=='GET':
        username = request.GET['mturk_id']
        user = User.objects.get(username=username)
        doctypetext=request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        my_memos=Memo.objects.filter(user=user, doctype=doctype)
        if(len(my_memos)==0):
            return JsonResponse({
                'memo': ''
            })
        else:
            return JsonResponse({
                'memo': my_memos[0].text
            })

def assignRandomSuggestions(user, thisSuggestion): # assume that we have enough issue pull to choose from
    thisSubCat=thisSuggestion.subcat
    thisCat=thisSubCat.initcat
    suggestions=[]
    
    selections_samesubcat=list(SelectedSuggestion.objects.filter(~Q(user=user), annotation__subcat=thisSubCat))
    if(len(selections_samesubcat)>=2):
        rand_selections_samesubcat = random.sample(selections_samesubcat,2)
        suggestions=rand_selections_samesubcat
    else: 
        suggestions=selections_samesubcat
    
    selections_samecat=list(SelectedSuggestion.objects.filter((~Q(user=user)&~Q(annotation__subcat=thisSubCat)), annotation__subcat__initcat=thisCat))
    if(len(selections_samecat)>=2):
        rand_selections_samecat=random.sample(selections_samecat, 2)
        suggestions = suggestions+rand_selections_samecat
    else:
        suggestions=suggestions+selections_samecat

    n_needed=6-len(suggestions)
    selections_othercat=list(SelectedSuggestion.objects.filter((~Q(user=user)&~Q(annotation__subcat__initcat=thisCat))))
    if(len(selections_othercat)>=n_needed):
        rand_selections_othercat = random.sample(selections_othercat, n_needed)
        suggestions=suggestions + rand_selections_othercat
    else:
        suggestions=suggestions + rand_selections_othercat 
    
    assigned_suggestions=[]
    for suggestion in suggestions: 
        newAssignedSuggestion=AssignedSuggestion(user=user, my_suggestion=thisSuggestion, others=suggestion, is_reviewed=False)
        newAssignedSuggestion.save()
        assigned_suggestions.append(newAssignedSuggestion)
    
    return assigned_suggestions

def getSuggestionsToReview(user, doctype, thisSuggestion):
    assigned_suggestions=AssignedSuggestion.objects.filter(user=user, my_suggestion=thisSuggestion)
    if(len(assigned_suggestions)>0):
        unreviewed_suggestions=assigned_suggestions.filter(is_reviewed=False)
    else:
        unreviewed_suggestions=assignRandomSuggestions(user, thisSuggestion)
    return unreviewed_suggestions

def checkIfEnoughSuggestions(user):
    others_suggestions=list(SelectedSuggestion.objects.filter(~Q(user=user)))
    if(len(others_suggestions)>11):
        response=True
    else: 
        response=False
    return response

def getIssuesWithRandomSuggestions(user, doctype):
    mySelections=SelectedSuggestion.objects.filter(user=user)
    mySuggestions=list(set([selection.suggestion for selection in mySelections]))
    
    response=[]
    for suggestion in mySuggestions:
        # get my annotation with this suggestion 
        mySelections=SelectedSuggestion.objects.filter(user=user, suggestion=suggestion)
        mine=[]
        for myselection in mySelections: 
            mine.append({'image_no': myselection.annotation.document.doc_no, 'boxes_id': myselection.annotation.boxes_id, 'reason': myselection.reason, 'issue_pk': myselection.pk})
            
        assignedSuggestions=getSuggestionsToReview(user, doctype, suggestion)
        others=[]
        for assignment in assignedSuggestions:
            others.append({'image_no': assignment.others.annotation.document.doc_no, 'boxes_id': assignment.others.annotation.boxes_id, 'reason': assignment.others.reason, 'worker': assignment.others.user.username, 'issue_pk': assignment.others.pk})

        response.append({
            'suggestion_pk': suggestion.pk, 'suggestion_cat': suggestion.subcat.initcat.cat_text, 'suggestion_subcat': suggestion.subcat.subcat_text, 'suggestion_text': suggestion.suggested_subcat, 'n_issues': len(list(mySelections)), 'mine':mine, 'others':others
        })
    return response

@csrf_exempt
def getRandomSuggestionsToReview(request):
    if request.method=='GET':
        doctypetext=request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        username = request.GET['mturk_id']
        user = User.objects.get(username=username)
        if(checkIfEnoughSuggestions(user)):
            status=True
            suggestions=getIssuesWithRandomSuggestions(user, doctype)
        else:
            status=False
            suggestions=[]
        # get my suggestions           
        return JsonResponse({
            'status': status,
            'suggestions': suggestions
        })
@csrf_exempt
def saveSimilarity(request):
    if(request.method=='POST'):
        query_json = json.loads(request.body)
        username = query_json['mturk_id']
        doctype=query_json['doctype']
        suggestion_pk=query_json['suggestion_pk']
        my_issue_pks=query_json['my_issue_pks']
        other_issue_pk=query_json['other_issue_pk']
        similarity=query_json['similarity']

        try: 
            user = User.objects.get(username=username)
            suggestion=UserSuggestion.objects.get(pk=suggestion_pk)
            others=SelectedSuggestion.objects.get(pk=other_issue_pk)
        
            # save pairwise similarity
            for my_issue_pk in my_issue_pks:
                mine=SelectedSuggestion.objects.get(pk=my_issue_pk)
                others=SelectedSuggestion.objects.get(pk=other_issue_pk)
                newSimilarity=Similarity(user=user, mine=mine, others=others, is_similar=similarity)
                newSimilarity.save()

            # mark assigned suggestion as reviewed 
            thisAssignment=AssignedSuggestion.objects.get(user=user, my_suggestion=suggestion, others=others)
            thisAssignment.is_reviewed=True
            thisAssignment.save()

            return JsonResponse(
                {'result': True}
            )
        except: 
            return JsonResponse({
                'result': False
            })

@csrf_exempt
def updateStatus(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        #user=request.user
        username = query_json['mturk_id']
        user = User.objects.get(username=username)
        profile=Profile.objects.get(user=user)
        image_id = query_json['image_id']
        status= query_json['status']
        doctype=profile.doctype

        document=Document.objects.get(doctype=doctype, doc_no=int(image_id))
        user = User.objects.get(username=username)
        if(status):
            Status.objects.filter(user=user, document=document).update(status=True)
        else:
            Status.objects.filter(user=user, document=document).update(status=False)
        return HttpResponse('')

@csrf_exempt
def getStatus(request):
    if request.method=='GET':
        username = request.GET['mturk_id']
        user = User.objects.get(username=username)
        profile=Profile.objects.get(user=user)
        status=Status.objects.filter(user=user).values_list('status', flat=True)
        return JsonResponse({'status': list(status)})
