# Generated by Django 1.11.17 on 2019-10-21 02:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("menu", "0006_mealrating"),
    ]

    operations = [
        migrations.AddField(
            model_name="autolateplate",
            name="dietary",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="lateplate",
            name="dietary",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="autolateplate",
            name="days",
            field=models.TextField(default=""),
        ),
    ]
