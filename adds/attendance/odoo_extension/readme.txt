1、开发backend的widget步骤：
	.1.设计widget模板，主要定义ui的layout模板。模板文件的路径随意，习惯上放在当前addon的static\src\xml目录下。本例文件为：static\src\xml\backend_template.xml
	.2.设计widget的js程序，主要定义如何渲染ui以及ui的交互行为。程序文件的路径必须位于当前addon的static\src\js目录下。本例文件为：static\src\js\backend.js
	.3.设计widget的qweb视图，主要是将当前设计的js和css文件路径注册到系统，以便web框架在运行时将其注入到backend框架的主页面内。本例文件为：backend_view.xml
	.4.将widget模板路径注册到addon内，以便web框架在运行时将widget模板从服务器读取到浏览器内

	调用例子：
		在form视图中加入如下语句：
			<widget type="map" options="{'longitude': 'geo_longitude', 'latitude': 'geo_latitude'}"/>
		解释：geo_longitude和geo_latitude是当前模型的field。

2、开发frontend的widget步骤：
	.1.设计widget视图。视图文件的路径随意。本例文件为：frontend_view.xml
	.2.设计widget的python渲染程序。本例文件为：frontend.py
	.3.由于python渲染程序是扩展服务器的qweb website框架，所以依赖于website addon，将这个信息加入到__openerp__.py的depends中，这可以保证服务器在加载本addon之前确保
		website已经被加载。

	调用例子：
		在qweb视图中加入如下语句：
			<div t-esc="room" t-esc-options='{"widget": "map", "fields": ["geo_longitude", "geo_latitude"]}'/>
		解释：geo_longitude和geo_latitude是模型实例room的field。