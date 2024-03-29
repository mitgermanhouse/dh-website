# Generated by Django 3.2.11 on 2022-01-12 04:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0003_auto_20220107_2341"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dietaryrestriction",
            name="long_name",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="dietaryrestriction",
            name="short_name",
            field=models.CharField(max_length=127),
        ),
        migrations.AlterField(
            model_name="member",
            name="major",
            field=models.CharField(max_length=127, null=True),
        ),
    ]
