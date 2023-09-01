from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView,PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView,PasswordResetCompleteView
from .forms import ResetPasswordForm, NewPasswordForm

from . import views

urlpatterns = [

    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('register/',views.UserRegister.as_view(),name='register'),
    path('profile/',views.Profile.as_view(),name='profile'),
    path('address/',views.AddressUser.as_view(),name='address'),
    path('deladdress/<str:pk>/',views.DelAddress.as_view(),name='deladdress'),

    path('password-change/',views.passwordChange.as_view(),name='password-change'),
    path('password-change-done/',views.passwordchangedone.as_view(),name='password-change-done'),

    path('password-reset-view/',PasswordResetView.as_view(template_name='base/password_reset_form.html',form_class=ResetPasswordForm),name='password_reset_view'),
    path('password-reset-done/',PasswordResetDoneView.as_view(template_name='base/password_reset_done.html',),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name='base/password_reset_confirm.html',form_class=NewPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='base/password_reset_complete.html'),name='password_reset_complete'),


    path('',views.home,name='home'),
    path('food-details/<str:pk>/',views.productDetail,name='details'),
    path('bookatble/',views.BookATable.as_view(),name='book'),
    path('menu/',views.foodMenu,name='menu'),
    path('chefs/',views.chefs,name='chefs'),
    path('contact/',views.contactUS,name='contact'),

    path('add_to_cart/',views.addtocart,name='add-to-cart'),
    path('buy/',views.buy_now,name='buy'),
    path('cart/',views.cart,name='cart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('checkout/',views.checkout,name='checkout'),
    path('paymentdone/',views.payment_done,name='paymentdone'),
    path('orders/',views.orders,name='orders'),
    path('search/',views.search,name='search'),
    path('news/',views.newsLetter,name='news')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)