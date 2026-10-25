from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.main, name='main'),
    path("quote/", views.quote, name="quote"),
    path("author/", views.author, name="author"),
    path("author_detail/<str:fullname>", views.author_detail, name="author_detail"),
    path("scrap/", views.scrap, name="scrap"),
    path("tag/<str:tag>", views.tag, name="tag"),
]
