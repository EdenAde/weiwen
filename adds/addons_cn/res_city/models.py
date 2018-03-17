# -*- coding: utf-8 -*-

from odoo.osv import  osv

from odoo import tools,fields,models


class CountryCity(models.Model):
    _description = "Country City"
    _name = 'res.country.city'


    state_id=fields.Many2one('res.country.state', 'State',
                                    required=True)
    name=fields.Char('City Name', required=True,
                            help='City name of a country.')


    _order = 'name'

class County(models.Model):
    _description = "County"
    _name = 'res.country.county'
    _inherit = ['base.model']
    city_id=fields.Many2one('res.country.city', 'City',required=True)
    name=fields.Char('County Name', required=True,help='County name of a country.')
    translate=fields.Char('外文')


    _order = 'name'

class Town(models.Model):
    _description = "乡镇"
    _name = 'res.country.county.town'
    _inherit = ['base.model']

    county_id=fields.Many2one('res.country.county', '区/县',required=True)
    name=fields.Char('乡镇', required=True,help='County name of a country.')
    translate=fields.Char('外文')
    sort=fields.Integer('排序')

    _order = 'name'

class Village(models.Model):
    _description = "村"
    _name = 'res.country.county.town.village'
    _inherit = ['base.model']

    town_id = fields.Many2one('res.country.county.town', '区/县',required=True)
    name=fields.Char('村', required=True,help='County name of a country.')
    translate=fields.Char('外文')
    _order = 'name'



class res_company(models.Model):
    _inherit = "res.company"

    village=fields.Many2one("res.country.county.town.village", '村', ondelete='restrict')
    town=fields.Many2one("res.country.county.town", '乡镇', ondelete='restrict')
    county=fields.Many2one("res.country.county", '区县', ondelete='restrict')
    city_id=fields.Many2one("res.country.city", '城市', ondelete='restrict')
    organization_code=fields.Char(u'组织机构代码')


    def onchange_city_id(self, city):
        if city:
            city_obj = self.env['res.country.city'].browse(city)
            return {'value': {'state_id': city_obj.state_id.id}}
        return {}

    def onchange_county(self, county):
        if county:
            county_obj = self.env['res.country.county'].browse(county)
            return {'value': {'city_id': county_obj.city_id.id}}
        return {}
    def onchange_town(self, town):
        if town:
            town_obj = self.env['res.country.county.town'].browse(town)
            return {'value': {'county_id': town_obj.county_id.id}}
        return {}
    def onchange_village(self, village):
        if village:
            village_obj = self.env['res.country.county'].browse(village)
            return {'value': {'town_id': village_obj.town_id.id}}
        return {}





class res_partner(models.Model):
    _inherit = "res.partner"

    village=fields.Many2one("res.country.county.town.village", '村', ondelete='restrict')
    town=fields.Many2one("res.country.county.town", '乡镇', ondelete='restrict')
    county=fields.Many2one("res.country.county", '区县', ondelete='restrict')
    city_id=fields.Many2one("res.country.city", 'City', ondelete='restrict')
    identification=fields.Selection([
            ('identity_card', u'身份证'),
            ('passport', u'护照'),
            ('driving_license', u'驾照'),
            ('certificate_officer', u'军官证'),
            ('other', u'其他'),
        ], string=u'证件类型')
    identification_code=fields.Char(u'证件号码')
    organization_code=fields.Char(u'组织机构代码')
    tax_registration=fields.Char(u'税务登记号')


    def onchange_city_id(self, city):
        if city:
            city_obj = self.env['res.country.city'].browse(city)
            return {'value': {'state_id': city_obj.state_id.id}}
        return {}

    def onchange_county(self, county):
        if county:
            county_obj = self.env['res.country.county'].browse(county)
            return {'value': {'city_id': county_obj.city_id.id}}
        return {}
    def onchange_town(self, town):
        if town:
            town_obj = self.env['res.country.county.town'].browse(town)
            return {'value': {'county_id': town_obj.county_id.id}}
        return {}
    def onchange_village(self, village):
        if village:
            village_obj = self.env['res.country.county'].browse(village)
            return {'value': {'town_id': village_obj.town_id.id}}
        return {}

class crm_lead(models.Model):
    _inherit = "crm.lead"

    county=fields.Many2one("res.country.county", 'County')
    city=fields.Many2one("res.country.city", 'City')


    def onchange_city(self,city):
        if city:
            city_obj = self.env['res.country.city'].browse(city)
            return {'value': {'state_id': city_obj.state_id.id}}
        return {}

    def onchange_county(self,county):
        if county:
            county_obj = self.env['res.country.county'].browse(county)
            return {'value': {'city_id': county_obj.city_id.id}}
        return {}