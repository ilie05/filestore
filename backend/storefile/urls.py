from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from storefile import views

urlpatterns = [
    path('', views.SnippetList.as_view()),
    path('<int:pk>', views.SnippetDetail.as_view()),
    path('/file', views.FileView.as_view()),
    path('/files', views.FilesView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
