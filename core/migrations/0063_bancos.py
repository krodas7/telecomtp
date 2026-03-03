from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0062_bitacora_tareas_subtareas'),
    ]

    operations = [
        migrations.CreateModel(
            name='BancoCuenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('banco', models.CharField(blank=True, max_length=100)),
                ('numero_cuenta', models.CharField(blank=True, max_length=50)),
                ('tipo_cuenta', models.CharField(choices=[('ahorro', 'Ahorro'), ('corriente', 'Corriente'), ('monedero', 'Monedero/Virtual'), ('otros', 'Otros')], default='corriente', max_length=20)),
                ('moneda', models.CharField(default='USD', max_length=10)),
                ('saldo_inicial', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('activo', models.BooleanField(default=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Cuenta Bancaria',
                'verbose_name_plural': 'Cuentas Bancarias',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='MovimientoBanco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('ingreso', 'Ingreso'), ('egreso', 'Egreso')], max_length=10)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=12)),
                ('fecha_movimiento', models.DateField(default=django.utils.timezone.now)),
                ('descripcion', models.TextField(blank=True)),
                ('referencia', models.CharField(blank=True, max_length=100)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimientos', to='core.bancocuenta')),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movimientos_bancarios_creados', to=settings.AUTH_USER_MODEL)),
                ('factura', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movimientos_bancarios', to='core.factura')),
                ('gasto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movimiento_bancario', to='core.gasto')),
                ('pago', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movimiento_bancario', to='core.pago')),
            ],
            options={
                'verbose_name': 'Movimiento Bancario',
                'verbose_name_plural': 'Movimientos Bancarios',
                'ordering': ['-fecha_movimiento', '-id'],
            },
        ),
        migrations.AddField(
            model_name='pago',
            name='cuenta_bancaria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pagos', to='core.bancocuenta'),
        ),
        migrations.AddField(
            model_name='gasto',
            name='cuenta_bancaria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gastos', to='core.bancocuenta'),
        ),
        migrations.AddConstraint(
            model_name='movimientobanco',
            constraint=models.UniqueConstraint(fields=('pago',), name='unique_movimiento_por_pago'),
        ),
        migrations.AddConstraint(
            model_name='movimientobanco',
            constraint=models.UniqueConstraint(fields=('gasto',), name='unique_movimiento_por_gasto'),
        ),
    ]


