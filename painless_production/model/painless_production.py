
from odoo import fields, models, api, _


class painlessProduction(models.Model):
    _name = 'painless.production'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _description = 'A Painless Production App'

    name = fields.Char(string='Order Reference', required=True, readonly=True, default=lambda self: _('New'))
    product_id = fields.Many2one('product.product', string='Product', tracking=True)
    subtotal = fields.Char(string='Subtotal', compute='_compute_subtotal')
    subtotal_taxed = fields.Char(string='Subtotal Taxed', compute='_compute_subtotal_taxed')
    scheduled_date = fields.Datetime(string='Date', default=fields.datetime.now())
    responsible_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, readonly=True)

    status = fields.Selection(string='Status', copy=False,
                              selection=[('draft', 'Draft'), ('confirmed', 'Confirmed'),
                                         ('done', 'Done'), ('cancel', 'Cancel')], default='draft', tracking=True)
    description_id = fields.Char(string='Description')
    ################################
    painless_product_line_ids = fields.One2many('painlessproduct.info', 'painless_product_line_id')
    product_line_name_ids = fields.One2many('painlessproduct.info', 'product_line_name_id')
    ################################
    ratio = fields.Integer()
    flag = fields.Integer()

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('painless.production')
        res = super(painlessProduction, self).create(vals)
        return res

    @api.depends('painless_product_line_ids.quantity', 'painless_product_line_ids.product_price')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = str(record.painless_product_line_ids.quantity * record.painless_product_line_ids.product_price) + " " + str(record.currency_id.symbol)

    @api.depends('painless_product_line_ids.quantity', 'painless_product_line_ids.product_price')
    def _compute_subtotal_taxed(self):
        for record in self:
            record.subtotal_taxed = str((record.painless_product_line_ids.quantity * record.painless_product_line_ids.product_price) + record.painless_product_line_ids.quantity * record.painless_product_line_ids.product_price * 20 / 100) + " " + str(record.currency_id.symbol)

    def button_confirmed(self):
        self.status = 'confirmed'

    def button_mark_as_done(self):
        self.status = 'done'

    def button_cancel(self):
        self.status = 'cancel'
