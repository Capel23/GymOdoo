from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class GymSubscription(models.Model):
    _name = 'gym.subscription'
    _description = 'Suscripción del Socio'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Nombre de la Suscripción', compute='_compute_name', store=True)
    
    # Socio
    partner_id = fields.Many2one('gym.partner', string='Socio', required=True, 
                                 ondelete='cascade', tracking=True)
    
    # Plan
    plan_type = fields.Selection([
        ('basic', 'Plan Básico'),
        ('premium', 'Plan Premium'),
        ('vip', 'Plan VIP'),
        ('custom', 'Plan Personalizado'),
    ], required=True, tracking=True, string='Tipo de Plan')
    
    description = fields.Text('Descripción del Plan')
    
    # Fechas
    start_date = fields.Date('Fecha de Inicio', required=True, default=fields.Date.today, 
                             tracking=True)
    end_date = fields.Date('Fecha de Vencimiento', required=True, tracking=True)
    
    # Montos
    monthly_fee = fields.Float('Cuota Mensual', required=True, default=0, tracking=True)
    discount = fields.Float('Descuento (%)', default=0, help='Porcentaje de descuento')
    amount_paid = fields.Float('Monto Pagado', default=0, tracking=True)
    remaining_balance = fields.Float('Saldo Pendiente', compute='_compute_remaining_balance', 
                                     store=True, readonly=True)
    
    # Clases
    class_ids = fields.Many2many('gym.class', relation='gym_class_subscription',
                                string='Clases Incluidas')
    unlimited_classes = fields.Boolean('Clases Ilimitadas', default=False)
    
    days_remaining = fields.Integer('Días Restantes', compute='_compute_days_remaining',
                                    help='Días que faltan para que venza la suscripción')

    # Estado
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('active', 'Activa'),
        ('paused', 'Pausada'),
        ('expired', 'Expirada'),
        ('cancelled', 'Cancelada'),
    ], default='draft', tracking=True, string='Estado')
    
    active = fields.Boolean(default=True)
    
    # Método de pago
    payment_method = fields.Selection([
        ('cash', 'Efectivo'),
        ('transfer', 'Transferencia'),
        ('card', 'Tarjeta'),
        ('check', 'Cheque'),
    ], string='Método de Pago', tracking=True)
    
    # Notas
    notes = fields.Text('Notas', tracking=True)

    @api.depends('partner_id', 'plan_type', 'start_date')
    def _compute_name(self):
        for record in self:
            if record.partner_id:
                record.name = f"{record.partner_id.name} - {record.get_plan_type_display()} ({record.start_date})"
            else:
                record.name = "Nueva Suscripción"

    def get_plan_type_display(self):
        """Retorna el nombre legible del tipo de plan"""
        plan_dict = {
            'basic': 'Básico',
            'premium': 'Premium',
            'vip': 'VIP',
            'custom': 'Personalizado',
        }
        return plan_dict.get(self.plan_type, self.plan_type)

    @api.depends('monthly_fee', 'discount', 'amount_paid')
    def _compute_remaining_balance(self):
        for record in self:
            total_amount = record.monthly_fee * (1 - record.discount / 100)
            record.remaining_balance = total_amount - record.amount_paid

    @api.depends('end_date')
    def _compute_days_remaining(self):
        today = fields.Date.today()
        for record in self:
            if record.end_date:
                delta = record.end_date - today
                record.days_remaining = delta.days
            else:
                record.days_remaining = 0

    @api.onchange('plan_type', 'start_date')
    def _onchange_plan_type(self):
        """Sugiere la cuota mensual y calcula la fecha de vencimiento según el plan"""
        prices = {'basic': 80.0, 'premium': 150.0, 'vip': 250.0, 'custom': 100.0}
        if self.plan_type:
            self.monthly_fee = prices.get(self.plan_type, 0.0)
        if self.start_date:
            from dateutil.relativedelta import relativedelta
            self.end_date = self.start_date + relativedelta(months=1)

    @api.constrains('amount_paid')
    def _check_amount_paid(self):
        for record in self:
            if record.amount_paid < 0:
                raise ValidationError("El monto pagado no puede ser negativo.")

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        """Validar que la fecha de vencimiento sea posterior a la de inicio"""
        for record in self:
            if record.start_date and record.end_date:
                if record.end_date <= record.start_date:
                    raise ValidationError("La fecha de vencimiento debe ser posterior a la fecha de inicio")

    def action_activate(self):
        """Activar la suscripción"""
        for record in self:
            record.state = 'active'

    def action_pause(self):
        """Pausar la suscripción"""
        for record in self:
            record.state = 'paused'

    def action_cancel(self):
        """Cancelar la suscripción"""
        for record in self:
            record.state = 'cancelled'

    def action_mark_expired(self):
        """Marcar como expirada"""
        for record in self:
            record.state = 'expired'

    def check_expired_subscriptions(self):
        """
        Método llamado por el cron para verificar suscripciones vencidas.
        Cron Action Method.
        """
        today = fields.Date.today()
        expired_subs = self.search([
            ('state', 'in', ['active', 'paused']),
            ('end_date', '<', today)
        ])
        for subscription in expired_subs:
            subscription.action_mark_expired()
        return len(expired_subs)

    def reconcile_payment(self, amount):
        """Registrar un pago en la suscripción"""
        self.amount_paid += amount
        if self.remaining_balance <= 0:
            # La suscripción está pagada
            return True
        return False
