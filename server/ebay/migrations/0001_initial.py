# Generated by Django 2.1 on 2018-09-16 02:46

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('company_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('email_address', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('ebay_name', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('wholesale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('retail_price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('profit', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('profit_percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('wholesale_weight', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('wholesale_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('units_sold', models.IntegerField()),
                ('updates', models.CharField(blank=True, max_length=255)),
                ('date', models.DateTimeField(auto_now=True)),
                ('image', models.CharField(max_length=255)),
                ('source', models.CharField(max_length=255)),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ebay.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Projection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_name', models.CharField(max_length=255)),
                ('purchase_price', models.CharField(max_length=255)),
                ('purchase_quantity', models.IntegerField()),
                ('purchase_date', models.CharField(max_length=255)),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ebay.Product')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_address', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ebay.Login')),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ebay.User'),
        ),
        migrations.AddField(
            model_name='account',
            name='company_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ebay.Company'),
        ),
        migrations.AddField(
            model_name='account',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ebay.User'),
        ),
    ]
