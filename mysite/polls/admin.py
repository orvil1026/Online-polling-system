from django.contrib import admin
from .models import Poll,Choice,Quiz,Vote
# Register your models here.



class ChoiceInline(admin.TabularInline):
    model=Choice
    extra=3

class PollAdmin(admin.ModelAdmin):
    fields=['text','pub_date','active']
    list_display=('text','pub_date','active')

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