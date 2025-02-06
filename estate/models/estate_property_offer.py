from odoo import fields, models
from odoo import fields, models, api

# u. Llistat d'ofertes
class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Ofertes per a propietats immobiliàries'

    price = fields.Float('Preu de l’Oferta', required=True)
    status = fields.Selection([
        ('pending', 'En tractament'),
        ('accepted', 'Acceptada'),
        ('rejected', 'Rebutjada')
    ], string='Estat', default='pending')

    partner_id = fields.Many2one(
        'res.partner',
        string='Comprador',
        required=True,
        help="Selecciona un comprador existent."
    )

    comment = fields.Text('Comentaris')

    # ✅ Assignació automàtica de la propietat
    property_id = fields.Many2one(
        'estate.property',
        string='Propietat',
        required=True,
        ondelete='cascade',
        readonly=True
    )

    @api.constrains('status')
    def _check_accepted_offer(self):
        """ Quan una oferta és acceptada, rebutja les altres i assigna el preu final. """
        for offer in self:
            if offer.status == 'accepted':
                # Rebutjar totes les altres ofertes de la mateixa propietat
                other_offers = offer.property_id.offer_ids.filtered(lambda o: o.id != offer.id)
                other_offers.write({'status': 'rejected'})

                # Assignar el preu final de venda de la propietat
                offer.property_id.selling_price = offer.price