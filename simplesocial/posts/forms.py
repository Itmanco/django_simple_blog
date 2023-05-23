from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('message', 'image', 'group')

    widgets = {
        'message': forms.Textarea(attrs={'class': 'form-control'}),
        'image': forms.FileInput(attrs={'class': 'form-control'}),
        'group': forms.Select(attrs={'class': 'form-control'})
    }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['message'].label = ""



