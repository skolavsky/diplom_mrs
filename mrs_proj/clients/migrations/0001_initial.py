# Generated by Django 5.0 on 2024-01-25 18:46

import datetime
import django.db.models.deletion
import simple_history.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalInfo',
            fields=[
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('patronymic', models.CharField(blank=True, max_length=100)),
                ('gender', models.BooleanField(choices=[(0, 'Женский'), (1, 'Мужской')], default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalClientData',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('date_added', models.DateTimeField(blank=True, editable=False)),
                ('date_last_modified', models.DateTimeField(blank=True, editable=False)),
                ('age', models.IntegerField(blank=True, default=0)),
                ('body_mass_index', models.FloatField(blank=True, null=True)),
                ('spo2', models.IntegerField(blank=True, null=True)),
                ('admission_date', models.DateField(blank=True, default=datetime.date.today)),
                ('result', models.IntegerField(blank=True, null=True)),
                ('dayshome', models.IntegerField(blank=True, null=True)),
                ('f_test_ex', models.IntegerField(blank=True, null=True)),
                ('f_test_in', models.IntegerField(blank=True, null=True)),
                ('comorb_ccc', models.BooleanField(blank=True, default=False)),
                ('comorb_bl', models.BooleanField(blank=True, default=False)),
                ('cd_ozhir', models.BooleanField(blank=True, default=False)),
                ('comorb_all', models.BooleanField(blank=True, default=False)),
                ('l_109', models.FloatField(blank=True, null=True)),
                ('lf', models.FloatField(blank=True, null=True)),
                ('rox', models.FloatField(blank=True, null=True)),
                ('spo2_fio', models.FloatField(blank=True, null=True)),
                ('ch_d', models.IntegerField(blank=True, null=True)),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('personal_info', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='clients.personalinfo')),
            ],
            options={
                'verbose_name': 'historical client data',
                'verbose_name_plural': 'historical client datas',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='ClientData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_last_modified', models.DateTimeField(auto_now=True)),
                ('age', models.IntegerField(blank=True, default=0)),
                ('body_mass_index', models.FloatField(blank=True, null=True)),
                ('spo2', models.IntegerField(blank=True, null=True)),
                ('admission_date', models.DateField(blank=True, default=datetime.date.today)),
                ('result', models.IntegerField(blank=True, null=True)),
                ('dayshome', models.IntegerField(blank=True, null=True)),
                ('f_test_ex', models.IntegerField(blank=True, null=True)),
                ('f_test_in', models.IntegerField(blank=True, null=True)),
                ('comorb_ccc', models.BooleanField(blank=True, default=False)),
                ('comorb_bl', models.BooleanField(blank=True, default=False)),
                ('cd_ozhir', models.BooleanField(blank=True, default=False)),
                ('comorb_all', models.BooleanField(blank=True, default=False)),
                ('l_109', models.FloatField(blank=True, null=True)),
                ('lf', models.FloatField(blank=True, null=True)),
                ('rox', models.FloatField(blank=True, null=True)),
                ('spo2_fio', models.FloatField(blank=True, null=True)),
                ('ch_d', models.IntegerField(blank=True, null=True)),
                ('personal_info', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clients.personalinfo')),
            ],
        ),
    ]