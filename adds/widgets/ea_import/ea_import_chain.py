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
import base64
import csv
import re
#import MySQLdb as mdb
import datetime
from cStringIO import StringIO
try:
    from ftplib import FTP_TLS
except:
    from ftplib import FTP


import chardet
import logging
from odoo.exceptions import UserError, ValidationError
_logger=logging.getLogger(__name__)


# def unicode_xls_reader(unicode_xls_data, dialect=csv.excel, charset='utf-8', **kwargs):
#     # csv.py doesn't do Unicode; encode temporarily as UTF-8:
#     #csv_reader = csv.reader(utf_8_encoder(unicode_csv_data, charset),dialect=dialect, **kwargs)
#     xls_reader=pd.read_excel(unicode_xls_data)
#     for row in xls_reader:
#         # decode UTF-8 back to Unicode, cell by cell:
#         yield [unicode(cell, charset) for cell in row]




def unicode_csv_reader2(unicode_csv_data, dialect=csv.excel, charset='utf-8', **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    #print('charset='+charset)
    #charset="GBK"
    print (kwargs)
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data, charset),
                            dialect=dialect, **kwargs)

    print csv_reader
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, charset) for cell in row]


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, charset='utf-8', **kwargs):

    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data, charset),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        #decode UTF-8 back to Unicode, cell by cell:
        for cell in row:
            decType=chardet.detect(cell)
            #print(decType['encoding'])
            #print(unicode(cell,'windows-1252'))
        yield [unicode(cell, charset) for cell in row]
        #yield [unicode(cell, chardet.detect(cell).get('encoding')).encode('utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data, charset):
    for line in unicode_csv_data:
        yield line
        #yield line.decode(charset).encode('utf-8', 'ignore')


class ea_import_chain(models.Model):
    _name = 'ea_import.chain'

    name = fields.Char('Name', size=256, required=True)
    type = fields.Selection([
            ('csv', 'CSV Import'),
            ('ftp', 'Import from ftp server'),
            ('mysql', 'MySql Import'),
            ('xls', 'XLS Import'),
        ], 'Import Type', required=True, help="Type of connection import will be done from")
    mysql_config_id = fields.Many2one('mysql.config', 'MySql configuration')
    ftp_config_id = fields.Many2one('import.ftp_config', 'FTP Configuration')
    input_file = fields.Binary('Test Importing File', required=False)
    header = fields.Boolean('Header')
    template_ids = fields.One2many('ea_import.template', 'chain_id', 'Templates', )
    result_ids = fields.One2many('ea_import.chain.result', 'chain_id', 'Import Results', )  # to be removed
    log_ids = fields.One2many('ea_import.log', 'chain_id', 'Import Log', )
    separator = fields.Selection([
            (",", '<,> - Coma'),
            (";", '<;> - Semicolon'),
            ("\t", '<TAB> - Tab'),
            (" ", '<SPACE> - Space'),
        ], 'Separator', required=True)
    delimiter = fields.Selection([
            ("'", '<\'> - Single quotation mark'),
            ('"', '<"> - Double quotation mark'),
            ('None', 'None'),
        ], 'Delimiter', )
    charset = fields.Selection([
            ('us-ascii', 'US-ASCII'),
            ('utf-7', 'Unicode (UTF-7)'),
            ('utf-8', 'Unicode (UTF-8)'),
            ('utf-16', 'Unicode (UTF-16)'),
            ('windows-1250', 'Central European (Windows 1252)'),
            ('windows-1251', 'Cyrillic (Windows 1251)'),
            ('iso-8859-1', 'Western European (ISO)'),
            ('iso-8859-15', 'Latin 9 (ISO)'),
            ('GBK', 'GBK'),
        ], 'Encoding', required=True)
    model_id = fields.Many2one('ir.model', 'Related document model')
    ir_act_window_id = fields.Many2one('ir.actions.act_window', 'Sidebar action', readonly=True, )
    ir_value_id = fields.Many2one('ir.values', 'Sidebar button', readonly=True, )


    _defaults = {
        'separator': ",",
        'charset': 'utf-8',
        'delimiter': None,
        'type': 'csv',
    }

    def copy(self, default):
            if default is None:
                default = {}
            default.update({'result_ids': [],
                            'log_ids': [],
                            'ir_act_window_id': False,
                            'ir_value_id': False,
                            })
            return super(ea_import_chain, self).copy(default)

    def get_mysql_data(self, config_obj):
        pass
        # connect = mdb.connect(host=config_obj.host, user=config_obj.username,
        #                    passwd=config_obj.passwd, db=config_obj.db)
        # connect.escape_string("'")
        # cursor = connect.cursor()
        # if re.match(r'CREATE|DROP|UPDATE|DELETE', config_obj.query, re.IGNORECASE):
        #     raise UserError(('Error !'), ("Operation prohibitet!"))
        # cursor.execute(config_obj.query)
        # data = cursor.fetchall()
        # connect.close()
        # return '\n'.join([row[1:-2] for row in [str(item) + ',' for item in data]])

    @api.multi
    def get_ftp_data(self):
        for chain in self:
            config_obj = chain.ftp_config_id
            try:
                conn = FTP_TLS(host=config_obj.host, user=config_obj.username, passwd=config_obj.passwd)
                conn.prot_p()
            except:
                conn = FTP(host=config_obj.host, user=config_obj.username, passwd=config_obj.passwd)
            filenames = conn.nlst()
            for filename in filenames:
                input_file = StringIO()
                conn.retrbinary('RETR %s' % filename, lambda data: input_file.write(data))
                input_string = input_file.getvalue()
                input_file.close()
                csv_reader = unicode_csv_reader(StringIO(input_string), delimiter=str(chain.separator), quoting=(not chain.delimiter and csv.QUOTE_NONE) or csv.QUOTE_MINIMAL, quotechar=chain.delimiter and str(chain.delimiter) or None, charset=chain.charset)
                self.import_to_db( csv_reader=csv_reader)
                conn.delete(filename)
            conn.quit()
        return True

    def check_active_ids(self):
        """Checks whether import is run from form view
        of object with model name defined above if there
        is template line defined with relational type of
        'active_id'.
        """
        if not self.env.context.get('active_id') or len(self.env.context.get('active_ids', [])) > 1:
            raise UserError('Error!', "This import template can be used only from form view!")
        return True

    @api.multi
    def import_to_db(self, csv_reader=False):

        if not csv_reader:
            time_of_start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            self.with_context(time_of_start=time_of_start)
            self.with_context(result_ids=[])
            self.with_context(log_id=[])
            self.with_context(import_log=[])
            # context = dict(self.env.context)
            # context.update({'time_of_start': time_of_start})
            # context['result_ids'] = []
            # context['log_id'] = []
            # context['import_log'] = []
        result_pool = self.env['ea_import.chain.result']
        log_pool = self.env['ea_import.log']


        for chain in self:
            print chain.type
            if not chain.type:
                raise UserError(('Error !'), ("No connection type specified!"))
            # if chain.type == 'xls' and not csv_reader:
            # csv_reader = read_xls(file_name)
            if chain.type == 'csv' and not csv_reader:
                #print chain.input_file
                csv_reader = unicode_csv_reader(StringIO(base64.b64decode(chain.input_file)), delimiter=str(chain.separator), quoting=(not chain.delimiter and csv.QUOTE_NONE) or csv.QUOTE_MINIMAL, quotechar=chain.delimiter and str(chain.delimiter) or None, charset=chain.charset)
            elif chain.type == 'mysql' and not csv_reader:
                input_data = self.get_mysql_data(chain.mysql_config_id)
                csv_reader = unicode_csv_reader(StringIO(input_data), delimiter=str(chain.separator), quoting=(not chain.delimiter and csv.QUOTE_NONE) or csv.QUOTE_MINIMAL, quotechar=chain.delimiter and str(chain.delimiter) or None, charset=chain.charset)
            elif chain.type == 'ftp' and not csv_reader:
                self.get_ftp_data()
                continue
            print csv_reader
            if chain.header:
                #pass
                csv_reader.next()
                #csv_reader.next()
                #print "abbbccccbb"
            result = {}
            print "abbbbb"
            if any([True for template in chain.template_ids for line in template.line_ids if line.field_type == 'many2one' and line.many2one_rel_type == 'active_id']):
                self.check_active_ids()
            print "23232"
            for template in chain.template_ids:
                model_name = template.target_model_id.model
                result.update({model_name: {'ids': set([]), 'post_import_hook': template.post_import_hook}})
            for row_number, record_list in enumerate(csv_reader):
                print "11111111111112222225"
                _logger.info(record_list)
                if len(record_list) < max([template_line.sequence for template_line in template.line_ids for template in chain.template_ids]):
                    #_logger
                    _logger.info("Invalid File or template definition. You have less columns in file than in template. Check the file separator or delimiter or template.")
                    raise UserError(('Error !'), ("Invalid File or template definition. You have less columns in file than in template. Check the file separator or delimiter or template."))
                print "11111114111111"

                _logger.info("get_record_list")
                for template in sorted(chain.template_ids, key=lambda k: k.sequence):
                    print "1111111111111"
                    model_name = template.target_model_id.model
                    print("record_list")
                    print(record_list)
                    result_id=None
                    if self._context.get('type'):
                        result_id = template.generate_record(record_list,                                                                             row_number)
                    else:
                        result_id = template.with_context({'type':'book_import'}).generate_record(record_list, row_number)
                    _logger.info("get_record_list")
                    _logger.info(record_list)
                    result[model_name]['ids'] = result[model_name]['ids'] | set(result_id)
            for name, imported_ids, post_import_hook in [(name, value['ids'], value['post_import_hook']) for name, value in result.iteritems()]:
                if post_import_hook and hasattr(self.pool.get(name), post_import_hook):
                    getattr(self.env[name], post_import_hook)(list(imported_ids))
                result_ids_file = base64.b64encode(str(list(imported_ids)))
                result_ids = result_pool.create({
                    'chain_id': chain.id,
                    'result_ids_file': result_ids_file,
                    'name': name,
                    'import_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                })
                #self.env.context['result_ids'].append(result_ids)

            # log_id = log_pool.create( {
            #     'chain_id': chain.id,
            #     'import_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            # })
            #
            #
            # result_pool.browse(self.env.context.get('result_ids', [])).write( {'log_id': log_id})
            # log_line_obj = self.pool.get('ea_import.log.line')
            # for line in self.env.context.get('import_log', []):
            #     log_line_obj.create({
            #     'log_id': log_id,
            #     'name': line
            # })
            #self.env.context['log_id'].append(log_id)
        return True

    @api.multi
    def create_action(self):
        vals = {}
        action_obj = self.env['ir.actions.act_window']
        for chain in self:
            model_name = chain.model_id.model
            button_name = 'Import from CSV (%s)' % chain.name
            vals['ir_act_window_id'] = action_obj.create({
                'name': button_name,
                'type': 'ir.actions.act_window',
                'res_model': 'import.wizard',
                'src_model': model_name,
                'view_type': 'form',
                'context': "{'import_chain_id': %d}" % chain.id,
                'view_mode': 'form,tree',
                'res_id': chain.id,
                'target': 'new'
            }).id
            vals['ir_value_id'] = self.env['ir.values'].create( {
                 'name': button_name,
                 'model': model_name,
                 'key2': 'client_action_multi',
                 'value': "ir.actions.act_window," + str(vals['ir_act_window_id'])

             }).id
        self.write({
                    'ir_act_window_id': vals.get('ir_act_window_id', False),
                    'ir_value_id': vals.get('ir_value_id', False),
                })
        return True

    @api.multi
    def unlink_action(self):
        for chain in self:
            if chain.ir_act_window_id:
                self.pool.get('ir.actions.act_window').unlink(chain.ir_act_window_id.id)
            if chain.ir_value_id:
                ir_values_obj = self.pool.get('ir.values')
                ir_values_obj.unlink(chain.ir_value_id.id)
        return True



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
