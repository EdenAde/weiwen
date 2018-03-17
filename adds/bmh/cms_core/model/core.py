# -*- coding: utf-8 -*-
__author__ = 'guizhouyuntushidai'



from odoo import models, fields,api,modules
from odoo import tools

from odoo.osv import expression

class baseModel(models.Model):

    _inherit = 'blog.post'
    _description = 'Base model'



    def _default_image(self):
        image_path = modules.get_module_resource('im_livechat', 'static/src/img', 'default.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    sequence=fields.Integer(
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
