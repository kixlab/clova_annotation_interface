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
from api.models import * 

import string
import random
import json
from datetime import datetime, timedelta
from django.db.models import Max, Count, Q


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
   
    new_user=User(username=username, password=password)
    new_user.save()


    initstatus=initialize('receipt', username)
    print(initstatus)

    login(request, new_user)


    response = {
        'status': 'new',
        'doctype': 'receipt'
    }
    return JsonResponse(response)

def initialize(doctype_text, expert_id):
    doctype=DocType.objects.get(doctype=doctype_text)
    expert=User.objects.get(username=expert_id)

    # TargetBoxAnnotation by copying from BoxAnnotation 
    BoxAnnots=BoxAnnotation.objects.filter(document__doctype=doctype)
    for boxannot in BoxAnnots:
        TargetBoxAnnotation(expert=expert, user=boxannot.user, document=boxannot.document, subcat=boxannot.subcat, cat=boxannot.cat, annotation=boxannot.annotation, 
        box_id=boxannot.box_id,is_reviewed=False).save()

    # FinLabels by copying from InitSubcat, InitCat 
    for subcat in InitSubCat.objects.filter(initcat__doctype=doctype):
        FinalLabel(expert=expert, doctype=doctype, cat_text=subcat.initcat.cat_text, subcat_text=subcat.subcat_text).save()
    
    # review가 필요 없는 raw annotation에 대해서 revised annotation 생성 
    for rawannot in RawAnnotation.objects.filter(document__doctype=doctype, has_suggestion=False):
        subcat=rawannot.subcat 
        thisLabel=FinalLabel.objects.get(expert=expert, doctype=doctype, cat_text=subcat.initcat.cat_text, subcat_text=subcat.subcat_text)
        RevisedAnnotation(expert=expert, document=rawannot.document, label=thisLabel, box_id=rawannot.box_id, revision_type='auto').save()
        # for those box, update targetboxannotation as reviewed
        currTargets=TargetBoxAnnotation.objects.filter(expert=expert, document=rawannot.document, box_id=rawannot.box_id)
        for curTarget in currTargets: 
            curTarget.is_reviewed=True
            curTarget.save()
    return True

@csrf_exempt
def getDocTypes(request):
    if request.method == 'GET':
        doctypes=[doctype.doctype for doctype in DocType.objects.all()]
        return JsonResponse({'doctypes':doctypes})


def getNAs(doctype_text, expert_id):
    doctype=DocType.objects.get(doctype=doctype_text)
    expert=User.objects.get(username=expert_id)
    suggestions=UserSuggestion.objects.annotate(nselection=Count('selectedsuggestion')).filter(subcat__subcat_text="n/a").order_by('-selectedsuggestion')

    if(len(suggestions)>100):
        suggestions=suggestions[0:100]
    targetBoxes=TargetBoxAnnotation.objects.filter(expert=expert, is_reviewed=False)
    # count 
    na_suggestions=[]
    for suggestion in suggestions: 
        suggested_boxes=[]
        workers=[]
        n_boxes=0
        # get candidate docs 
        selections = SelectedSuggestion.objects.filter(suggestion=suggestion, annotation__document__doctype=doctype)
        cand_docs = [selection.annotation.document for selection in selections]
        for doc in cand_docs:
            #thisDoc=Document.objects.get(doctype=doctype, doc_no=doc_no)
            selections = SelectedSuggestion.objects.filter(suggestion=suggestion, annotation__document=doc) # 이 document에서 이 suggestion을 선택한 경우 
            boxes_id=[]
            for selection in selections: 
                thisannot=selection.annotation
                boxes=targetBoxes.filter(annotation=thisannot)
                boxes_id=boxes_id+[box.box_id for box in boxes]
                #print(boxes_id)
                workers.append(thisannot.user.username)
            if(len(boxes_id)>0):
                suggested_boxes.append({
                    'image_no': doc.doc_no, 
                    'boxes_id': list(set(boxes_id))
                })
                n_boxes=n_boxes+len(list(set(boxes_id)))
            workers=list(set(workers))
        if(n_boxes>0):
            na_suggestions.append({'suggestion_pk': suggestion.pk, 'suggestion_cat': suggestion.subcat.initcat.cat_text, 'suggestion_subcat': suggestion.subcat.subcat_text, 'suggestion_text': suggestion.suggested_subcat, 
            'n_images': len(suggested_boxes), 'n_workers': len(workers), 'n_boxes': n_boxes, 'suggested_boxes':suggested_boxes, 'workers': workers})
    return na_suggestions


def getCTs(doctype_text, expert_id):
    doctype=DocType.objects.get(doctype=doctype_text)
    expert=User.objects.get(username=expert_id)
    allsuggestions=UserSuggestion.objects.annotate(nselection=Count('selectedsuggestion')).order_by('-selectedsuggestion')
    suggestions=[]
    for sug in allsuggestions:
        if(sug.subcat.subcat_text!='n/a'):
            suggestions.append(sug)
    targetBoxes=TargetBoxAnnotation.objects.filter(expert=expert, is_reviewed=False)
    # count 
    close_to_suggestions=[]

    for suggestion in suggestions: 
        suggested_boxes=[]
        workers=[]
        n_boxes=0
        # get candidate docs 
        selections = SelectedSuggestion.objects.filter(suggestion=suggestion, annotation__document__doctype=doctype)
        cand_docs = [selection.annotation.document for selection in selections]
        for doc in cand_docs:
            #thisDoc=Document.objects.get(doctype=doctype, doc_no=doc_no)
            selections = SelectedSuggestion.objects.filter(suggestion=suggestion, annotation__document=doc) # 이 document에서 이 suggestion을 선택한 경우 
            boxes_id=[]
            for selection in selections: 
                thisannot=selection.annotation
                boxes=targetBoxes.filter(annotation=thisannot)
                boxes_id=boxes_id+[box.box_id for box in boxes]
                #print(boxes_id)
                workers.append(thisannot.user.username)
            if(len(boxes_id)>0):
                suggested_boxes.append({
                    'image_no': doc.doc_no, 
                    'boxes_id': list(set(boxes_id))
                })
                n_boxes=n_boxes+len(list(set(boxes_id)))
            workers=list(set(workers))
        if(n_boxes>0):
            close_to_suggestions.append({'suggestion_pk': suggestion.pk, 'suggestion_cat': suggestion.subcat.initcat.cat_text, 'suggestion_subcat': suggestion.subcat.subcat_text, 'suggestion_text': suggestion.suggested_subcat, 
            'n_images': len(suggested_boxes), 'n_workers': len(workers), 'n_boxes': n_boxes, 'suggested_boxes':suggested_boxes, 'workers': workers})
    return close_to_suggestions

@csrf_exempt
def getNASuggestions(request):
    if request.method == 'GET':
        expert_id= request.GET['mturk_id']        
        na_suggestions=getNAs('receipt', expert_id)
        return JsonResponse({
            'na_suggestions': na_suggestions
        })

@csrf_exempt
def getCloseToSuggestions(request):
    if request.method == 'GET':
        expert_id= request.GET['mturk_id']        
        close_to_suggestions=getCTs('receipt', expert_id)
        return JsonResponse({
            'close_to_suggestions': close_to_suggestions
        })


@csrf_exempt
def getCats(request):
    if request.method == 'GET':
        thisDocType=DocType.objects.get(doctype='receipt')
        initcats=InitCat.objects.filter(doctype=thisDocType)
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


def getDistn(doctype_text, expert_id):
    doctype=DocType.objects.get(doctype=doctype_text)
    expert=User.objects.get(username=expert_id)
    finLabels=FinalLabel.objects.filter(expert=expert, doctype=doctype)

    u_cats=list(set([label.cat_text for label in finLabels]))
    cat_distn=[]
    for cat in u_cats:
        subcat_distn=[]
        count=0
        labels=finLabels.filter(cat_text=cat)
        for label in labels:
            subcatcount=len(RevisedAnnotation.objects.filter(expert=expert, label=label))
            subcat_distn.append({'subcat': label.subcat_text, 'count': subcatcount})
            count=count+subcatcount
        cat_distn.append({'cat': cat, 'cat_count': count, 'subcat_distn': subcat_distn})
    return cat_distn

@csrf_exempt
def getCurrDistribution(request):
    if request.method == 'GET':
        expert_id= request.GET['mturk_id']
        distn=getDistn('receipt', expert_id)

        return JsonResponse({
            'distribution': distn
        })


def getRawDistn(doctype_text, expert_id):
    doctype=DocType.objects.get(doctype=doctype_text)
    expert=User.objects.get(username=expert_id)

    cat_distn=[]
    for cat in InitCat.objects.filter(doctype=doctype):
        subcat_distn=[]
        count=0
        for subcat in InitSubCat.objects.filter(initcat=cat):
            subcatcount=len(RawAnnotation.objects.filter(subcat=subcat))
            subcat_distn.append({'subcat': subcat.subcat_text, 'subcat_count': subcatcount})
            count=count+subcatcount
        cat_distn.append({'cat': cat.cat_text, 'cat_count': count, 'subcat_distn': subcat_distn})
    return cat_distn

@csrf_exempt
def getRawDistribution(request):
    if request.method == 'GET':
        expert_id= request.GET['mturk_id']
        distn=getRawDistn('receipt', expert_id)
        return JsonResponse({
            'distribution': distn
        })


def saveResolution(username, saved_boxes, revision_type):
    user = User.objects.get(username=username)

    for saved_box in saved_boxes: 
            boxes_id=saved_box['boxes_id']
            cat=saved_box['cat']
            subcat=saved_box['subcat']
            suggested_cat=saved_box['suggested_cat']
            suggested_subcat=saved_box['suggested_subcat']
            image_no=saved_box['image_no']

            thisDoc=Document.objects.get(doc_no=image_no, doctype__doctype='receipt')
            for box_id in boxes_id: 
                # add new label 
                ## check if cat, subcat match with existing final label 
                matched_label=FinalLabel.objects.filter(cat_text=cat, subcat_text=subcat, doctype=thisDoc.doctype)
                if(len(matched_label)==0): # no such label 
                    thislabel=FinalLabel(expert=user, doctype=thisDoc.doctype, cat_text=cat, subcat_text=subcat)
                    thislabel.save()
                else:
                    thislabel=matched_label[0]
                
                # save revised annotation
                newRevAnnot=RevisedAnnotation(expert=user, document=thisDoc, label=thislabel, 
                box_id=box_id, revision_type=revision_type)
                newRevAnnot.save()

                # mark the box as reviewed
                boxAnnots=TargetBoxAnnotation.objects.filter(expert=user, document=thisDoc, box_id=box_id)
                for boxAnnot in boxAnnots:
                    boxAnnot.is_reviewed=True
                    boxAnnot.save()
    return True


@csrf_exempt
def saveNAApprove(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['expert_id']
        saved_boxes=query_json['saved_boxes']

        result=saveResolution(username, saved_boxes, 'na-approve')

        na_suggestions=getNAs('receipt', username)
        current_distribution=getDistn('receipt', username)

        response={
            'na_suggestions': na_suggestions,
            'distribution': current_distribution
        }
        return JsonResponse(response)

@csrf_exempt
def saveNANew(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['expert_id']
        saved_boxes=query_json['saved_boxes']

        result=saveResolution(username, saved_boxes, 'na-new')

        na_suggestions=getNAs('receipt', username)
        current_distribution=getDistn('receipt', username)

        response={
            'na_suggestions': na_suggestions,
            'distribution': current_distribution
        }
        return JsonResponse(response)

@csrf_exempt
def saveNAExisting(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['expert_id']
        saved_boxes=query_json['saved_boxes']

        result=saveResolution(username, saved_boxes, 'na-existing')

        na_suggestions=getNAs('receipt', username)
        current_distribution=getDistn('receipt', username)

        response={
            'na_suggestions': na_suggestions,
            'distribution': current_distribution
        }
        return JsonResponse(response)

@csrf_exempt
def saveCloseToApprove(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['expert_id']
        saved_boxes=query_json['saved_boxes']

        result=saveResolution(username, saved_boxes, 'ct-approve')

        close_to_suggestions=getCTs('receipt', username)
        current_distribution=getDistn('receipt', username)
        response={
            'close_to_suggestions': close_to_suggestions,
            'distribution': current_distribution
        }
        return JsonResponse(response)


@csrf_exempt
def saveCloseToNew(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['expert_id']
        saved_boxes=query_json['saved_boxes']

        result=saveResolution(username, saved_boxes, 'ct-new')

        close_to_suggestions=getCTs('receipt', username)
        current_distribution=getDistn('receipt', username)
        response={
            'close_to_suggestions': close_to_suggestions,
            'distribution': current_distribution
        }
        return JsonResponse(response)

@csrf_exempt
def saveCloseToIgnore(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['expert_id']
        saved_boxes=query_json['saved_boxes']

        result=saveResolution(username, saved_boxes, 'ct-ignore')

        close_to_suggestions=getCTs('receipt', username)
        current_distribution=getDistn('receipt', username)
        response={
            'close_to_suggestions': close_to_suggestions,
            'distribution': current_distribution
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
def getWorkerAnnotations(request):
    if request.method=='GET':
        doctypetext=request.GET['doctype']
        doctypetext=request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        image_id =request.GET['image_id']
        document=Document.objects.get(doctype=doctype, doc_no=int(image_id))
        statuses=Status.objects.filter(document=document, status=True)
        workerannots=[]
        for status in statuses: 
            user=status.user
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
        cat = UserCat.objects.get(user=user, doctype=doctype, cat_text=cat)


        newSubcat=UserSubcat(usercat=cat, subcat_text=subcat, subcat_description=desc, made_at=int(image_id))
        newSubcat.save()
        response = {
            'newsubcat_pk': newSubcat.pk,
        }
        return JsonResponse(response)


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
        for status in statuses: 
            user=status.user
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

            # remove duplicate 

            workerannots.append({'user': user.username, 'annotations': getLastAnnotations(annotations)})
        for i in range(4-len(workerannots)):
            workerannots.append({'user': 'null', 'annotations': []})
        response={
            'workerannots':workerannots
        }
        return JsonResponse(response)
      
@csrf_exempt
def getWorkers(request):
    if request.method=='GET':
        doctypetext=request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        profiles=Profile.objects.filter(doctype=doctype)

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