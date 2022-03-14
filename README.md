# Annotation and Resolution Interface
This interface is used as a part of the funded project with Clova, to receive label suggestions from annotators during the annotation stage.

## Structure
* Frontend (`/front`): Vue.js
* Backend (`/server`) : Django + PostgreSQL

## Server Setup
* Assume that  `docker` and `docker-compose` are installed.
* Whenever `server/Dockerfile` is updated, run `docker-compose build`!

```
docker-compose up 
```
* `-d` option : running server on background

## Migration & Create admin

```
docker-compose exec server python manage.py makemigrations
docker-compose exec server python manage.py migrate
```
will reflect the updates in `models.py`.

```
docker-compose exec server python manage.py createsuperuser
```
helps creating an admin account.

## Server Off
```
docker-compose down 
```

# Data Pre/Post-processing 

## Initialize the Document and Labels
* Initialize the documents and labels before the annotation phase. 
* Edit the .csv files in `server/db_init/` so that each .csv file contains the document types, initial categories and subcategories. 
* Get into the docker container.
* Generate the initial label set and document objects.  
``` 
python manage.py shell
exec(open('api_00_db_init.py').read())
``` 

## Validate the Annotations
* Edit `server/api_01_validate.py` to set up validation condition for each annotation. 
* For the valid annotation objects, make sure to set `is_valid` field `True`, and update.  
* Update the Annotation objects by running below lines in the docker container. 
``` 
python manage.py shell
exec(open('api_01_validate.py').read())
``` 

## Annotation Data Processing for the Resolution Phase - Conversion into BoxAnnotation
* Annotations can have different boxes scopes for the same content (e.g., one annotator can group 'July 2nd, 2022' and label 'datetime' while another can annotate 'July' as 'month', '2nd' as 'date', and '2022' as 'year').
* In Resolution interface, the expert's operation will be saved by each box, as the expert will give only one final label to each box (e.g., 'July' as 'month'). 
* Therefore, we convert the Annotations into multiple BoxAnnotations that each object has only one box. To convert, run the following snippets. 
``` 
python manage.py shell
exec(open('api_02_generate_box_annotations.py').read())
``` 

## Annotation Data Processing for the Resolution Phase - Grouping the Suggestions 
* Edit `server/api_03_group_suggestions.py` to define similarity scores and threshold for grouping. 
* Based on the adjusted similarity score and threshold, group the suggestions by running the followings. 
``` 
python manage.py shell
exec(open('api_03_group_suggestions.py').read())
``` 

## Initialize the BoxAnnotation Objects for the Resolution Phase 
* Note that there can exist multiple BoxAnnotation objects on the same box but with different label. 
* To make the initial annotation dataset that expert user can start the resolution phase with, we make RawBoxAnnotation objects. The RawBoxAnnotation objects are duplicate-free version of the BoxAnnotation objects. The RawBoxAnnotation contains only one object for each box, and the label is determined by the majority voting on the labels on the box in the BoxAnnotation objects. 
* The following code will generate RawBoxAnnotation objects. 
``` 
python manage.py shell
exec(open('dashboard_generate_raw_box_annotation.py').read())
``` 

