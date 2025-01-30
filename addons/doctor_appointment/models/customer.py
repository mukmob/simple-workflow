from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime ,date
from odoo.tools import format_datetime
from collections import defaultdict
from dateutil.relativedelta import relativedelta

class Customer(models.Model):
    _name = 'appointment.customer'
    _description = 'appointment Appointment'
    _rec_name = 'partner_id'
    # _order = 'create_date desc'
    
    
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female'),
                               ('other', 'Other')], string="Gender")
    state = fields.Selection([('confirm', 'Confirm'), ('done', 'Done'), ('cancel', 'Cancel')], string="Status", default='confirm')
    status = fields.Selection([('married', 'Married'),
                               ('unmarried', 'Unmarried')],
                              string="Marital Status")
    profession = fields.Char(string="Profession")
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Char(compute='get_age', store=True, string="Age")
    contact = fields.Char(string='Contact Number')
    email = fields.Char(string="Email Id")
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street 2')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    zip = fields.Integer(string='Postal Code')
    country_id = fields.Many2one('res.country', string='Country')
    house_level = fields.Selection([('good', 'Good'),
                                    ('bad', 'Bad'),
                                    ('poor', 'Poor')],
                                   string="House Condition", help="Specify your house's condition")
    doctor_id = fields.Many2one(
        string='Appointment With',
        comodel_name='appointment.doctors'
    )
    service_ids = fields.Many2many(
        string='Services',
        comodel_name='appointment.service',
    ) 
    price = fields.Float(
        string='Total Price',
        compute='_compute_total_price',
        store=True,
    )
    customer_sequence = fields.Char(string='Customer Sequence', copy=False, 
    readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('appointment.customer.sequence'))
    
    time_slot_id = fields.Many2one(
        'appointment.time.slot', 
        string='Available Time Slot',
        domain="[('doctor_id', '=', doctor_id),('day', '=', selected_day)]"
    )
    appointment_date = fields.Date(string='Appointment Date')
    selected_day = fields.Char(string="Selected Day", compute="_compute_selected_day", store=False)
    

    @api.depends('appointment_date')
    def _compute_selected_day(self):
        for record in self:
            if record.appointment_date:
                record.selected_day = record.appointment_date.strftime('%A').lower()
            else:
                record.selected_day = ''
            print("Compute selected_day:", record.selected_day)

  
    def button_done(self):
        for record in self:
            record.state = "done"
        return True

    def button_confirm(self):
        for record in self:
            record.state = "confirm"
        return True
            
    
   
    @api.constrains('appointment_date')
    def _check_appointment_date(self):
        """Ensure that the appointment date is not in the past."""
        for record in self:
            if record.appointment_date and record.appointment_date < fields.Date.today():
                raise ValidationError("You cannot set an appointment in the past. Please select a valid date.")

    @api.depends('service_ids.price')
    def _compute_total_price(self):
        for record in self:
            record.price = sum(service.price for service in record.service_ids)

    @api.depends('date_of_birth')
    def get_age(self):
        today = datetime.today().date()
        for rec in self:
            if rec.date_of_birth:
                days = (today - rec.date_of_birth).days
                rec.age = round(days / 365)

