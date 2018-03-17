# -*- coding: utf-8 -*-
__author__ = 'guizhouyuntushidai'



from odoo.osv import osv,  expression
from odoo import tools,fields,models,api
from PIL import Image
from odoo.tools import image

class baseModel(models.Model):
    _name = 'base.model'
    _description = 'Base model'

    @api.depends('image')
    def _get_image(self):
        for record in self:
            if record.image:
                record.image_medium = image.crop_image(record.image, type='top', ratio=(4, 3), thumbnail_ratio=4)
                record.image_small = image.crop_image(record.image, type='top', ratio=(4, 3), thumbnail_ratio=6)
            else:
                record.image_medium = False
                record.image_small = False


    # _order = 'name asc'


    @api.one
    def _set_image(self):
        self._set_image_value(self.image)

    @api.one
    def _set_image_value(self, value):
        image = tools.image_resize_image_big(value)
        if self.product_tmpl_id.image:
            self.image_variant = image
        else:
            self.image = image


    name=fields.Char('Name', required=True)
    image=fields.Binary("Image",
            help="This field holds the image used as logo for the brand, limited to 1024x1024px.")
    image_medium=fields.Binary('Medium', compute="_get_image", inverse="_set_image",
            )
    sequence=fields.Integer(
            '序号',
            help=("Gives the sequence order when displaying "
                  "a list of contexts."))

    image_small=fields.Binary('small', compute="_get_image", inverse="_set_image",
           )



    _defaults = {
        'sequence': 1
    }
