import csv
from api.models import *
from dashboard.models import * 

# python manage.py shell
# exec(open('generate_raw_annotations.py').read())

RawAnnotation.objects.all().delete()

max_docno=210

for doc_no in range(max_docno):
    document=Document.objects.get(doctype__doctype='event', doc_no=doc_no)
    thisBoxAnnots=BoxAnnotation.objects.filter(document=document)
    cand_box_ids=list(set([box.box_id for box in thisBoxAnnots]))
    for box_id in cand_box_ids: 
        currBoxAnnots=thisBoxAnnots.filter(box_id=box_id)
        exactBoxAnnots=currBoxAnnots.filter(annot_type='exactly')
        if(len(currBoxAnnots)==len(exactBoxAnnots)):
            has_suggestion=False
        else:
            has_suggestion=True
        subcats=[ba.annotation.subcat for ba in currBoxAnnots]
        finsubcat=subcats[0]
        for subcat in subcats:
            if(subcats.count(subcat)>1):
                finsubcat=subcat
        newRawAnnot=RawAnnotation(document=document, subcat=finsubcat, box_id=box_id, has_suggestion=has_suggestion)
        newRawAnnot.save()
