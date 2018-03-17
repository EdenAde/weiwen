$('.o_tooltip').remove();
odoo.define('pos_library.sreen', function (require) {
    "use strict";

    var chrome = require('point_of_sale.chrome');
    var gui = require('point_of_sale.gui');
    var models = require('point_of_sale.models');
    var PosDB = require('point_of_sale.DB');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var session = require('web.session');
    var qweb = core.qweb;
    var Model = require('web.DataModel');
    var framework = require('web.framework');
    var PosBaseWidget = require('point_of_sale.BaseWidget');



    var ClientListScreenWidget=screens.ClientListScreenWidget.include({


        show:function () {
            var self=this
            this._super();

            //self.pos.db.get_partner_by_id(partner_id);

            $('.client-details-contents').on('click','.issued_book',function () {
                var parter_id = $(this).attr("data-id")

                var p_ids = $(this).attr("data-ids")

                var partner = self.pos.db.get_partner_by_id(parter_id);

                console.log(self.old_client)
                console.log(self.new_client)
                console.log(p_ids.split(','))
                self.clickTable(partner,p_ids.split(','))
            })

        },
         // Event click table
        clickTable: function(partner,pids){
            console.log("---------------------------------")
            var currentOrder = this.pos.get('selectedOrder');
            console.log(currentOrder)
            // var table_click = this.pos.db.get_table_by_id(table_id);
             var orders = this.pos.get('orders');

            this.pos.get_client()
             console.log(orders)
            // var order = orders.models.find(function (order) {
            //     if (order.table) {
            //         return order.table.id == table_id;
            //     }
            // });
            // if (order) {
            //     this.pos.set({ selectedOrder: order});
            //     order.trigger('change', order);
            // } else {
            //     if (!currentOrder.table) {
            //         currentOrder.setTable(table_click)
            //         this.pos.db.set_order_to_table(currentOrder);
            //         this.pos.set({ selectedOrder: currentOrder});
            //         currentOrder.trigger('change', currentOrder);
            //     } else {
            //         var new_order = new models.Order({}, {pos: this.pos});
            //         new_order.setTable(table_click)
            //         this.pos.db.set_order_to_table(new_order);
            //         orders.add(new_order)
            //         this.pos.set({ selectedOrder: new_order});
            //         new_order.trigger('change', new_order);
            //     }
            // }

            this.gui.show_screen('products');
            console.log("partner")
            console.log(partner)
            this.pos.add_new_order_with_client(partner,pids);

        },





    })

    var bookIssueWidget=screens.ActionpadWidget.include({


        get_remote_products:function () {

        },
        get_books_array:function (orders) {
            console.log(orders)
            return _.map(orders,function (order) {
                console.log(order.id)
                return order.id
            })
        },
        

        renderElement: function() {
        var self = this;
        this._super();
        this.$('.issue').click(function(){

            var order = self.pos.get_order()

            if(order.is_empty()){
                self.gui.show_popup('error',{
                title :"出错了",
                body  :"书籍为空",
                });
            }
            var order_line = self.pos.get_order().get_last_orderline();
            // if(order_line.model.product.availability=='available')
            // console.log("order")
            // console.log(order)
             var has_notavailable=false
            // if(self.pos.get_client())

            _.map(order_line.models,function (model) {
                if(model.product.availability=='notavailable'){
                    has_notavailable=true
                   // has_available=true
                }
            })

            if(has_notavailable){
                 var issue_books=[]
                var books_string = ""
                    _.map(order.orderlines.models,function (model) {
                            books_string +=model.product.display_name+","
                            issue_books.push(model.product)
                    })
                 self.gui.show_popup('confirm',{
                    'title': "续借信息确认",
                    'body':  "书籍："+books_string,
                    confirm: function(){
                      var issues={
                        book_ids:issue_books
                    }
                    //var order  = self.pos.get_order()

                    new Model('library.book.issue').call('createBatchReissue',{vals:issues}).then(function(res){
                         console.log("here_reissue!!!")
                            order.remove_orderline_all()
                    }, function(err,event){
                        self.gui.show_popup('error',{
                                        title :"出错了",
                                        body  :err.data.message,
                                    });
                        event.preventDefault();});
                    },
                });


            }else if(self.pos.get_client()&&!order.is_empty()){
                var issue_books=[]
                var books_string = ""
                    _.map(order.orderlines.models,function (model) {
                            books_string +=model.product.display_name+","
                            issue_books.push(model.product)
                    })
               // alert(self.$("span[data-product-id='"+issue_books[0].id+"']").find('.product-qty').length)
                 self.gui.show_popup('confirm',{
                    'title': "借书信息确认",
                    'body':  "读者："+self.pos.get_client().name+"／书籍："+books_string,
                    confirm: function(){
                      var issues={
                        book_ids:issue_books,
                        client:self.pos.get_client()
                    }
                    console.log("issues==")
                        console.log(issue_books)
                    var order  = self.pos.get_order()

                    new Model('library.book.issue').call('createBatch',{vals:issues}).then(function(res){
                        console.log("here_issue!!!")
                            order.remove_orderline_all()

                         // var lis = document.querySelector(".orderlines");
                         //      var lisli = document.querySelector(".orderlines li");
                         //         lis.removeChild(lisli)
                          //    document.querySelector(".summary .value").textContent='';
                        //
                        //
                             for(var i in issue_books){
                        //
                                 var bid = issue_books[i].id
                        //
                        //
                                 var pro = document.querySelector("span[data-product-id='"+bid+"'] .product-qty");
                                 pro.classList.remove("product-qty")
                                 pro.classList.toggle("product-qty-low")
                                 pro.innerHTML='借出'
                        //
                               //  self.pos.db.product_by_id[bid].availability="notavailable"
                               //  var barco = self.pos.db.product_by_id[bid].barcode
                             //    self.pos.db.product_by_barcode[barco].availability="notavailable"
                        //
                        //
                             }

                    }, function(err,event){
                        self.gui.show_popup('error',{
                                        title :"出错了",
                                        body  :err.data.message,
                                    });
                        event.preventDefault();});
                    },
                });
            }else{
                self.gui.show_popup('error',{
                title :"出错了",
                body  :"读者或书籍为空",
            });
            }
        });

        this.$('.return').click(function(){
            var order = self.pos.get_order();
            if(order){
                var issue_books=[]
                var books_string = ""
                    _.map(order.orderlines.models,function (model) {
                            books_string +=model.product.display_name+","
                            issue_books.push(model.product)
                    })
                 self.gui.show_popup('confirm',{
                    'title': "还书信息确认",
                    'body':  "书籍："+books_string,
                    confirm: function(){
                      var issues={
                        book_ids:issue_books,
                    }
                    console.log("issues====")
                        console.log(issues)

                    //console.log(order)
                    new Model('library.book.issue').call('returnBatch',{vals:issues}).then(function(res){
                        var order  = self.pos.get_order()
                        order.remove_orderline_all()
                         for(var i in issue_books){
                               // console.log(issue_books[i])
                                var bid = issue_books[i].id

                                //document.querySelector(".active a");
                                var pro = document.querySelector("span[data-product-id='"+bid+"'] .product-qty-low");
                                pro.classList.remove("product-qty-low")
                                pro.classList.toggle("product-qty")
                                pro.innerHTML='在馆'

                                self.pos.db.product_by_id[bid].availability="available"
                                var barco = self.pos.db.product_by_id[bid].barcode
                                self.pos.db.product_by_barcode[barco].availability="available"

                               // alert(self.$("div").length)
                               // alert(self.$("span[data-product-id='"+bid+"']").find('.product-qty').length)
                               // self.$("span[data-product-id='"+bid+"']").find('.product-qty').remove()
                            }



                            //  var lis = document.querySelector(".orderlines");
                            //  var lisli = document.querySelector(".orderlines li");
                            //     lis.removeChild(lisli)
                            //  document.querySelector(".summary .value").textContent='';


                             //order.deselect_orderline();orderlines




                    }, function(err,event){
                        self.gui.show_popup('error',{
                                        title :"出错了",
                                        body  :err.data.message,
                                    });
                        event.preventDefault();});
                    },
                });
            }else{
                self.gui.show_popup('error',{
                title :"出错了",
                body  :"读者或书籍为空",
            });
            }
        });


        this.$('.set-customer').click(function(){
            self.gui.show_screen('clientlist');
        });
    }
    })


    var BookCreationWidget = PosBaseWidget.extend({
        template: 'BookCreationWidget',
        init: function(parent, args) {
            this._super(parent, args);
            this.options = {};
            this.book={};
            this.db = new PosDB();


            this.racks=this.pos.db.racks

        },
        get_racks:function () {


        },
        events: {
            'click .button.cancel':  'click_cancel',
            'click .button.confirm': 'click_confirm',
        },
        show: function(book){
            console.log("optionsbook=")
            console.log(book)
            book = book || {};
            this._super(book);
            //this.category = options.category;

            this.book = book;
            //this.units = options.units;
            this.renderElement();
            this.$('.barcode').focus();
        },
        close: function(){
            if (this.pos.barcode_reader) {
                this.pos.barcode_reader.restore_callbacks();
            }
        },
        click_confirm: function(){
           // alert('kaishi')
            var self = this;
                //self.chrome.loading_show();

            // var name = this.$('.name').val();
            // var type = this.$('.type').val();
            // var category = this.$('.category').val();
            // var unit = this.$('.uom').val();
            // var price = this.$('.price').val();
            // if(isNaN(price) || !price) {
            //     alert("Please check the price !")
            // }
            // else {
                //  var product_vals = {
                //     'name': name,
                //     'type': type,
                //     'category': category,
                //     'price': price,
                //     'unit': unit
                // };
                this.book.rack = this.$('.rack').val();

                this.book.copy_num = this.$('.copy_num').val();
                this.book.tomes_num = this.$('.tomes_num').val();
                this.book.barcode = this.$('.barcode').val();
                this.book.company_id=session.company_id;
                if(this.book.barcode==''){
                    alert('条码不能为空')
                    return false
                }else{

                    framework.blockUI()
                     new Model('product.product').call('create_book_pos',[1, this.book]).then(function(product){
                        //self.pos.db.add_products([product]);
                         alert(product)
                        console.log(self)
                        framework.unblockUI()
                    }).fail(function () {
                       // alert('123')
                        framework.unblockUI()
               alert("Could not submit ! Try Again");
           });
              //  console.log(product_vals)
                this.gui.close_popup();
                if( this.options.confirm ){
                    this.options.confirm.call(this,name);
                }

                }



               // return ;

           // }
        },
        click_cancel: function(){
            this.gui.close_popup();
            if (this.options.cancel) {
                this.options.cancel.call(this);
            }
        },
    });
    gui.define_popup({name:'book_create', widget: BookCreationWidget});


    var BookIntentWidget = PosBaseWidget.extend({
        template: 'BookIntentWidget',
        init: function(parent, args) {
            this._super(parent, args);
            this.options = {};
            this.book={};
            this.db = new PosDB();
            this.click_return={}
            this.screen={};
           // this.category = [];
           // this.units = [];
        },
        events: {
            'click .button.return':  'click_return',
            'click .button.issue': 'click_issue',
            'click .button.cancel': 'click_cancel',
        },
        show: function(options){
            console.log("optionsbook=")
            console.log(options)
            options = options || {};
            this.click_return=options.return_action
            this.options=options;
            this._super(options);
            this.book = options.book;


            this.renderElement();

        },
        close: function(){
            if (this.pos.barcode_reader) {
                this.pos.barcode_reader.restore_callbacks();
            }
        },
        click_issue:function () {
            console.log("this.options.issue_action")
            console.log(this.options.issue_action)
            if (this.options.issue_action) {
                        this.options.issue_action.call(this,this.options.parsed_code);
             }
        },
        click_cancel: function(){
            this.gui.close_popup();
            if (this.options.cancel) {
                this.options.cancel.call(this);
            }
        },
    });
    gui.define_popup({name:'book_intent', widget: BookIntentWidget});

    screens.ScreenWidget.include({


        init: function(parent, args) {
            this._super(parent, args);
            this.parsed_code={}
            this.intent=''
            this.parsed_code2='1212'

        },

        click_return:function () {
            var self = this;
            self.intent='return'
            $('.action_title').text("归还")
        },
        click_issue: function(parsed_code){
            var self = this;
            self.intent='issue';
            //this.$('.pay').text("借阅")
            $('.action_title').text("借阅")
            self.gui.close_popup();
            console.log("parsed_code=")
            console.log(self)
            self.pos.scan_product_with_intent(parsed_code,self.intent)
            self.gui.show_screen('products', null, null, true);
        },
        show_book_intent:function (product,parsed_code) {
            var self = this
            var options={'book':product,'issue_action':self.click_issue,'return_action':self.click_return,'parsed_code':parsed_code}
            self.gui.show_popup('book_intent',options);
        },
        barcode_product_action: function(parsed_code){
        var self = this;
        this.parsed_code=parsed_code
        var product = self.pos.db.get_product_by_barcode(parsed_code.base_code);
        console.log("product=")
            console.log(product)
        if(!product){
             this._super(parsed_code);
            return ;
        }
        if(product.is_book){

            if(this.pos.intent!=""){
                this.show_book_intent(product,parsed_code)
            }else{
                this._super(parsed_code);
            }

        }
         //

        },
        show_book:function (parsed_code) {

            var self = this
            new Model('product.product').call('get_book_date_with_isbn',[1, parsed_code.base_code]).then(function(book){
                   // console.log(book)
                    self.gui.show_popup('book_create',book);
                });
        }
    });



});

