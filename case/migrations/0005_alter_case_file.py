# Generated by Django 3.2.7 on 2022-02-12 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0004_alter_case_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
    ]
