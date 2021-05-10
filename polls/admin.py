from django.contrib import admin

# Register your models here.
from .models import Choice, Question, Vote, Uni

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fields = ['active', 'question_text']
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Vote)
admin.site.register(Uni)