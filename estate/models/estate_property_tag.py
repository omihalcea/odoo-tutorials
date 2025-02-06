from odoo import fields, models

# k. Etiquetes
class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Etiquetes per a propietats immobiliàries'

    name = fields.Char('Etiqueta', required=True)