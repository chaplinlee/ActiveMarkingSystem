# Generated by Django 2.1.3 on 2018-12-17 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminMarker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=200)),
                ('psd', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ImgSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_name', models.CharField(max_length=200)),
                ('img_cat', models.CharField(max_length=200)),
                ('mark_flag', models.CharField(max_length=200)),
                ('img_tag_judgement', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TaggedImgSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_name', models.CharField(max_length=200)),
                ('img_cat', models.CharField(max_length=200)),
                ('mark_flag', models.CharField(max_length=200)),
                ('img_tag_judgement', models.CharField(max_length=200)),
            ],
        ),
    ]
