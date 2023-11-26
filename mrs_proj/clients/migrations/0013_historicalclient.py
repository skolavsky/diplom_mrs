# Generated by Django 4.2.7 on 2023-11-26 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import secrets
import simple_history.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0012_remove_client_added_user_remove_client_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalClient',
            fields=[
                ('token', models.CharField(db_index=True, default=secrets.token_urlsafe, max_length=100)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('patronymic', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('body_mass_index', models.FloatField()),
                ('SPO2', models.IntegerField()),
                ('admission_date', models.DateField()),
                ('result', models.IntegerField()),
                ('gender', models.BooleanField(choices=[(0, 'Female'), (1, 'Male')], default=False)),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical client',
                'verbose_name_plural': 'historical clients',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
