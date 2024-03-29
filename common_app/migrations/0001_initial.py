# Generated by Django 3.2 on 2023-04-22 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_code', models.CharField(max_length=50, null=True)),
                ('upload', models.FileField(upload_to='file_manager')),
                ('is_active', models.BooleanField(default=True)),
                ('expiry_date', models.IntegerField(default=0)),
            ],
        ),
    ]
