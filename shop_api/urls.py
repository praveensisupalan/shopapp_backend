from django.urls import path
from .views import Shop_view, SignUpView, LoginView, LogoutView, Shop_Detail_View, Shop_Delete_View

urlpatterns = [
    path("shops/",Shop_view.as_view(),name="add_shope"),
    path('user/create/',SignUpView.as_view(),name="create_user"),
    path('user/login/',LoginView.as_view(),name="login"),
    path('user/logout/',LogoutView.as_view(),name="logout"),
    path('shops/<int:id>/',Shop_Detail_View.as_view(),name="shop_detail"),
    path('shops/delete/<int:id>/',Shop_Delete_View.as_view(),name="shop_delete")
]
