import csv
from api.models import *
from dashboard.models import * 

# python manage.py shell
# exec(open('dashboard_generate_raw_box_annotations.py').read())

def most_frequent(List):
    return max(set(List), key = List.count)
 

RawBoxAnnotation.objects.all().delete()

max_docno=800
doctypes=['event']

for doctype in doctypes: 
    for doc_no in range(max_docno):
        documents=Document.objects.filter(doctype__doctype=doctype, doc_no=doc_no)
        if(len(documents)>0):
            document=documents[0]
            thisBoxAnnots=BoxAnnotation.objects.filter(document=document)
            cand_box_ids=list(set([boxAnnot.box_id for boxAnnot in thisBoxAnnots]))
            for box_id in cand_box_ids: 
                currBoxAnnots=thisBoxAnnots.filter(box_id=box_id)
                subcats=[ba.annotation.subcat for ba in currBoxAnnots]
                mv_subcat=most_frequent(subcats)
                newRawAnnot=RawBoxAnnotation(document=document, initcat=mv_subcat.initcat, initsubcat=mv_subcat, box_id=box_id)
                newRawAnnot.save()