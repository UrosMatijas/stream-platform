# Generated by Django 4.2.3 on 2023-07-05 12:38

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apipractice_app', '0003_video_platform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='platform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='apipractice_app.streamplatform'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.CharField(max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='apipractice_app.video')),
            ],
        ),
    ]
