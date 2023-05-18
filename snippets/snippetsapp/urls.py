# from django.urls import path # 与bili课不同，因版本差异，bili课是1.10版本
# from snippetsapp import views
#
# urlpatterns = [
#     path('snippets/', views.snippet_list),
#     path('snippets/<int:pk>/', views.snippet_detail), #此处也是和bili课差异较大，尤其int：pk那里
# ]


#
# from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns
# from snippetsapp import views
#
#
# urlpatterns = [
#     path('snippets/', views.snippet_list),
#     path('snippets/<int:pk>/', views.snippet_list),
# ]
#
# urlpatterns = format_suffix_patterns(urlpatterns)



from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippetsapp import views

urlpatterns = [
    path('snippets/', views.SnippetList.as_view(), name='snippet-list'),
    path('snippets/<int:pk>', views.SnippetDetail.as_view(), name='snippet-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)