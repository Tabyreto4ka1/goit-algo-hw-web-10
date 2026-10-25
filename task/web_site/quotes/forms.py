from django.forms import ModelForm, CharField, TextInput, DateField
from .models import Quote, Author


class QuoteForm(ModelForm):
    tags=CharField( required=True, widget=TextInput())
    quote = CharField(min_length=5, required=True, widget=TextInput())
    
    class Meta:
        model = Quote
        fields = ["tags", "quote", "author"]

class AuthorForm(ModelForm):
    fullname=CharField(min_length=5,widget=TextInput())
    born_date=DateField(input_formats=['%B %d, %Y'])
    born_location=CharField(max_length=200)
    description=TextInput()

    class Meta:
        model=Author
        fields=["fullname", "born_date", "born_location", "description"]