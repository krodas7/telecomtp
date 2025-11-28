# 📋 Instrucciones para Aplicar la Migración 0053 en el Servidor

## Pasos a Seguir:

### 1. Conectarse al Servidor
```bash
ssh root@tu-servidor
# o
ssh usuario@tu-servidor
```

### 2. Navegar al Directorio del Proyecto
```bash
cd /var/www/telecomtp
```

### 3. Activar el Entorno Virtual
```bash
source venv/bin/activate
```

### 4. Actualizar el Código desde el Repositorio
```bash
git pull origin main
```

### 5. Verificar el Estado de las Migraciones
```bash
python3 manage.py showmigrations core | grep "0053"
```

Deberías ver algo como:
- `[ ] 0053_cambiar_bono_produccion_a_monto_fijo` (no aplicada)
- o `[X] 0053_cambiar_bono_produccion_a_monto_fijo` (ya aplicada)

### 6. Aplicar la Migración
```bash
python3 manage.py migrate core 0053
```

O para aplicar todas las migraciones pendientes:
```bash
python3 manage.py migrate core
```

### 7. Verificar que se Aplicó Correctamente
```bash
python3 manage.py showmigrations core | grep "0053"
```

Deberías ver:
```
[X] 0053_cambiar_bono_produccion_a_monto_fijo
```

### 8. (Opcional) Reiniciar el Servidor
Si usas Gunicorn con supervisor o systemd:
```bash
# Con supervisor
sudo supervisorctl restart telecomtp

# O con systemd
sudo systemctl restart gunicorn

# O simplemente reiniciar Gunicorn manualmente
pkill -f gunicorn
# Luego iniciar de nuevo según tu configuración
```

## 🔍 Verificación Adicional

Para verificar que el campo fue removido correctamente (si usas SQLite):
```bash
sqlite3 db.sqlite3 "PRAGMA table_info(core_subproyecto);" | grep monto_cotizado
```

No debería mostrar nada (campo removido).

## ⚠️ Si hay Problemas

Si la migración falla, puedes:

1. **Ver los detalles del error:**
   ```bash
   python3 manage.py migrate core 0053 --verbosity 2
   ```

2. **Verificar el estado de la base de datos:**
   ```bash
   python3 manage.py showmigrations core
   ```

3. **Si hay conflictos, puedes aplicar la migración de forma forzada:**
   ```bash
   python3 manage.py migrate core 0053 --fake
   ```
   ⚠️ **CUIDADO**: Solo usar `--fake` si estás seguro de que la migración ya fue aplicada manualmente.

## ✅ Resumen Rápido

```bash
cd /var/www/telecomtp
source venv/bin/activate
git pull origin main
python3 manage.py migrate core 0053
sudo supervisorctl restart telecomtp  # o tu comando de reinicio
```

