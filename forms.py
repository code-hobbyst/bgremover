from django import forms
from .models import ProcessedImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ProcessedImage
        fields = ['original_image']
        widgets = {
            'original_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }