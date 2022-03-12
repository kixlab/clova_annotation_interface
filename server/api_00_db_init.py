import csv
from api.models import DocType, Document, InitCat, InitSubCat
# set initial categories and document sets before the annotation phase.


csv_path='db_init/db_init - doctype.csv'
csvfile=open(csv_path, 'r', encoding='utf8', errors='ignore')
reader=csv.reader(csvfile, delimiter=',')
next(reader, None)

DocType.objects.all().delete()

for row in reader:
    [doctype]=row
    doctype=DocType.objects.create(doctype=doctype)
    doctype.save()
    for i in range(1000):
        Document(doctype=doctype, doc_no=(i)).save()

csv_path='db_init/db_init - initcat.csv'
csvfile=open(csv_path, 'r', encoding='utf8', errors='ignore')
reader=csv.reader(csvfile, delimiter=',')
next(reader, None)
InitCat.objects.all().delete()
for row in reader:
    [doctype, cat_no, cat_text]=row
    print(row)
    doctype=DocType.objects.get(doctype=doctype)
    initcat=InitCat(doctype=doctype, cat_no=cat_no, cat_text=cat_text)
    initcat.save()

# add n/a to each doc category
for doctype in DocType.objects.all():
    InitCat(doctype=doctype, cat_no=99, cat_text='n/a').save()

csv_path='db_init/db_init - initsubcat.csv'
csvfile=open(csv_path, 'r', encoding='utf8', errors='ignore')
reader=csv.reader(csvfile, delimiter=',')
next(reader, None)
InitSubCat.objects.all().delete()

for row in reader:
    [doctype,initcat, subcat_no, subcat_text, subcat_description]=row
    #print(row)
    doctype=DocType.objects.get(doctype=doctype)
    initcat=InitCat.objects.get(doctype=doctype, cat_text=initcat)
    initsubcat=InitSubCat(initcat=initcat, subcat_no=subcat_no, subcat_text=subcat_text, subcat_description=subcat_description)
    initsubcat.save()

for cat in InitCat.objects.all():
    InitSubCat(initcat=cat, subcat_no=99, subcat_text='n/a', subcat_description='Not applicable').save()
