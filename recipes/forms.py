from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'subtitle',
            'ingredients',
            'instructions',
            'chefs_note',
            'cover_image',
        ]
        
class RecipeSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False,
         widget= forms.TextInput(attrs ={
                    'placeholder':'Search recipes by title or ingredient..',
                    'class':'search-input'
               }))
    def clean_query(self):
          query = self.cleaned_data.get('query')
          if query:
               query - query.strip()
               if len(query)<2:
                    raise forms.ValidationError('search term must be at least 2 characters.')
          return query