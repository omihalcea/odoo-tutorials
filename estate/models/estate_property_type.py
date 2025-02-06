from odoo import fields, models

# j. Tipus de propietat
class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Tipus de propietat immobiliària'

    name = fields.Char('Tipus', required=True)