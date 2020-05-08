# pages/urls.py
from django.urls import path,include
from django.conf.urls import url
from .views import SignUpView
from . import views

author_patterns = ([
    path('author',views.author_base,name='author-profile'),
], 'author')

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('wherenext/', views.where_next),
    path('author',views.author_base,name='author-profile'),
    # path('author',include(author_patterns)),
    path('editor',views.editor_base,name='editor-profile'),

    path('author/post',views.post_tweet,name="author-post"),
    path('author/thankyou',views.thank_you,name="thank-you"),
    path('author/thankyou/<int:tweet_id>',views.tweet_detail,name="post-detail"),
    path('author/post/edit/<int:tweet_id>',views.post_tweet,name="author-post"),

    path('editor/list',views.list_tweets,name='editor-list'),
    path('editor/review/<int:tweet_id>',views.review_tweet,name='review_tweet'),
    # url(
    #     r'users/(?P<user_id>\w+)$',
    #     views.UserProfileView.as_view(),
    #     name='user_profile',
    # ),
    # path('', views.HomePageView.as_view(), name='home'),
    # # path('form',views.contact),
    # path('test',views.testing),         #SIGNUP
    # path('test_log',views.user_login,name='login'),    #LOGIN 
    # path('index', views.index, name='index'),          #Landing Page after login

]