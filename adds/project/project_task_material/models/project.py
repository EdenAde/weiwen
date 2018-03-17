# -*- coding: utf-8 -*-
# Copyright 2012 - 2013 Daniel Reis
# Copyright 2015 - Antiun Ingeniería S.L. - Sergio Teruel
# Copyright 2016 - Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Task(models.Model):
    _inherit = "project.task"

    material_ids = fields.One2many(
        comodel_name='project.task.material', inverse_name='task_id',
        string='Material used')


class ProjectTaskMaterial(models.Model):
    _name = "project.task.material"
    _description = "Task Material Used"

    task_id = fields.Many2one(
        comodel_name='project.task', string='Task', ondelete='cascade',
        required=True)
    product_id = fields.Many2one(
        comodel_name='product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity')

    attachments = fields.One2many('ir.attachment',compute='_get_attachments')


    @api.multi
    def _get_attachments(self):
        for ma in self:
            ma.attachments = self.env['ir.attachment'].search([('res_model', '=', 'project.task.material'), ('res_id', '=', ma.id)])


    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        print "ress====start"
        ress1  = super(ProjectTaskMaterial,self).search(domain,fields,offset,limit,order)

        ress = super(ProjectTaskMaterial, self).search_read(domain, fields, offset, limit, order)

        print "ress===="

        print ress
        if ress:
            ress[0]['attachments'] = self.env['ir.attachment'].sudo().search_read([('res_model', '=', self._name), ('res_id', '=', ress1.id)])

        return ress



    @api.multi
    @api.constrains('quantity')
    def _check_quantity(self):
        for material in self:
            if not material.quantity > 0.0:
                raise ValidationError(
                    _('Quantity of material consumed must be greater than 0.')
                )
