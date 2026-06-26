from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Recipe
from .forms import RecipeForm, RecipeSearchForm

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
def recipe_create(request,pk):
     recipe = get_object_or_404(Recipe, pk=pk)
     return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

@login_required
def recipe_update(request):
     if request.method == 'POST':
          form = RecipeForm(request.POST, request.FILES)

          if form.is_valid():
               recipe = form.save(commit=False)
               recipe.user = request.user
               recipe.save()
               messages.success(request, 'Recipe updated successfully!')
               return redirect('recipe_detail', pk=recipe.pk)
     else:
               form = RecipeForm()

     context = {
               'form': form,
               'title': 'Update Recipe',
               'button_text': 'Upload',
          }
     return render(request, 'recipes/recipe_form.html', context)


@login_required
def recipe_update(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    
    if recipe.user != request.user:
        messages.error(request, 'You are not authorized to edit this recipe.')
        return redirect('recipe_detail', pk=recipe.pk)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
    
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipe updated successfully!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
        context = {
            'form': form,
            'title': 'Update Recipe',
            'button_text': 'Update',
    }
    return render(request, 'recipes/recipe_form.html', context)

@login_required
def recipe_delete(request, pk):
     recipe = get_object_or_404(Recipe, pk=pk)

     if recipe.user != request.user:
          messages.error(request, 'You are not authorized to delete this recipe.')
          return redirect('recipe_detail', pk=pk)

     if request.method == 'POST':
            recipe.delete()
            messages.success(request, 'Recipe deleted successfully!')
            return redirect('recipe_list')
     
     return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})
 
@login_required
def recipe_search(request):
    form = RecipeSearchForm(request.GET or None)
    recipes = Recipe.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        
        if query:
            recipes = recipes.filter(
                Q(title__icontains = query) | Q(ingredients__icontains = query)
            )
    
    context = {
        'form':form,
        'recipes':recipes,
        'is_search':bool(request.GET)
    }

    return render(request, 'recipes/recipe_search.html', context)