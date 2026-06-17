from django.db import models
from django.conf import settings

# Create your models here.

class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='recipes')
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200,blank=True)
    ingredients = models.TextField(help_text='List the ingredients here, each on a new line')
    instructions = models.TextField(help_text='List your step by step instructions here')
    chefs_note = models.TextField(blank=True,help_text='Optional tips or variations...')
    cover_image = models.ImageField(upload_to='recipe_covers/%Y/%m', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title