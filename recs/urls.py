from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('artistrec/', views.artistrec, name='artistrec'),
    path('artistrec/search/', views.searchArtist, name='searchartist'),
    path('trackrec/', views.trackrec, name='trackrec'),
    path('trackrec/search/', views.searchTrack, name='searchtrack'),
    path('genrerec/', views.genrerec, name='genrerec'),
    path('recs', views.recResults, name='recresults')
]