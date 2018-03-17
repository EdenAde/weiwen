/**
 * Created by guizhouyuntushidai on 2017/8/7.
 */



odoo.define('pos_library.library_dashboard.today', function (require) {

var core = require('web.core');
var data = require('web.data');
var ActionManager = require('web.ActionManager');
var form_common = require('web.form_common');
var time = require('web.time');
var _t = core._t;
var QWeb = core.qweb;
var Model = require('web.Model');
var LibraryDashboardSummaryToday = form_common.FormWidget.extend(form_common.ReinitializeWidgetMixin, {
        display_name: _t('Form'),
        view_type: "form",

        events: {
        'click .o_dashboard_action': 'on_dashboard_action_clicked',
        'click .o_target_to_set': 'on_dashboard_target_clicked',
        },
        on_dashboard_action_clicked: function(ev){

        ev.preventDefault();

        var $action = $(ev.currentTarget);
        var action_name = $action.attr('name');
        var action_extra = $action.data('extra');
        var additional_context = {};


       // alert(action_name)
        if(action_name==''){
            return false
        }

        // TODO: find a better way to add defaults to search view
        if (action_name === 'library.action_product_book_list') {
            additional_context.search_default_todaybook = 1;
        }
        if(action_name ==='school.action_student_student_form_12'){
            additional_context.search_default_todayreader=1
        }
         if(action_name ==='library.action_library_book_list11'){

            if(action_extra=='borrow'){
                additional_context.search_default_todayissue=1
                additional_context.search_default_issue=1
            }else{
               additional_context.search_default_todayissue=1
             additional_context.search_default_return=1
            }

        }

        // else if (action_name === 'crm.crm_lead_action_activities') {
        //     if (action_extra === 'today') {
        //         additional_context.search_default_today = 1;
        //     } else if (action_extra === 'this_week') {
        //         additional_context.search_default_this_week = 1;
        //     } else if (action_extra === 'overdue') {
        //         additional_context.search_default_overdue = 1;
        //     }
        // }
        // else if (action_name === 'crm.action_your_pipeline') {
        //     if (action_extra === 'overdue') {
        //         additional_context['search_default_overdue'] = 1;
        //     } else if (action_extra === 'overdue_opp') {
        //         additional_context['search_default_overdue_opp'] = 1;
        //     }
        // } else if (action_name === 'crm.crm_opportunity_report_action_graph') {
        //     additional_context.search_default_won = 1;
        // }

        this.do_action(action_name, {additional_context: additional_context});
    },
        init: function() {

            this.values=[]
            this._super.apply(this, arguments);
            if(this.field_manager.model == "library.summary")
            {
                $(".oe_view_manager_buttons").hide();
                $(".oe_view_manager_header").hide();

            }
            // alert($(".time_span").length);
            this.set({
                date_to: false,
                date_from: false,
                summary_header: false,
                room_summary: false,
            });
            this.summary_header = [];
            this.room_summary = [];
            // this.field_manager.on("field_changed:date_from", this, function() {
            //     this.set({"date_from": time.str_to_datetime(this.field_manager.get_field_value("date_from"))});
            // });
            // this.field_manager.on("field_changed:date_to", this, function() {
            //     this.set({"date_to": time.str_to_datetime(this.field_manager.get_field_value("date_to"))});
            // });

            this.field_manager.on("field_changed:summary_header", this, function() {
                this.set({"summary_header": this.field_manager.get_field_value("summary_header")});
            });
            this.field_manager.on("field_changed:room_summary", this, function() {
                this.set({"room_summary":this.field_manager.get_field_value("room_summary")});
            });



        },


        fetch_data: function() {
        return new Model('library.summary')
            .call('retrieve_today_dashboard', []);
        },

        initialize_field: function() {

            form_common.ReinitializeWidgetMixin.initialize_field.call(this);
            var self = this;
            self.on("change:summary_header", self, self.initialize_content);
            self.on("change:room_summary", self, self.initialize_content);
        },

      initialize_content: function() {
           var self = this;
           if (self.setting)
               return;

           if (!this.summary_header || !this.room_summary)
                  return
           // don't render anything until we have summary_header and room_summary

           this.destroy_content();

           if (this.get("summary_header")) {
            this.summary_header = py.eval(this.get("summary_header"));
           }
           if (this.get("room_summary")) {
            this.room_summary = py.eval(this.get("room_summary"));
           }

           this.renderElement();
           this.view_loading();
        },

        view_loading: function(r) {
            return this.load_form(r);
        },

        load_form: function(data) {
            self.action_manager = new ActionManager(self);

            // this.$el.find(".table_free").bind("click", function(event){
            //     self.action_manager.do_action({
            //             type: 'ir.actions.act_window',
            //             res_model: "quick.room.reservation",
            //             views: [[false, 'form']],
            //             target: 'new',
            //             context: {"room_id": $(this).attr("data"), 'date': $(this).attr("date")},
            //     });
            // });

        },

        renderElement: function() {
             this.destroy_content();

            var self = this
            this.fetch_data().then(function(result){

                console.log(result)
               self.$el.html(QWeb.render("pos_library.Dashboard.Today", {values:result,widget: self,show_demo:true}));



        });

        }
    });

core.form_custom_registry.add('Library_Dashboard_Today', LibraryDashboardSummaryToday);
});




odoo.define('pos_library.library_dashboard.history', function (require) {

var core = require('web.core');
var data = require('web.data');
var ActionManager = require('web.ActionManager');
var form_common = require('web.form_common');
var time = require('web.time');
var _t = core._t;
var QWeb = core.qweb;

var LibraryDashboardSummaryHistory = form_common.FormWidget.extend(form_common.ReinitializeWidgetMixin, {
        display_name: _t('Form'),
        view_type: "form",

        events: {
        'click .o_dashboard_action': 'on_dashboard_action_clicked',
        'click .o_target_to_set': 'on_dashboard_target_clicked',
        },



        on_dashboard_action_clicked: function(ev){

            var self = this
          //  alert('1');
        ev.preventDefault();

        var $action = $(ev.currentTarget);
        var action_name = $action.attr('name');


        var action_extra = $action.data('extra');
        var additional_context = {};

        // TODO: find a better way to add defaults to search view
        if (action_name === 'pos_library.action_library_report_school2') {

            additional_context.school_filter_book = 1;
            additional_context.from_t = self.field_manager.get_field_value("date_from");
            //console.log("this.date_from")
            //console.log(time.str_to_datetime(this.field_manager.get_field_value("date_from")))
           // console.log(self.field_manager.get_field_value("date_from"))
            additional_context.to_t = self.field_manager.get_field_value("date_to");
        }


        if(action_name ==='pos_library.action_library_report_school3'){
            additional_context.school_filter_reader = 1;
            additional_context.from_t = self.field_manager.get_field_value("date_from");
            additional_context.to_t = self.field_manager.get_field_value("date_to");

        }
        //  if(action_name ==='library.action_library_book_list11'){
        //
        //     if(action_extra=='borrow'){
        //         additional_context.search_default_todayissue=1
        //         additional_context.search_default_issue=1
        //     }else{
        //        additional_context.search_default_todayissue=1
        //      additional_context.search_default_return=1
        //     }
        //
        // }
            console.log(action_name)
        console.log(additional_context)
        this.do_action(action_name, {additional_context: additional_context});
    },

        init: function() {
            this._super.apply(this, arguments);
            if(this.field_manager.model == "library.summary")
            {
                $(".oe_view_manager_buttons").hide();
                $(".oe_view_manager_header").hide();
               }
            this.set({
                date_to: false,
                date_from: false,
                summary_header: false,
                library_summary: false,
            });
            this.summary_header = [];
            this.library_summary = [];
            this.field_manager.on("field_changed:date_from", this, function() {
                this.set({"date_from": time.str_to_datetime(this.field_manager.get_field_value("date_from"))});
            });
            this.field_manager.on("field_changed:date_to", this, function() {
                this.set({"date_to": time.str_to_datetime(this.field_manager.get_field_value("date_to"))});
            });

            this.field_manager.on("field_changed:summary_header", this, function() {
                this.set({"summary_header": this.field_manager.get_field_value("summary_header")});
            });
            this.field_manager.on("field_changed:library_summary", this, function() {
                //alert('1');
                this.set({"library_summary":this.field_manager.get_field_value("library_summary")});
            });
        },

        initialize_field: function() {

            form_common.ReinitializeWidgetMixin.initialize_field.call(this);
            var self = this;
            self.on("change:summary_header", self, self.initialize_content);
            self.on("change:library_summary", self, self.initialize_content);
        },

      initialize_content: function() {
           var self = this;
           if (self.setting)

               return;

           if (!this.summary_header || !this.library_summary)
                  return
           // don't render anything until we have summary_header and room_summary

           this.destroy_content();

           if (this.get("summary_header")) {
            this.summary_header = py.eval(this.get("summary_header"));
           }
           if (this.get("library_summary")) {
             //  alert('1');
            this.library_summary = py.eval(this.get("library_summary"));
           }

           this.renderElement();
           this.view_loading();
        },

        view_loading: function(r) {
            return this.load_form(r);
        },

        load_form: function(data) {
            self.action_manager = new ActionManager(self);

            // this.$el.find(".table_free").bind("click", function(event){
            //     self.action_manager.do_action({
            //             type: 'ir.actions.act_window',
            //             res_model: "quick.room.reservation",
            //             views: [[false, 'form']],
            //             target: 'new',
            //             context: {"room_id": $(this).attr("data"), 'date': $(this).attr("date")},
            //     });
            // });

        },

        renderElement: function() {
             this.destroy_content();

             var self = this

            //date_from = this.get("date_from")
            //console.log("date_from="+date_from)
           // this.fetch_data().then(function(result){})

             this.$el.html(QWeb.render("pos_library.Dashboard.History", {widget: this,show_demo:true,summary:this.library_summary}));
        }
    });

core.form_custom_registry.add('Library_Dashboard_History', LibraryDashboardSummaryHistory);
});




odoo.define('pos_library.update_batch', function (require) {

var core = require('web.core');
var data = require('web.data');
var ActionManager = require('web.ActionManager');
var form_common = require('web.form_common');
var time = require('web.time');
var pyeval = require('web.pyeval');
var _t = core._t;
var FormView = require('web.FormView');
var QWeb = core.qweb;
var session = require('web.session');
var Model = require('web.Model');
FormView.include({
	load_record: function(record) {
	    console.log("load_record");
	    console.log(record);
	    console.log(arguments)
	    //this.$buttons[0].innerHTML=''
		this._super.apply(this, arguments);
        //
        // var is_update = record['display_name'].indexOf('model.update.fields')
        // console.log(is_update)
        // if(this.$buttons[0].innerText=="编辑   创建" && is_update>0){
        //     this.$buttons[0].innerHTML=''
        // }


        // if (this.$buttons) {
		 //    console.log(this.datarecord.perm_create)
        //     console.log(this.datarecord.perm_write)
			// //if(!this.datarecord.perm_create) {
			// 	this.$buttons.find('.o_form_button_create').hide();
			// //}
        // //	if(!this.datarecord.perm_write) {
			// 	this.$buttons.find('.o_form_button_edit').hide();
        // //	}
        // }
	}
});

var LibraryBatchUpdate = form_common.FormWidget.extend(form_common.ReinitializeWidgetMixin, {
        display_name: _t('Form'),
        view_type: "form",
        events: {
        'change select#update_value_selection':  'on_update_value_selection',
        'click button.o_form_button_cancel':  'click_cancel',
        
        },


    click_confirm: function(){

        this.gui.close_popup();
            //var category = this.$('#update_value_selection').val();
        alert('confirm');
            // this.field_manager.set_values({'update_value': category}).done(function() {
            // //self.updating = false;
            // });
           // this._super.apply(this, arguments);
    },
    click_cancel: function(){
        this.gui.close_popup();
        if (this.options.cancel) {
            this.options.cancel.call(this);
        }

    },

    on_update_value_selection:function(ev){

            ev.preventDefault();
            var $action = $(ev.currentTarget);
            var field_value = $action.val();


            this.field_manager.set_values({'update_value': field_value}).done(function() {
            //self.updating = false;
            });


    },
    //
    //     on_batch_action_clicked: function(ev){
    //     ev.preventDefault();
    //     var $action = $(ev.currentTarget);
    //     var field_name = $action.attr('name');
    //     var additional_context = {};
    //    // alert(action_name)
    //     if(field_name==''){
    //         return false
    //     }
    //     //this.fetch_target_values()
    //     // TODO: find a better way to add defaults to search view
    //     // if (action_name === 'library.action_product_book_list') {
    //     //     additional_context.search_default_todaybook = 1;
    //     // }
    //     // if(action_name ==='school.action_student_student_form_12'){
    //     //     additional_context.search_default_todayreader=1
    //     // }
    //     //  if(action_name ==='library.action_library_book_list11'){
    //     //
    //     //     if(action_extra=='borrow'){
    //     //         additional_context.search_default_todayissue=1
    //     //         additional_context.search_default_issue=1
    //     //     }else{
    //     //        additional_context.search_default_todayissue=1
    //     //      additional_context.search_default_return=1
    //     //     }
    //     //
    //     // }
    //
    //     // else if (action_name === 'crm.crm_lead_action_activities') {
    //     //     if (action_extra === 'today') {
    //     //         additional_context.search_default_today = 1;
    //     //     } else if (action_extra === 'this_week') {
    //     //         additional_context.search_default_this_week = 1;
    //     //     } else if (action_extra === 'overdue') {
    //     //         additional_context.search_default_overdue = 1;
    //     //     }
    //     // }
    //     // else if (action_name === 'crm.action_your_pipeline') {
    //     //     if (action_extra === 'overdue') {
    //     //         additional_context['search_default_overdue'] = 1;
    //     //     } else if (action_extra === 'overdue_opp') {
    //     //         additional_context['search_default_overdue_opp'] = 1;
    //     //     }
    //     // } else if (action_name === 'crm.crm_opportunity_report_action_graph') {
    //     //     additional_context.search_default_won = 1;
    //     // }
    //    // this.do_action('', {additional_context: additional_context});
    // },
        init: function() {
            //this.$buttons.find('.o_form_button_edit').hide();
            this.values=[]
            this.options = {};
            this._super.apply(this, arguments);
            if(this.field_manager.model == "model.update.fields")
            {
                $(".oe_view_manager_buttons").hide();
                $(".oe_view_manager_header").hide();

            }
            // alert($(".time_span").length);
           // this.set({
           //      date_to: false,
           //      date_from: false,
           //      summary_header: false,
           //      room_summary: false,
           //  });
           //  this.summary_header = [];
           //  this.room_summary = [];z
            // this.field_manager.on("field_changed:date_from", this, function() {
            //     this.set({"date_from": time.str_to_datetime(this.field_manager.get_field_value("date_from"))});
            // });
            // this.field_manager.on("field_changed:date_to", this, function() {
            //     this.set({"date_to": time.str_to_datetime(this.field_manager.get_field_value("date_to"))});
            // });




            var self = this


            this.field_manager.on("field_changed:target_field_name", this, function() {
                var ftype = this.field_manager.get_field_value("field_type")

                var field_id_model_name = this.field_manager.get_field_value("field_id_model")
            var model_name = this.field_manager.get_field_value("related_field_model")
            var target_field_name = this.field_manager.get_field_value("target_field_name")


                console.log("ftype==="+ftype)
                console.log("field_id_model_name==="+field_id_model_name)
            console.log("model_name==="+model_name)
            console.log("target_field_name==="+target_field_name)

                console.log("field_changed:field_type")
                console.log(this.$selectioin)
                console.log(ftype)
                if(!(['Many2one','many2one','selection','Selection'].includes(ftype))){
                    console.log("hide")

                    if(this.$selectioin!=undefined){
                        this.$selectioin.hide()
                    }
                }else{

                   // if(['selection','Selection'].includes(ftype)){
                        self.fetch_field_data().then(function(result){
                        console.log("result=====")
                        console.log(result)
                        self.$selectioin = self.$el.html(QWeb.render("pos_library.update_batch", {target_vals:result,widget: self}));

                    });
                   // }

                    if(this.$selectioin!=undefined){
                        this.$selectioin.show()
                    }

                }

            })
                // self.fetch_field_data().then(function(result){
                // console.log("result=====")
                // console.log(result)
                // self.$selectioin = self.$el.html(QWeb.render("pos_library.update_batch", {target_vals:result,widget: self}));
                //
                // });
        },

        fetch_field_data:function () {
            var field_id_model_name = this.field_manager.get_field_value("field_id_model")
            var model_name = this.field_manager.get_field_value("related_field_model")
            var target_field_name = this.field_manager.get_field_value("target_field_name")



            if(model_name){
                return new Model('model.update.fields')
                 .call('get_field_values', [model_name]);
            }else{
                return new Model('model.update.fields')
                 .call('get_selection_from_name', [field_id_model_name,target_field_name]);
            }

        },


        fetch_data: function() {
            var self = this
            // console.log(session)
            // console.log(self.node.attrs.context)
            // console.log(this)
            // var context2 = pyeval.eval('context');
            // console.log(context2)
            var model_id = 0;
            switch(this.session.active_id){
                case 421:
                    model_id = 152;
                    break;
                case 478:
                    model_id = 417;
                    break;
                case 423:
                    model_id = 189;
                    break;
            }

            //var m_id = self.context.report_id
            // return new Model('model.update.fields')
            //     .call('get_model_fields', [model_id]);
        },

        initialize_field: function() {

            form_common.ReinitializeWidgetMixin.initialize_field.call(this);
            var self = this;
            //self.on("change:field_id", self, self.initialize_content);

          //  to_order.trigger('change', to_order);
//                 to_order.trigger('change:sync');


            //self.on("change:room_summary", self, self.initialize_content);
        },

      // initialize_content: function() {
      //      var self = this;
      //
      //      this.destroy_content();
      //
      //      this.renderElement();
      //      this.view_loading();
      //   },
      //
      //   view_loading: function(r) {
      //       return this.load_form(r);
      //   },

        load_form: function(data) {
            self.action_manager = new ActionManager(self);

            // this.$el.find(".table_free").bind("click", function(event){
            //     self.action_manager.do_action({
            //             type: 'ir.actions.act_window',
            //             res_model: "quick.room.reservation",
            //             views: [[false, 'form']],
            //             target: 'new',
            //             context: {"room_id": $(this).attr("data"), 'date': $(this).attr("date")},
            //     });
            // });

        },

        // renderElement: function() {
        //      this.destroy_content();
        //
        //     var self = this
        //     this.fetch_data().then(function(result){
        //
        //        console.log("result=====")
        //         console.log(result)
        //        self.$el.html(QWeb.render("pos_library.update_batch", {values:result,widget: self}));
        //
        // });
        //
        // }
    });

core.form_custom_registry.add('Library_batch_update', LibraryBatchUpdate);
});

