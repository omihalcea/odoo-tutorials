from odoo import fields, models, api
from datetime import timedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Model per estate_property'
    # a. Nom
    name = fields.Char('Propietat Immobiliària', required=True)

    # b. Descripció
    description = fields.Text('Descripció')

    # c. Codi postal
    postalcode = fields.Char('Codi Postal', required=True)

    # d. Data de disponibilitat
    date_availability = fields.Date(
        'Data de Disponibilitat',
        default=lambda self: fields.Date.today() + timedelta(days=30),
        copy=False
    )

    # e. Preu de venda esperat
    expected_price = fields.Float('Preu de Venda Esperat', required=True)

    # f. Preu de venda final
    selling_price = fields.Float('Preu de Venda Final', readonly=True, copy=False)

    # g. Millor oferta
    best_offer = fields.Float(
        'Millor Oferta',
        compute='_compute_best_offer',
        readonly=True,
        store=True
    )

    # h. Estat
    state = fields.Selection([
        ('new', 'Nova'),
        ('offer_received', 'Oferta Rebuda'),
        ('offer_accepted', 'Oferta Acceptada'),
        ('sold', 'Venuda'),
        ('canceled', 'Cancel·lada')
    ], string='Estat', default='new')

    # i. Nombre d'habitacions
    bedroom = fields.Integer('Nombre d\'Habitacions', required=True)

    # j. Tipus de propietat
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Tipus de Propietat',
        ondelete='restrict',
        help="Selecciona el tipus de propietat"
    )

    # k. Etiquetes
    tag_ids = fields.Many2many(
        'estate.property.tag', 
        string='Etiquetes', 
        help="Selecciona les etiquetes per a aquesta propietat")
        
    # l. Ascensor
    elevator = fields.Boolean('Ascensor', default=False)

    # m. Parquing
    parking = fields.Boolean('Parking', default=False)

    # n. Renovat
    renovated = fields.Boolean('Renovat', default=False)

    # o. Nombre de banys
    bathroom = fields.Integer('Nombre de Banys', required=True)

    # p. Superfície
    surface = fields.Float('Superfície (m2)', required=True)

    # q. Preu per m2
    price_per_m2 = fields.Float(
        'Preu per m2',
        compute='_compute_price_per_m2',
        readonly=True,
        store=False
    )

    # r. Any de construcció
    year_built = fields.Integer('Any de Construcció')

    # s. Certificat Energètic
    energy_certificate = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
        ('e', 'E'),
        ('f', 'F'),
        ('g', 'G')
    ], string='Certificat Energètic')

    # t. Actiu
    active = fields.Boolean('Actiu', default=True)


    # u. Llistat d'ofertes
    offer_ids = fields.One2many(
        'estate.property.offer',  # Model de les ofertes
        'property_id',  # Camp Many2one dins de l'oferta que el relaciona amb la propietat
        string='Ofertes'
    )

    # v. Comprador
    buyer_id = fields.Many2one(
        'res.partner',
        string='Comprador',
        compute='_compute_buyer',
        store=False,
        readonly=True
    )

    # w. Comercial
    salesman_id = fields.Many2one(
        'res.users',
        string='Comercial',
        default=lambda self: self.env.user
    )

    # v. Comprador
    @api.depends('offer_ids')
    def _compute_buyer(self):
        """ Calcula el comprador com el contacte associat a la millor oferta acceptada """
        for record in self:
            accepted_offer = record.offer_ids.filtered(lambda o: o.status == 'accepted')
            record.buyer_id = accepted_offer.partner_id if accepted_offer else False

    # f. Preu de venda final
    @api.depends('expected_price', 'surface')
    def _compute_price_per_m2(self):
        """ Calcula el preu per metre quadrat """
        for record in self:
            record.price_per_m2 = record.expected_price / record.surface if record.surface else 0

    # g. Millor oferta
    @api.depends('offer_ids.price', 'offer_ids.status')
    def _compute_best_offer(self):
        for property in self:
            valid_offers = property.offer_ids.filtered(lambda o: o.status != 'rejected')
            property.best_offer = max(valid_offers.mapped('price'), default=0.0)