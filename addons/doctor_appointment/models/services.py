from odoo import models, fields, api

class Service(models.Model):
    _name = 'appointment.service'
    _description = 'Appointment Services'
    _order = 'create_date desc'
    
    name = fields.Char(string='Service Name')
    service_image = fields.Binary()
    category_id = fields.Many2one('appointment.category', string='Category')
    duration = fields.Float(string='Duration (hours)', default=1.0)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    doctor_ids = fields.Many2many('appointment.doctors', string='Available Doctors')
    price = fields.Float(string='Service Price')
    currency_id = fields.Many2one(
        'res.currency', 
        string='Currency', 
        default=lambda self: self.env['res.currency'].search([('name', '=', 'INR')], limit=1).id
    )
    price_with_currency = fields.Char(string='Price with Currency', compute='_compute_price_with_currency', store=False)

    @api.depends('price', 'currency_id')
    def _compute_price_with_currency(self):
        for service in self:
            if service.price and service.currency_id:
                service.price_with_currency = f"{service.price} {service.currency_id.symbol}"
            else:
                service.price_with_currency = ''

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'The service name must be unique.')
    ]


