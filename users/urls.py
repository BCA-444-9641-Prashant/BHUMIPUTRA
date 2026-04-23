from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('change-password/<str:username>/', views.change_password, name='change_password'),
    path('logout/', views.logout_view, name='logout'),
    
    # Farmer URLs
    path('farmer/dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('farmer/farm-details/', views.farm_details, name='farm_details'),
    path('farmer/add-crop-sell/', views.add_crop_sell, name='add_crop_sell'),
    path('farmer/manage-crops/', views.manage_crops, name='manage_crops'),
    
    # Buyer URLs
    path('buyer/dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('buy-crops/', views.buy_crops, name='buy_crops'),
    path('crop-orders/', views.crop_orders, name='crop_orders'),
    path('create-crop-order/', views.create_crop_order, name='create_crop_order'),
    
    # Common URLs
    path('schemes/', views.scheme_view, name='scheme_view'),
    path('schemes/<int:pk>/', views.scheme_detail, name='scheme_detail'),
    path('crops/', views.crop_cards, name='crop_cards'),
    path('crops/<int:pk>/', views.crop_detail, name='crop_detail'),
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/rent/', views.rent_equipment, name='rent_equipment'),
    path('payment/razorpay/<int:order_id>/', views.razorpay_payment, name='razorpay_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failed/', views.payment_failed, name='payment_failed'),
    path('cart/', views.cart, name='cart'),
    path('order-history/', views.order_history, name='order_history'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/enroll/', views.enroll_course, name='enroll_course'),
    path('my-courses/', views.my_courses, name='my_courses'),
]
