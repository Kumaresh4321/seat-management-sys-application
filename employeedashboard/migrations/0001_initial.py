# Generated by Django 3.2.8 on 2022-06-16 05:43

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
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=50)),
                ('designation_name', models.CharField(max_length=50)),
                ('location_name', models.CharField(max_length=50)),
                ('reporting_to', models.CharField(max_length=50)),
                ('department_head', models.CharField(max_length=80)),
                ('shiftid', models.CharField(choices=[('ap', 'APAC'), ('uk', 'UK')], default='UK', max_length=6)),
                ('department_name', models.CharField(max_length=50, null=True)),
                ('seat_id', models.IntegerField(default=0)),
                ('reallocation_status', models.CharField(choices=[('active', 'ACTIVE'), ('inactive', 'INACTIVE')], default='INACTIVE', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
