from django import forms

from .models import Event


class CreateEventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['title', 'datetime', 'location', 'description', 'image', 'min_attendees', 'max_attendees',]
        

class EditEventForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = ['title', 'datetime', 'location', 'description', 'image', 'min_attendees', 'max_attendees',]
    
    def save(self, commit=True):
        event = self.instance
        event.title = self.cleaned_data['title']
        event.datetime = self.cleaned_data['datetime']
        event.location = self.cleaned_data['location']
        event.description = self.cleaned_data['description']
        event.min_attendees = self.cleaned_data['min_attendees']
        event.max_attendees = self.cleaned_data['max_attendees']

        if self.cleaned_data['image']:
            event.image = self.cleaned_data['image']
            
        if commit:
            event.save()
            
        return event
        