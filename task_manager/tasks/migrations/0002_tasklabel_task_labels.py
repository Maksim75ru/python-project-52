# Generated by Django 4.2.2 on 2023-07-15 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("labels", "0001_initial"),
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TaskLabel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "label",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="labels.label"
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tasks.task"
                    ),
                ),
            ],
            options={
                "unique_together": {("task", "label")},
            },
        ),
        migrations.AddField(
            model_name="task",
            name="labels",
            field=models.ManyToManyField(
                related_name="tasks", through="tasks.TaskLabel", to="labels.label"
            ),
        ),
    ]
