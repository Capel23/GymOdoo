from odoo import models, fields, api
from datetime import datetime, timedelta


class GymPartner(models.Model):
    _name = 'gym.partner'
    _description = 'Socio del Gimnasio'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Información personal
    name = fields.Char('Nombre Completo', required=True, tracking=True)
    email = fields.Char('Email', tracking=True)
    phone = fields.Char('Teléfono', tracking=True)
    mobile = fields.Char('Móvil', tracking=True)
    
    # Documento de identidad
    id_type = fields.Selection([
        ('dni', 'DNI'),
        ('passport', 'Pasaporte'),
        ('ruc', 'RUC'),
        ('other', 'Otro'),
    ], string='Tipo de Documento', default='dni')
    id_number = fields.Char('Número de Documento', tracking=True)
    
    # Información de contacto
    street = fields.Char('Calle')
    number = fields.Char('Número')
    city = fields.Char('Ciudad')
    state_id = fields.Char('Departamento/Provincia')
    zip_code = fields.Char('Código Postal')
    country = fields.Char('País', default='Perú')
    
    # Información médica
    blood_type = fields.Selection([
        ('o_pos', 'O+'),
        ('o_neg', 'O-'),
        ('a_pos', 'A+'),
        ('a_neg', 'A-'),
        ('b_pos', 'B+'),
        ('b_neg', 'B-'),
        ('ab_pos', 'AB+'),
        ('ab_neg', 'AB-'),
    ], string='Tipo de Sangre')
    
    allergies = fields.Text('Alergias')
    medical_conditions = fields.Text('Condiciones Médicas')
    emergency_contact = fields.Char('Contacto de Emergencia')
    emergency_phone = fields.Char('Teléfono de Emergencia')
    
    # Foto
    image_1920 = fields.Image('Foto', max_width=1920, max_height=1920)
    
    # Suscripción(es)
    subscription_ids = fields.One2many('gym.subscription', 'partner_id', 
                                       string='Suscripciones')
    subscription_count = fields.Integer('Nº Suscripciones', compute='_compute_subscription_count')
    active_subscription_id = fields.Many2one('gym.subscription', 
                                             compute='_compute_active_subscription',
                                             string='Suscripción Activa')
    
    # Registros de asistencia
    attendance_count = fields.Integer('Asistencias', compute='_compute_attendance_count', 
                                      store=False)
    last_visit = fields.Datetime('Última Visita', compute='_compute_last_visit', store=False)
    
    # Información financiera
    total_paid = fields.Float('Total Pagado', compute='_compute_total_paid', store=True)
    total_pending = fields.Float('Total Pendiente', compute='_compute_total_pending', store=True)
    
    # Estado
    state = fields.Selection([
        ('prospect', 'Prospecto'),
        ('active', 'Activo'),
        ('suspended', 'Suspendido'),
        ('inactive', 'Inactivo'),
    ], default='prospect', tracking=True, string='Estado')
    
    registration_date = fields.Date('Fecha de Registro', default=fields.Date.today, 
                                   tracking=True)
    active = fields.Boolean(default=True)

    @api.depends('subscription_ids')
    def _compute_subscription_count(self):
        for record in self:
            record.subscription_count = len(record.subscription_ids)

    @api.depends('subscription_ids')
    def _compute_active_subscription(self):
        """Obtener la suscripción activa del socio"""
        for record in self:
            active_sub = record.subscription_ids.filtered(lambda s: s.state == 'active')
            record.active_subscription_id = active_sub[0] if active_sub else None

    def _compute_attendance_count(self):
        """Contar las asistencias (simulado por ahora)"""
        for record in self:
            record.attendance_count = 0

    def _compute_last_visit(self):
        """Obtener la última visita (simulado por ahora)"""
        for record in self:
            record.last_visit = None

    @api.depends('subscription_ids.amount_paid')
    def _compute_total_paid(self):
        """Total pagado en todas las suscripciones"""
        for record in self:
            record.total_paid = sum(record.subscription_ids.mapped('amount_paid'))

    @api.depends('subscription_ids.remaining_balance')
    def _compute_total_pending(self):
        """Total pendiente en todas las suscripciones"""
        for record in self:
            record.total_pending = sum(record.subscription_ids.mapped('remaining_balance'))

    @api.constrains('email')
    def _check_email(self):
        import re
        for record in self:
            if record.email and not re.match(
                r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$', record.email
            ):
                raise ValidationError(
                    "El formato del email '%s' no es válido." % record.email
                )

    @api.constrains('registration_date')
    def _check_registration_date(self):
        today = fields.Date.today()
        for record in self:
            if record.registration_date and record.registration_date > today:
                raise ValidationError("La fecha de registro no puede ser una fecha futura.")

    def action_create_subscription(self):
        """Crear una nueva suscripción para el socio"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Nueva Suscripción',
            'res_model': 'gym.subscription',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_partner_id': self.id,
                'default_start_date': fields.Date.today(),
            },
        }

    def action_view_subscriptions(self):
        """Ver suscripciones del socio"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Suscripciones',
            'res_model': 'gym.subscription',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }

    def action_mark_active(self):
        """Marcar socio como activo"""
        for record in self:
            record.state = 'active'

    def action_mark_suspended(self):
        """Marcar socio como suspendido"""
        for record in self:
            record.state = 'suspended'

    def action_mark_inactive(self):
        """Marcar socio como inactivo"""
        for record in self:
            record.state = 'inactive'

    def get_address_formatted(self):
        """Retorna la dirección formateada"""
        address_parts = [self.street, self.number, self.city, self.zip_code]
        return ', '.join([p for p in address_parts if p])
