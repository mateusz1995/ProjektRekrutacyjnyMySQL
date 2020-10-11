from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProducerCreationForm, ProducerChangeForm, \
    ProductCreationForm, ProductChangeForm
from .models import CustomUser, Producer, Product
from django.contrib.auth.models import Group


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'user_type', 'is_staff', 'is_active',)
    list_filter = ('user_type', 'is_staff', 'is_active',)
    fieldsets = (
        ('Basic information', {'fields': ('email', 'password', 'user_type',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
             'email', 'password1', 'password2', 'user_type', 'is_staff', 'is_active',)}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class ProducerClassAdmin(admin.ModelAdmin):
    add_form = ProducerCreationForm
    form = ProducerChangeForm
    model = Producer
    list_display = ('name',)
    list_filter = ()
    fieldsets = (
        ('Information about producer', {'fields': ('name',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name',)}
         ),
    )
    search_fields = ('name',)
    ordering = ('name',)


class ProductClassAdmin(admin.ModelAdmin):
    add_form = ProductCreationForm
    form = ProductChangeForm
    model = Product
    list_display = ('name', 'producer', 'price', 'discounted_price', 'is_active',)
    list_filter = ()
    fieldsets = (
        ('Information about product', {'fields': ('name', 'producer', 'price', 'discounted_price', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'producer', 'price', 'discounted_price', 'is_active',)}
         ),
    )
    search_fields = ('producer__name',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Producer, ProducerClassAdmin)
admin.site.register(Product, ProductClassAdmin)
