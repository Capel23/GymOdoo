📱 GYM MANAGEMENT - GUÍA DE INICIO RÁPIDO
==========================================

## ⚡ Instalación (3 pasos)

1. 📁 El módulo ya está en: `addons/gym_management/`

2. 🔄 En Odoo:
   - Ir a: **Aplicaciones**
   - Clic: **Actualizar lista de aplicaciones**
   - Buscar: **Gym Management**
   - Clic: **Instalar**

3. ✅ ¡Listo!

---

## 🚀 Uso Básico (Primeros Pasos)

### 1️⃣ Crear tu primer Socio
```
Menú: Gimnasio → Socios → Crear
- Nombre: Ej. "Juan Pérez"
- Email: juan@email.com
- Teléfono: 555-1234
- Guardar
```

### 2️⃣ Asignar una Suscripción
```
Desde Socio: Botón "Nueva Suscripción"
O: Gimnasio → Suscripciones → Crear

- Plan: Elegir (Básico, Premium, VIP)
- Inicio: Hoy
- Vencimiento: Ej. 3 meses
- Cuota: Ingresar monto
- Guardar
- Clic: "Activar"
```

### 3️⃣ Generar Reportes
```
FICHA DE INSCRIPCIÓN:
  Socio → Inicio (ícono imprenta) → Ficha de Inscripción

RECIBO DE PAGO:
  Suscripción → Inicio (ícono imprenta) → Recibo de Pago
```

### 4️⃣ Ver Análisis
```
Gimnasio → Análisis → Seleccionar:
  - Análisis de Ingresos (gráficos de ingresos/mes)
  - Análisis de Clases (ocupación por tipo)
  - Análisis de Instructores (profesores e ingresos)
  - Análisis de Socios (crecimiento)
```

---

## 📊 Características Principales

| Característica | Ubicación | Descripción |
|---|---|---|
| **Socios** | Gimnasio > Socios | Registrar y gestionar miembros |
| **Clases** | Gimnasio > Clases | Crear tipos de actividades (yoga, crossfit, etc.) |
| **Instructores** | Gimnasio > Instructores | Registrar profesores |
| **Suscripciones** | Gimnasio > Suscripciones | Planes y membresías |
| **Reportes** | Desde modelos > Imprimir | Fichas e invoice (PDF) |
| **Gráficos** | Gimnasio > Análisis | Ingresos, ocupación, evolución |
| **Pivot** | Gimnasio > Análisis | Tablas dinámicas de datos |
| **Cron** | Automático (3am) | Marca suscripciones vencidas |

---

## 🎯 Tareas Principales Completadas

### ✅ Informes Técnicos QWeb
- **Ficha de Inscripción**: Foto, datos médicos, suscripciones
- **Recibo de Pago**: Logo, concepto, montos, resumen

### ✅ Vistas de Análisis (BI)
- **Gráficos**: 6 vistas diferentes (líneas, barras, pie)
- **Pivot**: 3 tablas dinámicas para análisis cruzado

### ✅ Automatización (Cron)
- **Diariamente**: Revisa suscripciones vencidas
- **Automático**: Cambia estado a "Expirado"

---

## 🔐 Datos de Demostración

**Cargados automáticamente:**
- 3 Instructores (Yoga, CrossFit, Spinning)
- 3 Clases programadas
- 3 Socios con suscripciones
- Ejemplos de datos para testear

---

## 📁 Archivos de Documentación

Lee en este orden:
1. **README.md** - Descripción general del módulo
2. **PROYECTO_COMPLETO.md** - Detalles técnicos completos
3. **ARQUITECTURA.md** - Diagramas y relaciones
4. **VERIFICACION.md** - Checklist de funcionalidades

---

## 🔧 Verificar Cron (Automatización)

```
Configuración → Datos Técnicos → Acciones Planificadas
Buscar: "Revisar Suscripciones Vencidas"

- Estado: Debe estar ACTIVO ✓
- Frecuencia: 1 día
- Última ejecución: Ver timestamp
- Próxima ejecución: Ver próximo horario
```

---

## 🆘 Troubleshooting Rápido

| Problema | Solución |
|---|---|
| Módulo no aparece en Apps | Ir a Aplicaciones > Actualizar lista |
| Error al instalar | Revisar logs: `tail -f odoo.log` |
| Cron no se ejecuta | Verificar que el servidor tenga Cron enabled |
| Reportes no se abren | Verificar que Wkhtmltopdf esté instalado |
| Permisos denegados | Revisar user group: base.group_user |

---

## 📞 Contacto

Para dudas, revisar:
- Documentación en archivos .md del módulo
- Logs de Odoo: `/var/log/odoo/`
- Consola de desarrollo: F12 en el navegador

---

## ✨ Próximas Opciones

Una vez funcionando, puedes:
- Agregar nuevos types de planes
- Crear reportes adicionales
- Personalizar colores y diseño
- Integrar con contabilidad
- Crear portal para socios

---

**¡Listo para usar! 🎉**

Comienza registrando tu primer socio ahora.
