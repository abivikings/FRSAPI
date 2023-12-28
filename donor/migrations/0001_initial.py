# Generated by Django 4.2.7 on 2023-12-28 03:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField(max_length=50, null=True)),
                ('last_name', models.TextField(max_length=50, null=True)),
                ('email', models.EmailField(max_length=50, null=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.campaign')),
            ],
        ),
        migrations.CreateModel(
            name='CardInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.TextField(max_length=50, null=True)),
                ('card_exp_date', models.DateField(max_length=10, null=True)),
                ('wallet_address', models.TextField(max_length=50, null=True)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.donor')),
            ],
        ),
    ]