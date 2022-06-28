from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("addentry", views.add_entry, name= "addentry"),
     path("randomentry", views.random_entry, name= "randomentry"),
    path("searchresult",views.search, name="searchresult"),
    path("edit",views.edit, name="edit"),
    path("editentry",views.edit_entry, name="editentry"),
    
]
