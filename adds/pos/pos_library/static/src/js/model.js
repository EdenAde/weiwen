odoo.define('pos_library.models', function (require) {
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');

    var _superPosModel = models.PosModel;
    models.PosModel = models.PosModel.extend({
        create_order: function(order){
            var self = this,
                model = null;
            this._super(order);
            model = self.get('selectedOrder');
            self.fetch('pos.order', ['table_id'], [['id', '=', model.get('order_id')]])
                .then(function(table_data) {
                    var table = self.db.get_table_by_id(table_data[0].table_id[0]);
                    model.setTable(table);
                    model.set_screen_data('cashier_screen', 'products');
                });
        },



        // Remove cache order inside tables db
        delete_current_order: function(){
            var order = this.get('selectedOrder')
            if (order.table) {
                this.db.remove_order_from_table(order.uid);
            }
            _superPosModel.prototype.delete_current_order.call(this);

        },
        // Get image of table filter id
        get_image: function(table_id) {
            if (table_id != undefined) {
                return ''
               // return window.location.origin + '/web/binary/image?model=pos.table&field=image&id=' + table_id;
            }
            else {
                return ''
            }
        },

        // Return table name
        get_table_name: function(){
            var order = this.get('selectedOrder')
            var table = order.table;
            return table ? table.name : "";
        },
    });

    var _super_order = models.Order;

 //domain: function(self) {return [['id','=', self.pos_session.config_id[0]]]},
     models.load_models([
        {
            model: 'library.rack',
            fields: ['name', 'code','active'],
            domain: function(self) {return [['active','=', true]]},
            context:{},
            loaded: function(self, racks){
                self.db.racks = racks
                console.log("self.racks = racks")
                console.log(racks)
                // for (var i=0; i < racks.length; i ++) {
                //     self.rack_ids = racks[i].table_ids;
                //     break;
                // }
            },
        },
        // {
        //     model: 'pos.table',
        //     fields: ['id', 'number', 'name', 'capacity'],
        //     domain: function(self) {return [['id','in', self.table_ids]]},
        //     context:{},
        //     loaded: function(self, tables){
        //         for (var i = 0; i < tables.length; i ++) {
        //             tables[i].image_url = self.get_image(tables[i].id)
        //         }
        //         self.db.tables = tables;
        //     },
        // }
    ]);

    models.Order = models.Order.extend({

        // initialize: function(session, attributes) {
        //     _super_order.prototype.initialize.call(this, attributes);
        //   //  this.gui2 = attributes.gui  _superPosModel
        //
        // },


        // i loading table from cache datas and re-render again
        init_from_JSON: function (json) {
            _super_order.prototype.init_from_JSON.apply(this,arguments);
            if (json.table) {
                table = this.pos.db.get_table_by_id(json.table.id)
                this.setTable(table);
                this.pos.db.set_order_to_table(this)
            }
        },

        export_for_printing: function(){
            var json = _super_order.prototype.export_for_printing.call(this);
            var table = this.get('table');
            if (typeof table !== 'undefined') {json.table = table.name;}
            return json;
        },

        // i save data table to cache
        export_as_JSON: function() {
            var json = _super_order.prototype.export_as_JSON.call(this);
            table = this.get('table');
            if (table) {
                json.tb_id = table.id
                json.table = {
                    capacity: table.capacity,
                    id: table.id,
                    name: table.name,
                    number: table.number
                }
            }
            if (this.moving_product) {
                json.moving_product = true;
            }
            if (this.moving_table) {
                json.moving_table = true;
            }
            return json;
        },

        setTable: function(table){
            this.set({table: table});
            this.table = table;

        },

        remove_order: function(){
            _super_order.prototype.remove_order.call(this);
            this.pos.pos_bus.updating_table({'tables': this.pos.db.get_table_list()});
        },
        get_table: function(){
            return this.get('table');
        },
        add_product:function(product, options){
            var self = this;
            //借书和续借必须分开
            var oder_line = _super_order.prototype.get_last_orderline.call(this)
           // _.map(oder_lines,function (line) {
                if(oder_line&&oder_line.product.availability!=product.availability){
                    if(oder_line.product.availability=='notavailable'){
                        alert('请另开一个面板操作续借或还书')
                    }else{
                        alert('请另开一个面板操作借书')
                    }
                   // alert('');
                 // console.log(_superPosModel.prototype.the_gui_error.call(this));

                  // console.log(gui)
                    return false

                }
           // })


            _super_order.prototype.add_product.call(this,product, options);
        },

        get_image: function() {
            var table = this.get('table');
            if (table) {
                return ''
                //return window.location.origin + '/web/binary/image?model=pos.table&field=image&id=' + this.get('table').id;
            }
            else {
                return ''
            }
        }
    });

    var _supoerOrderLine = models.Orderline;
    models.Orderline = models.Orderline.extend({
        initialize: function(){
            _supoerOrderLine.prototype.initialize.apply(this, arguments);

        },

        init_from_JSON: function (json) {
            if (json.state) {
                this.state = json.state;
            }
            _supoerOrderLine.prototype.init_from_JSON.apply(this,arguments);

        },

        export_as_JSON: function(){
            var json = _supoerOrderLine.prototype.export_as_JSON.apply(this, arguments);
            if (this.state) {
                json.state = this.state;
            }
            return json;
        },
    });

});