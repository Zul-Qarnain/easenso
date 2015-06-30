from django.contrib import admin
from .models import User

class User_Admin(admin.ModelAdmin):
  list_display = (
      'id', 'username', 'first_name', 'middle_name', 'last_name', 'email',
      'gender', 'date_of_birth', 'address', 'contact_number', 'date_joined',
      'is_superuser', 'is_staff', 'is_active', 'last_login', 'user_type'
  )

admin.site.register(User, User_Admin)