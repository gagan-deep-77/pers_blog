from django.urls import path

from . import views
urlpatterns = [
    path("",views.home,name="home"),
    path("register",views.register_user,name="register-user"),
    path('home',views.home,name="home"),
    path("create-post",views.create_post,name="create-post"),
    path("delete-post/<int:pk>",views.delete_post,name="delete-post"),
    path("logout",views.logout_view,name="logout"),
    path("login",views.login_view,name="login"),
    path("viewPost/<int:pk>",views.view_post,name="view-post"),
    path("test",views.show_test,name="test"),
    path("test-home",views.show_test_home,name="test-home"),
    path("comp",views.show_comp,name="comp"),
    path("create",views.create_ref,name="create_ref"),
    path("like-post/<int:post_id>",views.like_post,name="like-post"),
    path("unlike-post/<int:post_id>",views.unlike_post,name="unlike-post"),
    path("test-view/<int:pk>",views.test_view,name="test-view"),
    path("private-home",views.private_home,name="private-home"),
    path("make-public/<int:pk>",views.make_public,name="make-public"),
    path("make-private/<int:pk>",views.make_private,name="make-private")
]