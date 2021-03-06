# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-05 20:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0004_auto_20170514_2109'),
    ]

    operations = [
        migrations.CreateModel(
            name='_empresas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cuentas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=40, null=True)),
                ('empresa', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='Empresa',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='Cuentas_Asociadas',
            field=models.ManyToManyField(blank=True, null=True, to='clientes.Cuentas'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='Empresa',
            field=models.ManyToManyField(blank=True, null=True, to='clientes._empresas'),
        ),
    ]
