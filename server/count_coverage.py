import csv
from api.models import *
from dashboard.models import * 

# python manage.py shell
# exec(open('count_coverage.py').read())

all_Profile=Profile.objects.filter(practice_done=True)
done_Profile=Profile.objects.filter(done=True)

blacklist=[
    'A16X5FB3HAFCKN',
    'A1EX0MEOPF8AHT',
    'A1IOMFFEKCWOIT',
    'A1XO6ONCCTBMKW',
    'A3QI1RV4HQ9MOC',
    'A3TUMZ954ORSUC',
    'A5LYLHG880ABE'
]

valid_Profile=[]
for profile in done_Profile:
    is_troller=False
    for bad in blacklist:
        print(bad, profile.user.username)
        if(bad in profile.user.username):
            is_troller=True
            break
    if not is_troller: 
        valid_Profile.append(profile)

print('number of done profiles:', len(done_Profile))
print('number of valid profiles:', len(valid_Profile))


done_users=[]
valid_users=[]
for profile in done_Profile:
    done_users.append(profile.user)

for profile in valid_Profile:
    valid_users.append(profile.user)

doc_nos=range(800)


def coverage(users):
    over=[]
    less=[]
    for doc_no in doc_nos: 
        document=Document.objects.get(doctype__doctype='receipt', doc_no=doc_no)
        done_statuses=Status.objects.filter(document=document, status=True)
        fin_statuses=[status for status in done_statuses if status.user in users]
        if(len(fin_statuses)>5):
            over.append({'doc_no': doc_no, 'count': len(fin_statuses)})
        elif(len(fin_statuses)<5):
            less.append({'doc_no': doc_no, 'count': len(fin_statuses)})
    
    print("over:", over)
    print("less:", less)

print('done users')
coverage(done_users)
print('valid usres')
coverage(valid_users)