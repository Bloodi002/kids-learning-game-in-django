# Generated by Django 5.1.1 on 2024-10-05 08:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemLevel',
            fields=[
                ('problem_level_id', models.AutoField(primary_key=True, serialize=False)),
                ('level', models.CharField(max_length=100)),
                ('position_type_id', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=50)),
                ('symbol_position', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ProblemType',
            fields=[
                ('problem_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='contact',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.CreateModel(
            name='CourseContactMapping',
            fields=[
                ('course_contact_mapping_id', models.AutoField(primary_key=True, serialize=False)),
                ('contact_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.contact')),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.course')),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('problem_id', models.AutoField(primary_key=True, serialize=False)),
                ('statement', models.TextField()),
                ('max_score', models.IntegerField()),
                ('min_score', models.IntegerField()),
                ('time_bound', models.DateTimeField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('symbol_position', models.PositiveSmallIntegerField()),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.course')),
                ('problem_level_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.problemlevel')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemScoreMapping',
            fields=[
                ('problem_score_mapping_id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.IntegerField()),
                ('contact_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.contact')),
                ('problem_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.problem')),
            ],
        ),
    ]
