from django.urls import path

from subscriptions.views import SubscriptionView

app_name = 'subscriptions'
urlpatterns = [
    path('', SubscriptionView.as_view(), name='subscription'),
]
