from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0062_bitacora_tareas_subtareas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gasto',
            name='proyecto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.proyecto'),
        ),
        migrations.AddField(
            model_name='gasto',
            name='es_administrativo',
            field=models.BooleanField(default=False, help_text='Marca el gasto como administrativo (sin proyecto) o prorrateado.'),
        ),
        migrations.AddField(
            model_name='gasto',
            name='es_prorrateado',
            field=models.BooleanField(default=False, help_text='Indica si el gasto administrativo fue prorrateado a un proyecto.'),
        ),
        migrations.AddField(
            model_name='gasto',
            name='periodo_prorrateo',
            field=models.DateField(blank=True, help_text='Periodo de prorrateo (primer día del mes).', null=True),
        ),
    ]

