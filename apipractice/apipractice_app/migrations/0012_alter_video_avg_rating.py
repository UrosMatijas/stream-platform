# Generated by Django 4.2.3 on 2023-07-06 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apipractice_app', '0011_alter_review_review_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='avg_rating',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=3, null=True),
        ),
    ]