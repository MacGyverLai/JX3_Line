# Generated by Django 2.0.2 on 2018-04-01 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partner16', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=50)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='LineUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_id', models.CharField(max_length=30)),
                ('full_name', models.CharField(max_length=30)),
                ('nickname', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='statement',
            name='statement_text',
        ),
        migrations.AddField(
            model_name='keyword',
            name='statement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner16.Statement'),
        ),
    ]
