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
    doctype_text = request.data['doctype']

    if(len(User.objects.filter(username=username))>0):
        user=User.objects.filter(username=username)[0]
        login(request, user)
    
    else:
        password = username   
        new_user=User(username=username, password=password)
        new_user.save()
        initstatus=initialize(doctype_text, username)
        login(request, new_user)
    response = {
        'status': 'new',
        'doctype': 'receipt'
    }
    return JsonResponse(response)

def initialize(doctype_text, expert_id):
    doctype=DocType.objects.get(doctype=doctype_text)
    expert=User.objects.get(username=expert_id)

    # FinalCats and FinalSubCats
    for cat in InitCat.objects.filter(doctype=doctype):
        newFinCat=FinalCat(expert=expert, doctype=doctype, cat_text=cat.cat_text)
        newFinCat.save()
        for subcat in InitSubCat.objects.filter(initcat=cat):
            FinalSubCat(finalcat=newFinCat, subcat_text=subcat.subcat_text, subcat_description=subcat.subcat_description).save()
    # ?????? raw??? revised??? ?????? 
    for rawannot in RawBoxAnnotation.objects.filter(document__doctype=doctype):
        finalcat=FinalCat.objects.get(expert=expert, cat_text=rawannot.initcat.cat_text)
        finalsubcat=FinalSubCat.objects.get(finalcat=finalcat, subcat_text=rawannot.initsubcat.subcat_text)
        RevisedBoxAnnotation(expert=expert, document=rawannot.document, finalcat=finalcat, finalsubcat=finalsubcat, box_id=rawannot.box_id, revision_type='auto-mv').save()
    
       # n/a??? ?????? annotation --> target annotation?????? 
    for annot in GroupedAnnotation.objects.filter(document__doctype=doctype):
        thisProfile=Profile.objects.filter(user=annot.user)
        if(len(thisProfile)>0):
            thisProfile=thisProfile[0]
            if(thisProfile.done):
                if(len(TargetAnnotation.objects.filter(expert=expert, doctype=doctype, annotation=annot))==0):
                    TargetAnnotation(expert=expert, doctype=doctype, annotation=annot, is_reviewed=False).save()
    return True


@csrf_exempt
def getDocTypes(request):
    if request.method == 'GET':
        doctypes=[doctype.doctype for doctype in DocType.objects.all()]
        return JsonResponse({'doctypes':doctypes})

@csrf_exempt
def getCats(request):
    if request.method == 'GET':
        doctypetext= request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)

        initcats=InitCat.objects.filter(doctype=doctype)
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
def getFinalCats(request):
    if request.method == 'GET':
        expert_id= request.GET['mturk_id']
        expert=User.objects.get(username=expert_id)

        doctypetext= request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)

        finalcats=FinalCat.objects.filter(doctype=doctype, expert=expert)
        subcats=[]
        cats=[]
        for cat in finalcats:
            cats.append({'cat': cat.cat_text, 'pk': cat.pk})
            for subcat in FinalSubCat.objects.filter(finalcat=cat):
                subcats.append({'cat': subcat.finalcat.cat_text, 'subcat':subcat.subcat_text, 'description':subcat.subcat_description, 'pk':subcat.pk, 'catpk':subcat.finalcat.pk})
        response = {
            'final_cats': cats,
            'final_subcats': subcats
        }
        return JsonResponse(response)


def getDistn(doctype, expert):
    finCats=FinalCat.objects.filter(expert=expert, doctype=doctype)
    cat_distn=[]
    for cat in finCats: 
        subcat_distn=[]
        count=0
        finSubCats=FinalSubCat.objects.filter(finalcat=cat)
        for subcat in finSubCats: 
            subcatcount=len(RevisedBoxAnnotation.objects.filter(expert=expert, finalsubcat=subcat))
            subcat_distn.append({'subcat': subcat.subcat_text, 'description': subcat.subcat_description, 'count': subcatcount})
            count=count+subcatcount
        cat_distn.append({'cat': cat.cat_text, 'cat_count': count, 'subcat_distn': subcat_distn})
    return cat_distn

@csrf_exempt
def getCurrDistribution(request):
    if request.method == 'GET':
        expert_id= request.GET['mturk_id']
        expert=User.objects.get(username=expert_id)
        doctypetext= request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        distn=getDistn(doctype, expert)
        return JsonResponse({
            'distribution': distn
        })


def getRawDistn(doctype):
    initCats=InitCat.objects.filter(doctype=doctype)
    cat_distn=[]
    for cat in initCats: 
        subcat_distn=[]
        count=0
        initSubCats=InitSubCat.objects.filter(initcat=cat)
        for subcat in initSubCats: 
            subcatcount=len(RawBoxAnnotation.objects.filter(initsubcat=subcat))
            subcat_distn.append({'subcat': subcat.subcat_text, 'description': subcat.subcat_description, 'count': subcatcount})
            count=count+subcatcount
        cat_distn.append({'cat': cat.cat_text, 'cat_count': count, 'subcat_distn': subcat_distn})
    return cat_distn

@csrf_exempt
def getRawDistribution(request):
    if request.method == 'GET':
        doctypetext= request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        distn=getRawDistn(doctype)
        return JsonResponse({
            'distribution': distn
        })


@csrf_exempt
def getMemo(request):
    if request.method == 'GET':
        doctypetext= request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        memos_all=Memo.objects.filter(doctype=doctype)
        memos=[]
        for memo in memos_all:
            user=memo.user
            thisProfile=Profile.objects.get(user=user)
            if(thisProfile.done):
                memos.append({'worker_id': user.username, 'memo':memo.text})
        return JsonResponse({
            'memos': memos
        })


@csrf_exempt
def getNAs(doctype, expert):
        suggestions=FinalSuggestion.objects.filter(subcat__subcat_text="n/a", subcat__initcat__doctype=doctype)
        unreviewed=TargetAnnotation.objects.filter(expert=expert,doctype=doctype, annotation__annot_type='n/a', is_reviewed=False)
        
        response=[]
        for suggestion in suggestions: 
            annots=unreviewed.filter(annotation__final_suggestion=suggestion)
            n_workers=len(list(set([annot.annotation.user for annot in annots])))
            n_images=len(list(set([annot.annotation.document for annot in annots])))
            n_annotations=len(annots)
            annot_response=[]
            for annot in annots: 
                annot_response.append(
                    {
                        'annotation_pk': annot.pk, 
                        'image_no': annot.annotation.document.doc_no, 
                        'worker_id': annot.annotation.user.username,
                        'boxes_id':annot.annotation.boxes_id,
                        'reason': annot.annotation.reason,
                        'suggested_subcategory': suggestion.suggested_subcat
                    }
                )
            if(len(annots)>0):
                response.append({
                    'suggestion_pk': suggestion.pk, 'suggestion_cat': suggestion.subcat.initcat.cat_text, 'suggestion_subcat': suggestion.subcat.subcat_text, 'suggestion_text': suggestion.suggested_subcat,
                    'n_images': n_images, 'n_workers': n_workers, 'n_annotations': n_annotations, 'annotations': annot_response
                })
        return response


@csrf_exempt
def getNASuggestions(request):
    if request.method == 'GET':
        expert_id= request.GET['mturk_id']
        expert=User.objects.get(username=expert_id)
        doctypetext= request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)

        response=getNAs(doctype, expert)
        distn=getDistn(doctype, expert)
        return JsonResponse(
            {'na_suggestions': response,
            'distribution':distn}
        )

@csrf_exempt
def getCTs(doctype, expert):
    unreviewed=TargetAnnotation.objects.filter(expert=expert,doctype=doctype,is_reviewed=False).exclude(annotation__annot_type='n/a')
    response=[]
    for cat in InitCat.objects.filter(doctype=doctype): 
        cat_response=[]
        for subcat in InitSubCat.objects.filter(initcat=cat):
            suggestions=FinalSuggestion.objects.filter(subcat=subcat).exclude(subcat__subcat_text="n/a")
            suggest_response=[]
            for suggestion in suggestions: 
                unreviewed_this=unreviewed.filter(annotation__final_suggestion=suggestion)
                annot_response=[]
                n_workers=len(list(set([annot.annotation for annot in unreviewed_this])))
                n_images=len(list(set([annot.annotation.document for annot in unreviewed_this])))
                n_annotations=len(unreviewed_this)
                for annot in unreviewed_this:
                    annot_response.append({
                        'annotation_pk': annot.pk, 
                        'image_no': annot.annotation.document.doc_no, 
                        'worker_id': annot.annotation.user.username,
                        'boxes_id':annot.annotation.boxes_id,
                        'reason': annot.annotation.reason,
                        'suggested_subcategory': suggestion.suggested_subcat
                })
                if(len(annot_response)>0):
                    suggest_response.append({
                        'suggestion_pk': suggestion.pk, 'suggestion_cat': suggestion.subcat.initcat.cat_text, 'suggestion_subcat': suggestion.subcat.subcat_text, 
                        'suggested_subcat': suggestion.suggested_subcat, 'n_images':n_images, 'n_workers': n_workers, 'n_annotations':n_annotations, 'annotations': annot_response
                    })
            if(len(suggest_response)>0):
                cat_response.append({
                    'subcat': subcat.subcat_text, 'subcat_description': subcat.subcat_description, 'suggestions': suggest_response
                })
        if(len(cat_response)>0):
            response.append({
                'cat': cat.cat_text, 'subcat': cat_response
            })
    return response


def getCloseToSuggestions(request):
    if request.method == 'GET':
        expert_id= request.GET['mturk_id']
        expert=User.objects.get(username=expert_id)
        doctypetext= request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)

        response=getCTs(doctype, expert)
        distn=getDistn(doctype, expert)
        return JsonResponse(
            {'close_to_suggestions': response,
            'distribution':distn}
        )


def updateRevisedBoxAnnotation(expert, thisTargetAnnot, thisCat, thisSubCat, revision_type):
    print(expert, thisTargetAnnot, thisCat, thisSubCat, revision_type, flush=True)
    boxes_id=thisTargetAnnot.annotation.boxes_id.replace(',', ' ').replace('[', ' ').replace(']', ' ').split()
    document=thisTargetAnnot.annotation.document
    for box_id in boxes_id:
        thisRevBoxes=RevisedBoxAnnotation.objects.filter(expert=expert, document=document, box_id=box_id)
        if(len(thisRevBoxes)>0):
            thisRevBox=thisRevBoxes[0]
            thisRevBox.finalcat=thisCat
            thisRevBox.finalsubcat=thisSubCat
            thisRevBox.revision_type=revision_type
            thisRevBox.save()
        else:
            newRevBox=RevisedBoxAnnotation(expert=expert, document=document,finalcat=thisCat, finalsubcat=thisSubCat, box_id=box_id, revision_type=revision_type)
            newRevBox.save()
    return True

def saveResolution(expert, doctype, annotations_pk, cat_text, subcat_text, description, revision_type):  

    Revision(expert=expert, revision_type=revision_type, annotation_pks=annotations_pk).save()
     
    thisCats=FinalCat.objects.filter(expert=expert, cat_text=cat_text)
    if(len(thisCats)>0):
        thisCat=thisCats[0]
    else: 
        newFinalCat=FinalCat(expert=expert, doctype=doctype, cat_text=cat_text)
        newFinalCat.save()
        thisCat=newFinalCat

    thisSubCats=FinalSubCat.objects.filter(finalcat=thisCat, subcat_text=subcat_text)
    if(len(thisSubCats)>0):
        thisSubCat=thisSubCats[0]
    else: 
        newFinalSubCat=FinalSubCat(finalcat=thisCat, subcat_text=subcat_text, subcat_description=description)
        newFinalSubCat.save()
        thisSubCat=newFinalSubCat
    print(annotations_pk, flush=True)
    for annotation_pk in annotations_pk: # pks are for the targetAnnotation
        thisAnnot=TargetAnnotation.objects.get(pk=annotation_pk)
        thisAnnot.is_reviewed=True 
        thisAnnot.save()
        newRevAnnot=RevisedAnnotation(expert=expert, annotation=thisAnnot.annotation, finalcat=thisCat, finalsubcat=thisSubCat, revision_type=revision_type)
        newRevAnnot.save()
        result=updateRevisedBoxAnnotation(expert, thisAnnot, thisCat, thisSubCat, revision_type)
            
    return True

def saveApprove(expert, doctype, annot_dicts, cat_text, description, revision_type):  
    annotation_pks=[annot["annotation_pk"] for annot in annot_dicts]
    Revision(expert=expert, revision_type=revision_type, annotation_pks=annotation_pks).save()
     
    for annot in annot_dicts:
        annotation_pk=annot["annotation_pk"]
        subcat_text=annot["sugg_subcat"] 

        thisCats=FinalCat.objects.filter(expert=expert, cat_text=cat_text)
        if(len(thisCats)>0):
            thisCat=thisCats[0]
        else: 
            newFinalCat=FinalCat(expert=expert, doctype=doctype, cat_text=cat_text)
            newFinalCat.save()
            thisCat=newFinalCat

        thisSubCats=FinalSubCat.objects.filter(finalcat=thisCat, subcat_text=subcat_text)
        if(len(thisSubCats)>0):
            thisSubCat=thisSubCats[0]
        else: 
            newFinalSubCat=FinalSubCat(finalcat=thisCat, subcat_text=subcat_text, subcat_description=description)
            newFinalSubCat.save()
            thisSubCat=newFinalSubCat

        thisAnnot=TargetAnnotation.objects.get(pk=annotation_pk)
        thisAnnot.is_reviewed=True 
        thisAnnot.save()
        newRevAnnot=RevisedAnnotation(expert=expert, annotation=thisAnnot.annotation, finalcat=thisCat, finalsubcat=thisSubCat, revision_type=revision_type)
        newRevAnnot.save()
        result=updateRevisedBoxAnnotation(expert, thisAnnot, thisCat, thisSubCat, revision_type)
            
    return True


@csrf_exempt
def saveNAApprove(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        annot_dicts=query_json['annotation_pks']
        category_text=query_json['category']
        description=query_json['description']
        doctypetext=query_json['doctype']

        expert=User.objects.get(username=username)
        doctype=DocType.objects.get(doctype=doctypetext)


        result=saveApprove(expert, doctype,annot_dicts, category_text, description,'na-approve')
    
        na_suggestions=getNAs(doctype, expert)
        current_distribution=getDistn(doctype, expert)

        response={
            'na_suggestions': na_suggestions,
            'distribution': current_distribution
        }
        return JsonResponse(response)



@csrf_exempt
def saveNANew(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        annotation_pks=query_json['annotation_pks']
        category_text=query_json['category']
        subcategory_text=query_json['subcategory']
        description=query_json['description']
        doctypetext=query_json['doctype']

        expert=User.objects.get(username=username)
        doctype=DocType.objects.get(doctype=doctypetext)

        result=saveResolution(expert, doctype,annotation_pks, category_text, subcategory_text, description,'na-new')
    
        na_suggestions=getNAs(doctype, expert)
        current_distribution=getDistn(doctype, expert)

        response={
            'na_suggestions': na_suggestions,
            'distribution': current_distribution
        }
        return JsonResponse(response)

@csrf_exempt
def saveNAExisting(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        annotation_pks=query_json['annotation_pks']
        category_text=query_json['category']
        subcategory_text=query_json['subcategory']
        description=query_json['description']
        doctypetext=query_json['doctype']

        expert=User.objects.get(username=username)
        doctype=DocType.objects.get(doctype=doctypetext)

        result=saveResolution(expert, doctype,annotation_pks, category_text, subcategory_text, description,'na-existing')
    
        na_suggestions=getNAs(doctype, expert)
        current_distribution=getDistn(doctype, expert)

        response={
            'na_suggestions': na_suggestions,
            'distribution': current_distribution
        }
        return JsonResponse(response)

@csrf_exempt
def saveNAIgnore(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        annotation_pks=query_json['annotation_pks']
        category_text=query_json['category']
        subcategory_text=query_json['subcategory']
        description=query_json['description']
        doctypetext=query_json['doctype']

        expert=User.objects.get(username=username)
        doctype=DocType.objects.get(doctype=doctypetext)

        result=saveResolution(expert, doctype,annotation_pks, category_text, 'n/a', description,'na-ignore')
    
        na_suggestions=getNAs(doctype, expert)
        current_distribution=getDistn(doctype, expert)

        response={
            'na_suggestions': na_suggestions,
            'distribution': current_distribution
        }
        return JsonResponse(response)

@csrf_exempt
def saveCloseToApprove(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        annot_dicts=query_json['annotation_pks']
        category_text=query_json['category']
        description=query_json['description']
        doctypetext=query_json['doctype']

        expert=User.objects.get(username=username)
        doctype=DocType.objects.get(doctype=doctypetext)


        result=saveApprove(expert, doctype,annot_dicts, category_text, description,'ct-approve')
    
        ct_suggestions=getCTs(doctype, expert)
        current_distribution=getDistn(doctype, expert)

        response={
            'close_to_suggestions': ct_suggestions,
            'distribution': current_distribution
        }
        return JsonResponse(response)



@csrf_exempt
def saveCloseToNew(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        annotation_pks=query_json['annotation_pks']
        category_text=query_json['category']
        subcategory_text=query_json['subcategory']
        description=query_json['description']
        doctypetext=query_json['doctype']

        expert=User.objects.get(username=username)
        doctype=DocType.objects.get(doctype=doctypetext)

        result=saveResolution(expert, doctype,annotation_pks, category_text, subcategory_text, description,'ct-new')
    
        ct_suggestions=getCTs(doctype, expert)
        current_distribution=getDistn(doctype, expert)

        response={
            'close_to_suggestions': ct_suggestions,
            'distribution': current_distribution
        }
        return JsonResponse(response)

@csrf_exempt
def saveCloseToExisting(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        annotation_pks=query_json['annotation_pks']
        category_text=query_json['category']
        subcategory_text=query_json['subcategory']
        description=query_json['description']
        doctypetext=query_json['doctype']

        expert=User.objects.get(username=username)
        doctype=DocType.objects.get(doctype=doctypetext)

        result=saveResolution(expert, doctype,annotation_pks, category_text, subcategory_text, description,'ct-existing')
    
        ct_suggestions=getCTs(doctype, expert)
        current_distribution=getDistn(doctype, expert)

        response={
            'close_to_suggestions': ct_suggestions,
            'distribution': current_distribution
        }
        return JsonResponse(response)

@csrf_exempt
def saveCloseToIgnore(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        annotation_pks=query_json['annotation_pks']
        category_text=query_json['category']
        subcategory_text=query_json['subcategory']
        description=query_json['description']
        doctypetext=query_json['doctype']

        expert=User.objects.get(username=username)
        doctype=DocType.objects.get(doctype=doctypetext)

        result=saveResolution(expert, doctype,annotation_pks, category_text, 'n/a', description,'ct-ignore')
    
        ct_suggestions=getCTs(doctype, expert)
        current_distribution=getDistn(doctype, expert)

        response={
            'close_to_suggestions': ct_suggestions,
            'distribution': current_distribution
        }
        return JsonResponse(response)

@csrf_exempt
def changeCatText(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        doctypetext=query_json['doctype']
        old_cat=query_json['old_cat']
        new_cat=query_json['new_cat']

        expert=User.objects.get(username=username)
        doctype=DocType.objects.get(doctype=doctypetext)
        thisCat=FinalCat.objects.get(expert=expert, doctype=doctype,cat_text=old_cat)
        thisCat.cat_text=new_cat
        thisCat.save()
        return HttpResponse('')


@csrf_exempt
def changeSubCatText(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        doctypetext=query_json['doctype']
        cat=query_json['cat']
        old_subcat=query_json['old_subcat']
        new_subcat=query_json['new_subcat']

        expert=User.objects.get(username=username)
        doctype=DocType.objects.get(doctype=doctypetext)
        thisCat=FinalCat.objects.get(expert=expert, doctype=doctype,cat_text=cat)
        thisSubCat=FinalSubCat.objects.get(finalcat=thisCat, subcat_text=old_subcat)
        thisSubCat.subcat_text=new_subcat
        thisSubCat.save()
        return HttpResponse('')


@csrf_exempt
def changeSubCatDescription(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        doctypetext=query_json['doctype']
        cat=query_json['cat']
        subcat=query_json['subcat']
        new_description=query_json['new_description']

        expert=User.objects.get(username=username)
        doctype=DocType.objects.get(doctype=doctypetext)
        thisCat=FinalCat.objects.get(expert=expert, doctype=doctype,cat_text=cat)
        thisSubCat=FinalSubCat.objects.get(finalcat=thisCat, subcat_text=subcat)
        thisSubCat.subcat_description=new_description
        thisSubCat.save()
        return HttpResponse('')


@csrf_exempt
def moveSubCat(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        doctypetext=query_json['doctype']
        old_cat=query_json['old_cat']
        new_cat=query_json['new_cat']
        subcat=query_json['subcat']

        expert=User.objects.get(username=username)
        doctype=DocType.objects.get(doctype=doctypetext)
        oldCat=FinalCat.objects.get(expert=expert, doctype=doctype,cat_text=old_cat)
        newCat=FinalCat.objects.get(expert=expert, doctype=doctype,cat_text=new_cat) 
        
        thisSubCat=FinalSubCat.objects.get(finalcat=oldCat, subcat_text=subcat)
        thisSubCat.finalcat=newCat
        thisSubCat.save()

        if(len(FinalSubCat.objects.filter(finalcat=oldCat))==0):
            oldCat.delete()
        return HttpResponse('')

#path('add-cat/', views.addCat),

@csrf_exempt
def addCat(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        doctypetext=query_json['doctype']
        category_text=query_json['category']

        expert=User.objects.get(username=username)
        doctype=DocType.objects.get(doctype=doctypetext)
        newCat=FinalCat(expert=expert, doctype=doctype, cat_text=category_text)
        newCat.save()
        return HttpResponse('')

#    path('merge-cats/', views.mergeCats),

@csrf_exempt
def mergeCats(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        doctypetext=query_json['doctype']
        from_cat=query_json['from_cat']
        to_cat=query_json['to_cat']

        expert=User.objects.get(username=username)
        doctype=DocType.objects.get(doctype=doctypetext)

        fromCat=FinalCat.objects.get(expert=expert, doctype=doctype,cat_text=from_cat)
        toCat=FinalCat.objects.get(expert=expert, doctype=doctype,cat_text=to_cat)

        for subcat in FinalSubCat.objects.filter(finalcat=fromCat):
            subcat.finalcat=toCat
            subcat.save()

        fromCat.delete()
        return HttpResponse('')


#    path('merge-subcats/', views.mergeSubCats)
@csrf_exempt
def mergeSubCats(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        doctypetext=query_json['doctype']
        from_cat=query_json['from_cat']
        from_subcat=query_json['from_subcat']
        to_cat=query_json['to_cat']
        to_subcat=query_json['to_subcat']

        expert=User.objects.get(username=username)
        doctype=DocType.objects.get(doctype=doctypetext)

        fromCat=FinalCat.objects.get(expert=expert, doctype=doctype,cat_text=from_cat)
        fromSubCat=FinalSubCat.objects.get(finalcat=fromCat, subcat_text=from_subcat)

        toCat=FinalCat.objects.get(expert=expert, doctype=doctype,cat_text=to_cat)
        toSubCat=FinalSubCat.objects.get(finalcat=toCat, subcat_text=to_subcat)

        for box in RevisedBoxAnnotation.objects.filter(expert=expert, finalsubcat=fromSubCat):
            box.finalcat=toCat
            box.finalsubcat=toSubCat
            box.save()

        fromSubCat.delete()
        if(len(FinalSubCat.objects.filter(finalcat=fromCat))==0):
            fromCat.delete()
        return HttpResponse('')



@csrf_exempt
def getExamples(request):
    if request.method == 'GET':
        expert_id= request.GET['mturk_id']
        expert=User.objects.get(username=expert_id)
        doctypetext= request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        cat_text= request.GET['cat']
        subcat_text=request.GET['subcat']

        thisCat=FinalCat.objects.get(expert=expert, doctype=doctype, cat_text=cat_text)
        thisSubCat=FinalSubCat.objects.get(finalcat=thisCat, subcat_text=subcat_text)
        
        curBoxes=RevisedBoxAnnotation.objects.filter(expert=expert, finalsubcat=thisSubCat)
        docs=[]
        for curBox in curBoxes: # get max 6 docs
            doc=curBox.document
            docs=list(set(docs+[doc]))
            if(len(docs)>=6):
                break
        response=[]
        for doc in docs: 
            boxes=curBoxes.filter(document=doc)
            boxes_id=[box.box_id for box in boxes]
            response.append({
                'image_no': doc.doc_no, 
                'boxes_id': boxes_id
            })
        return JsonResponse(
            {'examples': response}
        )