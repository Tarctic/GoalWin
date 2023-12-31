# Generated by Django 4.2.4 on 2023-09-30 22:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GoalWin', '0004_alter_goal_setter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='setter',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='goal_setter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='group',
            name='admin',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='group_admin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='member_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
