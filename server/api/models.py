from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_comma_separated_integer_list
from django.core.validators import int_list_validator



class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    signuptime=models.DateTimeField(auto_now_add=True, blank=True)
    
    doctype=models.ForeignKey('DocType', on_delete=models.CASCADE)
    user_order=models.IntegerField(default=0)
    mod_order=models.IntegerField(default=0, blank=True, null=True)
    
    consent_agreed=models.BooleanField(default=False)
    instr_done=models.BooleanField(default=False)
    practice_done=models.BooleanField(default=False)
    annotation_done=models.BooleanField(default=False)
    review_done=models.BooleanField(default=False)
    survey_done=models.BooleanField(default=False)

    practice_starttime=models.DateTimeField(blank=True, null=True)
    practice_endtime=models.DateTimeField(blank=True, null=True)
    annot_endtime=models.DateTimeField(blank=True, null=True)
    review_endtime=models.DateTimeField(blank=True, null=True)
    survey_endtime=models.DateTimeField(blank=True, null=True)

    dropout=models.BooleanField(default=False)

    done=models.BooleanField(default=False)
    token=models.CharField(max_length=50, default='coffee chocolate black tea')

    def __str__(self):
        return self.user.username + '-'+self.doctype.doctype

@receiver(post_save, sender=User)
def create_user_profile(sender, instance,created, **kwargs):
    if created:
        doctype=DocType.objects.get(doctype='receipt')
        Profile.objects.create(user=instance, doctype=doctype)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Label(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imageID = models.IntegerField()
    groupID = models.IntegerField()
    boxIDs = models.TextField(validators=[validate_comma_separated_integer_list])
    label = models.CharField(max_length = 255)


class DocType(models.Model):
    doctype=models.CharField(max_length=250)
    def __str__(self):
        return self.doctype

class Document(models.Model):
    doctype=models.ForeignKey('DocType', on_delete=models.CASCADE)
    doc_no=models.IntegerField(default=999)
    def __str__(self):
        return self.doctype.doctype+"-"+str(self.doc_no)

class InitCat(models.Model):
    doctype=models.ForeignKey('DocType', on_delete=models.CASCADE)
    cat_no=models.IntegerField()
    cat_text=models.CharField(max_length=255)
    def __str__(self):
        return self.doctype.doctype+"-"+str(self.cat_no)+'-'+str(self.cat_text)


class InitSubCat(models.Model):
    initcat=models.ForeignKey('InitCat', on_delete=models.CASCADE)
    subcat_no=models.IntegerField()
    subcat_text=models.CharField(max_length=255)
    subcat_description=models.CharField(max_length=255)
    def __str__(self):
        return str(self.subcat_no)+'-'+str(self.subcat_text)

class UserSuggestion(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    subcat=models.ForeignKey('InitSubCat', on_delete=models.CASCADE)
    suggested_subcat=models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.user.username+'-'+str(self.subcat) + '-'+str(self.suggested_subcat)

class SelectedSuggestion(models.Model): # 각 issue! 
    suggestion=models.ForeignKey('UserSuggestion', on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    annotation=models.ForeignKey('Annotation', on_delete=models.CASCADE)
    reason=models.TextField(max_length=255, default="No reason", null=True, blank=True)
    def __str__(self):
        return self.user.username+'-'+str(self.suggestion)


class AssignedSuggestion(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    my_suggestion=models.ForeignKey(UserSuggestion, on_delete=models.CASCADE)
    others=models.ForeignKey(SelectedSuggestion, on_delete=models.CASCADE)
    is_reviewed=models.BooleanField(default=False, null=False)

class Similarity(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    mine=models.ForeignKey(SelectedSuggestion, on_delete=models.CASCADE, related_name='mine')
    others=models.ForeignKey(SelectedSuggestion, on_delete=models.CASCADE, related_name='others')
    is_similar=models.BooleanField(default=False, null=False)

class Annotation(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    document=models.ForeignKey('Document', on_delete=models.SET_NULL, null=True)
    boxes_id=models.TextField(validators=[validate_comma_separated_integer_list], null=True)
    subcat = models.ForeignKey('InitSubCat', on_delete=models.CASCADE, null=True)
    cat= models.ForeignKey('InitCat', on_delete=models.CASCADE, null=True)
    confidence=models.BooleanField(null=True, default=True)
    is_alive=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username+'-'+str(self.document)+'-'+str(self.boxes_id)+'-'+self.cat.cat_text+'-'+self.subcat.subcat_text

class Memo(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    doctype=models.ForeignKey('DocType', on_delete=models.CASCADE)
    text=models.CharField(max_length=99999)

    def __str__(self):
        return 'memo-'+self.user.username+'-'+self.doctype.doctype

class Status(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    document=models.ForeignKey('Document', on_delete=models.SET_NULL, null=True)
    status=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username+'-'+str(self.document)+'-'+str(self.status)


class Image(models.Model):
    image_id = models.CharField(max_length=256, primary_key=True)
    image = models.ImageField(upload_to='resume/', null=True, blank=True)
    is_done = models.BooleanField(default=False)

class Json(models.Model):
    json_id = models.CharField(max_length=256, primary_key=True)
    json = models.FileField(upload_to="resume/")

