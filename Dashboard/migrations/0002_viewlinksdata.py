# Generated by Django 4.0.1 on 2022-01-16 23:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewLinksData',
            fields=[
            ],
            options={
                'ordering': ['-id'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('Dashboard.linksinfo',),
        ),
    ]
