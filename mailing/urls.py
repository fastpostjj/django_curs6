"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from mailing.apps import MailingConfig
from django.urls import path
from mailing.views import ClientDetailView, ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    Toggle_Activity_Client, ClientDraftListView
from mailing.views import UserMessageDetailView, UserMessageListView, UserMessageCreateView, UserMessageUpdateView, \
    UserMessageDeleteView, Toggle_Activity_UserMessage, UserMessageDraftListView
from mailing.views import MailingDetailView, MailingListView, MailingCreateView, MailingUpdateView, \
    MailingDeleteView, Toggle_Activity_Mailing, MailingDraftListView
from mailing.views import index

app_name = MailingConfig.name

urlpatterns = [
    # path('', index, name='mailing'),

    path('', MailingListView.as_view(), name='mailings'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing/toggle/<int:pk>/', Toggle_Activity_Mailing.as_view(), name='toggle_activity_mailing'),
    path('mailing_drafts', MailingDraftListView.as_view(), name='mailing_drafts'),

    path('client/<int:pk>/', ClientDetailView.as_view(), name='client'),
    path('clients/', ClientListView.as_view(), name='clients'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('client/toggle/<int:pk>/', Toggle_Activity_Client.as_view(), name='toggle_activity_client'),
    path('client_drafts', ClientDraftListView.as_view(), name='client_drafts'),

    path('usermessage/<int:pk>/', UserMessageDetailView.as_view(), name='usermessage'),
    path('usermessages/', UserMessageListView.as_view(), name='usermessages'),
    path('usermessage/create/', UserMessageCreateView.as_view(), name='usermessage_create'),
    path('usermessage/update/<int:pk>/', UserMessageUpdateView.as_view(), name='usermessage_update'),
    path('usermessage/delete/<int:pk>/', UserMessageDeleteView.as_view(), name='usermessage_delete'),
    path('usermessage/toggle/<int:pk>/', Toggle_Activity_UserMessage.as_view(), name='toggle_activity_usermessage'),
    path('usermessage_drafts', UserMessageDraftListView.as_view(), name='usermessage_drafts'),




]
