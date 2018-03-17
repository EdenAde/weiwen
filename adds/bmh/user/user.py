# -*- coding: utf-8 -*-
from odoo import api, fields, models


class resPartner(models.Model):
    _inherit = 'res.partner'

    person_type = fields.Selection([('surveyee', u"受访人"), ('professioner', u"专家")], string=u"类型",default='surveyee')