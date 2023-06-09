# Generated by Django 4.2.1 on 2023-05-17 16:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('subject', models.CharField(blank=True, max_length=1024, null=True)),
                ('message', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('attachment', models.FileField(blank=True, default=None, null=True, upload_to='')),
                ('dev', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ConfigurationV1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_host', models.CharField(default=None, max_length=1024, null=True, verbose_name='EMAIL_HOST')),
                ('email_port', models.PositiveSmallIntegerField(default=587, verbose_name='EMAIL_PORT')),
                ('email_host_user', models.CharField(default=None, max_length=255, null=True, verbose_name='EMAIL_HOST_USER')),
                ('email_host_password', models.CharField(default=None, max_length=255, null=True, verbose_name='EMAIL_HOST_PASSWORD')),
                ('email_use_tls', models.BooleanField(default=True, null=True, verbose_name='EMAIL_USE_TLS')),
                ('email_use_ssl', models.BooleanField(default=False, null=True, verbose_name='EMAIL_USE_SSL')),
                ('dev', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
