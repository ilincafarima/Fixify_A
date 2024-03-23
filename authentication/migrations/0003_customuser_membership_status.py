# Generated by Django 5.0.2 on 2024-03-20 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_customuser_dob_remove_customuser_fixer_job_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='membership_status',
            field=models.CharField(choices=[('client', 'Client'), ('worker', 'Worker')], default='free', max_length=10),
        ),
    ]