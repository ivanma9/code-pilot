# Generated by Django 5.1.6 on 2025-02-09 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestion',
            name='language',
            field=models.CharField(default='python', max_length=100),
            preserve_default=False,
        ),
    ]
