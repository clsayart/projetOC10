# Generated by Django 4.0.4 on 2022-05-27 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('AUTHOR', 'Author'), ('CONTRIBUTOR', 'Contributor')], max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=5000)),
                ('type', models.CharField(choices=[('BACK-END', 'back-end'), ('FRONT-END', 'front-end'), ('IOS', 'iOS'), ('ANDROID', 'Android')], max_length=200)),
                ('contributor', models.ManyToManyField(related_name='project_contributed', through='softdeskapp.Contributor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('desc', models.CharField(max_length=5000)),
                ('tag', models.CharField(choices=[('BUG', 'Bug'), ('IMPROVEMENT', 'Amélioration'), ('TASK', 'Tâche')], max_length=30)),
                ('priority', models.CharField(choices=[('FAIBLE', 'Faible'), ('MOYENNE', 'Moyenne'), ('HIGH', 'Elevée')], max_length=30)),
                ('status', models.CharField(choices=[('TODO', 'A faire'), ('IN_PROGRESS', 'En cours'), ('COMPLETED', 'Terminé')], max_length=30)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('assignee_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='assignee', to=settings.AUTH_USER_MODEL)),
                ('author_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='softdeskapp.project')),
            ],
        ),
        migrations.AddField(
            model_name='contributor',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_contributor', to='softdeskapp.project'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=5000)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('author_user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='softdeskapp.issue')),
            ],
        ),
    ]
