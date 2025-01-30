from odoo import models, fields , api

class Category(models.Model):
    _name = 'appointment.category'
    _description = 'appointment Category'
    _order = 'create_date desc'

    name = fields.Char(string="Category Name")
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'The category name must be unique.')
    ]
    
    