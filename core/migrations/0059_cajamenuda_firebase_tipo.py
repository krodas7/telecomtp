from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0058_alter_bonocolaboradorproyecto_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="cajamenuda",
            name="tipo_movimiento",
            field=models.CharField(
                choices=[("deposito", "Depósito"), ("gasto", "Gasto")],
                default="gasto",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="cajamenuda",
            name="firebase_transaction_id",
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name="cajamenuda",
            name="firebase_sync_error",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="cajamenuda",
            name="firebase_synced_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]











