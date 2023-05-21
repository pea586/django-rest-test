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



# from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns
# from snippetsapp import views
#
# urlpatterns = [
#     path('snippets/', views.SnippetList.as_view(), name='snippet-list'),
#     path('snippets/<int:pk>', views.SnippetDetail.as_view(), name='snippet-detail'),
#
#     path('users/', views.UserList.as_view(), name='user-list'),
#     path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
#
#     path('snippets/<int:pk>/highlight', views.SnippetHighlight.as_view(), name='snippet-highlight'),
# # 此行/highlight/是地址栏里需要输入的后缀
#
#     path('', views.api_root),
# ]
#
# urlpatterns = format_suffix_patterns(urlpatterns)

#
#
# from snippetsapp.views import SnippetViewSet, UserViewSet, api_root
# from rest_framework import renderers
#
# from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns
#
#
#
# snippet_list = SnippetViewSet.as_view({
#     'get': 'list',
#     'post':'create'
# })
#
# snippet_detail = SnippetViewSet.as_view({
#     'get':'retrieve',
#     'put':'update',
#     'patch':'partial_update', # 后面partial update不能更改，是固定搭配
#     'delete':'destroy'
# })
#
# snippet_highlight = SnippetViewSet.as_view({
#     'get':'highlight'
# }, renderer_classes=[renderers.StaticHTMLRenderer])
#
# user_list = UserViewSet.as_view({
#     'get':'list'
# })
#
# user_detail = UserViewSet.as_view({
#     'get':'retrieve'
# })
#
#
#
# urlpatterns = format_suffix_patterns([
#     path('', api_root),
#     path('snippets/', snippet_list, name='snippet-list'),
#     path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'), # <>后面的/最好加上，这是地址栏的输入显示。否则可能因少输入/而报错
#     path('snippets/<int:pk>/highlight', snippet_highlight, name='snippet-highlight'),
#     path('users/', user_list, name='user-list'),
#     path('users/<int:pk>/', user_detail, name='user-detail')
# ])


from django.urls import path, include
from snippetsapp import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter() # router是第五级的特色（bili老师归为5类，第5类最高，通常使用3,4级
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]