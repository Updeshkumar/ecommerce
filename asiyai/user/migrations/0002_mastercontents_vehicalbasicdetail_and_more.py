# Generated by Django 4.0.3 on 2022-10-10 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterContents',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=200)),
                ('relate_to', models.IntegerField()),
            ],
            options={
                'db_table': 'user_mastercontents',
            },
        ),
        migrations.CreateModel(
            name='vehicalbasicdetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehical_name', models.CharField(max_length=200)),
                ('vehical_number', models.CharField(blank=True, max_length=500, null=True)),
                ('model_number', models.CharField(max_length=500, null=True)),
                ('ownername', models.CharField(max_length=300)),
                ('Aadhar_number', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.RenameField(
            model_name='user',
            old_name='apple_id',
            new_name='gender',
        ),
        migrations.RemoveField(
            model_name='user',
            name='agreeableness',
        ),
        migrations.RemoveField(
            model_name='user',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='user',
            name='conscientiousness',
        ),
        migrations.RemoveField(
            model_name='user',
            name='emotional_stability',
        ),
        migrations.RemoveField(
            model_name='user',
            name='extraversion',
        ),
        migrations.RemoveField(
            model_name='user',
            name='facebook_connect_username',
        ),
        migrations.RemoveField(
            model_name='user',
            name='facebook_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_notification',
        ),
        migrations.RemoveField(
            model_name='user',
            name='openness',
        ),
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
        migrations.RemoveField(
            model_name='user',
            name='twitter_connect_username',
        ),
        migrations.RemoveField(
            model_name='user',
            name='twitter_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='usage_alert_time',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.RemoveField(
            model_name='user',
            name='verification_key',
        ),
        migrations.AlterField(
            model_name='user',
            name='country_code',
            field=models.IntegerField(blank=True, null=True, verbose_name=91),
        ),
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
