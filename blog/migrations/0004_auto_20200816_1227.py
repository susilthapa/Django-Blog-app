# Generated by Django 2.2.5 on 2020-08-16 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='edited',
            field=models.DateTimeField(editable=False),
        ),
    ]
