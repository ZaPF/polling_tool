# Generated by Django 3.2 on 2022-10-05 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_alter_question_question_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='uni',
            name='voting_rights',
            field=models.BooleanField(default=True),
        ),
    ]
