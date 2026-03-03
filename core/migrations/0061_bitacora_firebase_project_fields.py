from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_bitacora_firebase_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='planificacionbitacora',
            name='firebase_project_id',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
        migrations.AddField(
            model_name='planificacionbitacora',
            name='firebase_project_name',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]



