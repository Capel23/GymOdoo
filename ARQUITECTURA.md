# 🏗️ Arquitectura y Relaciones del Módulo Gym Management

## Diagrama de Entidades (ERD)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DIAGRAMA DE RELACIONES                        │
└─────────────────────────────────────────────────────────────────────┘

                        ┌──────────────────┐
                        │  gym.instructor  │
                        │   (Instructor)   │
                        ├──────────────────┤
                        │ id               │
                        │ name             │
                        │ email            │
                        │ specializations  │
                        │ total_classes◄───┼─────┐ [Calculado]
                        │ total_students◄──┼─────┤ [Calculado]
                        │ state            │     │
                        └────────┬─────────┘     │
                                 │              │
                    ┌────────────┼──────────────┘
                    │            │
                    │ 1:N        │
                    │ (class_ids)│
                    │            │
                    ▼            │
    ┌──────────────────────────────────────────┐
    │        gym.class (Clase)                 │
    ├──────────────────────────────────────────┤
    │ id                                       │
    │ name                                     │
    │ class_type (yoga, crossfit, etc.)       │
    │ instructor_id ───┐                       │
    │ day_of_week      │      CLASS            │
    │ start_time       │    HAS MANY           │
    │ capacity         │    SUSCRIBER          │
    │ current_enrollment◄──┤ [Calculado]      │
    │ available_spots◄─┼─┤ [Calculado]        │
    │ price            │                       │
    │                  │                       │
    │ subscription_ids ├──┐  N:M             │
    │    (Many2many)   │  │ (Relación)       │
    │ state            │  │                   │
    └────────┬─────────┘  │                   │
             │            │                   │
      N:M    │            │                   │
      Rel    │            │                   │
           ┌─┴────────────┴────────┐          │
           │                       │          │
           ▼                       ▼          │
    ┌──────────────────────────────────────────┐
    │    gym.subscription (Suscripción)        │
    ├──────────────────────────────────────────┤
    │ id                                       │
    │ partner_id ─────────────┐                │
    │ plan_type               │               │
    │ start_date              │               │
    │ end_date (vencimiento)  │               │
    │ monthly_fee             │               │
    │ discount                │               │
    │ amount_paid             │               │
    │ remaining_balance◄──┬───┤ [Calculado]   │
    │ unlimited_classes      │               │
    │ payment_method         │               │
    │ state                  │               │
    │ class_ids ──────────────┼──►[Many2many]│
    │ notes                   │               │
    └────────┬────────────────┤──────■        │
             │                │      │        │
    1:N      │                │      │        │
    (Many)   │                │      │        │
             │                │      │        │
             ▼                │      │        │
    ┌──────────────────────────────────────────┐
    │     gym.partner (Socio)                  │
    ├──────────────────────────────────────────┤
    │ id                                       │
    │ name                                     │
    │ email                                    │
    │ phone, mobile                            │
    │ id_type, id_number                       │
    │ street, number, city, zip_code           │
    │ blood_type                               │
    │ allergies                                │
    │ medical_conditions                       │
    │ emergency_contact, emergency_phone       │
    │ image_1920                               │
    │                                          │
    │ subscription_ids◄────┐ [One2many]       │
    │ active_subscription  │ [Calculado]      │
    │ total_paid◄──────────┤ [Calculado]      │
    │ total_pending◄───────┤ [Calculado]      │
    │ attendance_count◄────┤ [Calculado]      │
    │                      │                  │
    │ state                │                  │
    │ registration_date    │                  │
    │ active               │                  │
    └──────────────────────┼───────────────────┘
                           │
                        [Contiene]
```

## Flujo de Estados

### Socio (gym.partner)
```
  prospect (Prospecto)
      │
      ▼
  active (Activo) ◄─────────────┐
      │                          │
      └──────┬──────┬───────────┘
             │      │
             ▼      ▼
      suspended   inactive
      (Suspendido) (Inactivo)
```

### Suscripción (gym.subscription)
```
  draft (Borrador)
      │
      ▼
  active (Activa) ─────┬───────┐
      │                │       │
      │          paused│       │  [CRON Diario]
      │          (Pausa│da)    │
      │                │       │
      └────────┬───────┘       │
               │               │
               ▼               ▼
          cancelled────────► expired
          (Cancelada)      (Expirada)
          
          [El CRON ejecuta:
           - Si hoy > end_date y state='active'|'paused'
           - Entonces: state = 'expired']
```

### Clase (gym.class)
```
  draft (Borrador)
      │
      ▼
  active (Activa)
      │
      └──────► cancelled
               (Cancelada)
```

### Instructor (gym.instructor)
```
  active (Activo)      inactive (Inactivo)
      │                         ▲
      └──────────────────────────┘
      [Método toggle_active()
       cambia entre estados]
```

## Relaciones de Datos

### 1:N (Uno a Muchos)
```
Instructor ───────► Clases
(1 instructor)      (N clases)

Socio ──────────────► Suscripciones
(1 socio)            (N suscripciones)
```

### N:M (Muchos a Muchos)
```
Clase  ◄──────────────► Suscripción
(N)     (Relación)      (M)
        gym_class_subscription
        (tabla intermedia)
```

## Flujo de Negocio

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUJO DE NEGOCIO                             │
└─────────────────────────────────────────────────────────────────┘

1. REGISTRAR SOCIO
   ┌──────────────────────┐
   │  Crear nim.partner   │
   │  - Datos personales  │
   │  - Información médica│
   │  - Contacto emergenc│
   └──────────────────────┘
          │
          ▼
   Estado: Prospecto
   
2. CREAR SUSCRIPCIÓN
   ┌──────────────────────┐
   │ Crear gym.subscription
   │ - Seleccionar plan   │
   │ - Fechas             │
   │ - Cuota              │
   │ - Clases incluidas   │
   └──────────────────────┘
          │
          ▼
   Estado: Borrador
          │
          ▼ [Activar]
   Estado: Activa
          │
          ├──► [Pausar] → Paused
          │
          ├──► [Cancelar] → Cancelled
          │
          └──► [Esperar a vencimiento]
                    │
                    ▼ [CRON Diario]
                   EXPIRADA
                   
3. FACTURACIÓN
   ┌─────────────────────┐
   │ Imprimir Recibo PDF │
   │ Desde suscripción   │
   │ - Concepto cuota    │
   │ - Monto             │
   │ - Descuentos        │
   │ - Saldo             │
   └─────────────────────┘

4. ANÁLISIS
   ┌─────────────────────┐
   │ Ver Gráficos/Pivot  │
   │ - Ingresos/mes      │
   │ - Ocupación clases  │
   │ - Profesores        │
   │ - Evolución socios  │
   └─────────────────────┘
```

## Cálculos Automáticos

```
┌─────────────────────────────────────────────────────────────────┐
│              CAMPOS CALCULADOS EN TIEMPO REAL                   │
└─────────────────────────────────────────────────────────────────┘

SUSCRIPCIÓN (gym.subscription)
├─ remaining_balance = monthly_fee * (1 - discount/100) - amount_paid
└─ name = "{partner_name} - {plan_type} ({start_date})"

CLASE (gym.class)
├─ current_enrollment = COUNT(subscription_ids)
└─ available_spots = capacity - current_enrollment

SOCIO (gym.partner)
├─ total_paid = SUM(subscription_ids.amount_paid)
├─ total_pending = SUM(subscription_ids.remaining_balance)
├─ active_subscription_id = First(subscription_ids WHERE state='active')
└─ total_pending > 0 → [Filtro: Con saldo pendiente]

INSTRUCTOR (gym.instructor)
├─ total_classes = COUNT(class_ids)
└─ total_students = SUM(class_ids.capacity)
```

## Automatización (Cron)

```
┌────────────────────────────────────────────────────────────────┐
│         CRON: "Revisar Suscripciones Vencidas"                │
├────────────────────────────────────────────────────────────────┤
│ Frecuencia: Diaria (cada 24 horas)                            │
│ Usuario: Administrator (root)                                  │
│ Método: gym.subscription.check_expired_subscriptions()        │
├────────────────────────────────────────────────────────────────┤
│ LÓGICA:                                                        │
│                                                                │
│ Cada día ejecuta:                                             │
│                                                                │
│ 1. today = HOY                                                │
│ 2. Buscar todas las suscripciones donde:                      │
│    - state IN ['active', 'paused']                           │
│    - end_date < today                                        │
│ 3. Para cada suscripción encontrada:                         │
│    - Cambiar state = 'expired'                               │
│ 4. Retornar cantidad procesada                               │
│                                                                │
└────────────────────────────────────────────────────────────────┘

EJEMPLO DE EJECUCIÓN:
─────────────────────
Hora de ejecución: 03:00 AM (configurable)
Fecha: 5 de Marzo 2026

Búsqueda:
  SELECT * FROM gym_subscription
  WHERE state IN ('active', 'paused')
  AND end_date < '2026-03-05'

Resultados encontrados:
  ✓ ID 10: Suscripción Roberto - Vence 02/03 → EXPIRADA
  ✓ ID 12: Suscripción Patricia - Vence 04/03 → EXPIRADA
  ✗ ID 14: Suscripción Andrés - Vence 10/03 → SIN CAMBIOS

Registro en log:
  [2026-03-05 03:00:00] Cron "Revisar Suscripciones Vencidas"
  ejecutado exitosamente. 2 registros actualizados.
```

## Seguridad y Permisos

```
┌────────────────────────────────────────────────────────────────┐
│                    MATRIZ DE PERMISOS                          │
├────────────┬──────────┬──────────┬──────────┬────────────────┤
│  Modelo    │  Leer   │ Escribir │ Crear    │ Eliminar       │
├────────────┼──────────┼──────────┼──────────┼────────────────┤
│            │ Usuario  │ Usuario  │ Usuario  │ Usuario/Mgr    │
├────────────┼──────────┼──────────┼──────────┼────────────────┤
│ Socio      │    ✓     │    ✓     │    ✓     │ ✓ / ✓          │
│ Suscripción│    ✓     │    ✓     │    ✓     │ ✓ / ✓          │
│ Clase      │    ✓     │    ✓     │    ✓     │ ✓ / ✓          │
│ Instructor │    ✓     │    ✓     │    ✓     │ ✓ / ✓          │
├────────────┴──────────┴──────────┴──────────┴────────────────┤
│ Usuarios normales: Todos los permisos EXCEPTO eliminar       │
│ Gerentes ERP: Todos los permisos INCLUIDO eliminar           │
└────────────────────────────────────────────────────────────────┘
```

## Stack Tecnológico

```
┌──────────────────────────────────────────┐
│         STACK TÉCNICO ODOO 19.0          │
├──────────────────────────────────────────┤
│                                          │
│ Backend:                                 │
│ • Python 3.x                             │
│ • Odoo ORM (Models)                      │
│ • PostgreSQL (Base de datos)             │
│                                          │
│ Frontend:                                │
│ • QWeb (Motor de templates)              │
│ • XML (Vistas)                           │
│ • JavaScript (Interactividad)            │
│                                          │
│ Reportes:                                │
│ • QWeb + Wkhtmltopdf (PDFs)             │
│ • CSS para estilos                       │
│                                          │
│ Análisis:                                │
│ • Business Intelligence (Odoo BI)        │
│ • Gráficos (Chart.js)                    │
│ • Tablas Pivot (Odoo Pivot)              │
│                                          │
│ Automatización:                          │
│ • APScheduler (Cron Jobs)                │
│ • Python async                           │
│                                          │
└──────────────────────────────────────────┘
```

---

**Arquitectura diseñada para Odoo 19.0**  
**Última actualización: 3 de Marzo de 2026**
