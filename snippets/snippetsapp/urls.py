from django.urls import path # 与bili课不同，因版本差异，bili课是1.10版本
from snippetsapp import views

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail), #此处也是和bili课差异较大，尤其int：pk那里
]