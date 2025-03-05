from odoo import http
from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.tools import lazy


class WebsiteSaleInherit(WebsiteSale):
    @route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>',
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        """Main function of Website Sale"""
        res = super(WebsiteSaleInherit, self).shop(page, category, search, min_price, max_price, ppg, **post)
        res_user_object = request.env['res.users'].sudo().browse(request.uid)
        if res_user_object.partner_id.allowed_product_ids:
            product_template_object = res_user_object.partner_id.allowed_product_ids
        elif res_user_object.partner_id.allowed_category_ids:
            product_template_object = request.env['product.template'].search([]).filtered(
                lambda l: any(cat_id in res_user_object.partner_id.allowed_category_ids.ids
                              for cat_id in l.public_categ_ids.ids))
        else:
            product_template_object = request.env['product.template'].search([])

        res.qcontext['products'] = product_template_object
        res.qcontext['categories'] = product_template_object.public_categ_ids
        res.qcontext['attributes'] = product_template_object.attribute_line_ids.attribute_id
        res.qcontext['search_product'] = product_template_object
        res.qcontext['search_count'] = len(product_template_object)
        x = res.qcontext.get('products_prices')
        for rec in product_template_object:
            x[rec.id] = {'price_reduce': rec.list_price}
        res.qcontext['products_prices'] = x

        # categories
        if res.qcontext['category']:
            products = product_template_object.filtered(lambda l: res.qcontext['category'].id in l.public_categ_ids.ids)
            res.qcontext['products'] = products
            res.qcontext['attributes'] = products.attribute_line_ids.attribute_id
            res.qcontext['search_product'] = products
            res.qcontext['search_count'] = len(products)
            res.qcontext['bins'] = lazy(
                lambda: TableCompute().process(products, res.qcontext.get("ppg"), res.qcontext.get('ppr')))
        # attribute
        attribute_list = []
        if res.qcontext['attrib_set']:
            for val in res.qcontext['attrib_set']:
                attribute_list.append(val)
            for rec in product_template_object.attribute_line_ids:
                for x in rec.value_ids.ids:
                    if x in attribute_list:
                        products = res.qcontext['products'].filtered(
                            lambda l: x in l.attribute_line_ids.value_ids.ids)
                        res.qcontext['products'] = products
                        res.qcontext['search_product'] = products
                        res.qcontext['search_count'] = len(products)
                        res.qcontext['bins'] = lazy(
                            lambda: TableCompute().process(products, res.qcontext.get("ppg"),
                                                           res.qcontext.get('ppr')))
        # pager
        website = request.env['website'].get_current_website()
        pager = website.pager(url='/shop', total=res.qcontext.get('search_count'), page=page,
                              step=res.qcontext.get('ppg'), scope=5, url_args=post)
        offset = pager['offset']
        products_on_page = res.qcontext.get('search_product')[offset:offset + res.qcontext.get('ppg')]
        res.qcontext['pager'] = pager
        res.qcontext['bins'] = lazy(
            lambda: TableCompute().process(products_on_page, res.qcontext.get("ppg"), res.qcontext.get('ppr')))

        # filter
        if res.qcontext['order'] == 'website_sequence asc':
            product = products_on_page.sorted(lambda l: l.website_sequence)
            res.qcontext['bins'] = lazy(
                lambda: TableCompute().process(product, res.qcontext.get("ppg"), res.qcontext.get('ppr')))
        if res.qcontext['order'] == 'create_date desc':
            product = products_on_page.sorted(lambda l: l.create_date, reverse=True)
            res.qcontext['bins'] = lazy(
                lambda: TableCompute().process(product, res.qcontext.get("ppg"), res.qcontext.get('ppr')))
        if res.qcontext['order'] == 'name asc':
            product = products_on_page.sorted(lambda l: l.name)
            res.qcontext['bins'] = lazy(
                lambda: TableCompute().process(product, res.qcontext.get("ppg"), res.qcontext.get('ppr')))
        if res.qcontext['order'] == 'list_price asc':
            product = products_on_page.sorted(lambda l: l.list_price)
            res.qcontext['bins'] = lazy(
                lambda: TableCompute().process(product, res.qcontext.get("ppg"), res.qcontext.get('ppr')))
        if res.qcontext['order'] == 'list_price desc':
            product = products_on_page.sorted(lambda l: l.list_price, reverse=True)
            res.qcontext['bins'] = lazy(
                lambda: TableCompute().process(product, res.qcontext.get("ppg"), res.qcontext.get('ppr')))

        return res
