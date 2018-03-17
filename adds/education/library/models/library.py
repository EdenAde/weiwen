# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

import time
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, Warning as UserError
import logging
_logger = logging.getLogger(__name__)

class LibraryRack(models.Model):
    _name = 'library.rack'
    _description = "Library Rack"

    name = fields.Char('Name', required=True,
                       help="it will be show the position of book")
    code = fields.Char('Code')
    active = fields.Boolean('Active', default='True')
    school_id = fields.Many2one('school.school','学校')


class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = "Author"

    name = fields.Char('Name', required=True)
    born_date = fields.Date('Date of Birth')
    death_date = fields.Date('Date of Death')
    biography = fields.Text('Biography')
    note = fields.Text('Notes')
    editor_ids = fields.Many2many('res.partner', 'author_editor_rel',
                                  'author_id', 'parent_id', 'Editors')

    _sql_constraints = [('name_uniq', 'unique (name)',
                         'The name of the author must be unique !')]





class LibraryCard(models.Model):
    _name = "library.card"
    _description = "Library Card information"
    _rec_name = "code"




    @api.multi
    def name_get(self):
        '''Method to display name and code
        {u'lang': u'zh_CN', u'params': {u'action': 581}, u'tz': u'Asia/Shanghai', u'uid': 1, u'bin_size': True}

'''
        #print self.env.context
        if self.env.context.get('params') or self.env.context.get('is_link'):

            return [(rec.id, rec.code) for rec in self]
        return [(rec.id, rec.code,rec.type_book_limit,rec.student_id.id,rec.teacher_id.id,rec.left_limit,rec.issue_ids_string) for rec in self]





    @api.onchange('student_id')
    def on_change_student(self):
        print "on_change_student"
        '''  This method automatically fill up student roll number
             and standard field  on student_id field
        @param self : Object Pointer
        @param cr : Database Cursor
        @param uid : Current Logged in User
        @param ids : Current Records
        @student : Apply method on this Field name
        @param context : standard Dictionary
        @return : Dictionary having identifier of the record as key
            and the value of student roll number and standard'''
        pass
        # student_data = self.env['student.student'].browse(self.student_id.id)
        # self.standard_id = student_data.standard_id.id
        # self.roll_no = student_data.roll_no

    @api.multi
    @api.depends('student_id')
    def _compute_name(self):
        print "_compute_name"
        for rec in self:
            if rec.student_id:
                user = rec.student_id.name
            else:
                user = rec.teacher_id.name
            rec.gt_name = user

    @api.multi
    @api.onchange('type')
    def _compute_left_limit(self):
        for rec in self:
            issue_ids = self.env['library.book.issue'].search([('card_id', '=', rec.id),('state', 'in', ['issue', 'reissue'])])

            if not rec.type_book_limit:
                rec.left_limit = 0
            else:
                rec.left_limit= 0 if (rec.type_book_limit-len(issue_ids))<0 else rec.type_book_limit-len(issue_ids)

    @api.multi
    def _issue_ids_string(self):
        for rec in self:
            istring=''
            if rec.issue_ids:
                for issue in rec.issue_ids:
                    istring+=str(issue.name.id)+','
                _logger.info(istring[:-1])
                rec.issue_ids_string=istring[:-1]
            else:
                rec.issue_ids_string = istring


    # @api.model
    # def create(self, vals):
    #
    #     newcard  = super(LibraryCard, self).create(vals)
    #     if vals.get('student_id'):
    #         student = self.env['student.student'].browse(vals.get('student_id'
    #                                                               ))
    #         vals.update({'standard_id': student.standard_id.id,
    #                      'roll_no': student.roll_no})
    #
    #         user = self.env['res.partner'].browse(vals.get('user_id'))
    #
    #         print "newcard.id"
    #         print newcard.id
    #         #self._cr.commit()
    #         #user.update({"card_id":newcard.id})
    #
    #     return newcard


    # @api.model
    # def write(self, vals):
    #     if vals.get('student_id'):
    #         student = self.env['student.student'].browse(vals.get('student_id'
    #                                                               ))
    #         vals.update({'standard_id': student.standard_id.id,
    #                      'roll_no': student.roll_no})
    #
    #         user = self.env['res.partner'].browse(vals.get('user_id'))
    #
    #         user.update({"card_id":vals.get("id")})
    #
    #     return super(LibraryCard, self).write(vals)



    @api.multi
    def write(self, vals):
        if vals.get('student_id'):
            student = self.env['student.student'].browse(vals.get('student_id'
                                                                  ))
            vals.update({'standard_id': student.standard_id.id,
                         'roll_no': student.roll_no})
        return super(LibraryCard, self).write(vals)

    code = fields.Char('Card No', required=True, default=lambda self:
                       self.env['ir.sequence'].get('library.card') or '/')
    book_limit = fields.Integer('No Of Book Limit On Card')
    left_limit = fields.Integer(compute="_compute_left_limit",method="True", string='剩余可借书籍')
    student_id = fields.Many2one('student.student', 'Student Name',ondelete="cascade")
    standard_id = fields.Many2one('school.standard', 'Standard')
    gt_name = fields.Char(compute="_compute_name", method=True, string='Name')
    user = fields.Selection([('student', 'Student'), ('teacher', 'Teacher')],
                            'User')
    roll_no = fields.Integer('Roll No')
    teacher_id = fields.Many2one('hr.employee', 'Teacher Name',ondelete="cascade")
    issue_ids = fields.One2many('library.book.issue','card_id',string='Name',domain=[('state', 'in', ['issue','reissue'])],ondelete='cascade')
    issue_ids_string = fields.Char(compute="_issue_ids_string", method=True,)





class LibraryBookIssue(models.Model):
    '''Book variant of product'''
    _name = "library.book.issue"
    _description = "Library information"
    _rec_name = "standard_id"

    @api.onchange('date_issue', 'day_to_return_book')
    def onchange_day_to_return_book(self):
        ''' This method calculate a book return date.
        @param self : Object Pointer
        @param cr : Database Cursor
        @param uid : Current Logged in User
        @param ids : Current Records
        @param name : Functional field's name
        @param args : Other arguments
        @param context : standard Dictionary
        @return : Dictionary having identifier of the record as key
                  and the book return date as value'''
        t = "%Y-%m-%d %H:%M:%S"
        rd = relativedelta(days=self.day_to_return_book or 0.0)
        if self.date_issue and rd:
            ret_date = datetime.strptime(self.date_issue, t) + rd
            self.date_return = ret_date

    @api.multi
    @api.depends('date_issue', 'day_to_return_book')
    def _compute_return_date(self):
        ''' This method calculate a book return date.
        @param self : Object Pointer
        @param cr : Database Cursor
        @param uid : Current Logged in User
        @param ids : Current Records
        @param name : Functional field's name
        @param args : Other arguments
        @param context : standard Dictionary
        @return : Dictionary having identifier of the record as key
                  and the book return date as value'''
        t = "%Y-%m-%d %H:%M:%S"
        for rec in self:
            rd = relativedelta(days=rec.day_to_return_book or 0.0)
            if rec.date_issue and rd:
                ret_date = datetime.strptime(rec.date_issue, t) + rd
                rec.date_return = ret_date

    @api.multi
    @api.depends('actual_return_date', 'day_to_return_book')
    def _compute_penalty(self):
        ''' This method calculate a penalty on book .
        @param self : Object Pointer
        @param cr : Database Cursor
        @param uid : Current Logged in User
        @param ids : Current Records
        @param name : Functional field's name
        @param args : Other arguments
        @param context : standard Dictionary
        @return : Dictionary having identifier of the record as key
                  and penalty as value
        '''
        for line in self:
            if line.date_return:
                start_day = datetime.strptime(line.actual_return_date,
                                              "%Y-%m-%d %H:%M:%S")
                end_day = datetime.strptime(line.date_return,
                                            "%Y-%m-%d %H:%M:%S")
                if start_day > end_day:
                    diff = relativedelta(start_day.date(), end_day.date())
                    day = float(diff.days) or 0.0
                    if line.day_to_return_book:
                        line.penalty = day * line.name.fine_late_return or 0.0

    @api.multi
    @api.depends('state')
    def _compute_lost_penalty(self):
        ''' This method calculate a penalty on book lost .
        @param self : Object Pointer
        @param cr : Database Cursor
        @param uid : Current Logged in User
        @param ids : Current Records
        @param name : Functional field's name
        @param args : Other arguments
        @param context : standard Dictionary
        @return : Dictionary having identifier of the record as key
                  and book lost penalty as value
        '''

        for rec in self:
            if rec.state and rec.state == 'lost':
                rec.lost_penalty = rec.name.fine_lost or 0.0

    @api.multi
    @api.constrains('card_id', 'state')
    def _check_issue_book_limit(self):
        ''' This method used how many book can issue as per user type  .
        @param self : Object Pointer
        @param cr : Database Cursor
        @param uid : Current Logged in User
        @param ids : Current Records
        @param context : standard Dictionary
        @return : True or False
        '''
        if self.env.context.get('type')=='issue_import':


            return True


        for rec in self:
            if rec.card_id and rec.card_id.type_book_limit and rec.card_id.type_book_limit!=0:
                card_ids = rec.search([('card_id', '=', rec.card_id.id),
                                       ('state', 'in', ['issue', 'reissue'])])
                if rec.state == 'issue' or rec.state == 'reissue':
                    if rec.card_id.type_book_limit > len(card_ids) - 1:
                        return True
                    else:
                        # Check the book issue limit on card if it is over it
                        # give warning
                        raise UserError(_('超过借书上限'))
                else:
                    if rec.card_id.type_book_limit > len(card_ids):
                        return True
                    else:
                        raise UserError(_('Book issue limit is over on\
                        this card'))

    name = fields.Many2one('product.product', 'Book Name', required=True,ondelete="cascade")
    issue_code = fields.Char('Issue No.', required=True,
                             default=lambda self:
                             self.env['ir.sequence'
                                      ].get('library.book.issue') or '/')
    student_id = fields.Many2one('student.student', 'Student Name')
    teacher_id = fields.Many2one('hr.employee', 'Teacher Name')
    gt_name = fields.Char('Name')
    standard_id = fields.Many2one('standard.standard', 'Standard')
    roll_no = fields.Integer('Roll No')
    invoice_id = fields.Many2one('account.invoice', "User's Invoice")
    date_issue = fields.Datetime('Release Date', required=True,
                                 help="Release(Issue) date of the book",
                                 default=lambda *a:
                                 time.strftime('%Y-%m-%d %H:%M:%S'))
    date_return = fields.Datetime(compute="_compute_return_date",
                                  string='Return Date',
                                  store=True,
                                  help="Book To Be Return On This Date")
    actual_return_date = fields.Datetime("Actual Return Date",
                                         help="Actual Return Date of Book",
                                         default=lambda *
                                         a: time.strftime('%Y-%m-%d %H:%M:%S'))
    penalty = fields.Float(compute="_compute_penalty",
                           string='Penalty', store=True,
                           help='It show the late book return penalty')
    lost_penalty = fields.Float(compute="_compute_lost_penalty",
                                string='Fine', store=True,
                                help='It show the penalty for lost book')
#    return_days = fields.Integer('Return Days')
    day_to_return_book = fields.Integer('Book Return Days')
    card_id = fields.Many2one("library.card", "Card No", required=True)
    state = fields.Selection([('draft', 'Draft'), ('issue', 'Issued'),
                              ('reissue', 'Reissued'), ('cancel', 'Cancelled'),
                              ('return', 'Returned'), ('lost', 'Lost'),
                              ('fine', 'Fined'),
                              ('paid', 'Done')],
                             "State", default='draft')
    user = fields.Char("User")
    compute_inv = fields.Integer('Number of invoice',
                                 compute="_compute_invoices")
    color = fields.Integer("Color Index")
    # school_id = fields.Many2one('school.school', 'School')


    @api.onchange('card_id')
    def onchange_card_issue(self):
        ''' This method automatically fill up values on card.
            @param self : Object Pointer
            @param cr : Database Cursor
            @param uid : Current Logged in User
            @param ids : Current Records
            @param card : applied change on this field
            @param context : standard Dictionary
            @return : Dictionary having identifier of the record as key
                      and the user info as value
        '''
        if self.card_id:
            self.user = str(self.card_id.user.title()) or ''
            if self.card_id.user.title() == 'Student':
                self.student_id = self.card_id.student_id.id or False
                self.standard_id = self.card_id.standard_id.id or False
                self.roll_no = int(self.card_id.roll_no) or False
                self.gt_name = self.card_id.gt_name or ''

            else:
                self.teacher_id = self.card_id.teacher_id.id
                self.gt_name = self.card_id.gt_name



    @api.model
    def create(self, vals):
        '''Override create method'''
        if vals.get('card_id') and vals.get('user') == 'Student':
            # fetch the record of user type student
            card = self.env['library.card'].browse(vals.get('card_id'))
            vals.update({'student_id': card.student_id.id,
                         'standard_id': card.standard_id.id,
                         'roll_no': int(card.roll_no),
                         'gt_name': card.gt_name
                         })
        if vals.get('card_id') and vals.get('user') == 'Teacher':
            # fetch the record of user type teacher
            card = self.env['library.card'].browse(vals.get('card_id'))
            vals.update({'teacher_id': card.teacher_id.id,
                         'gt_name': card.gt_name
                         })
        return super(LibraryBookIssue, self).create(vals)

    @api.multi
    def write(self, vals):
        '''Override write method'''
        if vals.get('card_id') and vals.get('user') == 'Student':
            # update the details of user type student
            card = self.env['library.card'].browse(vals.get('card_id'))
            vals.update({'student_id': card.student_id.id,
                         'standard_id': card.standard_id.id,
                         'roll_no': int(card.roll_no),
                         'gt_name': card.gt_name
                         })
        if vals.get('card_id') and vals.get('user') == 'Teacher':
            # upate the details of user type Teacher
            card = self.env['library.card'].browse(vals.get('card_id'))
            vals.update({'teacher_id': card.teacher_id.id,
                         'gt_name': card.gt_name
                         })
        return super(LibraryBookIssue, self).write(vals)

    @api.multi
    def draft_book(self):
        '''
        This method for books in draft state.
        @param self : Object Pointer
        @param cr : Database Cursor
        @param uid : Current Logged in User
        @param ids : Current Records
        @param context : standard Dictionary
        @return : True
        '''
        for rec in self:
            rec.write({'state': 'draft'})
        return True

    @api.model
    def createBatchReissue(self,vals):

        reissue_ids=[]
        for book_issue in vals.get('book_ids'):
            if 'id' in book_issue:
                ones = self.env['library.book.issue'].search([('name','=',book_issue['id']),('state','in',['issue','reissue'])])
                if ones:
                    reissue_ids.push(ones[0])
                else:
                    raise ValidationError(_('This Book is not available!'
                                            '\nPlease try after sometime !'))

        self.browse(reissue_ids).reissue_book()

        # for rec in self:
        #     rec.state = 'reissue'
        #     rec.write({'date_issue': time.strftime('%Y-%m-%d %H:%M:%S')})
        #return True


    @api.model
    def createBatch(self, vals):
        ''' This method is Create new student
        @param self : Object Pointer
        @param cr : Database Cursor
        @param uid : Current Logged in User
        @param vals : dict of new values to be set
        @param context : standard Dictionary
        @return :ID of newly created record.
        '''
        _logger.warn(vals)
        for book_issue in vals.get('book_ids'):
            book_to_issue=dict()
            if book_issue.get('issue_code', 'New') == 'New':
                seq_obj = self.env['ir.sequence']
                book_to_issue['issue_code'] = seq_obj.next_by_code('library.book.issue')

            if 'id' in book_issue:

                #sql3 = "select availability from product_product where id=%s" % (book_issue['id'])
                product = self.env['product.product'].browse(book_issue['id'])
                # _logger.warn(sql3)
                # self.env.cr.execute(sql3)
                # book_availability = self.env.cr.fetchone()

                _logger.warn(product.availability)
                if product.availability=='available':
                    book_to_issue['name'] = book_issue['id']
                else:
                    raise ValidationError(_('This Book is not available!'
                                            '\nPlease try after sometime !'))
            else:
                raise ValidationError(_('This Book is not available!'
                                        '\nPlease try after sometime !'))
            if vals.get("client"):
                cart_id=vals.get("client")['card_id'][0]
                book_to_issue['card_id']=cart_id
                issue_str = ''
                sql = "select * from library_book_issue where card_id=%s and state='fine'" % (cart_id)
                _logger.warn(sql)
                self.env.cr.execute(sql)
                book_fines = self.env.cr.fetchall()

                if book_fines:
                    for book in book_fines:
                        issue_str += str(book.issue_code) + ', '
                        # check if fine on book is paid until then user
                        # cannot issue new book
                    raise UserError(_('You can not request for a book until'
                                      ' the fine is not paid for book issues'
                                      ' %s!') % issue_str)

                sql2 = "select * from library_book_issue where card_id=%s and state in ('issue','reissue')" % (cart_id)
                _logger.warn(sql2)
                self.env.cr.execute(sql2)
                issue_ids = self.env.cr.fetchall()

                card=self.env['library.card'].sudo().browse(cart_id)

                _logger.warn(card.book_limit)
                _logger.warn(len(issue_ids))

                #card = self.env['library.card'].sudo().browse(cart_id)
                if card.type_book_limit and card.type_book_limit > len(issue_ids):
                    newissue = self.env['library.book.issue'].sudo().create(book_to_issue)
                    return_day = card.type_day_limit
                    newissue.write({'state': 'issue',
                                    'day_to_return_book': return_day})
                    newissue.name.write({
                        'quantity': 0
                    })
                else:
                    raise UserError("超过借书上限")

                #self.env['library.book.issue'].sudo().create(book_to_issue)
                #县取消

        return True

    @api.multi
    def issue_book(self):
        '''
        This method used for issue a books.
        @param self : Object Pointer
        @param cr : Database Cursor
        @param uid : Current Logged in User
        @param ids : Current Records
        @param context : standard Dictionary
        @return : True
        '''
        for rec in self:
            if rec.name and rec.name.availability == 'notavailable':
                raise ValidationError(_('This Book is not available!'
                                        '\nPlease try after sometime !'))
            if rec.student_id:
                issue_str = ''
                book_fines = rec.search([('card_id', '=', rec.card_id.id),
                                         ('state', '=', 'fine')])
                if book_fines:
                    for book in book_fines:
                        issue_str += str(book.issue_code) + ', '
                        # check if fine on book is paid until then user
                        # cannot issue new book
                    raise UserError(_('You can not request for a book until'
                                      ' the fine is not paid for book issues'
                                      ' %s!') % issue_str)
            if rec.card_id:
                card_ids = rec.search([('card_id', '=', rec.card_id.id),
                                       ('state', 'in', ['issue', 'reissue'])])
                #if rec.card_id.book_limit > len(card_ids):
                if  rec.card_id.type_book_limit and rec.card_id.type_book_limit > len(card_ids):
                    return_day = rec.card_id.day_limit
                    rec.write({'state': 'issue',
                               'day_to_return_book': return_day})
                    rec.name.write({
                        'quantity':0
                    })
            return True

    @api.multi
    def reissue_book(self):
        '''
        This method used for reissue a books.
        @param self : Object Pointer
        @param cr : Database Cursor
        @param uid : Current Logged in User
        @param ids : Current Records
        @param context : standard Dictionary
        @return : True
        '''
        for rec in self:
            rec.state = 'reissue'
            rec.write({'date_issue': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True

    @api.model
    def returnBatch(self, vals):

        if vals.get("book_ids"):
            books_string = ''
            for book in vals.get("book_ids"):
                books_string+=str(book['id'])+','

            sql="update library_book_issue set state='return' where name in("+books_string[:-1]+")"
            _logger.info(sql)
            self.env.cr.execute(sql)
            return True
        else:
            raise UserError("书籍为空")

    @api.multi
    def return_book(self):
        '''
        This method used for return a books.
        @param self : Object Pointer
        @param cr : Database Cursor
        @param uid : Current Logged in User
        @param ids : Current Records
        @param context : standard Dictionary
        @return : True
        '''
        for rec in self:
            rec.write({'state': 'return'})
            rec.name.write({
                'quantity': 1
            })
        return True

    @api.multi
    def lost_book(self):
        stock_scrap_obj = self.env['stock.scrap']
        for rec in self:
            scrap_fields = list(stock_scrap_obj._fields)
            scrap_vals = stock_scrap_obj.default_get(scrap_fields)
            origin_str = 'Book lost : '
            if rec.issue_code:
                origin_str += rec.issue_code
            if rec.student_id:
                origin_str += "(" + rec.student_id.name + ")" or ''
            scrap_vals.update({'product_id': rec.name.id,
                               'product_uom_id': rec.name.uom_id.id,
                               'origin': origin_str})
            stock_scrap_obj.with_context({'book_lost': True}
                                         ).create(scrap_vals)
            rec.state = 'lost'
            rec.lost_penalty = self.name.fine_lost
        return True

    @api.multi
    def cancel_book(self):
        '''
        This method used for cancel book issue.
        @param self : Object Pointer
        @param cr : Database Cursor
        @param uid : Current Logged in User
        @param ids : Current Records
        @param context : standard Dictionary
        @return : True
        '''
        for rec in self:
            rec.write({'state': 'cancel'})
        return True

    @api.multi
    def user_fine(self):
        '''
        This method used when penalty on book either late return or book lost
        and generate invoice of fine.
        @param self : Object Pointer
        @param cr : Database Cursor
        @param uid : Current Logged in User
        @param ids : Current Records
        @param context : standard Dictionary
        @return : new form of account.invoice
        '''
#
        invoice_obj = self.env['account.invoice']
        for record in self:
            if record.user == 'Student':
                usr = record.student_id.partner_id.id
                if not record.student_id.partner_id.contact_address:
                    raise UserError(_('Error !'
                                    'The Student must have a Home address.'))
            else:
                usr = record.teacher_id.id
                if not record.teacher_id.address_home_id:
                    raise UserError(_('Error ! Teacher must have a Home'
                                      'address.'))
            vals_invoice = {'type': 'out_invoice',
                            'partner_id': usr,
                            'book_issue': record.id,
                            'book_issue_reference': record.issue_code or ''}
            new_invoice_id = invoice_obj.create(vals_invoice)
            acc_id = new_invoice_id.journal_id.default_credit_account_id.id
            invoice_line_ids = []
            if record.lost_penalty:
                lost_pen = record.lost_penalty
                invoice_line2 = {'name': 'Book Lost Fine',
                                 'price_unit': lost_pen,
                                 'invoice_id': new_invoice_id.id,
                                 'account_id': acc_id}
                invoice_line_ids.append((0, 0, invoice_line2))
            if record.penalty:
                pen = record.penalty
                invoice_line1 = {'name': 'Late Return Penalty',
                                 'price_unit': pen,
                                 'invoice_id': new_invoice_id.id,
                                 'account_id': acc_id}
                invoice_line_ids.append((0, 0, invoice_line1))
            new_invoice_id.write({'invoice_line_ids': invoice_line_ids})
        self.write({'state': 'fine'})
        view_id = self.env.ref('account.invoice_form')
        return {'name': _("New Invoice"),
                'view_mode': 'form',
                'view_id': view_id.ids,
                'view_type': 'form',
                'res_model': 'account.invoice',
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'res_id': new_invoice_id.id,
                'target': 'current',
                'context': {'default_type': 'out_invoice'}}

    @api.multi
    def view_invoice(self):
        '''this method is use for the view invoice of penalty'''
        invoice_obj = self.env['account.invoice']
        for rec in self:
            invoices = invoice_obj.search([('book_issue', '=', rec.id)])
            action = self.env.ref('account.action_invoice_tree1').read()[0]
            if len(invoices) > 1:
                action['domain'] = [('id', 'in', invoices.ids)]
            elif len(invoices) == 1:
                action['views'] = [(self.env.ref('account.invoice_form').id,
                                    'form')]
                action['res_id'] = invoices.ids[0]
            else:
                action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.multi
    def _compute_invoices(self):
        inv_obj = self.env['account.invoice']
        for rec in self:
            count_invoice = inv_obj.search_count([('book_issue', '=', rec.id)
                                                  ])
            rec.compute_inv = count_invoice


class LibraryBookRequest(models.Model):
    '''Request for Book'''
    _name = "library.book.request"
    _rec_name = 'req_id'

    @api.multi
    @api.depends('type')
    def _compute_bname(self):
        if self.type:
            if self.type == 'existing':
                book = self.name.name
            else:
                book = self.new_book
            self.bk_nm = book

    req_id = fields.Char('Request ID', readonly=True, default='New')
    card_id = fields.Many2one("library.card", "Card No", required=True)
    type = fields.Selection([('existing', 'Existing'), ('new', 'New')],
                            'Book Type', default="existing")
    name = fields.Many2one('product.product', 'Book Name')
    new_book = fields.Char('Book Name')
    bk_nm = fields.Char('Name', compute="_compute_bname", store=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('cancel', 'Cancelled'),
                              ], "State", default='draft')
    book_return_days = fields.Integer(related='name.day_to_return_book',
                                      string="Return Days")
    active = fields.Boolean(default=True, help='''Set active to false to hide
    the category without removing it.''')

    @api.model
    def create(self, vals):
        res = super(LibraryBookRequest, self).create(vals)
        if res.req_id == 'New':
            seq_obj = self.env['ir.sequence']
            res.write({'req_id': (seq_obj.next_by_code('library.book.request'
                                                       ) or 'New')})
        return res

    @api.multi
    def draft_book_request(self):
        for book in self:
            book.state = 'draft'

    @api.multi
    def confirm_book_request(self):
        '''Method to confirm book request'''
        book_issue_obj = self.env['library.book.issue']
        for rec in self:
            vals = {'card_id': rec.card_id.id,
                    'type': rec.type,
                    'name': rec.name.id}
            issue_id = book_issue_obj.create(vals)
            # changes state to confirm
            rec.state = 'confirm'
            if issue_id:
                issue_id.onchange_card_issue()
                return {'name': ('Book Issue'),
                        'view_mode': 'form',
                        'view_type': 'form',
                        'res_id': issue_id.id,
                        'res_model': 'library.book.issue',
                        'type': 'ir.actions.act_window',
                        'target': 'current'}

    @api.multi
    def cancle_book_request(self):
        for book in self:
            book.state = 'cancel'
