from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView, 
    FormView,
)
from .models import Recipe
from .forms import RecipeForm, RecipeSearchForm

# Create your views here.

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    login_url = reverse_lazy('login')

class MyRecipesView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return self.request.user.recipes.all()

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'
    login_url = reverse_lazy('login')
    pk_url_kwarg = 'pk'

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Upload Recipe'
        context['button_text'] = 'Upload'
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Recipe uploaded.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    login_url = reverse_lazy('login')

    def test_func(self):
        recipe = self.get_object()
        return recipe.user == self.request.user

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipe_list')
    login_url = reverse_lazy('login')

    def test_func(self):
        recipe = self.get_object()
        return recipe.user == self.request.user

# @login_required
# def recipe_detail(request, pk):
#     recipe = get_object_or_404(Recipe, pk=pk)
#     return render(request, 'recipes/recipe_detail.html', {'recipe':recipe})


# @login_required
# def recipe_create(request):

#     if request.method == 'POST':
#         form = RecipeForm(request.POST, request.FILES)
        
#         if form.is_valid():
#             recipe = form.save(commit=False)
#             recipe.user = request.user

#             recipe.save()
#             messages.success(request, 'Recipe uploaded.')
#             return redirect('recipe_detail', pk=recipe.pk)
#     else:
#         form = RecipeForm()
#         context = {
#             'form' : form,
#             'title' : 'Upload Recipe',
#             'button_text' : 'Upload',
#         }
#     return render(request, 'recipes/recipe_form.html', context)

# @login_required
# def recipe_update(request, pk):
#     recipe = get_object_or_404(Recipe, pk=pk)
#     if recipe.user != request.user:
#         messages.error(request, "You cannot edit another user's recipe.")
#         return redirect('recipe_detail', pk=pk)
#     if request.method == 'POST':
#         form = RecipeForm(request.POST, request.FILES, instance=recipe)
        
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Recipe updated successfully")
#             return redirect('recipe_detail', pk=recipe.pk)
#     else:
#         form = RecipeForm(instance=recipe)
#         context = {
#             'form' : form,
#             'title' : 'Upload Recipe',
#             'button_text' : 'Upload',
#         }
#     return render(request, 'recipes/recipe_form.html', context)


# @login_required
# def recipe_delete(request, pk):
#     recipe = get_object_or_404(Recipe, pk=pk)

#     if recipe.user != request.user:
#         messages.error("You can't delete a recipe you don't own.")
#         return redirect('recipe_detail', pk=pk)
    
#     if request.method == 'POST':
#         recipe.delete()
#         messages.success("Recipe deleted successfullly.")
#         return redirect('recipe_list')
    
#     return render(request, 'recipes/recipe_confirm_delete.html', {'recipe':recipe})

@login_required
def recipe_search(request):
    form = RecipeSearchForm(request.GET or None)
    recipes = Recipe.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            recipes = recipes.filter(
                Q(title__icontains=query) |
                Q(ingredients__icontains=query)
            )

    context = {
        'form': form,
        'recipes': recipes,
        'is_search': bool(request.GET)
    }
    return render(request, 'recipes/recipe_search.html', context)