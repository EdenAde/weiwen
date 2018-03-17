# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# 1:  imports of odoo
from odoo import models, fields, api, _
import json
from inspect import isfunction
class LabelPrintField(models.Model):
    _name = "model.update.fields"


    field_id = fields.Many2one('ir.model.fields', 'Fields', required=False)
    field_id_model = fields.Char("参考")
    target_field_name = fields.Char('更新字段名称')
    target_field_type = fields.Char('更新字段类型')
    report_id = fields.Many2one('label.print', 'Report')
    update_value = fields.Char("更新值")
    related_field_model = fields.Char('related_field_model', size=512, )
    field_type = fields.Char("更新值类型")
    action_model_from=fields.Integer('操作模型')


    @api.model
    def get_model_fields(self,model_id):
        print "model_id==="
        print model_id
        model_fields = self.env['ir.model.fields']

        fields_obj = model_fields.search([('model_id','=',model_id)])
        resjson={}
        res = []
        if fields_obj:
            for field in fields_obj:
                fieldone={}
                fieldone['name']=field.name
                fieldone['field_description'] = field.field_description
                #if field.field_description in ['name',]:
                res.append(fieldone)
        #resjson['values'] = res
        #print fields_obj
        return res


    @api.onchange('field_id')
    def onchange_field_id(self,field_id):
        print "get_field_id==========="
        print field_id
        if field_id:
            model_fields = self.env['ir.model.fields']
            field_obj = model_fields.browse(field_id)
            if field_obj.ttype not in ['Many2one','many2one','selection','Selection']:
                return {'value': {'field_id_model':field_obj.model,'target_field_name': field_obj.name,'field_type': field_obj.ttype, 'related_field_model': field_obj.relation}}

            print "field_obj.relation="
            print field_obj
            return {'value': {'field_id_model':field_obj.model,'target_field_name': field_obj.name,'field_type': field_obj.ttype, 'related_field_model': field_obj.relation}}
        else:
            return {'value': {}}


    @api.model
    def create(self,vals):
        print "我要crreatele "
        print (vals)
        model = self._context.get('active_model')
        ids = self._context.get('active_ids')
        print model
        print ids

        objs = self.env[model].browse(ids)

        print objs
        objs.update({vals.get("target_field_name"):vals.get("update_value")})

        #print status
        result = super(LabelPrintField, self).create(vals)
        return result

    @api.multi
    def action_confirm(self):

        print "action_confirm_context"
        print self

        return
        # self.filtered(lambda picking: not picking.move_lines).write({'launch_pack_operations': True})
        # # TDE CLEANME: use of launch pack operation, really useful ?
        # self.mapped('move_lines').filtered(lambda move: move.state == 'draft').action_confirm()
        # self.filtered(
        #     lambda picking: picking.location_id.usage in ('supplier', 'inventory', 'production')).force_assign()
        # return True

    @api.model
    def get_selection_from_name(self, model,target_string):
        print "get_selection_from_name"
        print model
        print target_string
        target_model_pool = self.env[model]
        selection_dict_1 = target_model_pool.fields_get().get(target_string)
        print selection_dict_1

        selection_dict = selection_dict_1.get('selection')

            # .selection
        if isfunction(selection_dict):
            selection_dict = dict(getattr(target_model_pool, selection_dict.__name__)())
        else:
            selection_dict = dict(selection_dict)

        #return selection_dict.get('selection')
        revrese_selection_dict=[]
        for id, value in selection_dict.iteritems():
            new_option={}
            new_option['id']=id
            new_option['name']=value
            revrese_selection_dict.append(new_option)
        print revrese_selection_dict
        return revrese_selection_dict

            #return
            # unicode(a, 'gb2312')
            #print target_string.decode('utf-8')
            #print revrese_selection_dict.get(target_string.decode('utf-8'))
            #return revrese_selection_dict.get(target_string.decode('utf-8'))


    @api.model
    def get_field_values(self,t_model):

        sql = "select * from "+t_model.replace('.','_')+" order by create_date desc limit 5 "
        self._cr.execute(sql)
        values_obj = self._cr.dictfetchall()

        res=[]
        if values_obj:
            for field in values_obj:
                fieldone={}
                fieldone['id']=field['id']
                fieldone['name'] = field['name']
                res.append(fieldone)

        return res



    # @api.onchange('report_id')
    def onchange_model(self):
        model_list = []
        if self.model_id:
            model_obj = self.env['ir.model']
            current_model = self.model_id.model
            model_list.append(current_model)
            active_model_obj = self.env[self.model_id.model]
            if active_model_obj._inherits:
                for key, val in active_model_obj._inherits.items():
                    model_ids = model_obj.search([('model', '=', key)])
                    if model_ids:
                        model_list.append(key)
        self.model_list = model_list


class LabelPrintFieldTeacher(models.Model):
    _name = "model.update.fields.teacher"


    field_id = fields.Many2one('ir.model.fields', 'Fields', required=False)
    field_id_model = fields.Char("参考")
    target_field_name = fields.Char('更新字段名称')
    target_field_type = fields.Char('更新字段类型')
    report_id = fields.Many2one('label.print', 'Report')
    update_value = fields.Char("更新值")
    related_field_model = fields.Char('related_field_model', size=512, )
    field_type = fields.Char("更新值类型")
    action_model_from=fields.Integer('操作模型')


    @api.model
    def get_model_fields(self,model_id):
        print "model_id==="
        print model_id
        model_fields = self.env['ir.model.fields']

        fields_obj = model_fields.search([('model_id','=',model_id)])
        resjson={}
        res = []
        if fields_obj:
            for field in fields_obj:
                fieldone={}
                fieldone['name']=field.name
                fieldone['field_description'] = field.field_description
                #if field.field_description in ['name',]:
                res.append(fieldone)
        #resjson['values'] = res
        #print fields_obj
        return res


    @api.onchange('field_id')
    def onchange_field_id(self,field_id):
        print "get_field_id==========="
        print field_id
        if field_id:
            model_fields = self.env['ir.model.fields']
            field_obj = model_fields.browse(field_id)
            if field_obj.ttype not in ['Many2one','many2one','selection','Selection']:
                return {'value': {'field_id_model':field_obj.model,'target_field_name': field_obj.name,'field_type': field_obj.ttype, 'related_field_model': field_obj.relation}}

            print "field_obj.relation="
            print field_obj
            return {'value': {'field_id_model':field_obj.model,'target_field_name': field_obj.name,'field_type': field_obj.ttype, 'related_field_model': field_obj.relation}}
        else:
            return {'value': {}}


    @api.model
    def create(self,vals):
        print "我要crreatele "
        print (vals)
        model = self._context.get('active_model')
        ids = self._context.get('active_ids')
        print model
        print ids

        objs = self.env[model].browse(ids)

        print objs
        objs.update({vals.get("target_field_name"):vals.get("update_value")})

        #print status
        result = super(LabelPrintFieldTeacher, self).create(vals)
        return result

    @api.multi
    def action_confirm(self):

        print "action_confirm_context"
        print self

        return
        # self.filtered(lambda picking: not picking.move_lines).write({'launch_pack_operations': True})
        # # TDE CLEANME: use of launch pack operation, really useful ?
        # self.mapped('move_lines').filtered(lambda move: move.state == 'draft').action_confirm()
        # self.filtered(
        #     lambda picking: picking.location_id.usage in ('supplier', 'inventory', 'production')).force_assign()
        # return True

    @api.model
    def get_selection_from_name(self, model,target_string):
        print "get_selection_from_name"
        print model
        print target_string
        target_model_pool = self.env[model]
        selection_dict_1 = target_model_pool.fields_get().get(target_string)
        print selection_dict_1

        selection_dict = selection_dict_1.get('selection')

            # .selection
        if isfunction(selection_dict):
            selection_dict = dict(getattr(target_model_pool, selection_dict.__name__)())
        else:
            selection_dict = dict(selection_dict)

        #return selection_dict.get('selection')
        revrese_selection_dict=[]
        for id, value in selection_dict.iteritems():
            new_option={}
            new_option['id']=id
            new_option['name']=value
            revrese_selection_dict.append(new_option)
        print revrese_selection_dict
        return revrese_selection_dict

            #return
            # unicode(a, 'gb2312')
            #print target_string.decode('utf-8')
            #print revrese_selection_dict.get(target_string.decode('utf-8'))
            #return revrese_selection_dict.get(target_string.decode('utf-8'))


    @api.model
    def get_field_values(self,t_model):

        sql = "select * from "+t_model.replace('.','_')+" order by create_date desc limit 5 "
        self._cr.execute(sql)
        values_obj = self._cr.dictfetchall()

        res=[]
        if values_obj:
            for field in values_obj:
                fieldone={}
                fieldone['id']=field['id']
                fieldone['name'] = field['name']
                res.append(fieldone)

        return res



    # @api.onchange('report_id')
    def onchange_model(self):
        model_list = []
        if self.model_id:
            model_obj = self.env['ir.model']
            current_model = self.model_id.model
            model_list.append(current_model)
            active_model_obj = self.env[self.model_id.model]
            if active_model_obj._inherits:
                for key, val in active_model_obj._inherits.items():
                    model_ids = model_obj.search([('model', '=', key)])
                    if model_ids:
                        model_list.append(key)
        self.model_list = model_list


class LabelPrintFieldStudent(models.Model):
    _name = "model.update.fields.student"


    field_id = fields.Many2one('ir.model.fields', 'Fields', required=False)
    field_id_model = fields.Char("参考")
    target_field_name = fields.Char('更新字段名称')
    target_field_type = fields.Char('更新字段类型')
    report_id = fields.Many2one('label.print', 'Report')
    update_value = fields.Char("更新值")
    related_field_model = fields.Char('related_field_model', size=512, )
    field_type = fields.Char("更新值类型")
    action_model_from=fields.Integer('操作模型')


    @api.model
    def get_model_fields(self,model_id):
        print "model_id==="
        print model_id
        model_fields = self.env['ir.model.fields']

        fields_obj = model_fields.search([('model_id','=',model_id)])
        resjson={}
        res = []
        if fields_obj:
            for field in fields_obj:
                fieldone={}
                fieldone['name']=field.name
                fieldone['field_description'] = field.field_description
                #if field.field_description in ['name',]:
                res.append(fieldone)
        #resjson['values'] = res
        #print fields_obj
        return res


    @api.onchange('field_id')
    def onchange_field_id(self,field_id):
        print "get_field_id==========="
        print field_id
        if field_id:
            model_fields = self.env['ir.model.fields']
            field_obj = model_fields.browse(field_id)
            if field_obj.ttype not in ['Many2one','many2one','selection','Selection']:
                return {'value': {'field_id_model':field_obj.model,'target_field_name': field_obj.name,'field_type': field_obj.ttype, 'related_field_model': field_obj.relation}}

            print "field_obj.relation="
            print field_obj
            return {'value': {'field_id_model':field_obj.model,'target_field_name': field_obj.name,'field_type': field_obj.ttype, 'related_field_model': field_obj.relation}}
        else:
            return {'value': {}}


    @api.model
    def create(self,vals):
        print "我要crreatele "
        print (vals)
        model = self._context.get('active_model')
        ids = self._context.get('active_ids')
        print model
        print ids

        objs = self.env[model].browse(ids)

        print objs
        objs.update({vals.get("target_field_name"):vals.get("update_value")})

        #print status
        result = super(LabelPrintFieldStudent, self).create(vals)
        return result

    @api.multi
    def action_confirm(self):

        print "action_confirm_context"
        print self

        return
        # self.filtered(lambda picking: not picking.move_lines).write({'launch_pack_operations': True})
        # # TDE CLEANME: use of launch pack operation, really useful ?
        # self.mapped('move_lines').filtered(lambda move: move.state == 'draft').action_confirm()
        # self.filtered(
        #     lambda picking: picking.location_id.usage in ('supplier', 'inventory', 'production')).force_assign()
        # return True

    @api.model
    def get_selection_from_name(self, model,target_string):
        print "get_selection_from_name"
        print model
        print target_string
        target_model_pool = self.env[model]
        selection_dict_1 = target_model_pool.fields_get().get(target_string)
        print selection_dict_1

        selection_dict = selection_dict_1.get('selection')

            # .selection
        if isfunction(selection_dict):
            selection_dict = dict(getattr(target_model_pool, selection_dict.__name__)())
        else:
            selection_dict = dict(selection_dict)

        #return selection_dict.get('selection')
        revrese_selection_dict=[]
        for id, value in selection_dict.iteritems():
            new_option={}
            new_option['id']=id
            new_option['name']=value
            revrese_selection_dict.append(new_option)
        print revrese_selection_dict
        return revrese_selection_dict

            #return
            # unicode(a, 'gb2312')
            #print target_string.decode('utf-8')
            #print revrese_selection_dict.get(target_string.decode('utf-8'))
            #return revrese_selection_dict.get(target_string.decode('utf-8'))


    @api.model
    def get_field_values(self,t_model):

        sql = "select * from "+t_model.replace('.','_')+" order by create_date desc limit 5 "
        self._cr.execute(sql)
        values_obj = self._cr.dictfetchall()

        res=[]
        if values_obj:
            for field in values_obj:
                fieldone={}
                fieldone['id']=field['id']
                fieldone['name'] = field['name']
                res.append(fieldone)

        return res



    # @api.onchange('report_id')
    def onchange_model(self):
        model_list = []
        if self.model_id:
            model_obj = self.env['ir.model']
            current_model = self.model_id.model
            model_list.append(current_model)
            active_model_obj = self.env[self.model_id.model]
            if active_model_obj._inherits:
                for key, val in active_model_obj._inherits.items():
                    model_ids = model_obj.search([('model', '=', key)])
                    if model_ids:
                        model_list.append(key)
        self.model_list = model_list









#
class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'

    @api.multi
    def name_get(self):
        res = []
        for field in self:
            print "self.env.user._is_superuser"

            if self.env.user._is_superuser():
                res.append((field.id, '%s' % (field.field_description)))
            else:
                res.append((field.id, '%s (%s)' % (field.field_description, field.model)))
        return res


    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=None):

        data = self._context.get('model_id_list', None)

        print eval(data)
        #data2 = self._context.get('perm_field_list', None)
        if data:
            args.append(('model_id', 'in', eval(data)))

        if 152 in eval(data):
            args.append(('name', 'in', ['availability','name','author']))
        if 417 in eval(data):
            args.append(('name', 'in', ['name']))
        if 189 in eval(data):
            args.append(('name', 'in', ['name']))
        ret_vat = super(IrModelFields, self).name_search(name=name,
                                                         args=args,
                                                         operator=operator,
                                                         limit=limit)
        return ret_vat
