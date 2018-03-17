openerp.widget_amaps = function (openerp)
{   
 openerp.web.form.widgets.add('amap', 'openerp.widget_amaps.amap');
 openerp.widget_amaps.amap = openerp.web.form.FieldChar.extend(
        {
        template : "amap",
        init: function (view, code) {
            this._super(view, code);
        },
        render_value: function() {
            var show_value = this.format_value(this.get('value'), '');
            this.$el.find('input').val(show_value);
            
            /*
             * Center
             * Es la latitud y la longitud del mapa
             * 
             * Tipo de Mapas
             * satellite (photographic map)
             * roadmap (normal, default 2D map)
             * hybrid (photographic map + roads and city names)
             * terrain (map with mountains, rivers, etc.)
             * 
             * Zoom
             * Entre 0 y 20
             */
            
            var lt = '', ln = '';
            var API_KEY = 'AIzaSyCQI-OVySMOxJCQFCEux6SDeN_eXk1Uvvo';
            var center = '';
            var zoom = '';
            var maptype = 'roadmap';
            var viewtype = 'view'
            var q = '';
            var vars = [], hash;
            var hashes = show_value.slice(show_value.indexOf('google') + 5).split('/');
            
            for(var i = 0; i < hashes.length; i++){
	            hash = String(hashes[i]);
	            if (hash[0] == '@'){
	            	lt = hash.split('@')[1].split(',')[0]
	            	ln = hash.split('@')[1].split(',')[1];
	            	zoom = hash.split('@')[1].split(',')[2]
	            }
            }
            center = '&center=' + lt + ',' + ln
            if (show_value.indexOf('m/data') != -1){
            	maptype = 'satellite'
            }
            
            // Ver si la vista es de Place
            if (show_value.indexOf('/place') != -1){
            	viewtype = 'search';
            	q = show_value.slice(show_value.indexOf('/place') + 6).split('/')[1];
            	center = '&q=' + q
            }
            
            if (String(lt) == '' || String(ln) == '' || String(zoom) == ''){
                //var src_iframe = '';
            }

            else{
              //  this.$("#gmap").attr('src', src_iframe)
                var mapObj = new AMap.Map("amap");
                 mapObj.plugin(["AMap.ToolBar","AMap.OverView","AMap.Scale"],function(){

                //加载工具条

                tool=new AMap.ToolBar({

                  direction:false,//隐藏方向导航

                  ruler:false,//隐藏视野级别控制尺

                  autoPosition:false//禁止自动定位

                });

                mapObj.addControl(tool);

                //加载鹰眼

                view=new AMap.OverView();

                mapObj.addControl(view);

                //加载比例尺

                scale=new AMap.Scale();

                mapObj.addControl(scale);

              });



                 var marker = new AMap.Marker({

                id:"m",

                position:new AMap.LngLat(lt,ln),

                offset: new AMap.Pixel(-8,-34),

                icon: "http://webapi.amap.com/static/images/marker_sprite.png",

                level: 15

            });


            }
            	//var src_iframe = 'https://www.google.com/maps/embed/v1/' + viewtype + '?key=' + API_KEY + center + '&zoom=' + zoom + '&maptype=' + maptype;
                    //this.$("#gmap").attr('src', src_iframe)




       //      var mapObj = new AMap.Map("container");










        },
    });
}