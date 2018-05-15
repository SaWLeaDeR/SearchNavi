from django.urls import path

from . import views

app_name = 'solr'
urlpatterns = [
    # default view: /solr/ or /
    path(r'', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('query/', views.resultset, name='resultset'),
    path('searchtree/', views.searchtree, name='searchtree'),
    path('resultset2/', views.resultset2, name='resultset2'),
    path('query2/', views.resultset2, name='resultset2'),
]
