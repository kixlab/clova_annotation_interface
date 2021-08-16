from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import int_list_validator
from rest_framework.authtoken.models import Token


from api.models import *

class BoxAnnotation(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    document=models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    subcat=models.ForeignKey(InitSubCat, on_delete=models.CASCADE)
    cat=models.ForeignKey(InitCat, on_delete=models.CASCADE)
    annotation=models.ForeignKey(Annotation, on_delete=models.SET_NULL, null=True, blank=True)

    annot_type=models.CharField(max_length=255) #exactly, closeto, na 
    suggested_subcat=models.CharField(max_length=255, null=True, blank=True)

    box_id=models.IntegerField(default=999, null=True, blank=True)
    def __str__(self):
        return 'boxannot-'+self.user.username+'-'+str(self.document)+'-'+str(self.box_id)+'-'+self.annot_type

class TargetAnnotation(models.Model):
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
class FinalLabel(models.Model):
    expert=models.ForeignKey(User, on_delete=models.CASCADE)
    doctype=models.ForeignKey(DocType, on_delete=models.CASCADE)
    cat_text=models.CharField(max_length=225)
    subcat_text=models.CharField(max_length=225)
    def __str__(self):
        return 'newlabel-'+self.expert.username+'-'+self.cat_text+'-'+self.subcat_text

class RevisedAnnotation(models.Model):
    expert=models.ForeignKey(User, on_delete=models.CASCADE)
    document=models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    label=models.ForeignKey(FinalLabel, on_delete=models.SET_NULL, null=True)

    box_id=models.IntegerField(default=999, null=True, blank=True)
    revision_type=models.CharField(max_length=225) #na-approve, na-new, na-existing, ct-approve, ct-new, ct-ignore, 'auto'
    #is_alive=models.BooleanField(default=False)

class RawAnnotation(models.Model):
#    user=models.ForeignKey(User, on_delete=models.CASCADE)
    document=models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    subcat=models.ForeignKey(InitSubCat, on_delete=models.SET_NULL, null=True)
    box_id=models.IntegerField(default=999, null=True, blank=True)
    has_suggestion=models.BooleanField(default=False)
