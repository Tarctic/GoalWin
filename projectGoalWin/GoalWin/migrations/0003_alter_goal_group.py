# Generated by Django 4.2.4 on 2023-09-30 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GoalWin', '0002_group_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='group',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='goal_group', to='GoalWin.group'),
        ),
    ]
