from django.urls import path
from default.views import * #import from views.py the class Index

urlpatterns = [ #always put .as_view() after the view name in url
    path('', Index.as_view(), name='index'),
    path('music', Music.as_view(), name='music'),
    path('learn', Learn.as_view(), name='learn'),
    path('quiz', Quiz.as_view(), name='quiz')
]
