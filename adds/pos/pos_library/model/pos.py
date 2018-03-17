# -*- coding: utf-8 -*-
import logging
from pyquery import PyQuery as pyq
_logger = logging.getLogger(__name__)
from babel.dates import format_datetime, format_date
import json
from datetime import datetime, timedelta

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools.misc import formatLang
from odoo.exceptions import UserError, ValidationError

import re




import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#
from odoo import models, api, _, fields

from datetime import datetime as dtime

from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as dt
import time
from BeautifulSoup import *
from selenium import webdriver

import urllib
from urllib import urlencode


class SchoolNews1(models.Model):
    _inherit = 'student.news'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        #print "self.env.user.company_id.id"
        #print self.env.user.company_id.id
        if self.env.user.company_id.id!=1:
            args += [('company_id', 'child_of', [self.env.user.company_id.id])]

        return super(SchoolNews1, self).search(args, offset, limit, order, count)


class Reader(models.Model):
    _inherit = 'res.partner'

    card_id = fields.Many2one('library.card', 'card')

    _sql_constraints = [
        ('barcode_uniq', 'unique (barcode,company_id)', "编号重复!"),
    ]

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        #print("aaaaa")
        # if operator not in ('ilike', 'like', '=', '=like', '=ilike'):
        #     return super(Reader, self).name_search(name, args, operator, limit)
        # args = args or []
        # domain = ['|', ('code', operator, name), ('name', operator, name)]
        # partners = self.env['res.partner'].search([('name', operator, name)], limit=limit)
        # if partners:
        #     domain = ['|'] + domain + [('partner_id', 'in', partners.ids)]
        # recs = self.search(domain + args, limit=limit)


        if self.env.user._is_superuser():
            args += [('company_id', 'child_of', [self.env.user.company_id.id])]

        #return super(SchoolNews1, self).search(args, offset, limit, order, count)

        return super(Reader, self).search(args, offset, limit, order, count=count)

        #sql="select rp.*,lc.  from res_partner rp left join  library_card lc on lc.id=rp.card_id"
        #self.env
        #return True




class ClassSummery(models.Model):
    _inherit = 'school.school'

    @api.one
    def _kanban_dashboard(self):
        self.kanban_dashboard = json.dumps(self.get_journal_dashboard_datas())

    @api.one
    def _kanban_dashboard_graph(self):
        self.kanban_dashboard_graph = json.dumps(self.get_bar_graph_datas())

    @api.multi
    def open_action(self):
        """return action based on type for related journals"""
        action_name = self._context.get('action_name', False)
        if action_name == 'book':
            action_name = 'action_product_book_list'
            [action] = self.env.ref('library.%s' % action_name).read()
        elif action_name == 'student':
            action_name = 'action_student_student_form_2'
            [action] = self.env.ref('school.%s' % action_name).read()




        ctx = self._context.copy()
        ctx.pop('group_by', None)
        ctx.update({
            'search_default_school_id': self._context.get('school_id'),

        })

        #[action] = self.env.ref('school.%s' % action_name).read()
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', [])
        return action


    @api.multi
    def get_line_graph_datas(self):
        return []
        # data = []
        # today = datetime.today()
        # last_month = today + timedelta(days=-30)
        # bank_stmt = []
        # # Query to optimize loading of data for bank statement graphs
        # # Return a list containing the latest bank statement balance per day for the
        # # last 30 days for current journal
        # query = """SELECT a.date, a.balance_end
        #                     FROM account_bank_statement AS a,
        #                         (SELECT c.date, max(c.id) AS stmt_id
        #                             FROM account_bank_statement AS c
        #                             WHERE c.journal_id = %s
        #                                 AND c.date > %s
        #                                 AND c.date <= %s
        #                                 GROUP BY date, id
        #                                 ORDER BY date, id) AS b
        #                     WHERE a.id = b.stmt_id;"""
        #
        # self.env.cr.execute(query, (self.id, last_month, today))
        # bank_stmt = self.env.cr.dictfetchall()
        #
        # last_bank_stmt = self.env['account.bank.statement'].search(
        #     [('journal_id', 'in', self.ids), ('date', '<=', last_month.strftime(DF))], order="date desc, id desc",
        #     limit=1)
        # start_balance = last_bank_stmt and last_bank_stmt[0].balance_end or 0
        #
        # locale = self._context.get('lang', 'en_US')
        # show_date = last_month
        # # get date in locale format
        # name = format_date(show_date, 'd LLLL Y', locale=locale)
        # short_name = format_date(show_date, 'd MMM', locale=locale)
        # data.append({'x': short_name, 'y': start_balance, 'name': name})
        #
        # for stmt in bank_stmt:
        #     # fill the gap between last data and the new one
        #     number_day_to_add = (datetime.strptime(stmt.get('date'), DF) - show_date).days
        #     last_balance = data[len(data) - 1]['y']
        #     for day in range(0, number_day_to_add + 1):
        #         show_date = show_date + timedelta(days=1)
        #         # get date in locale format
        #         name = format_date(show_date, 'd LLLL Y', locale=locale)
        #         short_name = format_date(show_date, 'd MMM', locale=locale)
        #         data.append({'x': short_name, 'y': last_balance, 'name': name})
        #     # add new stmt value
        #     data[len(data) - 1]['y'] = stmt.get('balance_end')
        #
        # # continue the graph if the last statement isn't today
        # if show_date != today:
        #     number_day_to_add = (today - show_date).days
        #     last_balance = data[len(data) - 1]['y']
        #     for day in range(0, number_day_to_add):
        #         show_date = show_date + timedelta(days=1)
        #         # get date in locale format
        #         name = format_date(show_date, 'd LLLL Y', locale=locale)
        #         short_name = format_date(show_date, 'd MMM', locale=locale)
        #         data.append({'x': short_name, 'y': last_balance, 'name': name})
        #
        # return [{'values': data, 'area': True}]

    @api.multi
    def get_bar_graph_datas(self):
        data = []
        today = datetime.strptime(fields.Date.context_today(self), DF)
        data.append({'label': _('Past'), 'value': 0.0, 'type': 'past'})
        day_of_week = int(format_datetime(today, 'e', locale=self._context.get('lang', 'en_US')))
        first_day_of_week = today + timedelta(days=-day_of_week + 1)
        for i in range(-1, 4):
            if i == 0:
                label = "本周流通"
            elif i == 3:
                label = "未来流通"
            else:
                start_week = first_day_of_week + timedelta(days=i * 7)
                end_week = start_week + timedelta(days=6)
                if start_week.month == end_week.month:
                    label = str(start_week.day) + '-' + str(end_week.day) + ' ' + format_date(end_week, 'MMM',
                                                                                              locale=self._context.get(
                                                                                                  'lang', 'en_US'))
                else:
                    label = format_date(start_week, 'd MMM',
                                        locale=self._context.get('lang', 'en_US')) + '-' + format_date(end_week,
                                                                                                       'd MMM',
                                                                                                       locale=self._context.get(
                                                                                                           'lang',
                                                                                                           'en_US'))
            data.append({'label': label, 'value': 0.0, 'type': 'past' if i < 0 else 'future'})

        # Build SQL query to find amount aggregated by week
        select_sql_clause = """SELECT count(*) as total ,min(date_issue) as aggr_date from library_book_issue where school_id = %(school_id)s """
        query = ''
        start_date = (first_day_of_week + timedelta(days=-7))
        for i in range(0, 6):
            if i == 0:
                query += "(" + select_sql_clause + "  and date_issue < '" + start_date.strftime(DF) + "')"
            elif i == 5:
                query += " UNION ALL (" + select_sql_clause + " and date_return >= '" + start_date.strftime(DF) + "')"
            else:
                next_date = start_date + timedelta(days=7)
                query += " UNION ALL (" + select_sql_clause + " and date_issue >= '" + start_date.strftime(
                    DF) + "' and date_issue < '" + next_date.strftime(DF) + "')"
                start_date = next_date

        print query
        self.env.cr.execute(query, {'school_id': self.id})
        query_results = self.env.cr.dictfetchall()
        for index in range(0, len(query_results)):
            if query_results[index].get('aggr_date') != None:
                data[index]['value'] = query_results[index].get('total')
        print "get_journal_dashboard_datas"
        print data
        return [{'values': data}]

    @api.multi
    def get_journal_dashboard_datas(self):
        pass
        # currency = self.currency_id or self.company_id.currency_id
        # number_to_reconcile = last_balance = account_sum = 0
        # ac_bnk_stmt = []
        # title = ''
        # number_draft = number_waiting = number_late = sum_draft = sum_waiting = sum_late = 0
        # if self.type in ['bank', 'cash']:
        #     last_bank_stmt = self.env['account.bank.statement'].search([('journal_id', 'in', self.ids)],
        #                                                                order="date desc, id desc", limit=1)
        #     last_balance = last_bank_stmt and last_bank_stmt[0].balance_end or 0
        #     # Get the number of items to reconcile for that bank journal
        #     self.env.cr.execute("""SELECT COUNT(DISTINCT(statement_line_id))
        #                     FROM account_move where statement_line_id
        #                     IN (SELECT line.id
        #                         FROM account_bank_statement_line AS line
        #                         LEFT JOIN account_bank_statement AS st
        #                         ON line.statement_id = st.id
        #                         WHERE st.journal_id IN %s and st.state = 'open')""", (tuple(self.ids),))
        #     already_reconciled = self.env.cr.fetchone()[0]
        #     self.env.cr.execute("""SELECT COUNT(line.id)
        #                         FROM account_bank_statement_line AS line
        #                         LEFT JOIN account_bank_statement AS st
        #                         ON line.statement_id = st.id
        #                         WHERE st.journal_id IN %s and st.state = 'open'""", (tuple(self.ids),))
        #     all_lines = self.env.cr.fetchone()[0]
        #     number_to_reconcile = all_lines - already_reconciled
        #     # optimization to read sum of balance from account_move_line
        #     account_ids = tuple(filter(None, [self.default_debit_account_id.id, self.default_credit_account_id.id]))
        #     if account_ids:
        #         amount_field = 'balance' if not self.currency_id else 'amount_currency'
        #         query = """SELECT sum(%s) FROM account_move_line WHERE account_id in %%s;""" % (amount_field,)
        #         self.env.cr.execute(query, (account_ids,))
        #         query_results = self.env.cr.dictfetchall()
        #         if query_results and query_results[0].get('sum') != None:
        #             account_sum = query_results[0].get('sum')
        # # TODO need to check if all invoices are in the same currency than the journal!!!!
        # elif self.type in ['sale', 'purchase']:
        #     title = _('Bills to pay') if self.type == 'purchase' else _('Invoices owed to you')
        #     # optimization to find total and sum of invoice that are in draft, open state
        #     query = """SELECT state, amount_total, currency_id AS currency FROM account_invoice WHERE journal_id = %s AND state NOT IN ('paid', 'cancel');"""
        #     self.env.cr.execute(query, (self.id,))
        #     query_results = self.env.cr.dictfetchall()
        #     today = datetime.today()
        #     query = """SELECT amount_total, currency_id AS currency FROM account_invoice WHERE journal_id = %s AND date < %s AND state = 'open';"""
        #     self.env.cr.execute(query, (self.id, today))
        #     late_query_results = self.env.cr.dictfetchall()
        #     sum_draft = 0.0
        #     number_draft = 0
        #     number_waiting = 0
        #     for result in query_results:
        #         cur = self.env['res.currency'].browse(result.get('currency'))
        #         if result.get('state') in ['draft', 'proforma', 'proforma2']:
        #             number_draft += 1
        #             sum_draft += cur.compute(result.get('amount_total'), currency)
        #         elif result.get('state') == 'open':
        #             number_waiting += 1
        #             sum_waiting += cur.compute(result.get('amount_total'), currency)
        #     sum_late = 0.0
        #     number_late = 0
        #     for result in late_query_results:
        #         cur = self.env['res.currency'].browse(result.get('currency'))
        #         number_late += 1
        #         sum_late += cur.compute(result.get('amount_total'), currency)




        # return {
        #     'number_to_reconcile': number_to_reconcile,
        #     'account_balance': formatLang(self.env, account_sum,
        #                                   currency_obj=self.currency_id or self.company_id.currency_id),
        #     'last_balance': formatLang(self.env, last_balance,
        #                                currency_obj=self.currency_id or self.company_id.currency_id),
        #     'difference': (last_balance - account_sum) and formatLang(self.env, last_balance - account_sum,
        #                                                               currency_obj=self.currency_id or self.company_id.currency_id) or False,
        #     'number_draft': number_draft,
        #     'number_waiting': number_waiting,
        #     'number_late': number_late,
        #     'sum_draft': formatLang(self.env, sum_draft or 0.0,
        #                             currency_obj=self.currency_id or self.company_id.currency_id),
        #     'sum_waiting': formatLang(self.env, sum_waiting or 0.0,
        #                               currency_obj=self.currency_id or self.company_id.currency_id),
        #     'sum_late': formatLang(self.env, sum_late or 0.0,
        #                            currency_obj=self.currency_id or self.company_id.currency_id),
        #     'currency_id': self.currency_id and self.currency_id.id or self.company_id.currency_id.id,
        #     'bank_statements_source': self.bank_statements_source,
        #     'title': title,
        # }

    kanban_dashboard = fields.Text(compute='_kanban_dashboard')
    kanban_dashboard_graph = fields.Text(compute='_kanban_dashboard_graph')
    belongs_to_company = fields.Boolean('bc',default=True)
    show_on_dashboard = fields.Boolean("收藏",default=True)


class LibrarySummary(models.TransientModel):

    _name = 'library.summary'
    _description = 'library summary'



    @api.model
    def retrieve_today_dashboard(self):

        resp = {}

        sql = "select count(*) as num from library_book_issue where school_id=%s and state in('issue','reissue') and  create_date>CURRENT_DATE" % self.env.user.company_id.school_id
        print sql
        self._cr.execute(sql)
        result = self._cr.dictfetchone()
        resp['today_bowwor'] = result['num']

        sql = "select count(*) as num from library_book_issue where school_id=%s and state='return' and  create_date>CURRENT_DATE" % self.env.user.company_id.school_id
        print sql
        self._cr.execute(sql)
        result1 = self._cr.dictfetchone()
        resp['today_return'] = result1['num']

        sql = "select count(*) as num from product_product where school_id=%s and create_date>CURRENT_DATE" % self.env.user.company_id.school_id
        print sql
        self._cr.execute(sql)
        result2 = self._cr.dictfetchone()
        resp['today_book_issue'] = result2['num']

        sql = "select count(*) as num from student_student where school_id=%s and create_date>CURRENT_DATE" % self.env.user.company_id.school_id
        print sql
        self._cr.execute(sql)
        result3 = self._cr.dictfetchone()
        resp['today_student'] = result3['num']


        print "Resp"
        print resp

        return resp


    @api.multi
    def _get_library_summary(self):
        for sum in self:
            resp = {}
            # 借阅人数
            sql = "select count(DISTINCT(card_id)) as num from library_book_issue  where school_id=%s and create_date >='%s' and create_date <='%s' " % (
                self.env.user.company_id.school_id, sum.date_from, sum.date_to)
            self._cr.execute(sql)
            result = self._cr.dictfetchone()
            resp['dis_reader'] = result['num']

            # 流通总册数
            sql1 = "select count(DISTINCT(lbi.name)) as num from library_book_issue lbi  where lbi.school_id=%s and lbi.create_date >='%s' and lbi.create_date <='%s' " % (
                self.env.user.company_id.school_id, sum.date_from, sum.date_to)
            print("sql1")
            print(sql1)
            self._cr.execute(sql1)
            result1 = self._cr.dictfetchone()
            resp['dis_book'] = result1['num']

            # 其他
            sql2 = "select book_amount,student_amount,issue_amount,round(book_amount/issue_amount,2) as book_rate,round(student_amount/issue_amount,2) as student_rate  from school_school where id=%s " % self.env.user.company_id.school_id
            self._cr.execute(sql2)
            result5 = self._cr.dictfetchone()
            dictMerged2 = dict(resp, **result5)

            sum.library_summary=str(dictMerged2)


    @api.onchange('date_from', 'date_to')
    def get_library_summary(self):
        resp = {}

        #总借阅人数
        contxt = self._context or {}
        print "contxt==="
        print contxt
        print ("get_library_summary")

        #借阅人数
        sql = "select count(DISTINCT(card_id)) as num from library_book_issue  where school_id=%s and create_date >='%s' and create_date <='%s' " % (self.env.user.company_id.school_id,self.date_from,self.date_to)
        self._cr.execute(sql)
        result = self._cr.dictfetchone()
        resp['dis_reader'] = result['num']

        #流通总册数
        sql1 = "select count(DISTINCT(lbi.name)) as num from library_book_issue lbi  where lbi.school_id=%s and lbi.create_date >='%s' and lbi.create_date <='%s' " % (self.env.user.company_id.school_id,self.date_from,self.date_to)
        self._cr.execute(sql1)
        print(sql1)
        result1 = self._cr.dictfetchone()
        resp['dis_book'] = result1['num']

        #其他
        sql2 = "select book_amount,student_amount,issue_amount,case when issue_amount=0 then 0 else round(book_amount/issue_amount,2) end as book_rate ,case when issue_amount=0 then 0 else round(student_amount/issue_amount,2) end as student_rate   from school_school where id=%s " % self.env.user.company_id.school_id
        self._cr.execute(sql2)
        result5 = self._cr.dictfetchone()
        dictMerged2 = dict(resp, **result5)

        print "dictMerged2"
        print dictMerged2

        self.library_summary = str(dictMerged2)

        return resp

    @api.one
    def _kanban_dashboard(self):
        self.kanban_dashboard = json.dumps(self.get_journal_dashboard_datas())

    @api.one
    def _kanban_dashboard_graph(self):
        self.kanban_dashboard_graph = json.dumps(self.get_bar_graph_datas())

    @api.multi
    def get_line_graph_datas(self):
        pass
        # data = []
        # today = datetime.today()
        # last_month = today + timedelta(days=-30)
        # bank_stmt = []
        # # Query to optimize loading of data for bank statement graphs
        # # Return a list containing the latest bank statement balance per day for the
        # # last 30 days for current journal
        # query = """SELECT a.date, a.balance_end
        #                     FROM account_bank_statement AS a,
        #                         (SELECT c.date, max(c.id) AS stmt_id
        #                             FROM account_bank_statement AS c
        #                             WHERE c.journal_id = %s
        #                                 AND c.date > %s
        #                                 AND c.date <= %s
        #                                 GROUP BY date, id
        #                                 ORDER BY date, id) AS b
        #                     WHERE a.id = b.stmt_id;"""
        #
        # self.env.cr.execute(query, (self.id, last_month, today))
        # bank_stmt = self.env.cr.dictfetchall()
        #
        # last_bank_stmt = self.env['account.bank.statement'].search(
        #     [('journal_id', 'in', self.ids), ('date', '<=', last_month.strftime(DF))], order="date desc, id desc",
        #     limit=1)
        # start_balance = last_bank_stmt and last_bank_stmt[0].balance_end or 0
        #
        # locale = self._context.get('lang', 'en_US')
        # show_date = last_month
        # # get date in locale format
        # name = format_date(show_date, 'd LLLL Y', locale=locale)
        # short_name = format_date(show_date, 'd MMM', locale=locale)
        # data.append({'x': short_name, 'y': start_balance, 'name': name})
        #
        # for stmt in bank_stmt:
        #     # fill the gap between last data and the new one
        #     number_day_to_add = (datetime.strptime(stmt.get('date'), DF) - show_date).days
        #     last_balance = data[len(data) - 1]['y']
        #     for day in range(0, number_day_to_add + 1):
        #         show_date = show_date + timedelta(days=1)
        #         # get date in locale format
        #         name = format_date(show_date, 'd LLLL Y', locale=locale)
        #         short_name = format_date(show_date, 'd MMM', locale=locale)
        #         data.append({'x': short_name, 'y': last_balance, 'name': name})
        #     # add new stmt value
        #     data[len(data) - 1]['y'] = stmt.get('balance_end')
        #
        # # continue the graph if the last statement isn't today
        # if show_date != today:
        #     number_day_to_add = (today - show_date).days
        #     last_balance = data[len(data) - 1]['y']
        #     for day in range(0, number_day_to_add):
        #         show_date = show_date + timedelta(days=1)
        #         # get date in locale format
        #         name = format_date(show_date, 'd LLLL Y', locale=locale)
        #         short_name = format_date(show_date, 'd MMM', locale=locale)
        #         data.append({'x': short_name, 'y': last_balance, 'name': name})
        #
        # return [{'values': data, 'area': True}]

    @api.multi
    def get_bar_graph_datas(self):
        data = []
        today = datetime.strptime(fields.Date.context_today(self), DF)
        data.append({'label': _('Past'), 'value': 0.0, 'type': 'past'})
        day_of_week = int(format_datetime(today, 'e', locale=self._context.get('lang', 'en_US')))
        first_day_of_week = today + timedelta(days=-day_of_week + 1)
        for i in range(-1, 4):
            if i == 0:
                label = "本周"
            elif i == 3:
                label = "未来"
            else:
                start_week = first_day_of_week + timedelta(days=i * 7)
                end_week = start_week + timedelta(days=6)
                if start_week.month == end_week.month:
                    label = str(start_week.day) + '-' + str(end_week.day) + ' ' + format_date(end_week, 'MMM',
                                                                                              locale=self._context.get(
                                                                                                  'lang', 'en_US'))
                else:
                    label = format_date(start_week, 'd MMM',
                                        locale=self._context.get('lang', 'en_US')) + '-' + format_date(end_week,
                                                                                                       'd MMM',
                                                                                                       locale=self._context.get(
                                                                                                           'lang',
                                                                                                           'en_US'))
            data.append({'label': label, 'value': 0.0, 'type': 'past' if i < 0 else 'future'})

        # Build SQL query to find amount aggregated by week
        select_sql_clause = """SELECT count(*) as total  from library_book_issue where school_id = %(school_id)s """
        query = ''
        start_date = (first_day_of_week + timedelta(days=-7))
        for i in range(0, 6):
            if i == 0:
                query += "(" + select_sql_clause + " and date_issue < '" + start_date.strftime(DF) + "')"
            elif i == 5:
                query += " UNION ALL (" + select_sql_clause + " and date_issue >= '" + start_date.strftime(DF) + "')"
            else:
                next_date = start_date + timedelta(days=7)
                query += " UNION ALL (" + select_sql_clause + " and date_issue >= '" + start_date.strftime(
                    DF) + "' and date_issue < '" + next_date.strftime(DF) + "')"
                start_date = next_date

        self.env.cr.execute(query, {'school_id': self.id})
        query_results = self.env.cr.dictfetchall()
        for index in range(0, len(query_results)):
            if query_results[index].get('aggr_date') != None:
                data[index]['value'] = query_results[index].get('total')

        return [{'values': data}]

    @api.multi
    def get_journal_dashboard_datas(self):
        pass
        # currency = self.currency_id or self.company_id.currency_id
        # number_to_reconcile = last_balance = account_sum = 0
        # ac_bnk_stmt = []
        # title = ''
        # number_draft = number_waiting = number_late = sum_draft = sum_waiting = sum_late = 0
        # if self.type in ['bank', 'cash']:
        #     last_bank_stmt = self.env['account.bank.statement'].search([('journal_id', 'in', self.ids)],
        #                                                                order="date desc, id desc", limit=1)
        #     last_balance = last_bank_stmt and last_bank_stmt[0].balance_end or 0
        #     # Get the number of items to reconcile for that bank journal
        #     self.env.cr.execute("""SELECT COUNT(DISTINCT(statement_line_id))
        #                     FROM account_move where statement_line_id
        #                     IN (SELECT line.id
        #                         FROM account_bank_statement_line AS line
        #                         LEFT JOIN account_bank_statement AS st
        #                         ON line.statement_id = st.id
        #                         WHERE st.journal_id IN %s and st.state = 'open')""", (tuple(self.ids),))
        #     already_reconciled = self.env.cr.fetchone()[0]
        #     self.env.cr.execute("""SELECT COUNT(line.id)
        #                         FROM account_bank_statement_line AS line
        #                         LEFT JOIN account_bank_statement AS st
        #                         ON line.statement_id = st.id
        #                         WHERE st.journal_id IN %s and st.state = 'open'""", (tuple(self.ids),))
        #     all_lines = self.env.cr.fetchone()[0]
        #     number_to_reconcile = all_lines - already_reconciled
        #     # optimization to read sum of balance from account_move_line
        #     account_ids = tuple(filter(None, [self.default_debit_account_id.id, self.default_credit_account_id.id]))
        #     if account_ids:
        #         amount_field = 'balance' if not self.currency_id else 'amount_currency'
        #         query = """SELECT sum(%s) FROM account_move_line WHERE account_id in %%s;""" % (amount_field,)
        #         self.env.cr.execute(query, (account_ids,))
        #         query_results = self.env.cr.dictfetchall()
        #         if query_results and query_results[0].get('sum') != None:
        #             account_sum = query_results[0].get('sum')
        # # TODO need to check if all invoices are in the same currency than the journal!!!!
        # elif self.type in ['sale', 'purchase']:
        #     title = _('Bills to pay') if self.type == 'purchase' else _('Invoices owed to you')
        #     # optimization to find total and sum of invoice that are in draft, open state
        #     query = """SELECT state, amount_total, currency_id AS currency FROM account_invoice WHERE journal_id = %s AND state NOT IN ('paid', 'cancel');"""
        #     self.env.cr.execute(query, (self.id,))
        #     query_results = self.env.cr.dictfetchall()
        #     today = datetime.today()
        #     query = """SELECT amount_total, currency_id AS currency FROM account_invoice WHERE journal_id = %s AND date < %s AND state = 'open';"""
        #     self.env.cr.execute(query, (self.id, today))
        #     late_query_results = self.env.cr.dictfetchall()
        #     sum_draft = 0.0
        #     number_draft = 0
        #     number_waiting = 0
        #     for result in query_results:
        #         cur = self.env['res.currency'].browse(result.get('currency'))
        #         if result.get('state') in ['draft', 'proforma', 'proforma2']:
        #             number_draft += 1
        #             sum_draft += cur.compute(result.get('amount_total'), currency)
        #         elif result.get('state') == 'open':
        #             number_waiting += 1
        #             sum_waiting += cur.compute(result.get('amount_total'), currency)
        #     sum_late = 0.0
        #     number_late = 0
        #     for result in late_query_results:
        #         cur = self.env['res.currency'].browse(result.get('currency'))
        #         number_late += 1
        #         sum_late += cur.compute(result.get('amount_total'), currency)




        # return {
        #     'number_to_reconcile': number_to_reconcile,
        #     'account_balance': formatLang(self.env, account_sum,
        #                                   currency_obj=self.currency_id or self.company_id.currency_id),
        #     'last_balance': formatLang(self.env, last_balance,
        #                                currency_obj=self.currency_id or self.company_id.currency_id),
        #     'difference': (last_balance - account_sum) and formatLang(self.env, last_balance - account_sum,
        #                                                               currency_obj=self.currency_id or self.company_id.currency_id) or False,
        #     'number_draft': number_draft,
        #     'number_waiting': number_waiting,
        #     'number_late': number_late,
        #     'sum_draft': formatLang(self.env, sum_draft or 0.0,
        #                             currency_obj=self.currency_id or self.company_id.currency_id),
        #     'sum_waiting': formatLang(self.env, sum_waiting or 0.0,
        #                               currency_obj=self.currency_id or self.company_id.currency_id),
        #     'sum_late': formatLang(self.env, sum_late or 0.0,
        #                            currency_obj=self.currency_id or self.company_id.currency_id),
        #     'currency_id': self.currency_id and self.currency_id.id or self.company_id.currency_id.id,
        #     'bank_statements_source': self.bank_statements_source,
        #     'title': title,
        # }


    date_from = fields.Datetime('Date From')
    date_to = fields.Datetime('Date To')
    summary_header = fields.Text('Summary Header')
    library_summary = fields.Text('Room Summary',compute="_get_library_summary",store=False)
    kanban_dashboard = fields.Text(compute='_kanban_dashboard')
    kanban_dashboard_graph = fields.Text(compute='_kanban_dashboard_graph')





    @api.model
    def default_get(self, fields):
        """
        To get default values for the object.
        @param self: The object pointer.
        @param fields: List of fields for which we want default values
        @return: A dictionary which of fields with values.
        """
        if self._context is None:
            self._context = {}
        res = super(LibrarySummary, self).default_get(fields)
        # Added default datetime as today and date to as today + 30.
        import datetime
        from_dt = datetime.date.today()
        dt_from = from_dt.strftime(dt)
        to_dt = from_dt + relativedelta(days=-30)
        dt_to = to_dt.strftime(dt)



        #self.library_summary = str(dictMerged2)


        res.update({'date_from': dt_to, 'date_to': dt_from})

        if not self.date_from and self.date_to:
            date_today = datetime.datetime.today()
            first_day = datetime.datetime(date_today.year,
                                          date_today.month, 1, 0, 0, 0)
            first_temp_day = first_day + relativedelta(months=1)
            last_temp_day = first_temp_day - relativedelta(days=1)
            last_day = datetime.datetime(last_temp_day.year,
                                         last_temp_day.month,
                                         last_temp_day.day, 23, 59, 59)
            date_froms = first_day.strftime(dt)
            date_ends = last_day.strftime(dt)
            res.update({'date_from': date_froms, 'date_to':date_ends })
        return res


    # @api.onchange('date_from', 'date_to')
    # def get_library_summary(self):
    #     company_id = self.env.context.get('company_id')
    #
    #     res = {}
    #
    #
    #     return res

class Teacher(models.Model):
    _inherit = 'hr.employee'

    #
    #
    # @api.model
    # def create(self,vals):
    #     new_teacher = super(TeacherCard, self).create(vals)
    #
    #     self.env['library.card'].create({'barcode':new_teacher.barcode,'teacher_id':new_teacher.id})



    @api.model
    def onchange_barcode(self,barcode):

        res ={}

        res.setdefault('value', {})

        if barcode:

            res['value']['work_email'] = str(self.env.user.company_id.school_id)+"_"+barcode+"@zyhanyuqi.com"
        return res



    @api.model
    def create(self,vals):



        rec = super(Teacher, self).create(vals)

        print "card----rec"
        print rec.id
        print rec.school.id

        card = self.env['library.card'].create({
            'teacher_id': rec.id,
            'code': rec.barcode,
            'user': 'teacher',
            'gt_name': rec.name,
            'book_limit': 0
        })


        self._cr.commit()

        print "card"
        print card
        rec.user_id.write({'card_id': card.id})
        return rec

    @api.model
    def on_change_address(self):
        pass

    @api.model
    def on_change_is_school_teacher(self,val):

        res = {}
        res.setdefault('value', {})
        print "antoine@openerp.comantoine@openerp.comantoine@openerp.comantoine@openerp.comantoine@openerp.com"
        res['value']['school'] = self.env.user.company_id.school_id
        # res['value']['country_id'] = self.env.user.company_id.country_id
        # res['value']['state_id'] = self.env.user.company_id.state_id
        # res['value']['city_id'] = self.env.user.company_id.city
        #
        # res['value']['county'] = self.env.user.company_id.county
        # res['value']['town'] = self.env.user.company_id.town

        return res

    @api.model
    def change_teacher(self):

        sql = "select distinct(id)  from school_school"
        self._cr.execute(sql)
        schools = self._cr.fetchall()

        print "schools="
        print schools
        for (next_sequence, ) in schools:

            teachers = self.search([('school', '=', next_sequence)])
            for teacher in teachers:

                teacher.with_context(cron_action=True).update({'company_id': teacher.school.company_id.id})
                if self.barcode:
                    card = self.env['library.card'].search(['teacher_id','=',self.id])
                    userp = self.env['res.partner'].sudo().search([('barcode','=',self.barcode)])
                    if userp:
                        userp.update({'card_id':card.id})

    @api.model
    def change_teacher2(self):

        sql = "select distinct(id),company_id  from school_school"
        self._cr.execute(sql)
        schools = self._cr.fetchall()

        print "schools="
        print schools
        for (next_sequence, company_id) in schools:

            teachers = self.search([('company_id', '=', company_id)])
            for teacher in teachers:
                if not teacher.school:
                    #company = self.env['res.company'].browse(company_id)
                    teacher.sudo().with_context(cron_action=True).write({'school':next_sequence})



    barcode = fields.Char('教师编号',related='user_id.barcode',store=True)


    _sql_constraints = [
            ('value_teacher_uniq', 'unique (barcode,school)', '老师编号重复 !')
        ]



class SchoolstandardStandardS(models.Model):
    ''' Defining a standard related to school '''
    _inherit = 'standard.standard'


    student_num = fields.Integer('年级人数')
    issue_num = fields.Integer('流通册数')


class SchoolStandardS(models.Model):
    ''' Defining a standard related to school '''
    _inherit = 'school.standard'
    _rec_name = 'all_name'

    @api.one
    @api.onchange('standard_id','name')
    def get_all_name(self):
        if self.name and self.standard_id.name:
            self.all_name = self.standard_id.name + '[' + self.name  +']班'
        else:
            self.all_name = ''


    @api.one
    def set_all_name(self):
        print self.all_name
        s_pos = self.all_name.find('[')
        s_pos2 = self.all_name.find(']')
        if s_pos>0 and s_pos2>0:
            stand_name = self.all_name[0:s_pos]
            stand_standard = self.env['standard.standard'].search([('name','=',stand_name)])
            if stand_standard:
                self.standard_id = self.env['standard.standard'].browse(stand_standard[0]).id
                #self.write({'standard_id':stand_standard[0]})
                #self.standard_id = stand_standard
            else:
                raise ValidationError(_('年级名不符合规范.'))
                #self.standard_id = self.env['standard.standard'].create({'name':stand_name})

            self.name = self.all_name[s_pos+1:s_pos2]

        else:
            raise ValidationError(_('班级名不符合规范.'))

        pass

    all_name=fields.Char('全名',inverse='set_all_name',store=True)
    student_num = fields.Integer('班级人数')
    issue_num = fields.Integer('流通册数')

    _sql_constraints = [
        ('name_calss_uniq', 'unique (name,standard_id,school_id)', "班级重复!"),
    ]


class LibraryIssue(models.Model):
    _inherit = 'library.book.issue'



    # @api.multi
    # def unlink(self):
    #     product_ctx = dict(self.env.context or {}, active_test=False)
    #     print "ids"
    #     print self.ids
    #     print self.id
    #     if self.with_context(product_ctx).search_count([('id', 'in', self.ids), ('state', 'in',['issue','issue'] )]):
    #         raise UserError("有书籍未还")
    #     return super(PosLibraryBook, self).unlink()




    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        context = self._context or {}

        print "search_context="
        print context
        if context.get('school_filter_book'):
            sql = "select distinct on (lbi.name) lbi.name,lbi.id  from library_book_issue lbi  where lbi.school_id=%s and lbi.create_date >='%s' and lbi.create_date <='%s' " % (
            self.env.user.company_id.school_id, context.get('from_t'), context.get('to_t'))
            print(sql)
            self._cr.execute(sql)
            result = self._cr.fetchall()
            print "school_filter_book"


            ids = [id for (name,id) in result]
            print ids

            if ids:
                args += [('id', 'in', ids)]


        if context.get('school_filter_reader'):
            sql = "select distinct on (lbi.card_id) lbi.card_id,lbi.id  from library_book_issue lbi  where lbi.school_id=%s and lbi.create_date >='%s' and lbi.create_date <='%s' " % (
            self.env.user.company_id.school_id, context.get('from_t'), context.get('to_t'))
            self._cr.execute(sql)
            result = self._cr.fetchall()
            print "school_filter_book"


            ids = [id for (name,id) in result]
            print ids

            if ids:
                args += [('id', 'in', ids)]


        return super(LibraryIssue, self).search(args, offset, limit, order, count=count)



class PosLibraryCompany(models.Model):
    _inherit = 'product.category'


    cn_cat=fields.Char('分类号')

class PosLibraryCompany(models.Model):
    _inherit = 'res.company'


    @api.one
    @api.onchange('partner_id')
    def _get_school(self):

        _logger.info("_get_school_get_school_get_school_get_school_get_school_get_school_get_school_get_school")
        school = self.env['school.school'].search([('company_id','=',self.id)])
        if school:
            self.school_id=school[0].id
        else:
            raise UserError("学校错误")



    school_id=fields.Integer('学校',compute="_get_school",store=True)










class PosLibraryPublisher(models.Model):
    _name = 'product.publisher'


    name=fields.Char('名称')




class PosLibraryBook(models.Model):
    _inherit = 'product.product'




    # @api.multi
    # def unlink(self):
    #     product_ctx = dict(self.env.context or {}, active_test=False)
    #     if self.with_context(product_ctx).search_count([('id', 'in', self.ids), ('state', 'in',['issue','issue'] )]):
    #         raise UserError("有书籍未还")
    #     return super(PosLibraryBook, self).unlink()

    #
    # @api.model
    # def product_pic(self):
    #
    #     sql = "select * from product_product"
    #     self._cr.execute(sql)
    #
    #     pros = self._cr.dictfetchall()
    #
    #     for product in pros:
    #         print product
    #         product_obj= self.env['product.product'].browse(product['id'])
    #
    #         keyword = product_obj.name
    #         #p = re.compile(r'\S+')
    #
    #         result, number = re.subn(r'\S+', "+", keyword)
    #
    #         url = "http://search.jd.com/Search?keyword="+result+"&enc=utf-8&qrst=1&rt=1&stop=1&book=y&vt=2&page=1&s=1&click=0"
    #
    #         #pro_order = self.env['purchase.order'].search([('product_id', '=', product['id'])])
    #



    @api.multi
    def _comput_copy_num(self):
        #print ("_comput_copy_num_vals="+vals)
        for book in self:
            book.copy_num=len(book.copy_ids)

    @api.multi
    def _comput_tome_num(self):
        for book in self:
            book.tomes_num = len(book.tome_ids)

    @api.multi
    def update_product_available(self):

        sql = "select * from product_product"
        self._cr.execute(sql)

        pros = self._cr.dictfetchall()

        for product in pros:
            print product
            pro_order = self.env['purchase.order'].search([('product_id','=',product['id'])])
            if not pro_order and product['is_book']==True:
                order = self.env['purchase.order'].create({
                    "partner_id": 7,
                    "state": 'purchase',
                    "date_planned": fields.Datetime.now()
                })
                purline = self.env['purchase.order.line'].create({
                    "name": product['isbn'],
                    "product_qty": 1,
                    "qty_received": 1,
                    "date_planned": fields.Datetime.now(),
                    "product_uom": 1,
                    "product_id": product['id'],
                    "price_unit": 1,
                    "order_id": order.id,
                })
                pick = order.picking_ids

                pick.force_assign()
                pick.pack_operation_product_ids.write({'qty_done': 1})

                print "pick======"
                print pick

                pick.do_new_transfer()




    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if operator not in ('ilike', 'like', '=', '=like', '=ilike'):
            return super(PosLibraryBook, self).name_search(name, args, operator, limit)
        #print "123123123"
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search(
                [('name', operator, name)] + args, limit=limit)
        if not recs:
            recs = self.search(
                [('barcode', operator, name)] + args, limit=limit)
        return recs.name_get()


    @api.multi
    def _inverse_tome_num(self):
        print("_inverse_tome_num")
        _logger.info("_inverse_tome_num")
        if self._context.get('ts',0)=='':
            return
        begin_barcode = int(self._context.get('begin_barcode',0))

        ts = int(self._context.get('ts',0)) or self.tomes_num
        for book in self:

            print "tomes_num="
            print self
            print self._context
            print self.env.context
            print ts
            print "copy_num="
            print book.copy_num
            if ts>1:
                for i in range(ts-1):
                    begin_barcode += 1
                    tome=str(i+2)
                    if ts==2:
                        if i == 0:
                            tome = "下"
                    if ts==3:
                        if i == 0:
                            tome = "中"
                        if i == 1:
                            tome = "下"

                    new_vals = {
                        'name': book.name,
                        'isbn': book.isbn,
                        'barcode': str(begin_barcode),
                        #'barcode': self.env['ir.sequence'].next_by_code(
                        #    'library.book.sequence' + str(self.env.user.company_id.id)),
                        'categ_id': book.categ_id.id,
                        'school_id': book.school_id.id,
                        'list_price': book.price,
                        'available_in_pos': True,
                        'sale_ok': True,
                        'multy_tome':True,
                        'uom_id': 1,
                        'author': book.author.id,
                        'uom_po_id': 1,
                        'is_book': True,
                        'description': book.description,
                        'tome': tome,
                        'day_to_return_book': 0,
                        'catalog_num': book.catalog_num,
                        'num_edition': book.num_edition,
                        'nbpage': book.nbpage,
                        'rack': book.rack.id,
                        #'default_code': vals.get('default_code'),
                        'lang': 4,
                        'tome_base':book.tome_base
                    }
                    print new_vals


                    val = self.env['product.product'].create(new_vals)
                    print("val=")
                    print val







    @api.multi
    def _inverse_copy_num(self):
        _logger.info("_inverse_copy_num")
        print self

        print self._context.get('cs')
        print self._context.get('cs')==''
        if self._context.get('cs')=='':
            return

        ts = 0
        if self._context.get('ts') != '':
            ts = int(self._context.get('ts', 0)) or self.tomes_num


        #start_barcode = int(self.barcode)+self.tomes_num
        cs = int(self._context.get('cs',0)) or self.copy_num
        #ts = int(self._context.get('ts', 0)) or self.tomes_num

        for book in self:

            print "copy_num="
            print cs
            if cs>1:
                tome="1"
                if ts==2 or ts==3:
                    tome="上"
                for i in range(cs-1):
                    start_barcode = int(self.barcode) + self.tomes_num*(i+1)
                    new_vals = {
                        'name': book.name,
                        'isbn': book.isbn,
                        #'barcode': self.env['ir.sequence'].next_by_code('library.book.sequence'+str(self.env.user.company_id.id)),
                        'barcode': str(start_barcode),
                        'categ_id': book.categ_id.id,
                        'school_id': book.school_id.id,
                        'list_price': book.price,
                        'available_in_pos': True,
                        'sale_ok': True,
                        'tomes_num':ts,
                        'uom_id': 1,
                        'author': book.author.id,
                        'uom_po_id': 1,
                        'is_book': True,
                        'description': book.description,
                        'tome': tome,
                        'day_to_return_book': 0,
                        'catalog_num': book.catalog_num,
                        'num_edition': book.num_edition,
                        'nbpage': book.nbpage,
                        'rack': book.rack.id,
                        #'default_code': vals.get('default_code'),
                        'lang': 4
                    }

                    #if cs > 1:
                    if ts > 1:
                        new_vals['multy_tome']=True
                        new_vals['tome_base']=new_vals['barcode']
                        #new_vals['tomes_num'] = ts
                    print new_vals
                    val = self.env['product.product'].with_context(begin_barcode=start_barcode).create(new_vals)
                    print("val=")
                    print val

            # book_new={}
            # print book.name
            # book_new['name']=book.name
            #book.copy_num

    is_book = fields.Boolean('是否是书籍',
                                 help='True when folio line created from \
                                 Reservation')

    multy_tome = fields.Boolean('是否多卷', default=False)

    tomes_num = fields.Integer('卷数',compute="_comput_tome_num",inverse='_inverse_tome_num',store=False)

    publisher = fields.Many2one('product.publisher',string="出版社")

    copy_num = fields.Integer('副本量', compute="_comput_copy_num", inverse='_inverse_copy_num', store=False)
    school_id = fields.Many2one('school.school', '学校')
    cncateg = fields.Many2one('product.category', '中图分类', help="Select category for the current product")



    _sql_constraints = [
        ('barcode_uniq', 'unique(barcode,school_id)', "条码重复!"),
    ]


    @api.model
    def create(self, vals):
        # When creating an expense product on the fly, you don't expect to
        # have taxes on it


        newbook = super(PosLibraryBook, self).create(vals)

        #school_obj = self.env['school.school'].browse(newbook.school_id.id)
        #school_obj.write({'book_amount': school_obj.book_amount + 1})
        #self._cr.commit()

        #update_str = "update school_school set book_amount=book_amount+1   where id=%s" % (newbook.school_id.id)
        #self._cr.execute(update_str)

        return newbook





    @api.model
    def onchange_isbn(self,isbn):
        if isbn and len(isbn)==13:
            bookvalue=dict()
            book =  self.get_book_date_with_isbn(isbn)
            #return partners.id or self.name_create(email)[0]
            #print book['lang']
            if self.env['product.lang'].name_search(book['lang']):
                book['lang'] =  self.env['product.lang'].name_search(book['lang'])[0][0]
            else:
                book['lang'] =  self.env['product.lang'].name_create(book['lang'])[0]

            #book['lang'] = self.env['product.lang'].name_search(book['lang'])[0][0] or self.env['product.lang'].name_create(book['lang'])[0]
            #print langs
            if self.env['library.author'].name_search(book['author']):
                book['author'] =  self.env['library.author'].name_search(book['author'])[0][0]
            else:
                book['author'] =  self.env['library.author'].name_create(book['author'])[0]

            book['categ_id'] = 59

            book['day_to_return_book'] = 5
            # if self.env['libra8y.author'].name_search(book['author']):
            #     book['catalog_num'] =  self.env['library.author'].name_search(book['author'])[0][0]
            # else:
            #     book['catalog_num'] =  self.env['library.author'].name_create(book['author'])[0]



            print book['author']

            # book['author'] = self.env['library.author'].name_search(book['author'])[0][0] or \
            #                self.env['library.author'].name_create(book['author'])[0]



            #print book['author']


            # if(len(langs)>0):
            #     book['lang'] =langs[0]
            # else:
            #     self.env['product.lang'].create({"name": book['lang']})
            #
            return {'value': book}





    def create_book_pos(self, vals):
        print ("httpvals")
        print vals
        if 'author' in vals:

            authors = self.env['library.author'].search([('name','=',vals['author'][:-3])])
            if authors:
                vals['author']=authors[0].id
            else:
                newauthor = self.env['library.author'].create({'name':vals['author'][:-3]})

                vals['author']=newauthor.id

        if "company_id" in vals:
            companies = self.env['school.school'].search([('company_id','=',vals['company_id'])])
            print companies[0].id
            if companies:
                vals['school_id']=companies[0].id
        if 'catalog_num' in vals:
            ids = self.env['product.category'].search([('name', 'ilike', vals['catalog_num'])])
            if ids:
                vals['cncateg'] = ids[0].id
            else:
                cncateg = self.env['product.category'].sudo().create({
                        'name': vals['catalog_num']
                    })
                vals['cncateg'] = cncateg.id


        #print  vals['author']

        _logger.info("get)vals")
        _logger.info(vals)

        tome = "1"
        print vals.get('tomes_num')
        if vals.get('tomes_num', 0) == '2' or vals.get('tomes_num', 0) == '3':
            tome = "上"


        new_vals = {
            'name': vals.get('name'),
            'display_name': vals.get('name'),
            'isbn': vals.get('isbn'),
            'barcode': vals.get('barcode'),
            'categ_id': 59,
            'school_id':vals.get('school_id'),
            'list_price': vals.get('price') if vals.get('price') else 1,
            'available_in_pos': True,
            'sale_ok': True,
            #'uom_id': 1,
            'author':vals.get('author'),
            #'uom_po_id': 1,
            'is_book':True,
            # 'tome_num在上面'
            'description':vals.get('description'),
            'tome': tome,
            'day_to_return_book':0,
            'catalog_num':vals.get('catalog_num'),
            'cncateg':vals.get('cncateg'),
            'num_edition': vals.get('num_edition',1),
            'nbpage':vals.get('nbpage') if vals.get('nbpage') else 1,
            'rack':vals.get('rack'),
            'default_code': vals.get('default_code'),
            'lang': 4,
            # 'copy_num'在下面'

            'tomes_num': vals.get('tomes_num', 0),
            'copy_num':vals.get('copy_num', 0)

        }
        #new_vals['copy_nums']=vals.get('copy_num', 0)

        if vals.get('tomes_num') != '' and int(vals.get('tomes_num'))>1:
            new_vals['multy_tome'] = True
            new_vals['tome_base'] = vals.get('barcode')


        #new_new_dic = [(k,new_vals[k]) for k in sorted(new_vals.keys())]
        new_new_dic = new_vals
        _logger.info ("new_new_dic")
        _logger.info (new_new_dic)

        rec = self.env['product.product'].with_context(begin_barcode=vals.get('barcode'),ts=vals.get('tomes_num', 0),cs=vals.get('copy_num', 0)).create(new_new_dic)

        _logger.info("has_create")
        _logger.info(rec)




        return 1






    def get_url_param_auto(self):

        #driver = webdriver.PhantomJS(
        #    executable_path='/Users/guizhouyuntushidai/PycharmProjects/lehman/odoo10/others/phantomjs/bin/phantomjs')
        driver = webdriver.PhantomJS()
        # executable_path为你的phantomjs可执行文件路径
        driver.get("http://opac.nlc.cn/")
        time.sleep(1)

        source = driver.page_source.encode('utf-8', 'ignore')
        bsObj = BeautifulSoup(driver.page_source)
        form1, form2 = bsObj.findAll('form')

        if len(form1['action'])>0:
            self.env['ir.config_parameter'].set_param('library.search.book', form1['action'])
        return form1['action']

    def get_url_param(self):

        base_url = self.env['ir.config_parameter'].get_param('library.search.book')
        if len(base_url)>0:
            return base_url

        driver = webdriver.PhantomJS(
            executable_path='/Users/guizhouyuntushidai/PycharmProjects/lehman/odoo10/others/phantomjs/bin/phantomjs')
        # driver = webdriver.PhantomJS()
        # executable_path为你的phantomjs可执行文件路径
        driver.get("http://opac.nlc.cn/")
        time.sleep(1)

        source = driver.page_source.encode('utf-8', 'ignore')
        bsObj = BeautifulSoup(driver.page_source)
        form1, form2 = bsObj.findAll('form')

        if len(form1['action'])>0:
            self.env['ir.config_parameter'].set_param('library.search.book', form1['action'])
        return form1['action']


    def get_book_date_from_server_with_barcode(self,barcode):

        productone = self.env['product.product'].search([('barcode','=',barcode)])
        print "get_book_date_from_server_with_barcode"
        reproduct={}
        product = productone[0]
        if product:
            print "has_product"
            reproduct['id'] = product.id
            reproduct['display_name']=product.display_name
            reproduct['list_price'] = product.list_price
            reproduct['price'] = product.price
            reproduct['pos_categ_id'] = product.pos_categ_id.id
            reproduct['taxes_id'] = product.taxes_id.id
            reproduct['barcode'] = product.barcode
            reproduct['default_code'] = product.default_code
            reproduct['to_weight'] = product.to_weight
            reproduct['uom_id'] = product.uom_id.id
            reproduct['description_sale'] = product.description_sale
            reproduct['description'] = product.description
            reproduct['product_tmpl_id'] = product.product_tmpl_id.id
            reproduct['tracking'] = product.tracking
            reproduct['description_sale'] = product.description_sale
            reproduct['qty_available'] = product.qty_available
            reproduct['is_book'] = product.is_book
            reproduct['availability'] = product.availability
            reproduct['day_to_return_book'] = product.day_to_return_book
            reproduct['isbn'] = product.isbn
            reproduct['school_id'] = product.school_id.id

            return json.dumps(reproduct)
        return False

    def get_book_date_with_isbn(self,isbn_number):
        book=dict()
        book['barcode'] = self.env['ir.sequence'].next_by_code('library.book.sequence'+str(self.env.user.company_id.id))

        base_url=self.get_url_param()
        _logger.info(base_url)

        _logger.info(base_url+isbn_number+'&local_base=NLC01&filter_code_1=WLN&filter_request_1=&filter_code_2=WYR&filter_request_2=&filter_code_3=WYR&filter_request_3=&filter_code_4=WFM&filter_request_4=&filter_code_5=WSL&filter_request_5=')
        doc = pyq(
            url=base_url+'?func=find-b&find_code=ISB&request='+isbn_number+'&local_base=NLC01&filter_code_1=WLN&filter_request_1=&filter_code_2=WYR&filter_request_2=&filter_code_3=WYR&filter_request_3=&filter_code_4=WFM&filter_request_4=&filter_code_5=WSL&filter_request_5=',
            encoding="utf-8")
        cts2 = doc('td')

        open('163.txt', 'w').write(cts2.html())

        pattern = re.compile(r"ISBN: (.*) CNY")
        pattern2 = re.compile(r"CNY(.*)\s")



        match = re.findall(pattern, doc.html())
        match2 = re.findall(pattern2, doc.html())
        book['isbn']=match[0] or ''
        book['list_price'] = match2[0] or 0

        for i in cts2:
            if (pyq(i).text() == 'ID 号'):
                book['default_code'] = pyq(i).nextAll().text()
            if (pyq(i).text() == '题名与责任'):
                book['name'] = pyq(i).nextAll().text()
            if (pyq(i).text() == '版本项'):
                banci = pyq(i).nextAll().text()
                book['num_edition']=banci[:-1] or 1
            if (pyq(i).text() == '出版项'):
                publisher = pyq(i).nextAll().find('a').text()
                publisher1 = publisher.split(' : ')
                publisher2 = publisher.split(', ')
                book['pub'] = publisher2[0] or ''
            if (pyq(i).text() == '载体形态项'):
                td4text = pyq(i).nextAll().text()
                td4s = td4text.split(';')
                # if re.match(r"\d册*",td4s[0]):
                #
                #
                #
                pattern = re.compile(r"\d*")
                match = re.findall(pattern, td4s[0])
                print match[0]
                book['nbpage'] = match[0] or 0
            if (pyq(i).text() == '语言'):
                eng = pyq(i).nextAll().text()
                book['lang'] = eng
            if (pyq(i).text() == '内容提要'):
                book['description'] = pyq(i).nextAll().text()
            if (pyq(i).text() == '中图分类号'):
                book['catalog_num'] = pyq(i).nextAll().text()
            if (pyq(i).text() == '著者'):
                book['author']  = pyq(i).nextAll().text()
                #print td7
        print book
        return book

    def request1(self,appkey, categ_id,m="GET"):
        url = "http://web.juhe.cn:8080/finance/gold/shgold"
        params = {
            "key": appkey,  # APP Key
            "v": "",  # JSON格式版本(0或1)默认为0

        }
        params = urlencode(params)
        if m == "GET":
            f = urllib.urlopen("%s?%s" % (url, params))
        else:
            f = urllib.urlopen(url, params)

        content = f.read()
        res = json.loads(content)
        if res:
            error_code = res["error_code"]
            if error_code == 0:
                # 成功请求
                #print res["result"][0]['4']['latestpri']
                if categ_id==4:
                    #return res["result"][0]['10']['latestpri']
                    return 281.5
                else:
                    #return res["result"][0]['4']['latestpri']
                    return 281.5
            else:
                _logger.error( "%s:%s" % (res["error_code"], res["reason"]))
                return 100
        else:
            _logger.error("request api error")

    def _get_book_from_jd(self, cr, uid,ids,field_name, arg, context=None):
        res={}
        #html = getHtml("http://tieba.baidu.com/p/2460150866")2fff67caeaf0c33f78e3af381c8269f0
        for pick in self.browse(cr, uid, ids, context=context):

            res[pick.id]=self.request1('d1748c45b8cd086312f9d70539a678dc',pick.categ_id)
        return res



