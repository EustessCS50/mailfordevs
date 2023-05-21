from django.urls import path

from . import views

urlpatterns = [
    path('', views.homePage, name='home'),
    path('mails/', views.user_mails, name='user-mails'),
    path('mails/<str:pk>/detail/', views.mail_detail, name='mail-detail'),
    path('mails/<str:pk>/reply/', views.reply_mail, name='mail-reply'),
    path('account/', views.accounts, name='accounts'),
    path('dev/', views.userProfile, name='dev'),
    path('docs/', views.docs, name="docs"),
    path('config/<str:username>/', views.viewUpdateConfig, name='edit_config'),
    path('testmail/', views.testmail, name='testmail'),
    path('support_ticket/', views.contact, name='contact'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    # path("", views.PostListCreateView.as_view(), name="list_posts"),
    # path(
    #     "<int:pk>/",
    #     views.PostRetrieveUpdateDeleteView.as_view(),
    #     name="post_detail",
    # ),
    # path("current_user/", views.get_mails_for_current_user, name="current_user"),
    # path(
    #     "posts_for/",
    #     views.ListPostsForAuthor.as_view(),
    #     name="posts_for_current_user",
    # ),
]


# Eustess B
