# Generated by Django 4.2.4 on 2023-08-11 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import palinodes.models


class Migration(migrations.Migration):

    dependencies = [
        ("palinodes", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Directory",
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
                ("name", models.CharField(max_length=50)),
                (
                    "parent_folder",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subdirectories",
                        to="palinodes.directory",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="File",
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
                    "file",
                    models.FileField(upload_to=palinodes.models.get_file_upload_path),
                ),
                (
                    "parent_folder",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to="palinodes.directory",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
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
                ("avatar", models.ImageField(blank=True, upload_to="media/avatar")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Repository",
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
                ("name", models.CharField(max_length=50)),
                ("created", models.DateField(auto_now=True)),
                (
                    "collaborators",
                    models.ManyToManyField(
                        blank=True,
                        related_name="collaborating",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="repositories",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="comment",
            name="song",
        ),
        migrations.AlterField(
            model_name="comment",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="comments",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.DeleteModel(
            name="Member",
        ),
        migrations.DeleteModel(
            name="Song",
        ),
        migrations.AddField(
            model_name="file",
            name="parent_repository",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contents",
                to="palinodes.repository",
            ),
        ),
        migrations.AddField(
            model_name="directory",
            name="parent_repository",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="directories",
                to="palinodes.repository",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="file",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="palinodes.file",
            ),
        ),
    ]