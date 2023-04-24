from django.urls import path
from .views import NewsList, PostDetail, NewsSearch, PostCreate, PostUpdate, PostDelete, subscribe, unsubscribe


urlpatterns = [
   path('', NewsList.as_view(), name='news'),
   path('<int:pk>', PostDetail.as_view(), name='post'),
   path('<int:pk1>/subscribe/<int:pk2>/', subscribe, name='subscribe'),
   path('<int:pk1>/unsubscribe/<int:pk2>/', unsubscribe, name='unsubscribe'),
   path('search/', NewsSearch.as_view(), name='news_search'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
