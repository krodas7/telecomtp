from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0059_cajamenuda_firebase_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='planificacionbitacora',
            name='firebase_document_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='planificacionbitacora',
            name='firebase_sync_error',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='planificacionbitacora',
            name='firebase_synced_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='planificacionbitacora',
            name='firebase_updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='avanceplanificacion',
            name='firebase_document_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='avanceplanificacion',
            name='firebase_sync_error',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='avanceplanificacion',
            name='firebase_synced_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='avanceplanificacion',
            name='firebase_source',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='avanceplanificacion',
            name='firebase_user_id',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
        migrations.AddField(
            model_name='avanceplanificacion',
            name='firebase_user_name',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='avanceplanificacion',
            name='firebase_user_email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
    ]



