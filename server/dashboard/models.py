from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import int_list_validator
from rest_framework.authtoken.models import Token


from api.models import *

class TargetAnnotation(models.Model):
    expert=models.ForeignKey(User, on_delete=models.CASCADE, related_name='expert_users')
    doctype=models.ForeignKey(DocType, on_delete=models.CASCADE, null=True)
    annotation=models.ForeignKey(GroupedAnnotation, on_delete=models.SET_NULL, null=True, blank=True)
    is_reviewed=models.BooleanField(default=False)

    def __str__(self):
        return 'targetannot-'+self.expert.username
""" 
class TargetBoxAnnotation(models.Model):
    expert=models.ForeignKey(User, on_delete=models.CASCADE, related_name='expert_users')
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_users')
    document=models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    subcat=models.ForeignKey(InitSubCat, on_delete=models.CASCADE)
    cat=models.ForeignKey(InitCat, on_delete=models.CASCADE)
    annotation=models.ForeignKey(Annotation, on_delete=models.SET_NULL, null=True, blank=True)

    annot_type=models.CharField(max_length=255) #exactly, closeto, na 
    suggested_subcat=models.CharField(max_length=255, null=True, blank=True)

    box_id=models.IntegerField(default=999, null=True, blank=True)
    is_reviewed=models.BooleanField(default=False)
    def __str__(self):
        return 'boxannot-'+self.expert.username+'-'+str(self.document)+'-'+str(self.box_id)+'-'+self.annot_type
 """

class FinalCat(models.Model):
    expert=models.ForeignKey(User, on_delete=models.CASCADE)
    doctype=models.ForeignKey(DocType, on_delete=models.CASCADE, null=True)
    cat_text=models.CharField(max_length=255)
    def __str__(self):
        return str(self.expert)+'-'+str(self.cat_text)

class FinalSubCat(models.Model):
    finalcat=models.ForeignKey(FinalCat, on_delete=models.CASCADE)
    subcat_text=models.CharField(max_length=255)
    subcat_description=models.CharField(max_length=255)
    def __str__(self):
        return str(self.finalcat.expert)+'-'+str(self.subcat_text)

class FinalLabel(models.Model):
    expert=models.ForeignKey(User, on_delete=models.CASCADE)
    doctype=models.ForeignKey(DocType, on_delete=models.CASCADE)
    cat_text=models.CharField(max_length=225)
    subcat_text=models.CharField(max_length=225)
    def __str__(self):
        return 'newlabel-'+self.expert.username+'-'+self.cat_text+'-'+self.subcat_text

class RevisedAnnotation(models.Model):
    expert=models.ForeignKey(User, on_delete=models.CASCADE)
    annotation=models.ForeignKey(GroupedAnnotation, on_delete=models.SET_NULL, null=True)
    finalcat=models.ForeignKey(FinalCat, on_delete=models.SET_NULL, null=True)
    finalsubcat=models.ForeignKey(FinalSubCat, on_delete=models.SET_NULL, null=True)
    revision_type=models.CharField(max_length=225) #na-new, na-existing, auto-mv


class RawBoxAnnotation(models.Model): ## same for each user 
    document=models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    initcat=models.ForeignKey(InitCat, on_delete=models.SET_NULL, null=True)
    initsubcat=models.ForeignKey(InitSubCat, on_delete=models.SET_NULL, null=True)
    box_id=models.IntegerField(default=999)


class RevisedBoxAnnotation(models.Model):
    expert=models.ForeignKey(User, on_delete=models.CASCADE)
    document=models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    finalcat=models.ForeignKey(FinalCat, on_delete=models.SET_NULL, null=True)
    finalsubcat=models.ForeignKey(FinalSubCat, on_delete=models.SET_NULL, null=True)
    box_id=models.IntegerField(default=999)
    revision_type=models.CharField(max_length=225) #na-new, na-existing, auto-mv


class Revision(models.Model):
    expert=models.ForeignKey(User, on_delete=models.CASCADE)
    revision_type=models.CharField(max_length=255)
    annotation_pks=models.TextField(validators=[validate_comma_separated_integer_list], null=True) #pks for TargetAnnotation 