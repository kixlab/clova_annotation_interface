import csv
from api.models import *
from dashboard.models import * 

# python manage.py shell
# exec(open('generate_box_annotations.py').read())


BoxAnnotation.objects.all().delete()

annotations=Annotation.objects.filter(is_alive=True)

annotations=annotations[0:500]


for annotation in annotations: 
    user=annotation.user
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