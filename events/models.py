from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import datetime

# from account.models import Account

def upload_location(instance, filename, **kwargs):
    file_path = 'events/{host_id}/{filename}'.format(
        host_id=str(instance.host.id), filename=filename
    )
    return file_path

class Event(models.Model):
    title           = models.CharField(max_length=50)
    datetime        = models.DateTimeField()
    location        = models.CharField(max_length=100)
    description     = models.TextField(max_length=200)
    image           = models.ImageField(upload_to=upload_location)
    host            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # attendees       = models.ManyToManyField(Account)
    min_attendees   = models.IntegerField()
    max_attendees   = models.IntegerField()
    
    
    def __str__(self):
        return self.title
    
    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.now():
            raise ValidationError("The date cannot be in the past!")
        return date
        
@receiver(models.signals.post_delete, sender=Event)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)
    
    
    