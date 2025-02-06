from odoo import models, fields , api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class Doctor(models.Model):
    _name = 'appointment.doctors'
    _description = 'appointment Doctors'
    _order = 'create_date desc'
    
    
    name = fields.Char(string="Name", compute="compute_doctor_name", store=True, default=lambda self: self.env.context.get('default_doctor_id'))
    image = fields.Binary()
    fname = fields.Char(string='First Name', required=True)
    mname = fields.Char(string="Middle Name", required=True)
    lname = fields.Char(string='Last Name', required=True)
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female'),
                               ('other', 'Other')], string="Gender")
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Char(compute='get_age', store=True, string="Age")
    contact = fields.Char(string='Contact Number')
    email = fields.Char(string="Email Id")
    # address
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street 2')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    zip = fields.Integer(string='Postal Code')
    country_id = fields.Many2one('res.country', string='Country')

    duration = fields.Float(string='Duration (hours)', default=1.0)
    qualification = fields.Char(string="Qualification", required=True)
    specialization = fields.Char(string="Specialization")
    years_of_experience = fields.Float(string="Total Years of Experience")

    service_ids = fields.Many2many(
        string='Services',
        comodel_name='appointment.service',
        ) 

    appointment_count = fields.Integer(compute='compute_appointment', string='Appointments')

    day_ids = fields.Many2many(
        string='Days',
        comodel_name='appointment.time.slot',
        store=True,
         default=lambda self: self.env.context.get('default_doctor_id')
    )
    


    
    @api.depends('name')
    def compute_appointment(self):
        for record in self:
            appointment_count = self.env['appointment.customer'].search_count(
                [('doctor_id', '=', record.id)])
            record.appointment_count = appointment_count

    def action_appoinments_view(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'view_mode': 'tree',
            'res_model': 'appointment.customer',
            'domain': [('doctor_id', '=', self.id)],
            'context': {'create': False, 'delete': False}
        }

    @api.depends('fname', 'mname', 'lname')
    def compute_doctor_name(self):
        for doctor in self:
            if doctor.exists():
                name_parts = [
                    doctor.fname.capitalize() if doctor.fname else '',
                    doctor.mname.capitalize() if doctor.mname else '',
                    doctor.lname.capitalize() if doctor.lname else ''
                ]
                doctor.name = ' '.join(name_parts).strip()
            else:
                doctor.name = False
                
    def get_doctor_name_by_id(self, doctor_id):
        doctor = self.search([('id', '=', doctor_id)], limit=1)
        return doctor.name if doctor else "Doctor not found"


    @api.depends('date_of_birth')
    def get_age(self):
        today = datetime.today().date()
        for rec in self:
            if rec.date_of_birth:
                days = (today - rec.date_of_birth).days
                rec.age = round(days / 365)

    @api.model
    def create(self, vals):
        doctor = super(Doctor, self).create(vals)
        if doctor.email:
            user = self.env['res.users'].search([('login', '=', doctor.email)], limit=1)
            if not user:
                user_vals = {
                    'name': f"Dr. {doctor.fname.capitalize()} {doctor.lname.capitalize()}",
                    'login': doctor.email,
                    'email': doctor.email,
                    'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],
                }
                self.env['res.users'].create(user_vals)
        return doctor
