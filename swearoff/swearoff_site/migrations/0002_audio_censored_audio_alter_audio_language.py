# Generated by Django 4.1.5 on 2023-01-29 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swearoff_site', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='censored_audio',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='audio',
            name='language',
            field=models.CharField(choices=[('fr', 'Francais'), ('en', 'English')], default='EN', max_length=2),
        ),
    ]