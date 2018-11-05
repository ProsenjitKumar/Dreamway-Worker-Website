from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import GuestEmail, Profile
from .forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'full_name', 'admin')
    history_list_display = ["status"]
    list_filter = ('admin', 'staff', 'active')
    list_per_page = 100
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ['full_name',
                                      'address',
                                      'age',
                                      'lead',
                                      'balance',
                                      'first_refer',
                                      'second_refer',
                                      'third_refer',
                                      'fourth_refer',
                                      'update',
                                      ]}),
        ('Permissions', {'fields': ('admin', 'staff', 'active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
# Remove Group Model from admin. We're not using it.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'weekly_lead']
    list_filter = ['user']
    search_fields = ['user']
    list_per_page = 100


admin.site.register(Profile, ProfileAdmin)


admin.site.unregister(Group)


class GuestEmailAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model = GuestEmail


admin.site.register(GuestEmail, GuestEmailAdmin)



