# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent
#    (<http://www.eficent.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

import xlwt
from datetime import *
from openerp.report import report_sxw
from openerp.addons.report_xls.report_xls import report_xls
from openerp.tools.translate import _

class attendance_table(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(attendance_table, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_children': self.get_children,
        })

    def get_children(self, val, level=0):
        result = {'latein':u"迟到",
                  'earlyout':u"早退",
                  'lateinearlyout':u"迟到早退",
                  'absent':u"缺席",
                  'normal':u"正常",
                  'semiabsent':u"半缺席",
                  }

        return result[val]

class attendance_table_xls2(report_xls):
    column_sizes = [40, 20, 20, 40, 20, 20, 20, 20, 20]

    def global_initializations(self, wb, _p, xlwtlib, _xs, o, data):
        # this procedure will initialise variables and Excel cell styles and
        # return them as global ones
        self.ws = wb.add_sheet(o.name.encode("UTF-8")+_(u'(')+o.start_date+_(u'至')+o.end_date+u')')
        self.ws.panes_frozen = True
        self.ws.remove_splits = True
        self.ws.portrait = 0  # Landscape
        self.ws.fit_width_to_pages = 1
        self.ws.header_str = self.xls_headers['standard']
        self.ws.footer_str = self.xls_footers['standard']
        # -------------------------------------------------------
        # number of columns
        self.nbr_columns = 9
        # -------------------------------------------------------
        self.style_default = xlwtlib.easyxf(_xs['borders_all'])
        # -------------------------------------------------------
        self.style_bold = xlwtlib.easyxf(_xs['bold'] + _xs['borders_all'])
        # -------------------------------------------------------
        # cell style for columns titles
        self.style_yellow_bold = xlwtlib.easyxf(
            _xs['bold'] + _xs['fill'] + _xs['borders_all'])
        # -------------------------------------------------------

    # send an empty row to the Excel document
    def print_empty_row(self, row_position):
        c_sizes = self.column_sizes
        c_specs = [('empty%s' % i, 1, c_sizes[i], 'text', None)
                   for i in range(0, len(c_sizes))]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_position = self.xls_write_row(
            self.ws, row_position, row_data, set_column_size=True)
        return row_position

    # Fill in a row with the titles of the columns
    def print_columns_title(self, _p, data, row_position):
        c_specs = [
            ('human_title', 1, 0, 'text', _('人员'), None,
             self.style_yellow_bold),
            ('attendance_date_title', 1, 0, 'text', _('考勤日期'),
             None, self.style_yellow_bold),
            ('attendance_series_item_name_title', 1, 0, 'text', _('班次明细名称'),
             None, self.style_yellow_bold),
            ('attendance_result_title', 1, 0, 'text', _('考勤结果'),
             None, self.style_yellow_bold),
            ('overtime_hours_title', 1, 0, 'text', _('签退延时'), None,
             self.style_yellow_bold),
            ('work_hours_title', 1, 0, 'text', _('工作时长'), None,
             self.style_yellow_bold),
            ('week_day_title', 1, 0, 'text', _('周几'),
             None, self.style_yellow_bold),
            ('checkintime_title', 1, 0, 'text', _('上班时间'),
             None, self.style_yellow_bold),
            ('checkouttime_title', 1, 0, 'text', _('下班时间'),
             None, self.style_yellow_bold),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_position = self.xls_write_row(
            self.ws, row_position, row_data, row_style=self.style_yellow_bold)
        return row_position

    # export the BOMs
    def print_boms(self, row_position, bom, _xs, xlwtlib, _p, data):
        #print '****************************************print_boms*********************************************'
        c_specs = [
            ('human', 1, 0, 'text', bom.human.name or ''),
            ('attendance_date', 1, 0, 'text', bom.attendance_date),
            ('attendance_series_item_name', 1, 0, 'text', bom.attendance_series_item_name or ''),
            ('attendance_result', 1, 0, 'text', _p.get_children(bom.attendance_result) or ''),
            ('overtime_hours', 1, 0, 'number', bom.overtime_hours),
            ('work_hours', 1, 0, 'number', bom.work_hours),
            ('week_day', 1, 0, 'number', bom.week_day),
            ('checkintime', 1, 0, 'text', bom.checkintime or ''),
            ('checkouttime', 1, 0, 'text', bom.checkouttime or ''),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_position = self.xls_write_row(
            self.ws, row_position, row_data, self.style_bold)
        return row_position

    def generate_xls_report(self, _p, _xs, data, objects, wb):  # main function

        
        for o in objects:
            # Initializations
            self.global_initializations(wb, _p, xlwt, _xs, o, data)
            row_pos = 0
            # Print empty row to define column sizes
            row_pos=self.print_empty_row(row_pos)
            # Print Header Table data
            row_pos = self.print_columns_title(_p, data, row_pos)
            # Freeze the line
            self.ws.set_horz_split_pos(row_pos)
            for ch in o.item_ids:
                row_pos = self.print_boms(row_pos, ch, _xs, xlwt,_p, data)

attendance_table_xls2('report.attendance.table.xls2', 'attendance_record.human_attendance_table', parser=attendance_table)
