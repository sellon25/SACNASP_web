from django.urls import path
from . import views

urlpatterns = [
    path('', views.university_list, name='university_list'),
    path('qualification-names/', views.qualification_names, name='qualification_names'),
    path('results/', views.results, name='results'),
    path('results-page/', views.results_page, name='results_page')
]
