openerp.odoo_extension = function(instance, local)
{
	var _t = instance.web._t;
	var _lt = instance.web._lt;
	var QWeb = instance.web.qweb;

	local.WidgetMap = instance.web.form.FormWidget.extend
	({
		init: function(field_manager, node)
		{
			this._super(field_manager, node);
			this.options = instance.web.py_eval(this.node.attrs.options || '{}');
		},
		start: function()
		{
			this._super();

			this.field_longitude = this.options.longitude || "geo_longitude";
			this.field_latitude = this.options.latitude || "geo_latitude";
			this.field_manager.on("field_changed:" + this.field_longitude, this, this.render);
			this.field_manager.on("field_changed:" + this.field_latitude, this, this.render);
			this.render();
		},
		render: function()
		{
			var html = QWeb.render("widgetMap", {
				"longitude": this.field_manager.get_field_value(this.field_longitude) || 0,
				"latitude": this.field_manager.get_field_value(this.field_latitude) || 0
			});
			this.$el.html(html);
		}
	});
	instance.web.form.custom_widgets.add('map', 'openerp.odoo_extension.WidgetMap');
};