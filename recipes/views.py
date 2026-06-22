from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Recipe
from .forms import RecipeForm

# Create your views here.

@login_required
def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

@login_required
def my_recipes(request):
    recipes = request.user.recipes.all()
    return render(request, 'recipes/my_recipes.html', {'recipes': recipes})

@login_required
def recipe_detail(request,pk):
    recipe = get_object_or_404(Recipe,pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

@login_required
def recipe_create(request):
    if request.method == 'POSt':
        form = RecipeForm(request.POST, request.FILE)
        
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            messages.success(request, 'Recipe uploaded successfully.')
            return redirect('recipe_detail',pk = recipe.pk)
    else:
        form = RecipeForm()
        
    context = {
        'form' : form,
        'title' : 'Upload Recipe',
        'button_text': 'Upload',
    }
    
    return render(request, 'recipes/recipe_form.html', context)

# @login_required
# def recipe_update(request,pk):
#     recipes = Recipe.objects.all()
#     return render(request, 'recipes/recipe_list.html', {'recipes': recipes})
