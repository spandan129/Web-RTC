# Generated by Django 4.2.7 on 2024-03-25 15:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('Friend_id', models.AutoField(primary_key=True, serialize=False)),
                ('Friend_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMessage',
            fields=[
                ('message_id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.CharField(max_length=1000)),
                ('sent_by', models.CharField(max_length=500)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.CharField(max_length=1000)),
                ('sent_by', models.CharField(max_length=50)),
                ('sent_to', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('friends', models.ManyToManyField(blank=True, to='api.friends')),
            ],
        ),
        migrations.CreateModel(
            name='GroupUser',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=50)),
                ('messages', models.ManyToManyField(blank=True, to='api.groupmessage')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('group_name', models.CharField(max_length=50)),
                ('group_users', models.ManyToManyField(blank=True, to='api.groupuser')),
            ],
        ),
        migrations.AddField(
            model_name='friends',
            name='message',
            field=models.ManyToManyField(blank=True, to='api.message'),
        ),
    ]
