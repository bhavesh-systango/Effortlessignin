# Generated by Django 4.0 on 2022-06-21 06:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0002_alter_user_groups_alter_user_user_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=256)),
                ('date', models.DateField()),
                ('amount', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='authentication.user')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_key', models.CharField(max_length=256)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='event_to_be_participate_in', to='event.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_participating_in_the_event', to='authentication.user')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='participant',
            field=models.ManyToManyField(related_name='participant_table', through='event.Participant', to=settings.AUTH_USER_MODEL),
        ),
    ]
