from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0061_bitacora_firebase_project_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='BitacoraTarea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200, verbose_name='Título')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('en_progreso', 'En Progreso'), ('completada', 'Completada')], default='pendiente', max_length=20, verbose_name='Estado')),
                ('comentario', models.TextField(blank=True, null=True, verbose_name='Comentario')),
                ('orden', models.PositiveIntegerField(default=0, verbose_name='Orden')),
                ('firebase_id', models.CharField(blank=True, default='', max_length=120)),
                ('firebase_source_id', models.CharField(blank=True, default='', max_length=120)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('asignado_a', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tareas_bitacora', to='core.colaborador', verbose_name='Asignado a')),
                ('creado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tareas_bitacora_creadas', to='auth.user')),
                ('planificacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tareas', to='core.planificacionbitacora', verbose_name='Planificación')),
            ],
            options={
                'verbose_name': 'Tarea de Bitácora',
                'verbose_name_plural': 'Tareas de Bitácora',
                'ordering': ['orden', 'creado_en'],
            },
        ),
        migrations.CreateModel(
            name='BitacoraSubtarea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200, verbose_name='Título')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('en_progreso', 'En Progreso'), ('completada', 'Completada')], default='pendiente', max_length=20, verbose_name='Estado')),
                ('comentario', models.TextField(blank=True, null=True, verbose_name='Comentario')),
                ('orden', models.PositiveIntegerField(default=0, verbose_name='Orden')),
                ('firebase_id', models.CharField(blank=True, default='', max_length=120)),
                ('firebase_source_id', models.CharField(blank=True, default='', max_length=120)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('tarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtareas', to='core.bitacoratarea', verbose_name='Tarea')),
            ],
            options={
                'verbose_name': 'Subtarea de Bitácora',
                'verbose_name_plural': 'Subtareas de Bitácora',
                'ordering': ['orden', 'creado_en'],
            },
        ),
        migrations.AddIndex(
            model_name='bitacoratarea',
            index=models.Index(fields=['planificacion', 'estado'], name='core_bitac_planifi_9d76f3_idx'),
        ),
        migrations.AddIndex(
            model_name='bitacorasubtarea',
            index=models.Index(fields=['tarea', 'estado'], name='core_bitac_tarea_0c9a6a_idx'),
        ),
    ]



