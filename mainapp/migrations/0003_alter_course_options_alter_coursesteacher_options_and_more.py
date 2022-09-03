# Generated by Django 4.0.6 on 2022-09-03 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_data_migration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'Course', 'verbose_name_plural': 'Courses'},
        ),
        migrations.AlterModelOptions(
            name='coursesteacher',
            options={'verbose_name': 'Teacher', 'verbose_name_plural': 'Teachers'},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ('course', 'num'), 'verbose_name': 'Lesson', 'verbose_name_plural': 'Lessons'},
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': 'News', 'verbose_name_plural': 'News'},
        ),
    ]