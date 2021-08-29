import csv
from api.models import *

# python manage.py shell
# exec(open('ignore_over_five.py').read())

doc_nos=range(800)
doctype=DocType.objects.get(doctype='event')

all_profiles=Profile.objects.filter(practice_done=True)

blacklist_full=[
    'A16X5FB3HAFCKN',
    'A1EX0MEOPF8AHT',
    'A1IOMFFEKCWOIT',
    'A1XO6ONCCTBMKW',
    'A3QI1RV4HQ9MOC',
    'A3TUMZ954ORSUC',
    'A5LYLHG880ABE'
]


blacklist=[
    'A16X5',
    'A1EX0',
    'A1IOM',
    'A1XO6',
    'A3QI1',
    'A3TUM',
    'A5LYL'
]

valid_profiles=[]
for profile in all_profiles:
    is_troller=False
    for bad in blacklist:
        #print(bad, profile.user.username)
        if(bad in profile.user.username):
            is_troller=True
            break
    if not is_troller: 
        valid_profiles.append(profile)

print('number of valid profiles:', len(valid_profiles))

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