# Generated by Django 4.2.7 on 2023-12-31 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0039_region_sort_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fact',
            name='countries',
        ),
        migrations.AddField(
            model_name='fact',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='facts', to='quiz.country'),
        ),
    ]
