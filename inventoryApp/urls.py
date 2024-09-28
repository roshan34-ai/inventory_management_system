from django.urls import path
from .views import ItemListCreateView, ItemRetrieveUpdateDestroyView, UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('items/', ItemListCreateView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemRetrieveUpdateDestroyView.as_view(), name='item-retrieve-update-destroy'),
]
