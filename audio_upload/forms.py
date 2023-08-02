from django import forms
from .models import Upload_audio
#DataFlair #File_Upload
class Profile_Form(forms.ModelForm):
    class Meta:
        model = Upload_audio
        fields = [
        'display_audio'
        ]
    labels = {
            'display audio': 'オーディオ選択'
        }