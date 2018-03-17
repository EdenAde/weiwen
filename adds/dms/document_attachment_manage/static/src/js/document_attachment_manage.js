odoo.define('document_attachment_manage', function (require) {
"use strict";

var core = require('web.core');
var Sidebar = require('web.Sidebar');
var _t = core._t;

var Model = require('web.Model');
var Dialog = require('web.Dialog');
var QWeb = core.qweb;
var framework = require('web.framework');


// alert("111");
Sidebar.include({



    render_value: function () {
            this._super();


        },


    _evalUrl: function( url ) {
		return jQuery.ajax({
			url: url,
			type: "GET",
			dataType: "script",
			async: false,
			global: false,
			"throws": true
		});
	},

    // on_attachment_changed: function(e) {
    //
    //     alert("on_attachment_changed")
    //     var $e = $(e.target);
    //     if ($e.val() !== '') {
    //         this.$('form.o_form_binary_form').submit();
    //         $e.parent().find('input[type=file]').prop('disabled', true);
    //         $e.parent().find('button').prop('disabled', true).find('img, span').toggle();
    //         this.$('.o_sidebar_add_attachment a').text(_t('Uploading...'));
    //         framework.blockUI();
    //     }else{
    //
    //     }
    // },

    _dataURItoBlob:function (dataURI) {
            var byteString = atob(dataURI.split(',')[1]);
            var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
            var ab = new ArrayBuffer(byteString.length);
            var ia = new Uint8Array(ab);
            for (var i = 0; i < byteString.length; i++) {
                ia[i] = byteString.charCodeAt(i);
            }
            return new Blob([ab], {type: mimeString});
    },

    start : function(){
        var self = this;
        self._super.apply(self, arguments);

         var WebCamDialog = $(QWeb.render("WebCamDialog")),
                img_data;

            // ::webcamjs:: < https://github.com/jhuckaby/webcamjs >
            // Webcam: Set Custom Parameters

            Webcam.set({
                width: 320,
                height: 240,
                dest_width: 320,
                dest_height: 240,
                image_format: 'jpeg',
                jpeg_quality: 90,
                force_flash: false,
                fps: 45,
                swfURL: '/web_widget_image_webcam/static/src/js/webcam.swf',
            });

          //  self.$el.find('.o_form_binary_file_web_cam').removeClass('col-md-offset-5');

            new Model('ir.config_parameter').call('get_param', ['web_widget_image_webcam.flash_fallback_mode', false]).
            then(function(default_flash_fallback_mode) {
                if (default_flash_fallback_mode == 1) {
                    Webcam.set({
                        /*
                            :: Important Note about Chrome 47+ :: < https://github.com/jhuckaby/webcamjs#important-note-for-chrome-47 >
                            Setting "force_flash" to "true" will always run in Adobe Flash fallback mode on Chrome, but it is not desirable.
                        */
                        force_flash: true,
                    });
                }
            });

            self.$el.on('click','.o_sidebar_camera_attachment', function(evt) {
                // Init Webcam
                new Dialog(self, {
                    size: 'large',
                    dialogClass: 'o_act_window',
                    title: _t("WebCam Booth"),
                    $content: WebCamDialog,
                    buttons: [
                        {
                            text: "拍摄", classes: 'btn-primary take_snap_btn',
                            click: function () {
                                Webcam.snap( function(data) {
                                    img_data = data;
                                    // Display Snap besides Live WebCam Preview
                                    WebCamDialog.find("#webcam_result").html('<img src="'+img_data+'"/>');
                                });
                                // Remove "disabled" attr from "Save & Close" button
                                $('.save_close_btn').removeAttr('disabled');
                            }
                        },
                        {
                            text: "保存&关闭", classes: 'btn-primary save_close_btn', close: true,
                            click: function () {
                              //  var img_data_base64 = img_data.split(',')[1];

                                /*
                                    Size in base64 is approx 33% overhead the original data size.

                                    Source: -> http://stackoverflow.com/questions/11402329/base64-encoded-image-size
                                            -> http://stackoverflow.com/questions/6793575/estimating-the-size-of-binary-data-encoded-as-a-b64-string-in-python

                                            -> https://en.wikipedia.org/wiki/Base64
                                            [ The ratio of output bytes to input bytes is 4:3 (33% overhead).
                                            Specifically, given an input of n bytes, the output will be "4[n/3]" bytes long in base64,
                                            including padding characters. ]
                                */

                                // From the above info, we doing the opposite stuff to find the approx size of Image in bytes.
                               // var approx_img_size = 3 * (img_data_base64.length / 4)  // like... "3[n/4]"

                                // Upload image in Binary Field
                               // self.on_file_uploaded(approx_img_size, "web-cam-preview.jpeg", "image/jpeg", img_data_base64);

                                    //$e.parent().find('input[type=file]').prop('disabled', true);
                                   // $e.parent().find('button').prop('disabled', true).find('img, span').toggle();
                                    $('.o_sidebar_add_attachment a').text(_t('Uploading...'));
                                    framework.blockUI();


                               // var file_slider = $("")
                                var formData = new FormData();
                                var url =$(".o_form_binary_form").attr("action")
                                //var file = {uri: "C:/fake.jpg", type: 'multipart/form-data', name: Date.parse(new Date())+".jpeg"};


                                var blob = self._dataURItoBlob(img_data);
                                formData.append('ufile',blob,Date.now() + '.jpg');
                                formData.append('csrf_token',$(".o_sidebar_add_attachment input[name='csrf_token']").attr("value"));
                                formData.append('callback',$(".o_sidebar_add_attachment input[name='callback']").attr("value") );
                                formData.append('model', $(".o_sidebar_add_attachment input[name='model']").attr("value"));
                                formData.append('id', $(".o_sidebar_add_attachment input[name='id']").attr("value"));
                               // formData.append('fileType', 'image');




                                $.ajax({
                                    type: 'POST',
                                    url: url,
                                    data: formData,
                                    processData: false, // 不会将 data 参数序列化字符串
                                    contentType: false, // 根据表单 input 提交的数据使用其默认的 contentType
                                    xhr: function() {
                                        var xhr = new window.XMLHttpRequest();
                                        xhr.upload.addEventListener("progress", function(evt) {
                                            if (evt.lengthComputable) {
                                                var percentComplete = evt.loaded / evt.total;
                                                console.log('进度', percentComplete);
                                            }
                                        }, false);

                                        return xhr;
                                    }
                                }).success(function (res) {
                                     framework.unblockUI();
                                    // 拿到提交的结果
                                }).error(function (err) {
                                    console.error(err);
                                });


                                // fetch(url,{
                                //     method: 'POST',
                                //     headers: {
                                //       'Content-Type': 'multipart/form-data',
                                //       'Accept': 'application/json'
                                //     },
                                //     body: formData,
                                //   }).then(function(res){
                                //       console.log("success")
                                //         framework.unblockUI();
                                //       console.log(res)
                                //
                                // }).catch(function (err) {
                                //     console.log("error")
                                //     console.log(err)
                                // })


                            }
                        },
                        {
                            text: "关闭", close: true
                        }
                    ]
                }).open();

                Webcam.attach('#live_webcam');

                // At time of Init "Save & Close" button is disabled
                $('.save_close_btn').attr('disabled', 'disabled');

                // Placeholder Image in the div "webcam_result"
                WebCamDialog.find("#webcam_result").html('<img src="/web_widget_image_webcam/static/src/img/webcam_placeholder.png"/>');
            });


        //var WebCamDialog = $(QWeb.render("WebCamDialog2"))
        //alert("111");
        self.$el.on('click','.o_sidebar_manage_attachment', function(evt) {
            self.do_action({
                name: _t('Attachment Management'),
                type: 'ir.actions.act_window',
                res_model: 'ir.attachment',
                domain: [
                    '&',
                    ['res_model', '=', self.dataset.model],
                    ['res_id', '=', self.model_id]
                ],
                view_mode: 'tree,form',
                view_type: 'form',
                views: [
                    [false, 'list'],
                    [false, 'form']
                ],
                context: {
                    'default_res_model': self.dataset.model,
                    'default_res_id': self.model_id
                }
            });
            evt.preventDefault();
        });

        // self.$el.on('click','.o_sidebar_camera_attachment', function(evt) {
        //
        //   //  alert("11");
        //
        //     new Dialog(self, {
        //             size: 'large',
        //             dialogClass: 'o_act_window',
        //             title: _t("WebCam Booth"),
        //             $content: WebCamDialog,
        //             buttons: [
        //                 {
        //                     text: "拍摄", classes: 'btn-primary take_snap_btn',
        //                     click: function () {
        //                         Webcam.snap( function(data) {
        //                             img_data = data;
        //                             // Display Snap besides Live WebCam Preview
        //                             WebCamDialog.find("#webcam_result").html('<img src="'+img_data+'"/>');
        //                         });
        //                         // Remove "disabled" attr from "Save & Close" button
        //                         $('.save_close_btn').removeAttr('disabled');
        //                     }
        //                 },
        //                 {
        //                     text: _t("保存 & 关闭"), classes: 'btn-primary save_close_btn', close: true,
        //                     click: function () {
        //                         var img_data_base64 = img_data.split(',')[1];
        //
        //                         /*
        //                             Size in base64 is approx 33% overhead the original data size.
        //
        //                             Source: -> http://stackoverflow.com/questions/11402329/base64-encoded-image-size
        //                                     -> http://stackoverflow.com/questions/6793575/estimating-the-size-of-binary-data-encoded-as-a-b64-string-in-python
        //
        //                                     -> https://en.wikipedia.org/wiki/Base64
        //                                     [ The ratio of output bytes to input bytes is 4:3 (33% overhead).
        //                                     Specifically, given an input of n bytes, the output will be "4[n/3]" bytes long in base64,
        //                                     including padding characters. ]
        //                         */
        //
        //                         // From the above info, we doing the opposite stuff to find the approx size of Image in bytes.
        //                         var approx_img_size = 3 * (img_data_base64.length / 4)  // like... "3[n/4]"
        //
        //                         // Upload image in Binary Field
        //                         self.on_file_uploaded(approx_img_size, "web-cam-preview.jpeg", "image/jpeg", img_data_base64);
        //                     }
        //                 },
        //                 {
        //                     text: "关闭", close: true
        //                 }
        //             ]
        //         }).open();
        //
        //
        //     // self.do_action({
        //     //     name: _t('Attachment Management'),
        //     //     type: 'ir.actions.act_window',
        //     //     res_model: 'ir.attachment',
        //     //     domain: [
        //     //         '&',
        //     //         ['res_model', '=', self.dataset.model],
        //     //         ['res_id', '=', self.model_id]
        //     //     ],
        //     //     view_mode: 'tree,form',
        //     //     view_type: 'form',
        //     //     views: [
        //     //         [false, 'list'],
        //     //         [false, 'form']
        //     //     ],
        //     //     context: {
        //     //         'default_res_model': self.dataset.model,
        //     //         'default_res_id': self.model_id
        //     //     }
        //     // });
        //
        //
        //   //  evt.preventDefault();
        // });

    }
});

});