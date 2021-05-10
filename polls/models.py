from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.choice_text

class Uni(models.Model):
    uni_id = models.IntegerField(unique=True, primary_key=True)
    uni_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.uni_name

class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='votes')
    uni = models.ForeignKey(Uni, on_delete=models.CASCADE)
    
