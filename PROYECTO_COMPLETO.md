# 📋 PROYECTO COMPLETO: GYM MANAGEMENT - Sistema de Gestión de Socios de un Gimnasio

## 🎯 Objetivos Completados

Este módulo Odoo 19.0 cumple con todas las tareas solicitadas:

### ✅ 1. Informes Técnicos (QWeb Reports)

#### 📝 Ficha de Inscripción
- **Ubicación**: `report/gym_partner_templates.xml` (Template: `report_gym_partner_inscription`)
- **Generador**: Desde modelo Socio (gym.partner)
- **Contenido**:
  - Logo e información del gimnasio
  - Zona de foto del socio
  - Datos personales completos
  - Información de identificación
  - Dirección y contactos
  - Información médica (tipo de sangre, alergias, condiciones)
  - Contacto de emergencia
  - Listado de suscripciones activas
  - Espacios para firmas (socio y autorizado)

#### 💳 Recibo de Pago (Factura Simplificada)
- **Ubicación**: `report/gym_partner_templates.xml` (Template: `report_gym_subscription_receipt`)
- **Generador**: Desde modelo Suscripción (gym.subscription)
- **Contenido**:
  - Logo e información del gimnasio con RUC
  - Número de recibo y fecha
  - Datos del socio
  - Detalles de la suscripción:
    - Concepto (tipo de plan)
    - Período de cobertura
    - Cuota mensual
  - Método de pago
  - Resumen financiero:
    - Subtotal
    - Descuentos aplicables
    - Monto pagado
    - Saldo pendiente
  - Términos y condiciones
  - Espacios para firmas

### ✅ 2. Vistas de Análisis (Business Intelligence)

#### 📊 Gráficos (Graph View)
- **Ingresos por Mes**: Vista con línea de evolución mensual
- **Distribución de Planes**: Gráfico de pie mostrando ingresos por tipo de plan
- **Ocupación por Tipo de Clase**: Barras con ocupación de cada tipo de actividad
- **Capacidad vs Ocupación**: Comparativa de capacidad instalada vs actual
- **Distribución de Socios**: Pie chart de estados de socios
- **Evolución de Socios**: Línea de crecimiento mensual

#### 🔄 Tablas Pivot
- **Ingresos**: Planes vs Estados con sumas de ingresos y pagos
- **Profesores vs Ingresos**: Instructores vs total de clases y estudiantes
- **Socios**: Estados vs período de registro (mes) con conteos

#### 📍 Ubicación
`views/gym_analysis_views.xml` - Menú Gimnasio > Análisis

### ✅ 3. Acciones de Servidor y Automatización

#### ⏰ Acción Planificada (Cron)
- **Nombre**: "Revisar Suscripciones Vencidas"
- **Frecuencia**: Diaria (ejecuta cada 24 horas)
- **Función**: 
  - Revisa todas las suscripciones con estado "activo" o "pausado"
  - Compara fecha de vencimiento (end_date) con hoy
  - Cambia automáticamente a estado "Expirado" si ya vencieron
  - Se ejecuta como usuario root
  - Siempre activo

- **Ubicación**: 
  - Archivo XML: `data/gym_cron.xml`
  - En Odoo: Configuración > Datos Técnicos > Acciones Planificadas > "Revisar Suscripciones Vencidas"

- **Método correspondiente**: `gym.subscription.check_expired_subscriptions()`
  - Ubicación: `models/gym_subscription.py`

---

## 📁 Estructura de Archivos del Módulo

```
gym_management/
├── __init__.py                          # Inicialización del módulo
├── __manifest__.py                      # Metadatos del módulo
├── README.md                            # Documentación
│
├── models/
│   ├── __init__.py
│   ├── gym_instructor.py               # Modelo: Instructores
│   ├── gym_class.py                    # Modelo: Clases
│   ├── gym_subscription.py             # Modelo: Suscripciones
│   └── gym_partner.py                  # Modelo: Socios
│
├── views/
│   ├── gym_instructor_views.xml        # Vistas de Instructores
│   ├── gym_class_views.xml             # Vistas de Clases
│   ├── gym_subscription_views.xml      # Vistas de Suscripciones
│   ├── gym_partner_views.xml           # Vistas de Socios
│   └── gym_analysis_views.xml          # Vistas de Análisis (Reportes BI)
│
├── report/
│   ├── __init__.py
│   ├── gym_partner_reports.xml         # Configuración de reportes
│   └── gym_partner_templates.xml       # Templates QWeb de reportes
│
├── security/
│   ├── __init__.py
│   └── ir.model.access.csv             # Reglas de seguridad
│
├── data/
│   ├── __init__.py
│   ├── gym_cron.xml                    # Acción planificada
│   └── demo_data.xml                   # Datos de demostración
│
└── static/
    └── description/
```

---

## 🗂️ Modelos de Datos Implementados

### 1️⃣ gym.partner (Socio)
**Campos principales:**
- Personal: name, email, phone, mobile, id_type, id_number
- Ubicación: street, number, city, state_id, zip_code, country
- Médica: blood_type, allergies, medical_conditions
- Emergencia: emergency_contact, emergency_phone
- Foto: image_1920
- Relaciones: subscription_ids (One2many)
- Calculados: active_subscription_id, total_paid, total_pending, etc.
- Estado: prospect, active, suspended, inactive
- Métodos: action_mark_active, action_mark_suspended, action_create_subscription

### 2️⃣ gym.subscription (Suscripción)
**Campos principales:**
- Socio: partner_id (Many2one)
- Plan: plan_type (básico, premium, VIP, personalizado)
- Fechas: start_date, end_date
- Montos: monthly_fee, discount, amount_paid, remaining_balance (calculado)
- Clases: class_ids (Many2many), unlimited_classes
- Pago: payment_method
- Estado: draft, active, paused, expired, cancelled
- Método importante: check_expired_subscriptions() - Usado por el cron

### 3️⃣ gym.class (Clase)
**Campos principales:**
- Información: name, class_type (yoga, crossfit, pilates, etc.)
- Instructor: instructor_id (Many2one)
- Horario: day_of_week, start_time, duration
- Capacidad: capacity, current_enrollment (calculado), available_spots (calculado)
- Precio: price
- Suscriptores: subscription_ids (Many2many)
- Estado: draft, active, cancelled

### 4️⃣ gym.instructor (Instructor)
**Campos principales:**
- Personal: name, email, phone, specializations
- Biografía: bio, image_1920
- Clases: class_ids (One2many)
- Calculados: total_classes, total_students
- Estado: active, inactive

---

## 🔐 Seguridad y Permisos

Archivo: `security/ir.model.access.csv`

**Roles definidos:**
- `access_gym_*_all`: Usuarios normales (lectura, escritura, creación)
- `access_gym_*_manager`: Gerentes ERP (acceso total incluyendo eliminación)

Modelos protegidos:
- gym.instructor
- gym.class
- gym.subscription
- gym.partner

---

## 📊 Vistas Implementadas

### Vista de Árbol (Lista)
- Todas los modelos tienen vista de árbol con campos relevantes
- Decoraciones de color según estado
- Columnas optimizadas para análisis rápido

### Vista de Formulario
- Formularios completos con pestañas
- Headers con acciones específicas
- Campos calculados en modo lectura
- Integración con chatter (comentarios y actividades)

### Vista de Búsqueda y Filtros
- Filtros predefinidos por estado
- Búsquedas en múltiples campos
- Agrupación dinámica
- Filtros contextuales (ej: "Con saldo pendiente")

### Vistas Especializadas
- **Kanban**: Vista de Socios con estatus visual
- **Calendario**: Vista de Clases con calendario
- **Graph**: 6 gráficos distintos para análisis
- **Pivot**: 3 tablas dinámicas para análisis cruzado

---

## 🎬 Cómo Instalar y Usar

### Instalación

1. **Copiar módulo a Odoo:**
   ```bash
   cp -r gym_management /path/to/odoo/addons/
   ```

2. **Actualizar lista de módulos en Odoo**
   - Ir a Aplicaciones
   - Hacer clic en "Actualizar lista de aplicaciones"

3. **Buscar e instalar**
   - Buscar "Gym Management"
   - Hacer clic en "Instalar"

4. **Cargar datos de demostración (opcional)**
   - Durante la instalación, marcar "Cargar datos de demo"
   - O reinstalar con demo data

### Uso Básico

#### Crear un Socio
```
Gimnasio > Socios > Crear
- Llenar nombre, email, teléfono
- Agregar información personal/médica
- Guardar
```

#### Crear una Suscripción
```
Desde Socio: Click en "Nueva Suscripción"
O: Gimnasio > Suscripciones > Crear
- Seleccionar socio y tipo de plan
- Establecer fechas
- Ingresar monto y descuento
- Guardar y Activar
```

#### Crear una Clase
```
Gimnasio > Clases > Crear
- Nombre, tipo, instructor
- Día y horario
- Capacidad máxima
- Precio (opcional)
- Activar
```

#### Ver Reportes
```
Desde Socio:
  > Imprimir > Ficha de Inscripción

Desde Suscripción:
  > Imprimir > Recibo de Pago
```

#### Ver Análisis
```
Gimnasio > Análisis > [Seleccionar análisis]
- Análisis de Ingresos (gráficos y pivot)
- Análisis de Clases (ocupación)
- Análisis de Instructores (rendimiento)
- Análisis de Socios (crecimiento)
```

#### Verificar Cron
```
Configuración > Datos Técnicos > Acciones Planificadas
- Buscar: "Revisar Suscripciones Vencidas"
- Ver: Última ejecución, próxima ejecución
- Estado: Debe estar "Activo"
```

---

## 📈 Datos de Demostración Incluidos

### Instructores (3)
- Juan Pérez Flores: Yoga, Pilates
- María García López: CrossFit, Boxeo
- Carlos Rodríguez Martínez: Spinning, Zumba

### Clases (3)
- Yoga Matutino (Lunes 6:30 AM)
- CrossFit Avanzado (Martes 5:30 PM)
- Spinning Nocturno (Miércoles 6:00 PM)

### Socios (3)
- Roberto Sánchez Díaz: Activo
- Patricia Hernández Vega: Activo
- Andrés Morales Castillo: Prospecto

### Suscripciones (3)
- Plan Básico: S/ 150 (Pagada)
- Plan Premium: S/ 300 con 10% descuento (Pagada)
- Plan VIP: S/ 500 (Pendiente de pago)

---

## 🔄 Automatización - Detalles del Cron

**Acción Planificada: "Revisar Suscripciones Vencidas"**

### Configuración
| Parámetro | Valor |
|-----------|-------|
| Modelo | gym.subscription |
| Método | check_expired_subscriptions() |
| Frecuencia | Cada 1 día |
| Usuario | Administrator (root) |
| Activo | Siempre |
| Repeticiones | Infinito (-1) |

### Lógica en `models/gym_subscription.py`
```python
def check_expired_subscriptions(self):
    """
    Cron Job: Revisa diariamente suscripciones vencidas
    """
    today = fields.Date.today()
    
    # 1. Busca suscripciones activas/pausadas que vencieron
    expired_subs = self.search([
        ('state', 'in', ['active', 'paused']),
        ('end_date', '<', today)
    ])
    
    # 2. Cambia estado a expirado
    for subscription in expired_subs:
        subscription.action_mark_expired()
    
    # 3. Retorna cantidad procesada
    return len(expired_subs)
```

### Ejemplo de Ejecución
```
HOY: 5 de Marzo 2026
Suscripción 1: end_date = 2 de Marzo 2026 → EXPIRADA ✓
Suscripción 2: end_date = 4 de Marzo 2026 → EXPIRADA ✓
Suscripción 3: end_date = 10 de Marzo 2026 → ACTIVA (sin cambios)

Resultado: 2 suscripciones cambiarán a estado "Expirado"
```

---

## ✨ Características Avanzadas

### Campos Calculados/Dinámicos
- `total_paid`: Suma de montos pagados
- `total_pending`: Suma de saldos pendientes
- `current_enrollment`: Conteo de suscriptores en clase
- `available_spots`: Capacidad - Ocupación
- `active_subscription_id`: Primera suscripción activa del socio
- `remaining_balance`: Monto adeudado

### Filtros Inteligentes
```xml
<!-- Ejemplos de filtros predefinidos -->
<filter name="active_partners" string="Activos" 
        domain="[('state', '=', 'active')]"/>
<filter name="expired_subs" string="Expiradas" 
        domain="[('state', '=', 'expired')]"/>
<filter name="with_pending" string="Con saldo pendiente"
        domain="[('total_pending', '&gt;', 0)]"/>
```

### Métodos de Transición de Estados
```python
# En cada modelo
action_activate()      # Cambiar a activo
action_pause()        # Pausar (suscripciones)
action_cancel()       # Cancelar
action_mark_expired() # Marcar expirado
toggle_active()       # Alternar activo/inactivo (instructores)
```

---

## 🎨 Interfaz y UX

### Colores y Decoraciones
```xml
<!-- En vistas de árbol -->
decoration-success="state == 'active'"      <!-- Verde -->
decoration-danger="state == 'expired'"      <!-- Rojo -->
decoration-warning="state == 'paused'"      <!-- Naranja -->
decoration-info="state == 'draft'"          <!-- Azul -->
```

### Acciones Contextuales
- Botones dinámicos según estado
- Botones para crear relaciones (ej: "Nueva Suscripción")
- Estadísticas visuales (ej: total de suscripciones)

### Búsqueda Flexible
```xml
<field name="name" string="Nombre o Especialidad"
       filter_domain="['|', ('name', 'ilike', self), 
                           ('specializations', 'ilike', self)]"/>
```

---

## 🚀 Próximas Mejoras (Roadmap)

- [ ] Módulo de asistencia con check-in QR
- [ ] Portal para socios (autoservicio)
- [ ] Integración con pasarelas de pago
- [ ] SMS automático de recordatorios
- [ ] Descuentos y promociones
- [ ] Programa de referidos y puntos
- [ ] Certificados de participación
- [ ] Integración con videos de clases
- [ ] App móvil nativa
- [ ] Estadísticas de IMC y progreso

---

## 📞 Soporte Técnico

Para problemas con el módulo:
1. Verificar instalación de dependencias
2. Revisar logs de Odoo
3. Validar permisos de archivos
4. Reiniciar servidor Odoo

## 📄 Licencia

LGPL-3

---

**Módulo desarrollado para Odoo 19.0**
**Última actualización: Marzo 2026**
