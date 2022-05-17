from odoo import models, fields, api

class Person(models.Model):
    _name = 'person'
    _description = 'person'
    
    name = fields.Char(string='Name')