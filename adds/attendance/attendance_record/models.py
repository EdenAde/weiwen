# -*- coding: utf-8 -*-
from datetime import *
from openerp import models, fields, api

class CheckInOutRecord(models.Model):
    _name = 'attendance_record.check_in_out_record'
    _order = 'create_date desc'
    
    create_uid = fields.Many2one('res.users',string=u"人员", readonly=True)
    create_date = fields.Datetime(string=u"时间", readonly=True)
    name = fields.Char(string=u"设备标识", readonly=True, required=True)
    longitude = fields.Float(string=u"经度", readonly=True, required=True)
    latitude = fields.Float(string=u"纬度", readonly=True, required=True)
    position_address = fields.Char(string=u"位置地址", readonly=True)    
    position_tpye = fields.Selection([
         ('gps', u"GPS"),
         ('non-gps', u"非GPS"),
    ], string=u"定位类型", readonly=True)
    check_in_out = fields.Selection([
         ('checkin', u"签到"),
         ('checkout', u"签退"),
    ], string=u"打卡类型", readonly=True)
    
class PhotoRecord(models.Model):
    _name = 'attendance_record.photo_record'
    _order = 'create_date desc'
    
    create_uid = fields.Many2one('res.users',string=u"人员", readonly=True)
    create_date = fields.Datetime(string=u"时间", readonly=True)
    name = fields.Char(string=u"设备标识", readonly=True, required=True)
    longitude = fields.Float(string=u"经度", readonly=True, required=True)
    latitude = fields.Float(string=u"纬度", readonly=True, required=True)
    position_address = fields.Char(string=u"位置地址", readonly=True)    
    position_tpye = fields.Selection([
         ('gps', u"GPS"),
         ('non-gps', u"非GPS"),
    ], string=u"定位类型", readonly=True)
    photo_updated=fields.Binary(u'相片',copy=False, readonly=True)
    
class AttendanceSeries(models.Model):
    _name = 'attendance_record.attendance_series'
    
    name = fields.Char(string=u"班次名称", required=True)
    item_ids = fields.One2many('attendance_record.attendance_series_item', 'attendance_series_id', string=u"班次明细")

class AttendanceSeriesItem(models.Model):
    _name = 'attendance_record.attendance_series_item'
    
    name = fields.Char(string=u"班次明细名称", required=True)
    displayorder = fields.Integer(string=u"顺序", required=True)
    min_before_from = fields.Integer(string=u"签到提前分钟数", required=True)
    hour_from = fields.Float(string=u"签到时间", required=True, select=True)
    min_after_from = fields.Integer(string=u"签到迟到分钟数", required=True)
    hour_to = fields.Float(string=u"签退时间", required=True)
    min_after_to = fields.Integer(string=u"签退允许分钟数", required=True)
    calc_overtime = fields.Selection([
         ('notcalc', u"不计算"),
         ('calc', u"计算"),
    ], string=u"计算加班时间", required=True)
    attendance_series_id = fields.Many2one('attendance_record.attendance_series', string=u"班次")

class HumanAttendanceSeries(models.Model):
    _name = 'attendance_record.human_attendance_series'
    
    human = fields.Many2one('res.users',string=u"人员", required=True)
    displayorder = fields.Integer(string=u"在考勤表上的顺序", required=True)   
    attendance_series_id = fields.Many2one('attendance_record.attendance_series', string=u"班次", required=True)

class HumanAttendanceTable(models.Model):
    _name = 'attendance_record.human_attendance_table'
    
    name = fields.Char(string=u"考勤表名称", required=True)
    start_date = fields.Date(string=u"开始日期", required=True)
    end_date = fields.Date(string=u"结束日期", required=True)
    item_ids = fields.One2many('attendance_record.hat_item', 'attendance_table_id', string=u"考勤表明细")

    #计算考勤表明细
    @api.one
    def action_generate_attendance_detail(self):
        #清空旧数据
        self.item_ids.unlink()
        
        #获取人员班次表数据
        human_attendance_series=self.env['attendance_record.human_attendance_series'].search([])
        
        #时区转换
        td=timedelta(0, 0, 0, 0, 0, 8, 0)
        
        #循环所有日期
        print 'end_date:'+self.end_date
        print 'start_date:'+self.start_date
        ed=datetime.strptime(self.end_date,'%Y-%m-%d')
        sd=datetime.strptime(self.start_date,'%Y-%m-%d')
        for i in range((ed - sd).days+1):  
            curday = sd + timedelta(days=i)
            print 'curday:'+str(curday)
            #循环所有人员班次
            for humanitem in human_attendance_series:
                  #循环所有班次明细
                  for itemdetail in humanitem.attendance_series_id.item_ids:
                    #根据人员班次明细信息查询打卡记录
                    attendance_result="normal"
                    overtime_hours=0
                    work_hours=0
                    displayorder=humanitem.displayorder
                    #签入
                    tt=itemdetail.hour_from-(itemdetail.min_before_from*1.0)/60.0   #减去提前量
                    curhour=int(tt)   #取小时数
                    curmin=int(round((tt-curhour)*60)) #取分钟数
                    print "hour_from: "+str(curhour)+':'+str(curmin)
                    starttime=datetime(curday.year,curday.month,curday.day,curhour,curmin)-td
                    
                    tt=itemdetail.hour_from+(itemdetail.min_after_from*1.0)/60.0   #加上延后量
                    curhour=int(tt)   #取小时数
                    curmin=int(round((tt-curhour)*60)) #取分钟数
                    print "hour_to: "+str(curhour)+':'+str(curmin)
                    endtime=datetime(curday.year,curday.month,curday.day,curhour,curmin)-td
                    
                    domain=[('create_date','>=',starttime.strftime("%Y-%m-%d %H:%M:%S")),('create_date','<=',endtime.strftime("%Y-%m-%d %H:%M:%S")),('create_uid','=',humanitem.human.id),('check_in_out','=','checkin')]
                    #domain=[('create_uid','=',humanitem.human.id)]
                    print 'domain: '+str(domain)
                    resscheckin=self.env['attendance_record.check_in_out_record'].search(domain,limit=1)
                    
                    #签退
                    tt=itemdetail.hour_to
                    curhour=int(tt)   #取小时数
                    curmin=int(round((tt-curhour)*60)) #取分钟数
                    print "hour_from: "+str(curhour)+':'+str(curmin)
                    starttime=datetime(curday.year,curday.month,curday.day,curhour,curmin)-td
                    
                    tt=itemdetail.hour_to+(itemdetail.min_after_to*1.0)/60.0 #加上延迟量
                    curhour=int(tt)   #取小时数
                    curmin=int(round((tt-curhour)*60)) #取分钟数
                    print "hour_to: "+str(curhour)+':'+str(curmin)
                    endtime=datetime(curday.year,curday.month,curday.day,curhour,curmin)-td
                    print endtime.isoformat()
                    domain=[('create_date','>=',starttime.strftime("%Y-%m-%d %H:%M:%S")),('create_date','<=',endtime.strftime("%Y-%m-%d %H:%M:%S")),('create_uid','=',humanitem.human.id),('check_in_out','=','checkout')]
                    #domain=[('create_uid','=',humanitem.human.id)]
                    print 'domain: '+str(domain)
                    resscheckout=self.env['attendance_record.check_in_out_record'].search(domain,limit=1)
                    
                    #确打卡记录算缺勤
                    if len(resscheckin)==0:
                        if len(resscheckout)>0:
                            attendance_result='semiabsent'
                        else:
                            attendance_result='absent'
                        print 'attendance_result:'+attendance_result
                    else:
                        print 'create_date:'+str(resscheckin[0].create_date)
                        checkintime=datetime.strptime(resscheckin[0].create_date, "%Y-%m-%d %H:%M:%S")
                        print "checkintime"+str(checkintime)
                        
                        #判断是否迟到
                        tt=itemdetail.hour_from
                        curhour=int(tt)   #取小时数
                        curmin=int(round((tt-curhour)*60)) #取分钟数
                        print "hour_from: "+str(curhour)+':'+str(curmin)
                        checkindelaytime=datetime(curday.year,curday.month,curday.day,curhour,curmin)-td
                        
                        if checkintime>checkindelaytime:
                            attendance_result="latein"
                            
                        #判断是否早退
                        if len(resscheckout)==0:
                            if attendance_result=="latein":
                                attendance_result="lateinearlyout"
                            else:
                                attendance_result="earlyout"
                        else:
                            checkouttime=datetime.strptime(resscheckout[0].create_date, "%Y-%m-%d %H:%M:%S")
                            print "checkouttime"+str(checkouttime)
                            
                            tt=itemdetail.hour_to  
                            curhour=int(tt)   #取小时数
                            curmin=int(round((tt-curhour)*60)) #取分钟数
                            print "hour_from: "+str(curhour)+':'+str(curmin)
                            allowcheckouttime=datetime(curday.year,curday.month,curday.day,curhour,curmin)-td
                            #计算签退延时
                            overtime_hours=(checkouttime-allowcheckouttime).total_seconds()/3600.0
                            print "overtime_hours:" + str(overtime_hours)
                        
                            #计算工作工作时长
                            work_hours=(checkouttime-checkintime).total_seconds()/3600.0
                            print "work_hours:" + str(work_hours)
                    
                    week_day=curday.weekday()+1
                    vals={'attendance_table_id':self.id,
                            'human':humanitem.human.id,
                            'attendance_date':curday,
                          'attendance_series_item_name':itemdetail.name,
                          'attendance_result':attendance_result,
                          'overtime_hours':overtime_hours,
                          'work_hours':work_hours,
                          'week_day':week_day,
                          'displayorder':displayorder}
                    
                    if len(resscheckin)>0:
                        vals['checkintime']=resscheckin[0].create_date
                    
                    if len(resscheckout)>0:
                        vals['checkouttime']=resscheckout[0].create_date
                    
                    self.item_ids.create(vals)


class HATItem(models.Model):
    _name = 'attendance_record.hat_item'
    _order = 'displayorder,attendance_date'
    
    human = fields.Many2one('res.users',string=u"人员")
    attendance_date = fields.Date(string=u"考勤日期")
    attendance_series_item_name = fields.Char(string=u"班次明细名称")
    attendance_result = fields.Selection([
         ('latein', u"迟到"),
         ('earlyout', u"早退"),
         ('lateinearlyout', u"迟到早退"),
         ('absent', u"缺席"),
         ('normal', u"正常"),
         ('semiabsent', u"半缺席"),
    ], string=u"考勤结果")

    overtime_hours = fields.Float(string=u"签退延时")
    work_hours = fields.Float(string=u"工作时长")
    week_day = fields.Integer(u"周几")
    attendance_table_id =  fields.Many2one('attendance_record.human_attendance_table', string=u"考勤表")
    checkintime = fields.Datetime(string=u"签到时间", required=False)
    checkouttime = fields.Datetime(string=u"签退时间", required=False)
    displayorder = fields.Integer(string=u"顺序", required=True)
