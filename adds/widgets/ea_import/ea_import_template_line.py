# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Enapps LTD (<http://www.enapps.co.uk>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import random
import uuid
from odoo.osv import osv
from odoo import fields,models,api
import datetime
from odoo.tools.translate import _
import base64
from inspect import isfunction
import logging
import uuid
from odoo.exceptions import UserError, ValidationError
_logger=logging.getLogger(__name__)

class ea_import_template_line(models.Model):

    _name = 'ea_import.template.line'
    _rec_name = "target_field"

    @api.multi
    def _get_related_field_model(self,name, args, context=None):
        if self:
            return {}
        result = {}
        for template_line in self:
            result[template_line.id] = template_line.target_field.relation
        return result


    def _get_next_sequence(self, context={}):
        template_id = context.get('template_id')
        if template_id:
            self._cr.execute("""
                SELECT MAX(sequence) + 1
                FROM ea_import_template_line
                WHERE template_id = %s
                      """, (template_id, ))
            for (next_sequence, ) in self._cr.fetchall():
                return next_sequence or 1
        return 1

    @api.one
    def _get_rel_field_type(self):
        self.real_field_type = self.self.target_field.ttype

        #related = 'target_field.ttype', selection = PACKAGE_TYPE_SELECTION

    target_field=fields.Many2one('ir.model.fields', string="Field Name", select=True)
    template_id=fields.Many2one('ea_import.template', 'Template', select=True, ondelete="cascade", )
    target_model_id=fields.Many2one('ir.model',string='Target Object',related='template_id.target_model_id',  readonly=True, store=False,)
    related_field=fields.Many2one('ir.model.fields', string="Related Field", select=True)
    related_field_model=fields.Char('related_field_model', size=512,)
    sequence=fields.Integer('Sequence', required=True, select=True)
    real_field_type=fields.Char('Field type',compute='_get_rel_field_type',readonly=True, store=False,)
    test_result_field=fields.Char('Test Result', size=512,)
    default_value=fields.Char('Default Value', size=512,)
    use_only_defaults=fields.Boolean('Use only defaults',)
    test_result_record_number=fields.Integer('Record Number')
    key_field=fields.Boolean('Key field for updating', select=True)
    required=fields.Boolean('Required for creating new', select=True)
    calculated=fields.Boolean('Calculated', select=True)
    calc_field_ids=fields.One2many('ea_import.template.line.calc_field', 'template_line_id', 'Calculated Field',)
    boolean_field_ids=fields.One2many('ea_import.template.line.boolean_field', 'template_line_id', 'Boolean Fields',)
    replace=fields.Boolean('Replace field before processing', select=True)
    regexp_field_ids=fields.One2many('ea_import.template.line.regexp_field', 'template_line_id', 'Regexp Fields',)
    header_column_name=fields.Char('Header Column Name', size=64,)
    many2one_rel_type = fields.Selection([
        ('dbid', 'Database ID'),
        ('subfield', 'Subfield'),
        ('template', 'Template'),
        ('active_id', 'Active ID'),
    ], 'Relation type', )
    match_limit = fields.Selection([('match_first', 'Match first result'),
                                    ('match_last', 'Match last result')],
                                   'Match Limit',
                                   help="If defined, will select one record with given order from several found for template line")
    related_template_id = fields.Many2one('ea_import.template', 'Related Template', select=True)
    time_format=fields.Char('Time Format', size=128)
    field_type=fields.Selection([('char', 'char'),
                                  ('text', 'text'),
                                  ('boolean', 'boolean'),
                                  ('integer', 'integer'),
                                  ('date', 'date'),
                                  ('datetime', 'datetime'),
                                  ('float', 'float'),
                                  ('selection', 'selection'),
                                  ('binary', 'binary'),
                                  ('many2one', 'many2one'),
                                 ], 'Field Type')


    _defaults = {
        'time_format': '%d/%m/%Y',
        'sequence': lambda self: self._get_next_sequence(),
        'many2one_rel_type': 'subfield',
        'default_value': None,
    }

    @api.multi
    def name_get(self):
        result = []
        for template_line in self:
            template_line_name = "%s/%s" % (template_line.target_model_id.name, template_line.related_field.name)
            result.append((template_line.id, template_line_name))
        return result

    @api.model
    def default_get(self,fields):
        result = super(ea_import_template_line, self).default_get(fields)
        template_id = self.env.context.get('template_id')
        target_model_id = self.env.context.get('target_model_id')
        result.update({'template_id': template_id, 'target_model_id': target_model_id})
        return result

    @api.multi
    def onchange_target_field(self, field_id):
        if field_id:
            model_fields = self.env['ir.model.fields']
            field_obj = model_fields.browse(field_id)

            print "field_obj.ttype="+field_obj.ttype
            return {'value': {'field_type': field_obj.ttype, 'related_field_model': field_obj.relation}}
        else:
            return {'value': {}}


    @api.model
    def match_limit_ac(self, template_line, result):
        if not result or not isinstance(result, list):

            return result
        if template_line.match_limit == 'match_first':
            result = [result[0]]
        elif template_line.match_limit == 'match_last':
            result = [result[-1]]
        return result

    @api.multi
    def get_field(self, input_list, row_number, testing=False):

        print "context==========="
        print self._context

        template_line_boolean_field_pool = self.pool.get('ea_import.template.line.boolean_field')
        template_line_regxp_field_pool = self.pool.get('ea_import.template.line.regexp_field')

        def test_many2one_result(result_list, template_line, target_string):
            if len(result_list) > 1 and not template_line.match_limit:
                raise osv.except_osv(_('Error !'), _("For %s/%s relation there more then 1 record. CSV row number %i." % (template_line.target_field.field_description, template_line.related_field.field_description,row_number+1)))
            if not result_list and template_line.required:
                #raise UserError(('Error creating record!'), ("CSV文件中存在科学记数法:货号" + str(value)))
                raise UserError(_("""Model - %s\nField - %s\nThere no related field '%s' in %s/%s relation (field is required) \nField name: %s \nColumn: %s\nRow number: %i\nRow Data: %s""" % (template_line.template_id.name, template_line.target_field.model, target_string, template_line.target_field.model, template_line.related_field.model, template_line.target_field.name, str(template_line.sequence),row_number+1, input_list)))
        print "input_list"
        print input_list
        for template_line in self:

            _logger.info(template_line.target_field.name)
            if not all([bool(field_str) == False for field_str in input_list]):
                if (template_line.use_only_defaults or not input_list[template_line.sequence - 1]) and template_line.many2one_rel_type != 'active_id':
                    target_string = template_line.default_value
                elif template_line.many2one_rel_type == 'active_id':
                    target_string = str(self.env.context['active_id'])
                else:
                    target_string = input_list[template_line.sequence - 1]
                    if not target_string.strip() and template_line.default_value:
                        target_string = template_line.default_value

                if template_line.replace:
                    target_string = self.env['ea_import.template.line.regexp_field'].browse([regexp_field.id for regexp_field in template_line.regexp_field_ids]).replace_string(target_string)
                    # target_string = template_line_regxp_field_pool.replace_string([regexp_field.id for regexp_field in template_line.regexp_field_ids],
                    #                                                               target_string)
                template_line_type = template_line.field_type
                if template_line.calculated and template_line_type in ['integer', 'float']:
                    calc_fields = sorted(template_line.calc_field_ids, key=lambda k: k.sequence)
                    result = float(input_list[calc_fields.pop(0).column_number - 1].strip() or "0")
                    for calc_field in calc_fields:
                        result = calc_field.calculate(result, input_list)
                    return result
                elif template_line_type in ['text', 'char']:
                    if target_string == False:
                        target_string = ''
                    return target_string.encode('utf-8')
                if template_line_type == 'selection':
                    return template_line.get_selection_from_name(target_string)

                if template_line_type == 'binary':
                    return base64.b32encode(target_string)
                elif template_line_type == 'integer':
                    print "template_line_typeinteger"
                    print target_string
                    try:
                        return int(target_string)
                    except Exception:
                        return 0

                elif template_line_type == 'float' and template_line.target_field.ttype=='float':
                    print "template_line_type=float"
                    print template_line.target_field.ttype
                    print template_line.target_field.name
                    print target_string
                    if not target_string:
                        raise osv.except_osv(('Error !'), ("Field %s has no value and cannot be converted.  Enter a default value in the template for this field or fix the CSV file so it contains data for this field row. \nField: %s\nColumn: %s\nRow number: %i \nRow Data: %s") % (template_line.target_field.name, template_line.target_field.name, str(template_line.sequence), row_number+1, input_list))
                    return float(target_string)
                elif template_line_type == 'boolean':
                    if template_line.boolean_field_ids:
                        return template_line_boolean_field_pool.get_value([boolean_field.id for boolean_field in template_line.boolean_field_ids],
                                                                          target_string)
                    else:
                        return bool(target_string)
                elif template_line_type == 'date':
                    try:
                        target_time = datetime.datetime.strptime(target_string, "%Y-%m-%d")
                        return target_time.strftime("%Y-%m-%d")
                    except ValueError:
                        return None
                elif template_line_type == 'datetime':
                    try:
                        print "target_string="
                        print template_line.time_format
                        target_time = datetime.datetime.strptime(target_string, "%Y-%m-%d")
                        return target_time.strftime("%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        return None
                elif template_line_type == 'time':
                    try:
                        target_time = datetime.datetime.strptime(target_string, template_line.time_format)
                        return target_time.strftime("%H:%M:%S")
                    except ValueError:
                        return None
                elif template_line_type == 'many2one':
                    print "many2onemany2onemany2onemany2onemany2onemany2onemany2onemany2onemany2onemany2one"
                    target_obj_pool = self.env[template_line.target_field.relation]
                    if template_line.many2one_rel_type in ['dbid', 'active_id']:
                        return int(target_string)

                    elif template_line.many2one_rel_type == 'subfield':
                        #print template_line.related_field.name
                        print "subfieldsubfieldsubfieldsubfieldsubfieldsubfield"

                        print (template_line.related_field.name)
                        print (target_string.strip())
                       # print ('standard='+str(self.env.context.get('default_standard_id')))
                        print (template_line.target_field.name)

                        print self.env.context.get('type')

                        print self.env.context.get('type')=='book_import'
                        print template_line.sequence - 1


                        if self.env.context.get('type','0')!='issue_import' and template_line.related_field.name == "code" and target_string != None :
                            # result_ids = self.env['library.card'].search([('code', '=', target_string), (
                            # 'standard_id', '=', self.env.context.get('default_standard_id'))])
                            # if not result_ids:
                            #     card_new = self.env['library.card'].sudo().create({
                            #         'code':target_string,
                            #         'standard_id':self.env.context.get('default_standard_id'),
                            #         'book_limit':5,
                            #         'country_id':49,
                            #         'state_id':668,
                            #         'city_id':247,
                            #         'user':'student'
                            #
                            #     })
                            #     result=[card_new]
                            # else:
                            #     result=result_ids
                            pass
                        # elif template_line.target_field.name == "user_id" and target_string != None:
                        #     user_new = self.env['res.users'].sudo().create({
                        #         'name': target_string,
                        #         'login':str(self.env.context.get('default_standard_id'))+'-'+target_string
                        #     })
                        #     result = [user_new]

                        #年级必须在前
                        elif self.env.context.get('type') == 'card_student_import' and template_line.related_field.name == "all_name" and target_string != None:

                            result_ids = self.env['school.standard'].search([('all_name', '=', target_string), ('school_id', '=', self.env.user.company_id.school_id)])
                            print "result_ids"
                            print result_ids
                            if not result_ids:
                                #pos_s = target_string.find('[')
                                #standard_name = target_string[0:pos_s]
                                #res = self.env['standard.standard'].search([('name','=','standard_name')])
                                standard_new = self.env['school.standard'].create({
                                    'all_name': target_string,
                                    'school_id': self.env.user.company_id.school_id,
                                })
                                result = [standard_new]
                            else:
                                result = result_ids

                        elif self.env.context.get(
                                'type') == 'card_student_import' and  target_string != None and template_line.target_field.name=='student_id' :
                            _logger.info("card_student_import,card_student_import,card_student_import,card_student_import,card_student_import")
                            #print target_string
                            # result_ids = self.env['student.student'].sudo().search([('name', '=', target_string), (
                            # 'school_id', '=', self.env.user.company_id.school_id),('roll_no','=',input_list[4])])
                            if True:
                                #pos_s = target_string.find('[')
                                standard_ids = self.env['school.standard'].search([('all_name','=',input_list[2]),('school_id','=',self.env.user.company_id.school_id)])
                                standard = None
                                if not standard_ids:

                                        #res = self.env['standard.standard'].search([('name','=','standard_name')])
                                    standard_new = self.env['school.standard'].create({
                                        'all_name': input_list[2],
                                        'school_id': self.env.user.company_id.school_id,
                                    })
                                    standard = standard_new.id
                                else:
                                    standard = standard_ids[0].id

                                _logger.info({
                                    'name': target_string,
                                    'barcode':input_list[4],
                                    'login': str(self.env.user.company_id.school_id)+target_string,
                                    'company_id':self.env.user.company_id.id

                                })

                                #user_new = self.env['res.users'].create({
                                #    'name': target_string,
                                #    'barcode':input_list[4],
                                #    'login': uuid.uuid1(),
                                #    'company_id':self.env.user.company_id.id,


                                #})
                                student_new = self.env['student.student'].create({
                                    'name': target_string,
                                    'school_id': self.env.user.company_id.school_id,
                                    'roll_no':input_list[4],
                                    'standard_id':standard,
                                    'barcode': input_list[4],
                                    'state':'done',
                                    'pid':input_list[4],
                                    #'user_id':user_new.id,
                                    'cmp_id':self.env.user.company_id.id
                                })
                                _logger.info("student============")
                                _logger.info(student_new)
                                result = [student_new]
                            # else:
                            #     result = result_ids

                        elif self.env.context.get('type')=='book_import' and  target_string != None and template_line.target_field.name=='author':

                            print "start book_importbook_importbook_importbook_importbook_importbook_import"
                            auther_ids = self.env['library.author'].search([('name', '=', target_string)])
                            print "book_importbook_importbook_importbook_importbook_importbook_import"

                            if not auther_ids:
                                auther_new = self.env['library.author'].sudo().create({
                                    'name': target_string
                                })

                                result = [auther_new]
                            else:
                                result = auther_ids
                        elif self.env.context.get(
                                'type') == 'book_import' and target_string != None and template_line.target_field.name=='cncateg':
                            auther_ids = self.env['product.category'].search([('cn_cat', '=', target_string)])
                            print "standardstandardstandardstandardstandardstandardstandardstandardstandard9999999"

                            if not auther_ids:
                                auther_new = self.env['product.category'].sudo().create({
                                    'cn_cat': target_string,
                                    'name':target_string,
                                    'pid':56
                                })
                                result = [auther_new]
                            else:
                                result = auther_ids
                        elif self.env.context.get(
                                'type') == 'book_import' and target_string != None and template_line.target_field.name=='publisher':
                            auther_ids = self.env['product.publisher'].sudo().search([('name', '=', target_string)])

                            if not auther_ids:
                                auther_new = self.env['product.publisher'].sudo().create({
                                    'name': target_string
                                })
                                result = [auther_new]
                            else:
                                result = auther_ids
                        elif self.env.context.get(
                                'type') == 'card_teacher_import' and template_line.related_field.name == "name" and target_string != None and template_line.sequence - 1==2:
                            #result_ids = self.env['hr.employee'].search([('name', '=', target_string),('barcode','=',input_list[3])])

                            if True:
                                #pos_s = target_string.find('[')
                                #standard = self.env['school.standard'].search([('all_name','=',input_list[2]),('school_id','=',self.env.user.company_id.school_id)])


                                # user_new = self.env['res.users'].sudo().create({
                                #     'name': target_string,
                                #     'barcode': input_list[3],
                                #     'login': input_list[3]
                                # })

                                teacher_new = self.env['hr.employee'].sudo().with_context(login=uuid.uuid1()).create({
                                    'name': target_string,
                                    'barcode':input_list[3],
                                    # 'user_id':user_new.id,
                                    'is_school_teacher': True,
                                    'company_id':self.env.user.company_id.id,
                                    'school': self.env.user.company_id.school_id,

                                })

                                # teacher_new = self.env['hr.employee'].create({
                                #     'school': self.env.user.company_id.school_id,
                                #     'is_school_teacher':True,
                                #     'resource_id':resource.id
                                #     # 'barcode':input_list[4],
                                #     # 'standard_id':standard[0]
                                # })
                                result = [teacher_new]
                            #else:
                                #result = result_ids

                        else:


                            result = target_obj_pool.search(
                                [(template_line.related_field.name, '=', target_string.strip())])





                        _logger.info(result)
                        #result = self.match_limit(template_line, result)
                        #print result
                        if testing:
                            test_many2one_result(result, template_line, target_string.strip())
                            return result and result[0].id or False
                        elif not result:
                            return None
                        else:
                            return result[0].id
                    elif template_line.many2one_rel_type == 'template':
                        result = template_line.related_template_id.get_related_id(input_list, row_number)
                        result = self.match_limit_ac(template_line, result)
                        if testing:
                            test_many2one_result(result, template_line, target_string.strip())
                        return result and result[0]
            else:
                continue

    @api.multi
    def get_selection_from_name(self,target_string):
        for template_line in self:
            target_model_pool = self.env[template_line.target_model_id.model]
            selection_dict_1 = target_model_pool.fields_get().get(template_line.target_field.name)
            print selection_dict_1

            selection_dict = selection_dict_1.get('selection')


                #.selection
            if isfunction(selection_dict):
                selection_dict = dict(getattr(target_model_pool, selection_dict.__name__)())
            else:
                selection_dict = dict(selection_dict)

            #print selection_dict
            revrese_selection_dict = dict((v, k) for k, v in selection_dict.iteritems())
            print revrese_selection_dict
            #unicode(a, 'gb2312')
            print target_string.decode('utf-8')
            print revrese_selection_dict.get(target_string.decode('utf-8'))
            return revrese_selection_dict.get(target_string.decode('utf-8'))



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
