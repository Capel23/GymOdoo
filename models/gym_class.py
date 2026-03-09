from odoo import models, fields, api
from datetime import datetime, timedelta


class GymClass(models.Model):
    _name = 'gym.class'
    _description = 'Clase del Gimnasio'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _check_capacity_positive = models.Constraint(
        'CHECK(capacity > 0)',
        'La capacidad máxima debe ser mayor a 0.',
    )
    _check_price_positive = models.Constraint(
        'CHECK(price >= 0)',
        'El precio no puede ser negativo.',
    )

    name = fields.Char('Nombre de la Clase', required=True, tracking=True)
    class_type = fields.Selection([
        ('yoga', 'Yoga'),
        ('crossfit', 'CrossFit'),
        ('pilates', 'Pilates'),
        ('zumba', 'Zumba'),
        ('boxeo', 'Boxeo'),
        ('natacion', 'Natación'),
        ('spinning', 'Spinning'),
        ('otro', 'Otro'),
    ], required=True, tracking=True, string='Tipo de Clase')
    
    description = fields.Text('Descripción')
    
    # Instructor
    instructor_id = fields.Many2one('gym.instructor', string='Instructor', required=True, 
                                    ondelete='restrict', tracking=True)
    
    # Horario y capacidad
    day_of_week = fields.Selection([
        ('0', 'Lunes'),
        ('1', 'Martes'),
        ('2', 'Miércoles'),
        ('3', 'Jueves'),
        ('4', 'Viernes'),
        ('5', 'Sábado'),
        ('6', 'Domingo'),
    ], required=True, string='Día de la Semana', tracking=True)
    
    start_time = fields.Float('Hora Inicio', required=True, help='Formato: 9.5 para 09:30')
    duration = fields.Float('Duración (minutos)', required=True, default=60)
    capacity = fields.Integer('Capacidad Máxima', required=True, default=20)
    current_enrollment = fields.Integer('Inscritos Actuales', compute='_compute_current_enrollment', 
                                        store=True, readonly=True)
    available_spots = fields.Integer('Espacios Disponibles', compute='_compute_available_spots',
                                    store=True, readonly=True)
    occupancy_rate = fields.Float('Ocupación (%)', compute='_compute_occupancy_rate',
                                  store=True, readonly=True,
                                  help='Porcentaje de ocupación respecto a la capacidad máxima')

    # Precio
    price = fields.Float('Precio por Sesión', default=0)
    
    # Estado
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('active', 'Activa'),
        ('cancelled', 'Cancelada'),
    ], default='draft', tracking=True, string='Estado')
    
    active = fields.Boolean(default=True)
    
    # Relaciones
    subscription_ids = fields.Many2many('gym.subscription', relation='gym_class_subscription',
                                        string='Suscripciones')

    @api.depends('subscription_ids')
    def _compute_current_enrollment(self):
        for record in self:
            record.current_enrollment = len(record.subscription_ids)

    @api.depends('current_enrollment', 'capacity')
    def _compute_available_spots(self):
        for record in self:
            record.available_spots = record.capacity - record.current_enrollment

    @api.depends('current_enrollment', 'capacity')
    def _compute_occupancy_rate(self):
        for record in self:
            if record.capacity > 0:
                record.occupancy_rate = (record.current_enrollment / record.capacity) * 100.0
            else:
                record.occupancy_rate = 0.0

    def action_activate(self):
        """Activar la clase"""
        for record in self:
            record.state = 'active'

    def action_cancel(self):
        """Cancelar la clase"""
        for record in self:
            record.state = 'cancelled'

    def format_time(self):
        """Convierte float a formato hora HH:MM"""
        hours = int(self.start_time)
        minutes = int((self.start_time - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"
