from unicodedata import category
from odoo import fields, models, api, Command


class WebsiteSearchableMixin(models.AbstractModel):
    _inherit = 'website.searchable.mixin'

    @api.model
    def _search_fetch(self, search_detail, search, limit, order):
        """returning the searchbar suggestions"""
        res_user_object = self.env.user
        if res_user_object.partner_id.allowed_product_ids:
            product_template_object = res_user_object.partner_id.allowed_product_ids
        elif res_user_object.partner_id.allowed_category_ids:
            product_template_object = self.env['product.template'].search([]).filtered(
                lambda l: any(cat_id in res_user_object.partner_id.allowed_category_ids.ids
                              for cat_id in l.public_categ_ids.ids))
        else:
            product_template_object = self.env['product.template'].search([])
        if search_detail['model'] == 'product.template':
            search_detail['base_domain'] += [[('id', 'in', product_template_object.ids)]]
        if search_detail['model'] == 'product.public.category':
            search_detail['base_domain'] += [[('id', 'in', product_template_object.public_categ_ids.ids)]]

        return super()._search_fetch(search_detail, search, limit, order)