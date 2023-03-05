from django import forms
from apps.product.models import Product, Banner
from ckeditor.widgets import CKEditorWidget


class BannerFrom(forms.ModelForm):
    desc = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Banner
        fields = '__all__'
