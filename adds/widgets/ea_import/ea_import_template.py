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

from odoo.osv import osv
from odoo import fields,models,api
from psycopg2.extensions import adapt
import logging
_logger = logging.getLogger(__name__)


from odoo.exceptions import UserError, ValidationError
class ea_import_template_unique_rule(models.Model):

    _name = 'ea_import.template.unique.rule'

    _rec_name = 'source_field_id'

    source_field_id = fields.Many2one('ir.model.fields', 'Template Line Fields', required=True)
    comparison_model_id = fields.Many2one('ir.model', 'Comparison Model', required=True)
    target_field_id = fields.Many2one('ir.model.fields', 'Target Model Fields', required=True)
    template_id = fields.Many2one('ea_import.template', 'EA import template')
    source_model_id = fields.Integer('Import Template Model',related='template_id.target_model_id.id',readonly=True, )


    def default_get(self,fields):
        # getting comparison_model_id
        if self.env.context is None:
            context = {}
        result = super(ea_import_template_unique_rule, self).default_get(fields)
        if 'target_model_id' in self.env.context:
            result.update({'source_model_id': self.env.context.get('target_model_id')})
        return result

    @api.multi
    def onchange_model_id(self,model_id):
        # onchange model id running
        if not model_id:
            return {'value': {}}
        return {'value': {'target_field_id': '', }}

    @api.multi
    def onchange_target_field_id(self, target_field_id):
        if target_field_id:
            field_in_table = self.check_field_in_table_presense(target_field_id)
            if not field_in_table.get('field_present'):
                raise UserError('%s is not storable and can not be selected as target field') % (field_in_table.get('target_field_name'))
        return {}

    @api.multi
    def write(self,vals):
        if vals.get('target_field_id'):
            field_in_table = self.check_field_in_table_presense( vals.get('target_field_id'))
            if not field_in_table.get('field_present'):
                raise UserError('%s is not storable and can not be selected as target field') % (field_in_table.get('target_field_name'))
        return super(ea_import_template_unique_rule, self).write(vals)


    @api.multi
    def check_field_in_table_presense(self, target_field_id):
        res = {}
        if target_field_id:
            target_field_obj = self.pool.get('ir.model.fields').browse(target_field_id)
            target_field_name = target_field_obj.name
            target_field_description = target_field_obj.field_description
            model_name = target_field_obj.model_id.model
            comparison_model_table = self.pool.get(model_name)._table
            self._cr.execute('''SELECT column_name
                          FROM information_schema.columns
                          WHERE table_name = '%s'
                          AND column_name = '%s' ''' % (comparison_model_table, target_field_name, ))
            result = self._cr.fetchall()
            res = {'field_present': bool(result), 'target_field_name': target_field_description}
        return res




class ea_import_template(models.Model):
    _name = 'ea_import.template'

    _order = 'target_model_id, chain_id, sequence'

    name = fields.Char('Name', size=256)
    target_model_id = fields.Many2one('ir.model', 'Target Model')
    test_input_file = fields.Binary('Test Importing File')
    update = fields.Boolean('Update exist',)
    update_current = fields.Boolean('Update only current records',)
    create_new = fields.Boolean('Create New',)
    create_unique_only = fields.Boolean('Create Unique only', help="Create record only if one matching key does not already exist.  Do not use with 'update'.")
    line_ids = fields.One2many('ea_import.template.line', 'template_id', 'Template Lines', )
    matching_rules_ids = fields.One2many('ea_import.template.unique.rule', 'template_id', 'Import Unique Rule')
    chain_id = fields.Many2one('ea_import.chain', 'Import Chain')
    sequence = fields.Integer('Sequence',)
    post_import_hook = fields.Char('Post-import method', size=512,
                                        help="Execute method after importing all records.\n"\
                                        "<target_model>.<function_name>(cr, uid, ids_of_imported_records, context=context)")


    _defaults = {
        'sequence': 1,
    }
    @api.multi
    def generate_record(self,record_list, row_number):


        result = []
        if len(record_list):
            for template in self:
                target_model_pool = self.env[template.target_model_id.model]
                record = {}
                upd_key = []
                updated = False
                ready_to_create_new = True

                if self.env.context.get('default_standard_id'):
                    record['state']='done'
                    record['pid']=self.env['ir.sequence'].next_by_code('student.student')
                    record['standard_id'] =self.env.context.get('default_standard_id')
                    record['school_id'] = self.env['school.standard'].browse(self.env.context.get('default_standard_id')).school_id.id

                if self.env.context.get('default_school_id'):
                    record['school_id'] = self.env.context.get('default_school_id')
                # 'name': vals.get('name'),
                # 'display_name': vals.get('name'),
                # 'isbn': vals.get('isbn'),
                # 'barcode': vals.get('barcode'),
                # 'categ_id': 8,
                # 'school_id':vals.get('school_id'),
                # 'list_price': vals.get('price') if vals.get('price') else 1,
                # 'available_in_pos': True,
                # 'sale_ok': True,
                # 'uom_id': 1,
                # 'author':vals.get('author'),
                # 'uom_po_id': 1,
                # 'is_book':True,
                # 'description':vals.get('description'),
                # 'tome': 1,
                # 'day_to_return_book':7,
                # 'catalog_num':vals.get('catalog_num'),
                # 'num_edition': vals.get('num_edition', 1),
                # 'nbpage':vals.get('nbpage') if vals.get('nbpage') else 1,
                # 'rack':vals.get('rack'),
                # 'default_code': vals.get('default_code'),
                # 'lang': 4,
                # 'copy_num':vals.get('copy_num', 0)

                if self.env.context.get('type')=='book_import':
                    record['school_id']=self.env.user.company_id.school_id
                    record['available_in_pos']=True
                    record['sale_ok']=True
                    record['uom_id']=1
                    record['uom_po_id']=1
                    record['is_book']=True


                if self.env.context.get('type')=='issue_import':
                    record['school_id'] = self.env.user.company_id.school_id


                if self.env.context.get('type')=='card_import':
                    record['school_id'] = self.env.user.company_id.school_id



                # if self.env.context.get('card_id'):
                #     record['standard_id'] =self.env.context.get('default_standard_id')

                for template_line in template.line_ids:
                    field_name = template_line.target_field.name




                    #print "field_name"
                    #print field_name
                    value = template_line.get_field(record_list, row_number, testing=True)
                    # _logger.info("value=")
                    # _logger.info(value)
                    # _logger.info(field_name)
                    # if isinstance(value,basestring):
                    #     value = value.strip()
                    # if field_name=="huohao" and  value!=None and value.find("E+") > -1:
                    #     raise  UserError(('Error creating record!'), ("CSV文件中存在科学记数法:货号"+str(value)))
                    #     print value



                        #raise  UserError(('Error creating record!'), ("CSV文件中存在科学记数法:货号"+str(value)))
                        #print value

                    if value:
                        print field_name
                        print value
                        record.update({field_name: value})
                        if template_line.key_field:
                            upd_key.append((template_line.target_field.name, '=', value))
                    else:
                        if template_line.required:
                            ready_to_create_new = False
                if template.create_new and template.create_unique_only and upd_key:
                    #check if record matching key already exists
                    if self.low_level_search(upd_key):
                        log_notes = "Record already exists - skipping ", record
                        self.env.context['import_log'].append(log_notes)
                        return result
                    #checking if record matching key already exists in fields defined in matching rules
                    matching_model_field_ids = []
                    for template_line in template.line_ids:
                        field_name = template_line.target_field.name
                        value = template_line.get_field(record_list, row_number, testing=True)
                        for matching_value in template.matching_rules_ids:
                            if matching_value.source_field_id.name == field_name:
                                matching_model = matching_value.comparison_model_id.model
                                matching_model_upd_key = []
                                matching_model_upd_key.append((matching_value.target_field_id.name, '=', value))
                                kwargs = {'matching_model_name': matching_model}
                                matching_model_field_ids = self.low_level_search( matching_model_upd_key)
                                if matching_model_field_ids:
                                    log_notes = ("Rules on other models checking:\
                                                  record already exists in model '%s';\
                                                  field: %s; value: %s - skipping " % (matching_model,
                                                                                       matching_value.target_field_id.name,
                                                                                       value)), record
                                    self.env.context['import_log'].append(log_notes)
                    if matching_model_field_ids:
                        return result
                    else:
                        try:
                            new_rec_id = target_model_pool.create(record)
                        except Exception, e:
                            raise ValidationError("Error message: %s\nRow Number: %s\n\nRecord: %s" % (e, row_number, record))
                        new_rec = target_model_pool.browse(new_rec_id)
                        if getattr(new_rec, target_model_pool._rec_name):
                            log_row_name = getattr(new_rec, target_model_pool._rec_name)
                        else:
                            log_row_name = ''
                        log_notes = "creating ", target_model_pool._name, "- name = ", new_rec._rec_name, "- data = ", record
                        self.env.context['import_log'].append(log_notes)
                        result.append(new_rec_id)
                        return result
                if template.update and upd_key:
                    if template.update_current:
                        upd_key.append(('create_date', '>', self.env.context['time_of_start']))
                    updating_record_id = self.low_level_search(upd_key)
                    if updating_record_id:
                        existing_rec = target_model_pool.browse(updating_record_id)[0]
                        if existing_rec.name:
                            log_row_name = existing_rec.name
                        else:
                            log_row_name = ''
                        if self.need_to_update(target_model_pool, updating_record_id, record):
                            target_model_pool.browse(updating_record_id).write(record)
                            #target_model_pool.write(cr, uid, updating_record_id, record, context=context)
                            result.append(updating_record_id[0])
                            log_notes = "update ", target_model_pool._name, "- record id = ", updating_record_id, "- name = ", log_row_name, "- data = ", record
                            self.env.context['import_log'].append(log_notes)
                        else:
                            log_notes = "no update ", target_model_pool._name, "- record id = ", updating_record_id, "- name = ", log_row_name, "- NO CHANGES REQUIRED - data = ", record
                            self.env.context['import_log'].append(log_notes)
                        updated = True
                if not updated and template.create_new and ready_to_create_new:
                    print "not updated"
                    # stock_picking = self.pool.get('stock.picking').browse(self.env.context.get('active_id'))
                    # if record.get("huohao")=="":
                    #     del record['huohao']
                    try:
                        #print "record"
                        _logger.info("record")
                        #print record
                        _logger.info(record)
                        #print "record_list"
                        _logger.info("record_list")
                        _logger.info(record_list)
                        #new_rec_id = target_model_pool.create(record)

                        new_rec = target_model_pool.sudo().create(record)
                        self._cr.commit()
                    except Exception, e:
                        raise UserError( "Error message: %s\nRow Number: %s\n\nRecord: %s" % (e, row_number, record))
                    #new_rec = target_model_pool.browse(cr, uid, new_rec_id)
                    # record1={}
                    # record1['categ_id'] = stock_picking.categ_id.id
                    # record1['web_front'] = stock_picking.web_front.id


                    #new_rec.write(record1)
                    print new_rec
                    # if new_rec and new_rec._rec_name:
                    #     log_row_name = new_rec._rec_name
                    # else:
                    #     log_row_name = ''
                    #log_notes = "creating ", target_model_pool._name, "- name = ",  "- data = ", record
                    #self.env.context['import_log'].append(log_notes)
                    #result.append(new_rec_id)
                    #result.append(new_rec.id)
                    print('new_rec_id')
                    print(new_rec)





                    # producct_id = self.pool.get('product.product').create(cr, uid, {
                    #     'product_tmpl_id': new_rec_id,
                    #     'ean13': '0000000000000'
                    # })
                    #
                    # if context.get('active_model')=='stock.picking':
                    #     self.pool.get('stock.move').create(cr,uid,{
                    #         'picking_id':context.get('active_id'),
                    #
                    #
                    #         'product_tmpl':new_rec_id,
                    #         'product_id':producct_id,
                    #         # 'pt_product_name':record_list[1],
                    #         # 'pt_percentage':record_list[0],
                    #         # 'pt_purity': record_list[2],
                    #         'pt_list_price_version_type':3,
                    #         'product_weight':'%s,%s'%(record_list[2],'a'),
                    #         'pt_process_cost_unit':record.get('process_cost_unit'),
                    #         'pt_percentage': record.get('percentage'),
                    #         'pt_product_name': record.get('product_name'),
                    #         'pt_purity':record.get('purity'),
                    #         'pt_inlay': record.get('inlay'),
                    #         'product_uom':1,
                    #         'partner_id':record.get('store'),
                    #         'location_id':1,
                    #         'name':'import p',
                    #         'location_dest_id':2
                    #
                    #     }, context=context)
        return result

    @api.multi
    def get_related_id(self,input_list, row_number):
        result = []
        for template in self:
            key = []
            for template_line in template.line_ids:
                if template_line.key_field:
                    field_name = template_line.target_field.name
                    value = template_line.get_field(input_list, row_number, testing=True)
                    if value:
                        key.append((field_name, '=', value))
            if template.update_current:
                key.append(('create_date', '>', self.env.context['time_of_start']))
            result = self.low_level_search([template.id], key)
            return result

    @api.multi
    def low_level_search(self, key_list, **kwargs):
        if not kwargs.get('matching_model_name'):
            for template in self:
                model = template.target_model_id.model
        else:
            model = kwargs.get('matching_model_name')
        target_model_pool = self.pool.get(model)
        where_string = "WHERE id IS NOT NULL\n"
        for key_sub_list in key_list:
            if isinstance(key_sub_list[2], basestring):
                second_parametr = adapt(key_sub_list[2]).getquoted()
            else:
                second_parametr = key_sub_list[2]
            where_string += "AND {0} {1} {2} \n".format(key_sub_list[0], key_sub_list[1], second_parametr)
        self._cr.execute("""
                    SELECT *
                    FROM %s
                    %s""" % (target_model_pool._table, where_string))
        result = self._cr.fetchall()
        result = [id_numders[0] for id_numders in result]
        return result

    @api.multi
    def need_to_update(self,target_model_pool, updating_record_id, record):
        for old_record in target_model_pool.read(updating_record_id):
            filtered_old_record = {}
            for key, value in old_record.items():
                if isinstance(value, tuple):
                    filtered_old_record[key] = value[0]
                elif isinstance(value, dict):
                    continue
                else:
                    filtered_old_record[key] = value
        return any([filtered_old_record.get(key) != value for key, value in record.items()])


    @api.model
    def update_templates(self):
        """Relink templates from old table 'ea_import_chain_link'
        directly to ea_import_chain
        """
        self._cr.execute("""SELECT *
                    FROM information_schema.tables
                    WHERE table_name='ea_import_chain_link'""")
        if self._cr.fetchone():
            self._cr.execute("""UPDATE ea_import_template tmpl
                        SET sequence = q1.sequence,
                            chain_id = q1.chain_id,
                            post_import_hook = q1.post_import_hook
                        FROM (SELECT eit.id,
                            eicl.sequence,
                            eicl.chain_id,
                            eicl.post_import_hook
                              from ea_import_template eit
                              LEFT JOIN ea_import_chain_link eicl ON eicl.template_id = eit.id) as q1
                        WHERE tmpl.id = q1.id
            """)
        return True


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
