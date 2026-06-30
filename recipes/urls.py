from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipe_list'),
    path('my_recipes/', views.MyRecipesView.as_view(), name='my_recipes'),
    path('create/', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('<int:pk>/edit/', views.RecipeUpdateView.as_view(), name='recipe_update'),
    path('<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='recipe_delete')
]