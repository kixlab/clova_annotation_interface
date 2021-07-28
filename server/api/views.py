from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions
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
from .serializers import *


n_documents=200
workers_per_image=5
window = 4

n_annotators=n_documents/window # now = 50 
images_per_worker=n_documents*workers_per_image / n_annotators # 200*5 / 50 = 20
workers_per_group=images_per_worker/window # 20 / 4 = 5


@csrf_exempt
@api_view(['POST','GET'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data['username']
    password = username
    if len(User.objects.filter(username=username))==0:
        new_user=User(username=username, password=password)
        new_user.save()
        login(request, new_user)
#        print('logged in?', new_user.is_authenticated)
        
        response = {
            'status': 'new',
            'doctype': 'receipt'
        }
    else: # if already signed up 
        user=User.objects.get(username=username)
        profile=Profile.objects.get(user=user)
        login(request, user)
        response = {
            'status': 'instruction',
            'doctype':profile.doctype.doctype
        }
    return JsonResponse(response)

@csrf_exempt
def startTask(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        username = query_json['mturk_id']
        user = User.objects.get(username=username)
        profile=Profile.objects.get(user=user)
        profile.instr_read = True

        # assign task by assigning start image number 
        ## get smallest available user_order 
        # check if there is a user order taken but not completed

        remaining_dropouts=Profile.objects.filter(instr_read=True, doctype=profile.doctype, done=False, starttime__lte=(datetime.now()-timedelta(hours=1, minutes=50)), dropout=False)
        
        if(len(remaining_dropouts)==0):
            active_profiles=Profile.objects.filter(instr_read=True,doctype=profile.doctype, dropout=False)
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

        print(profile.user_order, profile.mod_order)
        if(mod_order<=(n_annotators-workers_per_group)): # now: 50 -5 = 45 --> 45*4 ~ 45*4 + 20
            # assign documents 
            all_documents=Document.objects.filter(doctype=profile.doctype).order_by('doc_no')
            documents=all_documents[int(mod_order*window):int((mod_order*window+images_per_worker))]
            print('all doc', all_documents)
            print('all doc first 2', all_documents[0:2])
            print('small number', mod_order*window,(mod_order*window+images_per_worker))
        else: 
            # assign documents 
            end_docs=Document.objects.filter(doctype=profile.doctype).order_by('doc_no')[int(mod_order*window):] # now: 184: 188: 192: 196:  
            start_docs=Document.objects.filter(doctype=profile.doctype).order_by('doc_no')[:int((workers_per_group - (n_annotators-mod_order))*window)] # 46 --> 4*(5-(50-46)), 49 --> 4*(5-(50-49)) 
            documents=start_docs + end_docs 
 
        print(documents
        # initialize status 
        for document in documents:
            Status(user=user, document=document, status=False).save()

        response={
            'assigned_images': [doc.doc_no for doc in documents],
            'doctype': profile.doctype.doctype
        }
        return JsonResponse(response)

@csrf_exempt
def checkUser(request):
    if request.method =='GET':
        username = request.GET['mturk_id']
        user = User.objects.get(username=username)
        
        #user=request.user 
        #print('user', user)
        #print('request', request)
        if(user == None):
            response={
                'login_status': False
            }
        else:
            response={
                'login_status': True,
                'username': user.username
            }
        return JsonResponse(response)

        
""" @csrf_exempt
def checkUser(request):
    if request.method == 'GET':
        username = request.GET['mturk_id']
        print(User.objects)
        if(len(User.objects.filter(username=username))==0):
            user=User(username=username)
            user.save()
            # initialize status 
            for document in Document.objects.all():
                Status(user=user, document=document, status=False).save()
            # initialize usercats
            for initcat in InitCat.objects.all():
                usercat=UserCat(user=user, doctype=initcat.doctype, cat_text=initcat.cat_text)
                usercat.save()
            # add N/A category 
            for doctype in DocType.objects.all():
                UserCat(user=user, doctype=doctype, cat_text="N/A").save()
            # initialize usersubcats 
            for initsubcat in InitSubCat.objects.all():
                usercat=UserCat.objects.get(user=user, doctype=initsubcat.initcat.doctype, cat_text=initsubcat.initcat.cat_text)
                UserSubcat(usercat=usercat, subcat_text=initsubcat.subcat_text, subcat_description=initsubcat.subcat_description).save()   
            # add N/A subcategory to each category 
            for usercat in UserCat.objects.filter(user=user):
                UserSubcat(usercat=usercat, subcat_text="N/A", subcat_description="Not applicable or does not exist").save()
        else: 
            user=User.objects.get(username=username)
        user, created = User.objects.get_or_create(username=username)
        response = {
            'consent_agreed': user.consentAgreed,
            'step': 1
        }
        return JsonResponse(response) """

@csrf_exempt
def recordconsentAgreed(request):
    if request.method == 'GET':
        username = request.GET['mturk_id']
        user = User.objects.get(username=username)
        #user=request.user
        profile=Profile.objects.get(user=user)
        profile.consent_agreed=True
        profile.save()
        return HttpResponse('')

""" @csrf_exempt
def recordInstrDone(request):
    if request.method == 'GET':
        username = request.GET['mturk_id']
        user = User.objects.get(username=username)
        #user=request.user
        profile=Profile.objects.get(user=user)
        profile.instr_read=True
        profile.starttime=datetime.now()




        if (user.instrEnded == False):
            valid_usrs = len(list(User.objects.filter(instrEnded = True)))
            user.startTask(valid_usrs)

        return HttpResponse('') """

@csrf_exempt
def getDocTypes(request):
    if request.method == 'GET':
        doctypes=[doctype.doctype for doctype in DocType.objects.all()]
        return JsonResponse({'doctypes':doctypes})


@csrf_exempt
def recordLog(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
#        user=request.user
        username = query_json['mturk_id']
        behavior_type = query_json['type']
        box_ids = query_json['box_ids']
        image_id = query_json['image_id']
        label = query_json['label']

        user = User.objects.get(username=username)

        Log.objects.create(
            user = user,
            behavior = behavior_type,
            boxIDs = box_ids,
            imageID = image_id,
            label = label
        )

        return HttpResponse("")

@csrf_exempt
def getImageID(request):
    if request.method == 'GET':
        username = request.GET['mturk_id']        
        user = User.objects.get(username=username)
        profile=Profile.objects.get(user=user)

        #get least unannotated document
        startdoc=Status.objects.filter(user=user, document__doctype=profile.doctype)[0]
        startno=startdoc.document.doc_no
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
        print(annots)

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
def getWorkerAnnotations(request):
    if request.method=='GET':
        doctypetext=request.GET['doctype']
        doctypetext=request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        image_id =request.GET['image_id']
        document=Document.objects.get(doctype=doctype, doc_no=int(image_id))
        statuses=Status.objects.filter(document=document, status=True)
        workerannots=[]
        print(statuses)
        for status in statuses: 
            user=status.user
            annots=Annotation.objects.filter(user=user, document=document, is_alive=True)
            annotations=[]
            print(annots)
            for annot in annots: 
                boxes=annot.boxes_id.replace('[',' ').replace(']',' ').replace(', ',' ').split()
                for box in boxes:
                    if(annot.subcat==None):
                        annotations.append({'group_id':annot.pk, 'box_id': box, 'cat': annot.cat.cat_text, 'subcat':None, 'subcatpk': None, 'catpk':annot.cat.pk, 'confidence': None })
                    else:
                        if(annot.subcat.subcat_text=="N/A"):
                            annotations.append({'group_id':annot.pk,  'box_id': box,'cat': annot.cat.cat_text, 'subcat':annot.subcat.subcat_text, 'subcatpk':annot.subcat.pk, 'catpk':annot.cat.pk, 'confidence': None})
                        else:
                            annotations.append({'group_id':annot.pk,  'box_id': box, 'cat': annot.cat.cat_text, 'subcat':annot.subcat.subcat_text, 'subcatpk':annot.subcat.pk, 'catpk':annot.cat.pk, 'confidence': annot.confidence})
            annotations.sort(key=lambda s: int(s['box_id']))

            # remove duplicate 

            workerannots.append({'user': user.username, 'annotations': getLastAnnotations(annotations)})
        for i in range(4-len(workerannots)):
            workerannots.append({'user': 'null', 'annotations': []})
        response={
            'workerannots':workerannots
        }
        return JsonResponse(response)


def getLastAnnotations(jsonlist):
    result=[]
    result.append(jsonlist[0])
    for idx in range(len(jsonlist)-1):
        row=jsonlist[idx+1]
        if(row["box_id"]==result[-1]["box_id"]):
            result[-1]=row
        else: 
            result.append(row)
    return result
        
        
""" 
@csrf_exempt
def saveAnnotation(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        user = User.objects.get(username=username)
        profile=Profile.objects.get(user=user)

        image_id =query_json['image_id']
        document=Document.objects.get(doctype=profile.doctype, doc_no=int(image_id))
        boxes = query_json['boxes_id']
        labelpk = query_json['labelpk']
        thisLabel = InitSubCat.objects.get(pk=labelpk)
        newAnnot=Annotation(user=user, document=document, boxes_id = boxes, cat=thisLabel.initcat, subcat=thisLabel, is_alive=True)
        newAnnot.save()
        response={
            'annot_pk': newAnnot.pk
        }
        return JsonResponse(response) """

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
                newSelection = SelectedSuggestion(suggestion=newSuggestion, user=user, annotation=newAnnot)
                newSelection.save()
            else: #existing suggestion 
                thisSuggestion=thisSuggestions[0]
                newSelection = SelectedSuggestion(suggestion=thisSuggestion, user=user, annotation=newAnnot)
        response={
            'annot_pk': newAnnot.pk
        }
        return JsonResponse(response)

""" 
@csrf_exempt
def saveAsRegular(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
#        user=request.user
        username=query_json['mturk_id']
        user = User.objects.get(username=username)
        doctypetext=query_json['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)

        confDefAnnots=DefAnnotation.objects.filter(user=user, confidence=True, is_alive=True)
        for annot in confDefAnnots:
            newAnnot=Annotation(user=user, document=annot.document, boxes_id=annot.boxes_id, cat=annot.cat, subcat=annot.subcat, is_alive=True)
            newAnnot.save()
        response={
            'annot_pk': newAnnot.pk
        }
        return JsonResponse(response)
 """

""" @csrf_exempt
def deleteAnnotation(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
#        user=request.user
        username=query_json['mturk_id']
        user = User.objects.get(username=username)
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
        return JsonResponse(response) """
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
def submit(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        username = query_json['mturk_id']
        user = User.objects.get(username=username)

        profile=Profile.objects.get(user=user)
        profile.endtime=datetime.now()
        profile.done=True
        profile.save()
        return HttpResponse('')


@csrf_exempt
def submitSurvey(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        username = query_json['mturk_id']
        user = User.objects.get(username=username)

        profile=Profile.objects.get(user=user)
        profile.endsurveytime=datetime.now()

        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        profile.token=token

        profile.save()

        response={
            'token': token
        }
        return JsonResponse(response)


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
        print(image_id)

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

@csrf_exempt
def addCat(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username = query_json['mturk_id']
        doctypetext=query_json['doctype']
        image_id = query_json['image_id']
        cat= query_json['cat']
        doctype=DocType.objects.get(doctype=doctypetext)
        user = User.objects.get(username=username)
        #user=request.user
        newCat=UserCat(user=user, doctype=doctype, cat_text=cat, made_at=int(image_id))
        newCat.save()
        response = {
            'newcat_pk': newCat.pk,
        }
        return JsonResponse(response)


@csrf_exempt
def addSubcat(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username = query_json['mturk_id']
        doctypetext=query_json['doctype']
        image_id = query_json['image_id']
        cat= query_json['cat']
        subcat=query_json['subcat']
        desc=query_json['description']

        doctype=DocType.objects.get(doctype=doctypetext)
        user = User.objects.get(username=username)
        #user=request.user
        print(cat)
        cat = UserCat.objects.get(user=user, doctype=doctype, cat_text=cat)


        newSubcat=UserSubcat(usercat=cat, subcat_text=subcat, subcat_description=desc, made_at=int(image_id))
        newSubcat.save()
        response = {
            'newsubcat_pk': newSubcat.pk,
        }
        return JsonResponse(response)
""" 
@csrf_exempt
def reviseCat(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username = query_json['mturk_id']
        doctypetext=query_json['doctype']
        cat_pk= query_json['cat_pk']
        revcat=query_json['revcat']

        doctype=DocType.objects.get(doctype=doctypetext)
        user = User.objects.get(username=username)
        #user=request.user

        UserCat.objects.filter(user=user, doctype=doctype, pk=int(cat_pk)).update(cat_text=revcat)
        return HttpResponse('')
 """
""" 
@csrf_exempt
def reviseSubcat(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username = query_json['mturk_id']
        doctypetext=query_json['doctype']
        subcat_pk= query_json['subcat_pk']
        revsubcat=query_json['revsubcat']
        revdesc=query_json['revdesc']

        doctype=DocType.objects.get(doctype=doctypetext)
        user = User.objects.get(username=username)
#        user=request.user

        UserSubcat.objects.filter(pk=int(subcat_pk)).update(subcat_text=revsubcat, subcat_description=revdesc)
        return HttpResponse('')
 """

@csrf_exempt
def getImage(request, image_id):
    if request.method == 'GET':
        item = Image.objects.get(image_id=image_id)
        # item = Image.objects.filter(is_done=True)[int(num)]
        return HttpResponse(item.image.url)

@csrf_exempt
def uploadImage(request):
    if request.method == 'POST':
        file = request.FILES["image_file"]
        image_id = file.name.replace(".png", "")
        if len(Image.objects.filter(image_id=image_id)) != 0:
            return HttpResponseBadRequest("The image_id exists!")

        data = request.POST
        image = Image(image_id=file.name.replace(".png", ""), image=file, box_info=data["text"])
        image.save()
        return HttpResponse("Uploaded!")

@csrf_exempt
def getJson(request, json_id):
    if request.method == 'GET':
        item = Json.objects.get(json_id=json_id)
        # item = Image.objects.filter(is_done=True)[int(num)]
        return HttpResponse(item.json.url)


@csrf_exempt
def uploadJson(request):
    if request.method == 'POST':
        file = request.FILES["json_file"]
        json_id = file.name.replace(".json", "")
        if len(Image.objects.filter(json_id=json_id)) != 0:
            return HttpResponseBadRequest("The json_id exists!")

        data = request.POST
        json = Json(image_id=file.name.replace(".json", ""), image=file)
        json.save()
        return HttpResponse("Uploaded!")

# view for api call from resolution interface 
@csrf_exempt
def getAnnotationsByImage(request):
    if request.method=='GET':
        doctypetext=request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        image_id =request.GET['image_id']
        document=Document.objects.get(doctype=doctype, doc_no=int(image_id))
        statuses=Status.objects.filter(document=document, status=True)
        workerannots=[]
        print(statuses)
        for status in statuses: 
            user=status.user
            annots=Annotation.objects.filter(user=user, document=document, is_alive=True)
            annotations=[]
            print(annots)
            for annot in annots: 
                boxes=annot.boxes_id.replace('[',' ').replace(']',' ').replace(', ',' ').split()
                for box in boxes:
                    if(annot.subcat==None):
                        annotations.append({'group_id':annot.pk, 'box_id': box, 'cat': annot.cat.cat_text, 'subcat':None, 'subcatpk': None, 'catpk':annot.cat.pk, 'confidence': None })
                    else:
                        if(annot.subcat.subcat_text=="N/A"):
                            annotations.append({'group_id':annot.pk,  'box_id': box,'cat': annot.cat.cat_text, 'subcat':annot.subcat.subcat_text, 'subcatpk':annot.subcat.pk, 'catpk':annot.cat.pk, 'confidence': None})
                        else:
                            annotations.append({'group_id':annot.pk,  'box_id': box, 'cat': annot.cat.cat_text, 'subcat':annot.subcat.subcat_text, 'subcatpk':annot.subcat.pk, 'catpk':annot.cat.pk, 'confidence': annot.confidence})
            annotations.sort(key=lambda s: int(s['box_id']))

            # remove duplicate 

            workerannots.append({'user': user.username, 'annotations': getLastAnnotations(annotations)})
        for i in range(4-len(workerannots)):
            workerannots.append({'user': 'null', 'annotations': []})
        response={
            'workerannots':workerannots
        }
        return JsonResponse(response)


def getLastAnnotations(jsonlist):
    result=[]
    result.append(jsonlist[0])
    for idx in range(len(jsonlist)-1):
        row=jsonlist[idx+1]
        if(row["box_id"]==result[-1]["box_id"]):
            result[-1]=row
        else: 
            result.append(row)
    return result
        
      
@csrf_exempt
def getWorkers(request):
    if request.method=='GET':
        doctypetext=request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        print(doctype)
        profiles=Profile.objects.filter(doctype=doctype)
        print('profiles', profiles)

        users=[]
        for prof in profiles:
            # should be modified later to if (prof.endtime and prof.done)
            if (prof.consent_agreed and prof.instr_read):
                users.append({'username': prof.user.username, 'user_order': prof.user_order})
        return JsonResponse(users, safe=False)            


@csrf_exempt
def getAnnotationsByWorker(request):
    if request.method=='GET':
        username =request.GET['mturk_id']
        user = User.objects.get(username=username)
        profile=Profile.objects.get(user=user)
        statuses=Status.objects.filter(user=user, status=True)
        response={}
        response["username"]=username
        workerannot=[]
        for stat in statuses:
            document=stat.document            
            annots=Annotation.objects.filter(user=user, document=document, is_alive=True)
            annotations=[]
            for annot in annots: 
                boxes=annot.boxes_id.replace('[',' ').replace(']',' ').replace(', ',' ').split()
                for box in boxes:
                    if(annot.subcat==None):
                        annotations.append({'group_id':annot.pk, 'box_id': box, 'cat': annot.cat.cat_text, 'subcat':None, 'subcatpk': None, 'catpk':annot.cat.pk, 'confidence': None })
                    else:
                        if(annot.subcat.subcat_text=="N/A"):
                            annotations.append({'group_id':annot.pk,  'box_id': box,'cat': annot.cat.cat_text, 'subcat':annot.subcat.subcat_text, 'subcatpk':annot.subcat.pk, 'catpk':annot.cat.pk, 'confidence': None})
                        else:
                            annotations.append({'group_id':annot.pk,  'box_id': box, 'cat': annot.cat.cat_text, 'subcat':annot.subcat.subcat_text, 'subcatpk':annot.subcat.pk, 'catpk':annot.cat.pk, 'confidence': annot.confidence})
            annotations.sort(key=lambda s: int(s['box_id']))
            workerannot.append({'document_pk': document.pk, 'annotations': getLastAnnotations(annotations)})
        response["annotations"]=workerannot
        response["start_time"]=profile.starttime 
        response['end_time']=profile.endtime
        response['user_order']=profile.user_order
        response['start_image_no']=profile.user_order*7
        response['end_image_no']=profile.user_order*7+20
        return JsonResponse(response)


@csrf_exempt
def getEveryAnnotations(request):
    if request.method=='GET':
        doctypetext=request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        profiles=Profile.objects.filter(doctype=doctype)
        response=[]
        for prof in profiles:
            user=prof.user
            statuses=Status.objects.filter(user=user, status=True)
            userannots={}
            userannots["username"]=user.username
            workerannot=[]
            for stat in statuses:
                document=stat.document            
                annots=Annotation.objects.filter(user=user, document=document, is_alive=True)
                annotations=[]
                for annot in annots: 
                    boxes=annot.boxes_id.replace('[',' ').replace(']',' ').replace(', ',' ').split()
                    for box in boxes:
                        if(annot.subcat==None):
                            annotations.append({'group_id':annot.pk, 'box_id': box, 'cat': annot.cat.cat_text, 'subcat':None, 'subcatpk': None, 'catpk':annot.cat.pk, 'confidence': None })
                        else:
                            if(annot.subcat.subcat_text=="N/A"):
                                annotations.append({'group_id':annot.pk,  'box_id': box,'cat': annot.cat.cat_text, 'subcat':annot.subcat.subcat_text, 'subcatpk':annot.subcat.pk, 'catpk':annot.cat.pk, 'confidence': None})
                            else:
                                annotations.append({'group_id':annot.pk,  'box_id': box, 'cat': annot.cat.cat_text, 'subcat':annot.subcat.subcat_text, 'subcatpk':annot.subcat.pk, 'catpk':annot.cat.pk, 'confidence': annot.confidence})
                annotations.sort(key=lambda s: int(s['box_id']))
                workerannot.append({'document_pk': document.pk, 'annotations': getLastAnnotations(annotations)})
            userannots["annotations"]=workerannot
            response.append(userannots)
    return JsonResponse(response, safe=False)
