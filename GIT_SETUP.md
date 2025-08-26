# 🚀 Configuración de Git para Sistema ARCA Construcción

## 📋 Pasos para Configurar Git

### **Paso 1: Reiniciar Terminal**
Después de instalar Git, **cierra y vuelve a abrir** la terminal para que reconozca el comando `git`.

### **Paso 2: Verificar Instalación**
```bash
git --version
```
Deberías ver algo como: `git version 2.51.0.windows.1`

### **Paso 3: Configurar Usuario Git**
```bash
git config --global user.name "ARCA Construccion"
git config --global user.email "admin@arca-construccion.com"
```

### **Paso 4: Inicializar Repositorio**
```bash
git init
```

### **Paso 5: Agregar Archivos**
```bash
git add .
```

### **Paso 6: Primer Commit**
```bash
git commit -m "Version inicial del Sistema ARCA Construccion"
```

### **Paso 7: Crear Rama Principal**
```bash
git branch -M main
```

## 🔗 Conectar con Repositorio Remoto

### **Opción A: GitHub**
1. Crear cuenta en [GitHub.com](https://github.com)
2. Crear nuevo repositorio: `sistema-arca-construccion`
3. Conectar repositorio local:
```bash
git remote add origin https://github.com/tu-usuario/sistema-arca-construccion.git
git push -u origin main
```

### **Opción B: GitLab**
1. Crear cuenta en [GitLab.com](https://gitlab.com)
2. Crear nuevo proyecto: `sistema-arca-construccion`
3. Conectar repositorio local:
```bash
git remote add origin https://gitlab.com/tu-usuario/sistema-arca-construccion.git
git push -u origin main
```

## 📝 Comandos Git Básicos

### **Ver Estado del Repositorio**
```bash
git status
```

### **Ver Historial de Commits**
```bash
git log --oneline
```

### **Crear Nueva Rama**
```bash
git checkout -b feature/nueva-funcionalidad
```

### **Cambiar de Rama**
```bash
git checkout main
```

### **Fusionar Rama**
```bash
git merge feature/nueva-funcionalidad
```

### **Actualizar desde Remoto**
```bash
git pull origin main
```

### **Enviar Cambios al Remoto**
```bash
git push origin main
```

## 🏷️ Tags de Versión

### **Crear Tag de Versión**
```bash
git tag -a v1.0.0 -m "Version 1.0.0 estable"
```

### **Enviar Tags al Remoto**
```bash
git push origin v1.0.0
```

## 🔄 Workflow de Desarrollo

### **Flujo Diario**
1. **Actualizar** desde remoto: `git pull origin main`
2. **Crear rama** para cambios: `git checkout -b feature/cambio`
3. **Hacer cambios** en el código
4. **Agregar cambios**: `git add .`
5. **Commit**: `git commit -m "Descripción del cambio"`
6. **Push** de la rama: `git push origin feature/cambio`
7. **Merge** a main (desde GitHub/GitLab o localmente)

### **Flujo de Lanzamiento**
1. **Crear rama** de release: `git checkout -b release/v1.1.0`
2. **Hacer cambios** finales
3. **Commit** y push: `git push origin release/v1.1.0`
4. **Merge** a main
5. **Crear tag**: `git tag -a v1.1.0 -m "Version 1.1.0"`
6. **Push tag**: `git push origin v1.1.0`

## 🐛 Solución de Problemas

### **Error: "fatal: not a git repository"**
```bash
git init
```

### **Error: "Please tell me who you are"**
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

### **Error: "fatal: refusing to merge unrelated histories"**
```bash
git pull origin main --allow-unrelated-histories
```

### **Resetear Cambios Locales**
```bash
git reset --hard HEAD
git clean -fd
```

## 📚 Recursos Adicionales

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [GitLab Documentation](https://docs.gitlab.com/)

## 🎯 Próximos Pasos

1. ✅ Configurar Git localmente
2. 🔄 Crear repositorio remoto (GitHub/GitLab)
3. 🚀 Conectar repositorio local con remoto
4. 📱 Hacer primer push
5. 🔧 Configurar CI/CD para despliegue automático

---

**¡Con Git configurado, tendrás control total de versiones y podrás desplegar de forma segura!**
