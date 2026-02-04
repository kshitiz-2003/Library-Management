from .models import Book
from django import forms
class BookForm(forms.ModelForm):
    class Meta:
        model=Book
        fields='__all__'
        widgets = {
            'published_date':forms.DateInput(attrs={'type':'date'}),
        }