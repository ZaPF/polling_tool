# Generated by Django 3.2 on 2021-05-22 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_squashed_0006_alter_vote_uni'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_title',
            field=models.CharField(default='No title provided', max_length=200),
            preserve_default=False,
        ),
    ]
