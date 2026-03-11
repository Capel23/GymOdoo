# GymOdoo — Módulo de Gestión de Gimnasio para Odoo 19

Módulo personalizado desarrollado en **Odoo 19.0** para la gestión integral de socios, suscripciones, clases e instructores de un gimnasio.
Video de demostración en YOUTUBE: https://www.youtube.com/watch?v=zezGepJbUsY
---

## Índice

1. [Descripción](#descripción)
2. [Modelos y Relaciones](#modelos-y-relaciones)
3. [Restricciones Técnicas Implementadas](#restricciones-técnicas-implementadas)
4. [Lógica de Negocio](#lógica-de-negocio)
5. [Interfaz de Usuario](#interfaz-de-usuario)
6. [Instalación](#instalación)
7. [Datos de Prueba](#datos-de-prueba)

---

## Descripción

Módulo Odoo 19.0 completo para la gestión integral de socios y operaciones de un gimnasio. Incluye:

- **Gestión de Socios**: Registro detallado con información personal, médica y de contacto
- **Gestión de Suscripciones**: Planes de membresía con control de vencimiento automático
- **Gestión de Clases**: Horarios, instructores, capacidad y ocupación
- **Gestión de Instructores**: Registro de profesores con especialidades y estadísticas
- **Reportes QWeb**: Ficha de inscripción y recibos de pago profesionales
- **Business Intelligence**: Gráficos y vistas pivot para análisis de datos
- **Automatización**: Cron automático para revisar suscripciones vencidas

## Características Principales

### 1. Informes Técnicos (QWeb Reports)

#### Ficha de Inscripción
- Información personal del socio
- Datos médicos y de contacto
- Información de emergencia
- Suscripciones activas
- Espacios para firmas

#### Recibo de Pago
- Logo e información del gimnasio
- Datos del socio
- Detalles de la suscripción (concepto y monto)
- Método de pago
- Resumen financiero (subtotal, descuentos, pagado, saldo)
- Términos y condiciones

### 2. Vistas de Análisis (Business Intelligence)

#### Gráficos disponibles:
- **Ingresos por Mes**: Evolución de ingresos mensuales
- **Distribución de Planes**: Gráfico de pie showing ingresos por tipo de plan
- **Ocupación por Tipo de Clase**: Análisis de asistencia por tipo de actividad
- **Capacidad vs Ocupación**: Comparativa entre capacidad y ocupación actual
- **Distribución de Socios**: Estados de socios activos, inactivos, etc.
- **Evolución de Socios**: Crecimiento de inscritos por mes

#### Tablas Pivot:
- **Ingresos**: Cruzar planes vs estados con ingresos y pagos
- **Profesores vs Ingresos**: Análisis de clases y estudiantes por instructor
- **Socios**: Análisis por estado y mes de registro

### 3. Acción Planificada (Cron)

**Cron: "Revisar Suscripciones Vencidas"**
- Ejecuta diariamente
- Busca suscripciones con estado "activo" o "pausado" que hayan vencido
- Cambia automáticamente su estado a "Expirado"
- Método: `gym.subscription.check_expired_subscriptions()`

## Restricciones Técnicas Implementadas

Esta sección responde al criterio **ORM/Modelado (3 pts)** de la rúbrica.

### 1. Restricciones a nivel de base de datos (`models.Constraint`)

Odoo 19 reemplaza la lista `_sql_constraints` por atributos de clase `models.Constraint`. Se usan en:

**`gym.class`**
```python
_check_capacity_positive = models.Constraint(
    'CHECK(capacity > 0)',
    'La capacidad máxima debe ser mayor a 0.',
)
_check_price_positive = models.Constraint(
    'CHECK(price >= 0)',
    'El precio no puede ser negativo.',
)
```

**`gym.instructor`**
```python
_email_unique = models.Constraint(
    'UNIQUE(email)',
    'Ya existe un instructor con ese email.',
)
```

### 2. Restricciones a nivel de Python (`@api.constrains`)

**`gym.partner`** — Validación de formato de email con expresión regular:
```python
@api.constrains('email')
def _check_email_format(self):
    for record in self:
        if record.email:
            pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, record.email):
                raise ValidationError('El email no tiene un formato válido.')
```

**`gym.partner`** — Fecha de registro no puede ser futura:
```python
@api.constrains('registration_date')
def _check_registration_date(self):
    for rec in self:
        if rec.registration_date and rec.registration_date > fields.Date.today():
            raise ValidationError('La fecha de registro no puede ser futura.')
```

**`gym.subscription`** — El monto pagado no puede ser negativo:
```python
@api.constrains('amount_paid')
def _check_amount_paid(self):
    for rec in self:
        if rec.amount_paid < 0:
            raise ValidationError('El importe pagado no puede ser negativo.')
```

### 3. Campos calculados (`@api.depends`)

| Modelo | Campo | Descripción |
|--------|-------|-------------|
| `gym.class` | `occupancy_rate` | % de ocupación = (inscritos / capacidad) × 100 |
| `gym.class` | `current_enrollment` | Número de suscripciones activas en la clase |
| `gym.class` | `available_spots` | Espacios libres = capacidad − inscritos |
| `gym.subscription` | `days_remaining` | Días hasta el vencimiento de la suscripción |
| `gym.subscription` | `pending_amount` | Saldo pendiente = cuota − descuento − pagado |
| `gym.instructor` | `total_income` | Ingresos cruzando instructor → clases → suscripciones |
| `gym.instructor` | `total_classes` | Número de clases asignadas al instructor |
| `gym.partner` | `subscription_count` | Conteo de suscripciones para el stat button |

**Ejemplo de campo calculado cross-model (`total_income` en `gym.instructor`):**
```python
@api.depends('class_ids', 'class_ids.subscription_ids',
             'class_ids.subscription_ids.amount_paid',
             'class_ids.subscription_ids.state')
def _compute_total_income(self):
    for instructor in self:
        total = 0.0
        for clase in instructor.class_ids:
            subs = clase.subscription_ids.filtered(
                lambda s: s.state in ('active', 'paused', 'expired')
            )
            total += sum(subs.mapped('amount_paid'))
        instructor.total_income = total
```

### 4. Autocompletado con `@api.onchange`

Al cambiar el tipo de plan o la fecha de inicio en una suscripción, se autocompletan la cuota y la fecha de vencimiento:
```python
@api.onchange('plan_type', 'start_date')
def _onchange_plan_type(self):
    fees = {'basic': 80.0, 'premium': 150.0, 'vip': 250.0}
    if self.plan_type in fees:
        self.monthly_fee = fees[self.plan_type]
    if self.start_date:
        self.end_date = self.start_date + relativedelta(months=1)
```

### 5. Relaciones entre modelos

| Relación | Modelos | Tipo |
|----------|---------|------|
| Socio → Suscripciones | `gym.partner` → `gym.subscription` | One2many |
| Suscripción → Socio | `gym.subscription` → `gym.partner` | Many2one |
| Suscripción → Clases | `gym.subscription` ↔ `gym.class` | Many2many |
| Clase → Instructor | `gym.class` → `gym.instructor` | Many2one |
| Instructor → Clases | `gym.instructor` → `gym.class` | One2many |

---

## Modelos y Relaciones

### gym.partner (Socio)
```python
- Información personal: nombre, email, teléfono, documento
- Ubicación: dirección, ciudad, país
- Información médica: tipo de sangre, alergias, condiciones
- Contacto de emergencia
- Foto
- Estado: prospecto, activo, suspendido, inactivo
- Relación: múltiples suscripciones
```

### gym.subscription (Suscripción)
```python
- Socio relacionado
- Tipo de plan: básico, premium, VIP, personalizado
- Fechas: inicio y vencimiento
- Montos: cuota mensual, descuento, pagado, saldo pendiente
- Clases incluidas
- Estado: borrador, activa, pausada, expirada, cancelada
- Método de pago
```

### gym.class (Clase)
```python
- Nombre y tipo: yoga, crossfit, pilates, zumba, boxeo, natación, spinning
- Instructor
- Horario: día y hora
- Capacidad
- Precio por sesión
- Ocupación en tiempo real
- Estado: borro, activa, cancelada
```

### gym.instructor (Instructor)
```python
- Datos personales
- Especialidades
- Biografía
- Foto
- Relación: clases asignadas
- Estadísticas: total de clases, total de estudiantes
```

## Lógica de Negocio

### Automatización: Cron de suscripciones vencidas

Una acción planificada (`ir.cron`) se ejecuta **diariamente** y marca como `expired` todas las suscripciones activas o pausadas cuya `end_date` haya pasado:

```python
def check_expired_subscriptions(self):
    today = fields.Date.today()
    expired = self.search([
        ('state', 'in', ['active', 'paused']),
        ('end_date', '<', today),
    ])
    expired.write({'state': 'expired'})
```

### Reportes QWeb

| Reporte | Modelo | Descripción |
|---------|--------|-------------|
| Ficha de Inscripción | `gym.partner` | Datos personales, médicos y suscripciones activas |
| Recibo de Pago | `gym.subscription` | Detalles del plan, montos pagados y saldo |

---

## Interfaz de Usuario

### Decoraciones dinámicas en vistas de lista

**Clases** — colorea la fila según el % de ocupación:
```xml
<list decoration-danger="occupancy_rate >= 100"
      decoration-warning="occupancy_rate >= 80 and occupancy_rate &lt; 100">
```

**Suscripciones** — alerta cuando quedan pocos días:
```xml
<list decoration-danger="days_remaining <= 7 and state == 'active'"
      decoration-warning="days_remaining <= 15 and state == 'active'">
```

### Stat button en Socios

Muestra el número de suscripciones de cada socio con acceso directo:
```xml
<button name="action_view_subscriptions" type="object"
        class="oe_stat_button" icon="fa-id-card">
    <field name="subscription_count" widget="statinfo"
           string="Suscripciones"/>
</button>
```

### Vistas de Análisis (BI)

- **Gráfico de líneas**: Ingresos por mes  
- **Gráfico de tarta**: Distribución de planes  
- **Gráfico de barras**: Capacidad vs ocupación por tipo de clase  
- **Pivot**: Ingresos por plan/estado, instructores vs ingresos  

---

## Instalación

```bash
# 1. Copiar el módulo al directorio de addons
cp -r gym_management /path/to/odoo/addons/

# 2. Actualizar la lista de módulos
python odoo-bin -r <usuario> -w <contraseña> -d <base_de_datos> --update=all

# 3. Instalar desde Odoo: Aplicaciones > buscar "Gym Management" > Instalar
```

O con upgrade directo:
```bash
python odoo-bin -r odoo_user -w 1234 --addons-path=addons -d mi_odoo_db -u gym_management --stop-after-init
```

---

## Datos de Prueba

El repositorio incluye el script `insert_gym_data.py` para poblar la base de datos con:

- 3 instructores (Carlos Ramírez, Lucía Torres, Miguel Soto)
- 3 clases (Yoga Matutino, CrossFit Avanzado, Zumba Energética)
- 5 socios (Ana García López, Roberto Fernández Paz, Sofía Martínez Ruiz, Diego Vargas Quispe, Valentina Cruz Huanca)
- 4 suscripciones con distintos planes

```bash
python odoo-bin shell -r odoo_user -w 1234 -d mi_odoo_db --addons-path=addons < insert_gym_data.py
```

---

## Seguridad

Permisos definidos en `security/ir.model.access.csv`:

| Modelo | Usuario base | Gerente ERP |
|--------|-------------|-------------|
| gym.partner | leer/crear/escribir | + borrar |
| gym.subscription | leer/crear/escribir | + borrar |
| gym.class | leer/crear/escribir | + borrar |
| gym.instructor | leer/crear/escribir | + borrar |

---

## Tecnologías

- **Odoo 19.0** (Python 3.12)
- **PostgreSQL** (base de datos)
- **QWeb** (reportes PDF)
- **OWL** (framework de componentes frontend)
- **XML** (vistas y acciones)


## Licencia

LGPL-3
