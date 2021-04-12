from django.contrib import admin
from .models import Member, Profile
# Register your models here.


class ProfileInline(admin.StackedInline):
    model = Profile


class MemberAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]


admin.site.register(Member, MemberAdmin)
