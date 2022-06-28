from django.urls import path

from encyclopedia import views

urlpatterns = [
    
    path("<str:title>", views.entry, name ="entry")
  
 

]
