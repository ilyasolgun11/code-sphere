# Generated by Django 4.2.11 on 2024-05-03 16:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='facebook_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='instagram_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='linkedin_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile_default.jpg', null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='customuser',
            name='twitter_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
