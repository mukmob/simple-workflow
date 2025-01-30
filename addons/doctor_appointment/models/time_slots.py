from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class TimeSlot(models.Model):
    _name = 'appointment.time.slot'
    _description = 'Appointment Time Slot'
    _rec_name = "display_name"
    _order = 'create_date desc'

    doctor_id = fields.Many2one(comodel_name='appointment.doctors', string='Doctor')
    
    day = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday')
    ], string="Day", required=True)

    start_time = fields.Float(string='Start Time', required=True)
    end_time = fields.Float(string='End Time', required=True)
    description = fields.Text(string='Description')
    display_name = fields.Char(string="Time Slot", compute='_compute_display_name', store=True)
    booked = fields.Boolean(string="Booked", default=False)
    @api.model
    def create(self, vals):
        if 'doctor_id' not in vals and self.env.context.get('default_doctor_id'):
            vals['doctor_id'] = self.env.context['default_doctor_id']
        return super(TimeSlot, self).create(vals)

    
    @api.constrains('doctor_id','day','start_time', 'end_time')
    def _check_duplicate_time_slot(self):
        """ Check for duplicate time slots for the same doctor and day. """
        for record in self:
            existing_slots = self.search([
                ('doctor_id', '=', record.doctor_id.id),
                ('day', '=', record.day),
                ('start_time', '=', record.start_time),
                ('end_time', '=', record.end_time),
                ('id', '!=', record.id), 
            ])
            if existing_slots:
                raise ValidationError("This time slot already exists for the doctor on this day.")

    @api.model
    def get_available_dates(self, doctor_id):
        # You can no longer filter by date, since there is no date field
        time_slots = self.search([('doctor_id', '=', doctor_id), ('booked', '=', False)])
        return time_slots

    @api.constrains('start_time', 'end_time')
    def _check_time(self):
        """Ensure that start time is before end time."""
        for record in self:
            if record.start_time and record.end_time:
                if record.start_time >= record.end_time:
                    raise ValidationError("Start time must be before end time.")

    @api.depends('day', 'start_time', 'end_time')
    def _compute_display_name(self):
        """Compute the display name for the time slot."""
        for record in self:
            start_hour, start_minute = divmod(record.start_time * 60, 60)
            end_hour, end_minute = divmod(record.end_time * 60, 60)
            day_name = record.day.capitalize() if record.day else "Unknown Day"
            record.display_name = f"{day_name} {int(start_hour):02d}:{int(start_minute):02d} - {int(end_hour):02d}:{int(end_minute):02d}"

    @api.onchange('day')
    def _onchange_day(self):
        """Update the time slot display name based on the day and times."""
        for record in self:
            if record.day:
                start_hour, start_minute = divmod(record.start_time * 60, 60)
                end_hour, end_minute = divmod(record.end_time * 60, 60)
                record.display_name = f"{record.day.capitalize()} {int(start_hour):02d}:{int(start_minute):02d} - {int(end_hour):02d}:{int(end_minute):02d}"

    @api.model
    def create(self, vals):
        """Override create method to set the day based on the start time if needed."""
        if 'start_time' in vals:
            vals['day'] = vals.get('day', 'monday')
        return super(TimeSlot, self).create(vals)

    


