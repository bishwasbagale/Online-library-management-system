# Generated by Django 4.0.3 on 2022-03-20 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0005_feedback'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DeleteRequest',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='is_publisher',
            new_name='is_student',
        ),
    ]
