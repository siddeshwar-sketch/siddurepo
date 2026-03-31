from django.urls import path
from .views import CreateRazorpayOrderView, VerifyRazorpayPaymentView

urlpatterns = [
    path('create-order/', CreateRazorpayOrderView.as_view(), name='create-razorpay-order'),
    path('verify-payment/', VerifyRazorpayPaymentView.as_view(), name='verify-razorpay-payment'),
]
