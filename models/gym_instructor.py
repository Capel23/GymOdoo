from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GymInstructor(models.Model):
    _name = 'gym.instructor'
    _description = 'Instructor del Gimnasio'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _email_unique = models.Constraint(
        'UNIQUE(email)',
        'Ya existe un instructor registrado con este email.',
    )

    name = fields.Char('Nombre', required=True, tracking=True)
    email = fields.Char('Email', tracking=True)
    phone = fields.Char('Teléfono', tracking=True)
    specializations = fields.Char('Especialidades', help='Ej: Yoga, CrossFit, Pilates')
    bio = fields.Text('Biografía')
    image_1920 = fields.Image('Foto', max_width=1920, max_height=1920)
    
    # Relaciones
    class_ids = fields.One2many('gym.class', 'instructor_id', string='Clases')
    
    # Campos calculados
    total_classes = fields.Integer('Total de Clases', compute='_compute_total_classes', store=True)
    total_students = fields.Integer('Total de Estudiantes', compute='_compute_total_students', store=True)
    total_income = fields.Float('Ingresos Generados (S/)', compute='_compute_total_income', store=True,
                                help='Suma de pagos recibidos en suscripciones activas de sus clases')
    
    # Estado
    state = fields.Selection([
        ('active', 'Activo'),
        ('inactive', 'Inactivo'),
    ], default='active', tracking=True, string='Estado')
    
    active = fields.Boolean(default=True)

    @api.depends('class_ids')
    def _compute_total_classes(self):
        for record in self:
            record.total_classes = len(record.class_ids)

    @api.depends('class_ids')
    def _compute_total_students(self):
        for record in self:
            total = sum(record.class_ids.mapped('capacity'))
            record.total_students = total

    @api.depends('class_ids.subscription_ids.amount_paid', 'class_ids.subscription_ids.state')
    def _compute_total_income(self):
        for record in self:
            total = 0.0
            for cls in record.class_ids:
                paid_subs = cls.subscription_ids.filtered(
                    lambda s: s.state in ('active', 'paused', 'expired')
                )
                total += sum(paid_subs.mapped('amount_paid'))
            record.total_income = total

    def toggle_active(self):
        for record in self:
            record.active = not record.active
            record.state = 'inactive' if not record.active else 'active'
