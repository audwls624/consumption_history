from django.urls import path
from . import views

urlpatterns = [
    path('account/<int:account_id>', views.HouseholdAccountDetailView.as_view(), name='account_detail'),
    path('account/list', views.HouseholdAccountView.as_view(), name='account_list'),
    path('account/short/url/<int:account_id>', views.AccountGenerateShorUrlView.as_view(), name='account_short_url'),
]
