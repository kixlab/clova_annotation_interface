import csv
from api.models import *

# python manage.py shell
# exec(open('api_generate_box_annotations.py').read())

doctype=DocType.objects.get(doctype='event')

BoxAnnotation.objects.filter(document__doctype=doctype).delete()

annotations=Annotation.objects.filter(document__doctype=doctype, is_alive=True, is_valid=True)
print('all annots total', len(Annotation.objects.filter(document__doctype=doctype, is_alive=True))) #83393
print('valid annots total', len(annotations)) #45737
cur=0
for annotation in annotations: 
    cur=cur+1
    if(cur%100==0):
        print(cur)
    user=annotation.user
    profile=Profile.objects.get(user=user)
    document=annotation.document
    subcat=annotation.subcat
    cat=annotation.cat
    boxes_id=annotation.boxes_id.replace(',', ' ').replace('[', ' ').replace(']', ' ').split()
    if(annotation.confidence):
        annot_type='exactly'
        suggested_subcat=''
    else:
        suggestion=SelectedSuggestion.objects.filter(annotation=annotation)
        suggested_subcat=''
        if(len(suggestion)>0):
            suggsted_subcat=suggestion[0].suggestion.suggested_subcat 

        if(annotation.subcat.subcat_text=='n/a'):
            annot_type='na'
        else: 
            annot_type='closeto'
    for box_id in boxes_id:
        newBox=BoxAnnotation(user=user, document=document, subcat=subcat, cat=cat, annotation=annotation, annot_type=annot_type, suggested_subcat=suggested_subcat, 
        box_id=box_id)
        newBox.save()