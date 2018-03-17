# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models,api


class libraryConfiguration(models.TransientModel):
    _name = 'library.config.settings'
    _inherit = 'res.config.settings'

    day_to_return = fields.Integer("默认借出天数")
    book_limit = fields.Integer("默认借出限制")

    def get_default_day_to_return(self, fields):
        Param = self.env["ir.config_parameter"]
        return {
                'day_to_return': int(Param.get_param("day_to_return")),
                'book_limit': int(Param.get_param("book_limit")),
                }

    @api.multi
    def execute(self):
        super(libraryConfiguration,self).execute()
        Param = self.env["ir.config_parameter"]

        for config in self:
            Param.set_param( 'day_to_return',config.day_to_return)
            Param.set_param('book_limit', config.book_limit)


    # module_pos_restaurant = fields.Selection([
    #     (0, "Point of sale for shops"),
    #     (1, "Restaurant: activate table management")
    # ], string="Restaurant",
    #     help='This module adds several restaurant features to the Point of Sale: \n\n- Bill Printing: Allows you to print a receipt before the order is paid \n\n- Bill Splitting: Allows you to split an order into different orders \n\n- Kitchen Order Printing: allows you to print orders updates to kitchen or bar printers')
    # module_pos_loyalty = fields.Boolean(
    #     string="Loyalty Program",
    #     help='Allows you to define a loyalty program in the point of sale, where the customers earn loyalty points and get rewards')
    # module_pos_discount = fields.Selection([
    #     (0, "Allow discounts on order lines only"),
    #     (1, "Allow global discounts")
    # ], string="Discount",
    #     help='Allows the cashier to quickly give a percentage sale discount for all the sales order to a customer')
    # module_pos_mercury = fields.Selection([
    #     (0, "No credit card"),
    #     (1, "Allows customers to pay with credit cards.")
    # ], string="Credit Cards",
    #     help='The transactions are processed by MercuryPay')
    # module_pos_reprint = fields.Selection([
    #     (0, "No reprint"),
    #     (1, "Allow cashier to reprint receipts")
    # ], string="Reprints")
    # module_pos_data_drinks = fields.Boolean(string="Import common drinks data")