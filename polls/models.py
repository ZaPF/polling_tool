from django.db import models

# Create your models here.
class Question(models.Model):
    question_title = models.CharField(max_length=200)
    question_text = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.choice_text

class User(models.Model):
    user_name = models.CharField(max_length=200, unique=True, primary_key=True)
    voting_rights = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user_name

class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=User.objects.get_or_create(user_name="Migrated, delete me"))
    
