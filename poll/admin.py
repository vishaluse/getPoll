from poll.models import Option, Poll, ImageOption, PollHistory
from django.contrib import admin


# Register your models here.
class OptionInline(admin.TabularInline):
    model = Option

class ImageOptionInline(admin.TabularInline):
    model = ImageOption

class PollAdmin(admin.ModelAdmin):
    inlines = [OptionInline, ImageOptionInline]

admin.site.register(Poll, PollAdmin)
admin.site.register(Option)
admin.site.register(PollHistory)
