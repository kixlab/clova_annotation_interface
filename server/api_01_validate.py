import csv
from api.models import *

doc_nos=range(800)
doctype=DocType.objects.get(doctype='event')

all_profiles=Profile.objects.filter(practice_done=True)

blacklist=[
]

valid_profiles=[]
for profile in all_profiles:
    is_troller=False
    for bad in blacklist:
        if(bad in profile.user.username):
            is_troller=True
            break
    if not is_troller: 
        valid_profiles.append(profile)

valid_users=[]
for profile in valid_profiles:
    valid_users.append(profile.user)

def ignore_over_five(users):
    over=[]
    less=[]
    for doc_no in doc_nos: 
        document=Document.objects.get(doctype=doctype, doc_no=doc_no)
        done_statuses=Status.objects.filter(document=document, status=True)
        fin_statuses=[status for status in done_statuses if status.user in users]
        count=0
        for stat in fin_statuses: 
            # for annotations with this status, set is_valid True 
            this_annots=Annotation.objects.filter(user=stat.user, document=stat.document, is_alive=True)
            for annot in this_annots:
                annot.is_valid=True
                annot.save()
            count=count+1
            if(count>=5):
                break

ignore_over_five(valid_users)