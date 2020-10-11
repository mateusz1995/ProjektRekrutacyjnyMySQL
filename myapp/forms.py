from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Producer, Product
from django.forms import ModelForm


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        # Required fields
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        # Required fields
        fields = ('email',)


class ProducerCreationForm(ModelForm):

    class Meta:
        model = Producer
        # Required fields
        fields = ('name',)


class ProducerChangeForm(ModelForm):

    class Meta:
        model = Producer
        # Required fields
        fields = ('name',)


class ProductCreationForm(ModelForm):

    class Meta:
        model = Product
        # Required fields
        fields = ('name', 'producer', 'price', 'is_active',)


class ProductChangeForm(ModelForm):

    class Meta:
        model = Product
        # Required fields
        fields = ('name', 'producer', 'price', 'is_active',)
