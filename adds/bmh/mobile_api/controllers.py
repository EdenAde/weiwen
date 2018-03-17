# -*- coding: utf-8 -*-
##############################################################################
#
#    Diogo Carvalho Duarte
#    Copyright (C) 2004-2024 Diogo Duarte (<http://diogocduarte.github.io/>).
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
from odoo import http
from odoo.http import request
import werkzeug.utils
# from odoo.addons.mobile.controllers import login_redirect
# from odoo.addons.website.models.website import slug
from odoo.osv.orm import browse_record
import sys
import time
from odoo.addons.web.controllers.main import binary_content
from odoo import http, modules, SUPERUSER_ID, tools, _
import base64
import logging
from odoo import _, api, fields, models
_logger=logging.getLogger(__name__)


class QueryURL(object):
    def __init__(self, path='', path_args=None, **args):
        self.path = path
        self.args = args
        self.path_args = set(path_args or [])

    def __call__(self, path=None, path_args=None, **kw):
        path = path or self.path
        for k, v in self.args.items():
            kw.setdefault(k, v)
        path_args = set(path_args or []).union(self.path_args)
        #print kw.items()
        paths, fragments = [], []
        for key, value in kw.items()[::-1]:
            if value and key in path_args:
                if isinstance(value, browse_record):
                    paths.append((key, slug(value)))
                else:
                    paths.append((key, value))
            elif value:
                if isinstance(value, list) or isinstance(value, set):
                    fragments.append(werkzeug.url_encode([(key, item) for item in value]))
                else:
                    fragments.append(werkzeug.url_encode([(key, value)]))

        for key, value in paths:
            path += '/' + key + '/%s' % value
        if fragments:
            path += '?' + '&'.join(fragments)
        return path


MODULE_BASE_PATH = '/api/'
import json



class BmhController(http.Controller):
    # @http.route('/homedata', type='http', auth="public", methods=['GET'], website=True)
    # def bpmProcess(self,tem_id,userId):
    #
    #     #if(tem_id==24||userId)


    @http.route('/homedata', type='http', auth="public", methods=['GET'], website=True)
    def homeDate(self,uid, **kwargs):

        location={"lan":'',"long":''}


        res={}
        res["location"]=location
        return json.dumps(res)

    @http.route('/api/survey', type='http', auth="public", methods=['GET'], website=True)
    def survey(self):
        surveys=request.env['survey.survey'].sudo().search([])

        surs = []
        for survey in surveys:
            surv = {'id':survey.id,'name':survey.name,'stage_id':survey.stage_id}
        return

    @http.route('/api/applies/<int:eid>/<int:type>', type='http', auth="public", methods=['GET'], website=True)
    def myApply(self, eid,type):

        res_json={
            "process":[
                {
                    "id":129,
                    "name":"请假",
                    "type":"holiday"
                },
                {
                    "id": 131,
                    "name": "出差",
                    "type": "bt"
                },
                {
                    "id": 132,
                    "name": "费用",
                    "type": "expense"
                },
                {
                    "id": 133,
                    "name": "预付",
                    "type": "advance"
                }
            ],
            'pageNo':1,
            'list':[]


        }
        res_json_array = []
        if type==129:
            my_holidays = request.env['hr.holidays'].sudo().search([('employee_id','=',eid)])
            for holiday in my_holidays:
                holidaydic={"id":holiday.id,"name":holiday.display_name,"create_time":holiday.create_date,'status':holiday.state,"user":holiday.employee_id.name}
                res_json_array.append(holidaydic)
        if type == 131:
            my_travels = request.env['tms.travel'].sudo().search([('employee_id', '=', eid)])
            for travel in my_travels:
                traveldic = {"id":travel.id,"name": travel.display_name+travel.route_id.name, "create_time": travel.date, 'status': travel.state,"user":travel.employee_id.name}
                res_json_array.append(traveldic)
        if type == 132:
            my_expenses = request.env['hr.expense'].sudo().search([('employee_id', '=', eid)])
            for expense in my_expenses:
                expensedic = {"id":expense.id,"name": expense.display_name, "create_time": expense.create_date, 'status': expense.state,"user":expense.employee_id.name}
                res_json_array.append(expensedic)

        if type == 133:
            tmss = request.env['tms.advance'].sudo().search([('employee_id', '=', eid)])
            for tms in tmss:
                tmsdic = {"id":tms.id,"name": tms.display_name, "create_time": tms.create_date, 'status': tms.state,"user":tms.employee_id.name}
                res_json_array.append(tmsdic)

        res_json['list']=res_json_array

        return json.dumps(res_json)

    @http.route('/api/submit/bmhFuelMileCreate', type='http', auth="public", methods=['POST'], website=True)
    def bmhSubmitFuelMileCreate(self, **post):

        rec = request.env['tms.travel'].browse(post.get('tid'))
        # rec.validate_driver_license()
        # rec.validate_vehicle_insurance()

        newevent = {
            "name":u"里程表留存",
            "date":post.get("date"),
            "travel_id":post.get("tid"),
            "position_pi":post.get("location"),
            "state":'draft'
        }
        newe = request.env['travel.event'].create(newevent)

        data_attach = {
            'name': u"里程表留存",
            'datas': post.get("image"),
            'datas_fname': u"里程表留存",
            'res_model': 'travel.event',
            'res_id': newe.id,
        }

        request.env['ir.attchment'].create(data_attach)


        return json.dumps({'code':'success'})


        # travels = rec.search(
        #     [('state', '=', 'progress'), '|',
        #      ('employee_id', '=', rec.employee_id.id),
        #      ('travel_id', '=', post.get('tid'))])
        # if len(travels) >= 1:
        #     return json.dumps({})
        #     # raise ValidationError(
        #     #     _('The unit or driver are already in use!'))
        # rec.state = "progress"
        # rec.date_start_real = fields.Datetime.now()
        # rec.message_post('Travel Dispatched')

    @http.route('/api/bmhFuelMileCreate', type='http', auth="public", methods=['GET'], website=True)
    def bmhFuelMileCreate(self, eid):
        employee = request.env['hr.employee'].sudo().browse(int(eid))
        res_trival = {
            "name": "油补申请单",
            "code": "ybsqd",
            "listctrlVoList": [],
            "content": []
        }
        trival_user = {
            "title": "申请人",
            "content": employee.user_id.id,
            "name": "user_id",
            "type": "macros",
            "detailType": "sys_realname",
            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": False,
            "hide": True,
            "fileName": ""
        }
        car_dic = {
            "title": "车辆",
            "content": "年假",
            "name": "car",
            "type": "select",
            "items": [
            ],
            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": True,
            "hide": False,
            "fileName": ""
        }
        trival_start_mile = {
            "title": "最新里程数值",
            "content": "",
            "name": "start",
            "type": "text",
            "detailType": "text",
            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": False,
            "hide": False,
            "fileName": ""
        }
        trival_start = {
            "title": "时间",
            "content": "",
            "name": "date",
            "type": "macros",
            "detailType": "sys_time",
            "maxLength": "",
            "minlength": "",
            "readOnly": True,
            "required": True,
            "hide": False,
            "fileName": ""
        }
        place = {
            "title": "地点",
            "content": "",
            "name": "location",
            "type": "macros",
            "detailType": "sys_location",
            "maxLength": "",
            "minlength": "",
            "readOnly": True,
            "required": False,
            "hide": False,
            "fileName": ""
        }

        pic = {
            "title": "里程表留存",
            "content": "",
            "name": "image",
            "type": "text",
            "detailType": "camera",
            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": True,
            "hide": False,
            "fileName": ""
        }

        holidays_dic = {
            "title": "出差单号",
            "content": "年假",
            "name": "tid",
            "type": "select",
            "items": [
            ],
            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": True,
            "hide": False,
            "fileName": ""
        }

        if eid:

            travels = request.env['tms.travel'].sudo().search([])
            cars = request.env['fleet.vehicle'].sudo().search([])
            trival_user['content'] = employee.department_id.name + "-" + employee.name
            for car in cars:
                car_dic['items'].append({'label':car.name,"value":car.id})
            for travel in travels:
                holidays_dic['items'].append({'label':travel.name,"value":travel.id})
            cts = [trival_user,car_dic, trival_start, holidays_dic,place,trival_start_mile,pic]
            res_trival['content'] = cts
            return json.dumps(res_trival)


    @http.route('/api/bmhHolidaysCreate', type='http', auth="public", methods=['GET'], website=True)
    def bmhHolidaysCreate(self, eid):
        res_trival = {
            "name": "请休假申请单",
            "code": "qxjsqd",
            "listctrlVoList": [],
            "content": []
        }
        trival_user = {
            "title": "申请人",
            "content": eid,
            "name": "employee_id",
            "type": "text",
            "detailType": "text",
            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": False,
            "hide": True,
            "fileName": ""
        }
        trival_start = {
            "title": "开始时间",
            "content": "",
            "name": "date_from",
            "type": "text",
            "detailType": "fullDate",
            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": True,
            "hide": False,
            "fileName": ""
        }
        trival_end = {
            "title": "结束时间",
            "content": "",
            "name": "date_to",
            "type": "text",
            "detailType": "fullDate",
            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": True,
            "hide": False,
            "fileName": ""
        }
        holidays_dic={
            "title": "假期类别",
            "content": "年假",
            "name": "holiday_status_id",
            "type": "select",
            "items": [
            ],
            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": True,
            "hide": False,
            "fileName": ""
        }
        holidays_name = {
            "title": "说明",
            "content": "请假说明",
            "name": "name",
            "type": "textarea",

            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": False,
            "hide": False,
            "fileName": ""
        }

        if eid:
            employee = request.env['hr.employee'].sudo().browse(int(eid))
            holidays = request.env['hr.holidays.status'].sudo().search([])
            trival_user['content'] = employee.department_id.name + "-" + employee.name

            for holiday in holidays:
                holidays_dic['items'].append({"label":holiday.name,"value":holiday.id})
            cts = [trival_user, trival_start, trival_end, holidays_dic,holidays_name]
            res_trival['content'] = cts
            return json.dumps(res_trival)

    @http.route('/api/bmhexpenseCreate', type='http', auth="public", methods=['GET'], website=True)
    def bmhexpenseCreate(self, eid):

        expense_dic = {
            "name": "费用申请",
            "code": "ccsqd",
            "listctrlVoList": [],
            "content": []
        }
        expense_user = {
            "title": "申请人",
            "content": "李四",
            "name": "sqr",
            "type": "macros",
            "detailType": "sys_realname",
            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": False,
            "hide": False,
            "fileName": ""
        }
        expense_products = {
            "title": "费用产品",
            "content": "",
            "name": "product_id",
            "type": "select",
            "detailType": "fullDate",
            "items": [],
            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": True,
            "hide": False,
            "fileName": ""
        }
        expense_product_num = {
            "title": "产品数量",
            "content": "",
            "name": "quantity",
            "type": "text",
            "detailType": "int",
            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": True,
            "hide": False,
            "fileName": ""
        }
        expense_name = {
            "title": "费用说明",
            "content": "",
            "name": "name",
            "type": "textarea",
            "detailType": "fullDate",
            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": True,
            "hide": False,
            "fileName": ""
        }

        expense_analytic_account = {
            "title": "记账项",
            "content": "",
            "name": "analytic_account_id",
            "type": "select",
            "items": [],
            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": True,
            "hide": False,
            "fileName": ""
        }

        expense_pay_account = {
            "title": "付款人",
            "content": "",
            "name": "payment_mode",
            "type": "radios",
            "detailType":"",
            "items": [{"label":"员工","value":"own_account"},{"label":"公司","value":"company_account"}],
            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": True,
            "hide": False,
            "fileName": ""
        }

        # expense_pay_account = {
        #     "title": "付款人",
        #     "content": "",
        #     "name": "unit_amount",
        #     "type": "text",
        #     "detailType": "plus",
        #     "items": [{"label": "员工", "value": "own_account"}, {"label": "公司", "value": "company_account"}],
        #     "maxLength": "",
        #     "minlength": "",
        #     "readOnly": False,
        #     "required": True,
        #     "hide": True,
        #     "fileName": ""
        # }


        if eid:
            employee = request.env['hr.employee'].sudo().browse(int(eid))
            employee_id_input = {
                "title": "付款人",
                "content": employee.id,
                "name": "employee_id",
                "type": "text",
                "detailType": "int",
                "maxLength": "",
                "minlength": "",
                "readOnly": False,
                "required": True,
                "hide": True,
                "fileName": ""
            }
            company_id = employee.user_id.company_id.id
            analytics = request.env['account.analytic.account'].sudo().search([("company_id", '=', company_id)])
            products = request.env['product.product'].sudo().search([('can_be_expensed','=',1),('company_id','=',company_id)])
            if True:

                expense_user['content'] = employee.department_id.name + "-" + employee.name
                for product in products:
                    expense_products['items'].append({"label":product.name+"/¥"+str(product.list_price),"value":product.id})
                for pro in analytics:
                    expense_analytic_account['items'].append({"label":pro.name,"value":pro.id})
                cts = [employee_id_input,expense_user,expense_products,expense_product_num,expense_pay_account,expense_analytic_account,expense_name]
                expense_dic['content'] = cts
                return json.dumps(expense_dic)
        return json.dumps(expense_dic)


    @http.route('/api/bmhTrivalCreate', type='http', auth="public", methods=['GET'], website=True)
    def bmhTrivalCreate(self, eid):


        res_trival={
            "name": "出差申请单",
            "code": "ccsqd",
            "listctrlVoList": [],
            "content": []
        }
        trival_user={
            "title": "申请人",
            "content": "李四",
            "name": "sqr",
            "type": "macros",
            "detailType": "sys_realname",
            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": False,
            "hide": False,
            "fileName": ""
        }
        trival_start={
            "title": "开始时间",
            "content": "",
            "name": "kssj",
            "type": "text",
            "detailType": "fullDate",
            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": True,
            "hide": False,
            "fileName": ""
        }
        trival_end = {
            "title": "结束时间",
            "content": "",
            "name": "jssj",
            "type": "text",
            "detailType": "fullDate",
            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": True,
            "hide": False,
            "fileName": ""
        }



        projects_dic ={
            "title": "项目",
            "content": "项目",
            "name": "jqlb",
            "type": "select",
            "items": [],
            "maxLength": "",
            "minlength": "",
            "readOnly": False,
            "required": True,
            "hide": False,
            "fileName": ""
        }

        if eid:
            employee = request.env['hr.employee'].sudo().browse(int(eid))
            projects = request.env['project.project'].sudo().search([("members",'child_of',int(employee.user_id))])
            if True:

                trival_user['content'] = employee.department_id.name+"-"+employee.name

                for pro in projects:
                    projects_dic['items'].append(pro.name)
                cts = [trival_user,trival_start,trival_end,projects_dic]
                res_trival['content']=cts
                return json.dumps(res_trival)
        return json.dumps(res_trival)

    @http.route('/news', type='http', auth="public", methods=['GET'], website=True)
    def homeDate(self, uid, **kwargs):

        posts = self._env['blog.news'].search([('blog_id','=',1)], order='create_time ASC')

        return posts



    @http.route('/issues/task/<model("project.task"):task>', type='http', auth="public", methods=['GET'],website=True)
    def issuesGet(self,task, **kwargs):
        cr, uid, session = request.cr, request.uid, request.session
        return http.request.render('mobile_sample.issues', {
            'root': MODULE_BASE_PATH,
            'db': session.db,
            'task':task,
        })

    @http.route('/issue/add', type='http', methods=['POST'], auth="public",csrf=False)
    def issuesPost(self,name,description,task_id, status,priority,images,**kwargs):
        cr, uid, session = request.cr, request.uid, request.session

        obj={}
        issue_id=request.registry['project.issue'].create(request.cr, SUPERUSER_ID, {
                    'name': name,
                    'priority':priority,
                    'description': description,
                    'task_id': task_id,
                    'state':status,
                }, context=request.context)

        Model = request.session.model('ir.attachment')
        model="project.issue"

        #print 'request.images'
        #print json.loads(images)

        if images:
            for file in json.loads(images):
                fname='%s.jpg' % int(time.time())
                #print fname
                #print issue_id
                start=file.find(',')
                img= file[start+1:];
                img.replace(' ','+')
                # image = Image.open(cStringIO.StringIO(file))
                # image_data = image_save_for_web(image)
                attachment_id = Model.create({
                        'name': fname,
                        'datas': img,
                        'datas_fname': fname,
                        'res_model': model,
                        'res_id': issue_id,
                    })
                #print attachment_id

        obj['issue_id']=issue_id
        obj['status']='ok'
        #uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
        return json.dumps(obj)
        # return http.request.render('mobile_sample.issues', {
        #     'root': MODULE_BASE_PATH,
        #     'db': session.db,
        #     'task':task,
        # })


    @http.route(MODULE_BASE_PATH + 'contacts/<int:id>', type='http', auth="user")
    def getcustomer(self, id, **kwargs):
        cr, uid, session = request.cr, request.uid, request.session

        partners = request.registry.get("res.partner")
        ids = partners.search(cr, uid, [('id', '=', id)])
        obj = partners.browse(cr, uid, ids)
        return http.request.render('mobile_sample.customer', {
            'root': MODULE_BASE_PATH,
            'db': session.db,
            'customer': obj[0]
        })


    @http.route('/issue/add', type='http', methods=['GET'], auth="public",website=True)
    def addissue(self, **kwargs):
        cr, uid, session = request.cr, request.uid, request.session
        # task_id = request.params.get('task')
        # task =  request.registry['project.task'].browse(request.cr, SUPERUSER_ID,task_id)
        # if not session.uid:
        #     return login_redirect(MODULE_BASE_PATH)
        # return env.get_template("index.html").render({
        #     'debug': request.debug,
        # })
        return ''

    @http.route(['/forum/user/<int:user_id>/avatar'], type='http', auth="public", website=True)
    def user_avatar(self, user_id=0, **post):
        status, headers, content = binary_content(model='res.users', id=user_id, field='image_medium',
                                                  default_mimetype='image/png', env=request.env(user=SUPERUSER_ID))

        if not content:
            img_path = modules.get_module_resource('web', 'static/src/img', 'placeholder.png')
            with open(img_path, 'rb') as f:
                image = f.read()
            content = image.encode('base64')
        if status == 304:
            return werkzeug.wrappers.Response(status=304)
        image_base64 = base64.b64decode(content)
        headers.append(('Content-Length', len(image_base64)))
        response = request.make_response(image_base64, headers)
        response.status = str(status)
        return response



    @http.route('/issue/detail', type='http', methods=['GET'], auth="public",website=True)
    def issueDetail(self,issue_id, **kwargs):
        cr, uid, session = request.cr, request.uid, request.session
        # task_id = request.params.get('task')
        # task =  request.registry['project.task'].browse(request.cr, SUPERUSER_ID,task_id)
        #print session
        # if not session.uid:
        #     return login_redirect(MODULE_BASE_PATH)
        # return env.get_template("index.html").render({
        #     'debug': request.debug,
        #     'issue_id':issue_id
        # })


    @http.route('/issue', type='http', methods=['GET'], auth="public",website=True)
    def issueDetailJason(self,issue_id, **kwargs):
        cr, uid, session = request.cr, request.uid, request.session
        # task_id = request.params.get('task')
        # task =  request.registry['project.task'].browse(request.cr, SUPERUSER_ID,task_id)
        #print session
        # if not session.uid:
        #     return login_redirect(MODULE_BASE_PATH)

        issue=request.env()['project.issue'].sudo().search([('id','=',issue_id)])
        obj={}
        imgs=[]
        if issue.images:
            for img in issue.images:
                newimg = img.datas.replace('+',' ')
                imgs.append('data:image/png;base64,'+newimg)

        obj['name']=issue.name
        obj['description']=issue.description
        obj['status']=issue.state
        obj['priority']=issue.priority
        obj['images']=imgs

        return json.dumps(obj)
