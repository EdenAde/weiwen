# -*- coding: utf-8 -*-
from odoo import _
from odoo import models, api, fields,modules
from odoo.exceptions import ValidationError, AccessError, UserError


url_jaxws = "http://www.tsgcn.com:8066/bookservice1.asmx"
import json
import logging
_logger = logging.getLogger(__name__)
import urllib2
import base64
import xml.dom.minidom as dm


from odoo import tools




class baseModel(models.Model):
    _inherit = 'blog.post'
    _description = 'Base model'

    def _default_image(self):
        image_path = modules.get_module_resource('im_livechat', 'static/src/img', 'default.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    sequence = fields.Integer(
        '序号',
        help=("Gives the sequence order when displaying "
              "a list of contexts."))

    image = fields.Binary("Photo", default=_default_image, attachment=True,
                          help="This field holds the image used as photo for the employee, limited to 1024x1024px.")
    image_medium = fields.Binary("Medium-sized photo", attachment=True,
                                 help="Medium-sized photo of the employee. It is automatically "
                                      "resized as a 128x128px image, with aspect ratio preserved. "
                                      "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized photo", attachment=True,
                                help="Small-sized photo of the employee. It is automatically "
                                     "resized as a 64x64px image, with aspect ratio preserved. "
                                     "Use this field anywhere a small image is required.")

    _defaults = {
        'sequence': 1
    }



class ProductFromPos(models.Model):
    _name = 'library.library'


    count = fields.Integer("COUNT")


    @api.model
    def get_book_date_with_isbn(self, isbn_number):

        # bids=None
        _logger.info("1111111111111")


        pass

    @api.model
    def get_price(self,barcode):
        data_jaxws = '''<?xml version="1.0"?>
        <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <SOAP-ENV:Body><getBookPrice xmlns="http://tsgcn.net/">
        <isbn>%s</isbn>
        <keyvalue>C946AD370C3E8D211DEAC58C7DAD7408</keyvalue>
        </getBookPrice></SOAP-ENV:Body>
        </SOAP-ENV:Envelope>
        ''' % barcode

        headers = {'Content-Type': 'text/xml'}

        req = urllib2.Request(url_jaxws, data=data_jaxws.encode('utf-8'), headers=headers)
        res = urllib2.urlopen(req)

        xml = dm.parseString(res.read().decode('utf-8'))
        eles = xml.documentElement.getElementsByTagName("getBookPriceResult")

        tv = eles[0].childNodes[0].nodeValue
        _logger.info(tv)

        book={}

        vstring = base64.b64decode(tv)

    @api.model
    def get_book2(self, barcode):
        _logger.info("get barcode")
        _logger.info(barcode)
        data_jaxws = '''<?xml version="1.0"?>
            <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <SOAP-ENV:Body><getbook xmlns="http://tsgcn.net/">
            <isbn>%s</isbn>
            <keyvalue>C946AD370C3E8D211DEAC58C7DAD7408</keyvalue>
            </getbook></SOAP-ENV:Body>
            </SOAP-ENV:Envelope>
            ''' % barcode

        headers = {'Content-Type': 'text/xml'}

        req = urllib2.Request(url_jaxws, data=data_jaxws.encode('utf-8'), headers=headers)
        res = urllib2.urlopen(req)

        xml = dm.parseString(res.read().decode('utf-8'))
        eles = xml.documentElement.getElementsByTagName("getbookResult")

        tv = eles[0].childNodes[0].nodeValue
        _logger.info(tv)

        #book = {}
        #vstring = base64.b64decode(tv)
        return tv

    @api.model
    def get_book(self,barcode):
        _logger.info("get barcode")
        _logger.info(barcode)
        data_jaxws = '''<?xml version="1.0"?>
        <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <SOAP-ENV:Body><getbook xmlns="http://tsgcn.net/">
        <isbn>%s</isbn>
        <keyvalue>C946AD370C3E8D211DEAC58C7DAD7408</keyvalue>
        </getbook></SOAP-ENV:Body>
        </SOAP-ENV:Envelope>
        ''' % barcode

        headers = {'Content-Type': 'text/xml'}

        req = urllib2.Request(url_jaxws, data=data_jaxws.encode('utf-8'), headers=headers)
        res = urllib2.urlopen(req)

        xml = dm.parseString(res.read().decode('utf-8'))
        eles = xml.documentElement.getElementsByTagName("getbookResult")

        tv = eles[0].childNodes[0].nodeValue
        _logger.info(tv)

        book={}

        vstring = base64.b64decode(tv)
        #vstring = base64.b64decode(vstring1)
        _logger.info(vstring)
        sstr = vstring.split('>')
        slen = len(sstr)
        inde = slen-1
        inde2 = slen - 2
        book['name'] = sstr[0]
        book['isbn'] = barcode
        book['lang'] = 'chi'
        book['pub'] = sstr[2]
        book['author'] = sstr[1]
        book['description'] = sstr[inde]
        book['categ_name'] = sstr[inde2]
        book['list_price'] = 0
        #
        # _logger.info(sstr)
        # sstr1 = sstr[1].split('>')
        # _logger.info(sstr1)
        #
        # megazine = {}
        # megazine['issn'] = barcode
        # megazine['name']=sstr[0]
        # megazine['kanqi'] = sstr1[2]
        # megazine['publisher'] = sstr1[0]
        # megazine['catalog_num'] = sstr1[8]
        # megazine['catalog_name'] = sstr1[9]

        _logger.info(book)
        #return json.dumps(book)
        return book


    # def create_product_pos(self, vals):
    #     type = None
    #     if vals.get('type') == 'Stockable':
    #         type = 'product'
    #     elif vals.get('type') == 'Consumable':
    #         type = 'consu'
    #     elif vals.get('type') == 'Service':
    #         type = 'service'
    #     category = self.env['product.category'].search([('name', '=', vals.get('category'))], limit=1)
    #     uom_id = self.env['product.uom'].search([('name', '=', vals.get('unit'))], limit=1)
    #     new_vals = {
    #         'name': vals.get('name'),
    #         'display_name': vals.get('name'),
    #         'type': type,
    #         'categ_id': category.id if category else None,
    #         'list_price': vals.get('price') if vals.get('price') else 1,
    #         'available_in_pos': True,
    #         'sale_ok': True,
    #         'uom_id': uom_id.id,
    #         'uom_po_id': uom_id.id,
    #         'barcode':vals.get('barcode'),
    #         }
    #     rec = self.env['product.product'].create(new_vals)
    #     new_vals['id'] = rec.id
    #     new_vals['price'] = vals.get('price') if vals.get('price') else 1
    #     new_vals['pos_categ_id'] = [rec.pos_categ_id.id] if rec.pos_categ_id else None
    #     new_vals['taxes_id'] = [rec.taxes_id.id] if rec.taxes_id else []
    #     new_vals['barcode'] = rec.barcode
    #     new_vals['default_code'] = rec.default_code
    #     new_vals['to_weight'] = rec.to_weight
    #     new_vals['uom_id'] = [rec.uom_id.id, rec.uom_id.name]
    #     new_vals['description_sale'] = rec.description_sale
    #     new_vals['description'] = rec.description
    #     new_vals['product_tmpl_id'] = [rec.product_tmpl_id.id]
    #     new_vals['tracking'] = rec.tracking
    #
    #     return new_vals

#
# class BusinessTrip(models.Model):
#     _name = 'tms.travel'
#     _inherit = ['mail.alias.mixin',]
#     _description = 'Business Trip'
#
#     alias_id = fields.Many2one('mail.alias', string='Alias', ondelete="restrict",
#                                required=True)
#
#     trip_type = fields.Selection(
#         [('v', '驾车'), ('p', '公共交通')], '出行方式',default='p',
#         required=True)
#
#     project_id = fields.Many2one("project.project",string="项目")
#     project_task_id = fields.Many2one("project.task",string="任务")





# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
