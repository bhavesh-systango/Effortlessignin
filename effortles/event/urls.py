from re import template
from django.urls import path
from .views import (AddEvent, ListAllEvent, EventDetail,
                    EventPayment, CreatePaymentIntent, PaymentSuccess, EventDelete)
from django.views.generic.base import TemplateView

urlpatterns = [
    path('add', AddEvent.as_view(), name='add_event'),
    path('add_success', TemplateView.as_view(
        template_name='event/addEventSuccess.html'), name='add_success'),
    path('all_event', ListAllEvent.as_view(), name='all_event'),
    path('<int:pk>/detail', EventDetail.as_view(), name="event_detail"),
    path('<int:pk>/delete', EventDelete.as_view(), name="event_delete"),
    path('event_payment', EventPayment.as_view(), name="event_payment"),
    path('create_payment_intent', CreatePaymentIntent.as_view(),
         name="create_payment_intent"),
    path('payment_success/<int:event_id>',
         PaymentSuccess.as_view(), name="payment_success"),
]
