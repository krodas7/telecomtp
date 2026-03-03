from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0065_rename_core_bitac_tarea_0c9a6a_idx_core_bitaco_tarea_i_99fed1_idx_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BitacoraAsignacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tecnico_email', models.EmailField(blank=True, default='', max_length=254, verbose_name='Email técnico')),
                ('tecnico_nombre', models.CharField(blank=True, default='', max_length=200, verbose_name='Nombre técnico')),
                ('fecha', models.DateField(verbose_name='Fecha asignada')),
                ('porcentaje', models.PositiveIntegerField(default=0, verbose_name='Porcentaje')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('en_progreso', 'En Progreso'), ('completada', 'Completada')], default='pendiente', max_length=20, verbose_name='Estado')),
                ('comentario', models.TextField(blank=True, null=True, verbose_name='Comentario')),
                ('firebase_document_id', models.CharField(blank=True, default='', max_length=120)),
                ('firebase_sync_error', models.TextField(blank=True)),
                ('firebase_synced_at', models.DateTimeField(blank=True, null=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('asignacion_origen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reasignaciones', to='core.bitacoraasignacion', verbose_name='Asignación origen')),
                ('colaborador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asignaciones_bitacora', to='core.colaborador', verbose_name='Técnico (Colaborador)')),
                ('creado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asignaciones_bitacora_creadas', to='auth.user')),
                ('planificacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asignaciones', to='core.planificacionbitacora', verbose_name='Planificación')),
                ('subtarea', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asignaciones', to='core.bitacorasubtarea', verbose_name='Subtarea')),
                ('tarea', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asignaciones', to='core.bitacoratarea', verbose_name='Tarea')),
            ],
            options={
                'verbose_name': 'Asignación de Bitácora',
                'verbose_name_plural': 'Asignaciones de Bitácora',
                'ordering': ['-fecha', '-creado_en'],
            },
        ),
        migrations.CreateModel(
            name='BitacoraAvanceDiario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(verbose_name='Fecha del avance')),
                ('porcentaje', models.PositiveIntegerField(default=0, verbose_name='Porcentaje')),
                ('comentario', models.TextField(blank=True, null=True, verbose_name='Comentario')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('firebase_document_id', models.CharField(blank=True, default='', max_length=120)),
                ('firebase_sync_error', models.TextField(blank=True)),
                ('firebase_synced_at', models.DateTimeField(blank=True, null=True)),
                ('firebase_source', models.CharField(blank=True, default='', max_length=20)),
                ('asignacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avances_diarios', to='core.bitacoraasignacion', verbose_name='Asignación')),
                ('registrado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='avances_bitacora_registrados', to='auth.user')),
            ],
            options={
                'verbose_name': 'Avance Diario Bitácora',
                'verbose_name_plural': 'Avances Diarios Bitácora',
                'ordering': ['-fecha', '-creado_en'],
            },
        ),
        migrations.AddIndex(
            model_name='bitacoraasignacion',
            index=models.Index(fields=['planificacion', 'fecha'], name='core_bitac_planifi_c5c2d1_idx'),
        ),
        migrations.AddIndex(
            model_name='bitacoraasignacion',
            index=models.Index(fields=['estado', 'fecha'], name='core_bitac_estado_0c2b05_idx'),
        ),
        migrations.AddIndex(
            model_name='bitacoraavancediario',
            index=models.Index(fields=['fecha', 'porcentaje'], name='core_bitac_fecha_6f3c35_idx'),
        ),
    ]


