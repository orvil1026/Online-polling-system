from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Poll,Choice,Quiz,Vote
# Register your models here.

admin.site.site_header="PollLab Admin"
admin.site.site_title="PollLab Admin Area"
admin.site.index_title="Welcome to the PollLab Admin"

class ChoiceInline(admin.TabularInline):
    model=Choice
    

class PollAdmin(admin.ModelAdmin):
    fields=['text','pub_date','active']
    list_display=('text','pub_date','quiz','active')

    inlines=[ChoiceInline]

class PollInline(admin.StackedInline):
    model=Poll
    
    fields=['text','pub_date','active']
    list_display=('text','pub_date','active')
    inlines=[ChoiceInline]

class QuizAdmin(admin.ModelAdmin):
    fields=['quiz_owner','quiz_id','active']

    inlines=[PollInline]

    list_display=('quiz_owner','quiz_id','active')




admin.site.register(Quiz, QuizAdmin)
admin.site.register(Poll,PollAdmin)
admin.site.unregister(Group)
