    odoo.define('pos_product_available', function (require) {

"use strict";

	var module = require('point_of_sale.models');

    var models = module.PosModel.prototype.models;

    for(var i=0; i<models.length; i++){

        var model=models[i];

        if(model.model === 'product.product'){
             model.fields.push('qty_available');
             model.fields.push('is_book');
             model.fields.push('availability');
             model.fields.push('day_to_return_book');
             model.fields.push('isbn');
             model.fields.push('school_id');
        } 

    }

});
