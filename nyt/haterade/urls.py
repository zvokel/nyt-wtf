from django.urls import path

from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path('wordle/', views.wordle, name="wordle"),
    path('spelling-bee/', views.spelling_bee, name="spelling_bee"),
    path('connections/', views.connections, name='connections'),
    path('sudoku/', views.sudoku, name='sudoku'),
    path('strands/', views.strands, name='strands'),
    path('', views.index, name="index"),
]