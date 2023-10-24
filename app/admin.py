from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Meep
# Register your models here.

admin.site.unregister(Group)

#combine profile and user models info
class ProfileInline(admin.StackedInline):
    model = Profile

class Useradmin(admin.ModelAdmin):
    model = User
    #just display username fields in admin panel
    fields = ['username']
    inlines = [ProfileInline]

#unregister initial user
admin.site.unregister(User)
#reregister USer
admin.site.register(User, Useradmin)
# admin.site.register(Profile)

admin.site.register(Meep)


