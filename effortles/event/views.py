import stripe
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Event, Participant
from .forms import EventForm


User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY


class AddEvent(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event/addevent.html'
    queryset = Event.objects.all()
    success_url = 'add_success'


class ListAllEvent(LoginRequiredMixin, TemplateView):
    http_method_names = ['get']

    def get(self, request):
        queryset = Event.objects.all()
        return render(request, 'event/showAllEvent.html', {'current_user': request.user, 'all_event': queryset})


class EventDetail(LoginRequiredMixin, DetailView):
    model = Event
    template_name = "event/eventDetail.html"
    context_object_name = 'event_detail'

    def get(self, request, pk):
        participant_detail = Participant.objects.filter(
            event=pk, user=request.user.pk).first()

        context = {
            'event_detail': Event.objects.get(pk=pk),
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        }

        if participant_detail == None:
            context.update({'payment_status': 'not_done'})
        elif participant_detail.transaction_status == 'not_confirmed':
            context.update({'payment_status': 'not_done'})
        else:
            context.update({'payment_status': 'done'})

        return render(request, "event/eventDetail.html", context)


class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'event/deleteEventSuccess.html'


class EventPayment(LoginRequiredMixin, TemplateView):
    template_name = 'event/payment_successful.html'

    def post(self, request):
        event_id = request.POST['eventId']
        stripe_token = request.POST['stripeToken']

        event_detail = Event.objects.filter(pk=event_id).first()

        stripe.PaymentIntent.create(
            amount=event_detail.amount,
            currency="inr",
            source=stripe_token,
            description=f"{request.user.pk},{event_id} {event_detail.event_name} payment",
            payment_method_types=['card'],
        )
        return render(request, 'event/payment_successful.html', {})


@method_decorator(csrf_exempt, name='dispatch')
class CreatePaymentIntent(TemplateView):

    def post(self, request):

        sent_data = json.loads(request.body.decode("utf-8"))
        event_id = sent_data['items'][0]['id']
        event_detail = Event.objects.filter(pk=event_id).first()

        try:
            intent = stripe.PaymentIntent.create(
                amount=event_detail.amount*100,
                currency='inr',
                automatic_payment_methods={
                    'enabled': True,
                },
            )

            participant_detail = Participant.objects.filter(
                event=event_id, user=request.user.pk).first()

            if participant_detail == None:
                Participant.objects.create(user=User(request.user.id), event=Event(
                    event_id), transaction_key=intent['id'])
            else:
                participant_detail.transaction_key = intent['id']
                participant_detail.save()

            return JsonResponse({
                'clientSecret': intent['client_secret']
            })

        except Exception as e:
            return JsonResponse(error=str(e))


class PaymentSuccess(TemplateView):

    def get(self, request, event_id):
        participant_object = Participant.objects.filter(
            event=event_id, user=request.user.pk).first()
        participant_object.transaction_status = 'confirmed'
        participant_object.save()

        return render(request, 'event/payment_successful.html', {})
