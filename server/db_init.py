import csv
from api.models import DocType, Document, InitCat, InitSubCat
# python manage.py shell
# exec(open('db_init.py').read())



csv_path='db_init/db_init - doctype.csv'
csvfile=open(csv_path, 'r', encoding='utf8', errors='ignore')
reader=csv.reader(csvfile, delimiter=',')
next(reader, None)

DocType.objects.all().delete()

for row in reader:
    [doctype]=row
    doctype=DocType.objects.create(doctype=doctype)
    doctype.save()
    for i in range(20):
        Document(doctype=doctype, doc_no=(i+1)).save()

print('Hi')
csv_path='db_init/db_init - initcat.csv'
csvfile=open(csv_path, 'r', encoding='utf8', errors='ignore')
reader=csv.reader(csvfile, delimiter=',')
next(reader, None)
InitCat.objects.all().delete()
for row in reader:
    [doctype, cat_no, cat_text]=row
    doctype=DocType.objects.get(doctype=doctype)
    initcat=InitCat(doctype=doctype, cat_no=cat_no, cat_text=cat_text)
    initcat.save()

csv_path='db_init/db_init - initsubcat.csv'
csvfile=open(csv_path, 'r', encoding='utf8', errors='ignore')
reader=csv.reader(csvfile, delimiter=',')
next(reader, None)

InitSubCat.objects.all().delete()

for row in reader:
    [doctype,initcat, subcat_no, subcat_text, subcat_description]=row
    doctype=DocType.objects.get(doctype=doctype)
    initcat=InitCat.objects.get(doctype=doctype, cat_text=initcat)
    initsubcat=InitSubCat(initcat=initcat, subcat_no=subcat_no, subcat_text=subcat_text, subcat_description=subcat_description)
    initsubcat.save()