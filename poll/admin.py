from poll.models import Option, Poll
from django.contrib import admin


# Register your models here.
class OptionInline(admin.TabularInline):
    model = Option

class PollAdmin(admin.ModelAdmin):
    inlines = [OptionInline]

admin.site.register(Poll, PollAdmin)
admin.site.register(Option)
