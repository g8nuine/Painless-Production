from odoo import fields, models, api


class ProductInfoPainlessProduct(models.Model):
    _name = 'painlessproduct.info'

    painless_product_line_id = fields.Many2one('painless.production')
    product_line_name_id = fields.Many2one('product.product')
    description_id = fields.Char(string='Description')
    quantity = fields.Integer('Quantity', default=1)
    product_price = fields.Float(string='Price')
    # subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal')

    @api.onchange('product_line_name_id')
    def _onchange_product_id(self):
        if self.product_line_name_id:
            self.product_price = self.product_line_name_id.lst_price
        else:
            self.product_price = 0.0

    # @api.depends('quantity', 'product_price')
    # def _compute_subtotal(self):
        # for record in self:
            # record.subtotal = record.quantity * record.product_price
