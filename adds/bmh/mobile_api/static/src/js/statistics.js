function format (num) {
    return (num.toFixed(2) + '').replace(/\d{1,3}(?=(\d{3})+(\.\d*)?$)/g, '$&,');
}
$(function(){



var dom = document.getElementById("container");
var myChart = echarts.init(dom);
var app = {};
option = null;

var geoCoordMap = {

    "山盆镇":[106.675959,27.935679],
    "董公寺镇":[106.930924,27.785711],
    "团泽镇":[107.091922,27.811891],
    "高坪镇":[106.915117,27.822784],
    "板桥镇":[106.919698,27.977482],
    "泗渡镇":[106.943531,27.920345],
    "山盆镇":[106.676009,27.935678],
    "芝麻镇":[106.663374,27.889091],
    "沙湾镇":[106.82473,27.869565],
    "毛石镇":[106.738697,27.818297],
    "松林镇":[106.72294,27.727034],
    "市区":[106.939548,27.756305]
};

var data = [

    {name: "山盆镇", value: 2},
    {name: "董公寺镇", value: 13},
    {name: "团泽镇", value: 12},
    {name: "高坪镇", value: 14},
    {name: "板桥镇", value: 15},
    {name: "泗渡镇", value: 8},
    {name: "芝麻镇", value: 16},
    {name: "沙湾镇", value: 6},
    {name: "毛石镇", value: 17},
    {name: "松林镇", value: 10},
    {name: "市区", value: 4}
];

var todaydata = [

     {name: "山盆镇", value: 2},
    {name: "董公寺镇", value: 13},
    {name: "团泽镇", value: 12},
    {name: "高坪镇", value: 14},
    {name: "板桥镇", value: 15},
    {name: "泗渡镇", value: 8},
    {name: "芝麻镇", value: 16},
    {name: "沙湾镇", value: 6},
    {name: "毛石镇", value: 17},
    {name: "松林镇", value: 10},
    {name: "市区", value: 4}
];

var convertData = function (data,n) {
    var res = [];
    for (var i = 0; i < data.length; i++) {
        var geoCoord = geoCoordMap[data[i].name];
        if (geoCoord) {
            console.log(data[i].value)
            res.push({
                name: data[i].name,
                value: geoCoord.concat(data[i].value)
            });
        }
    }

    return res;
};

var convertedData = [
    convertData(data,100),
    convertData(data.sort(function (a, b) {
        return b.value - a.value;
    },100).slice(0, 15))
];
console.log("convertedData");
console.log(convertedData);

option = {
    backgroundColor: '#404a59',
    animation: true,
    animationDuration: 1000,
    animationEasing: 'cubicInOut',
    animationDurationUpdate: 1000,
    animationEasingUpdate: 'cubicInOut',
    title: [
        {
            text: '汇川区中小学图书室管理平台',
            subtext: '数据来源 涵雨淇在线图书馆',
            sublink: 'http://www.zyhanyuqi.com',
            left: 'center',
            textStyle: {
                color: '#fff'
            }
        },
        {
            id: 'statistic',
            right: 120,
            top: 40,
            width: 100,
            textStyle: {
                color: '#fff',
                fontSize: 16
            }
        }
    ],
    visualMap: [{
        min: 0,
        max: 100,
        left: 'left',
        top: 'bottom',
        text: ['高','低'],           // 文本，默认为数值文本
        calculable: true
    }],
    toolbox: {
        iconStyle: {
            normal: {
                borderColor: '#fff'
            },
            emphasis: {
                borderColor: '#b1e4ff'
            }
        }
    },

    bmap: {
        center: [106.972749,27.858296],
        zoom: 12,
        roam: false,
        click:false,
        mapStyle: {
            'styleJson': [
                {
                    'featureType': 'water',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#031628'
                    }
                },
                {
                    'featureType': 'land',
                    'elementType': 'geometry',
                    'stylers': {
                        'color': '#000102'
                    }
                },
                {
                    'featureType': 'highway',
                    'elementType': 'all',
                    'stylers': {
                        'visibility': 'off'
                    }
                },

                {
                    'featureType': 'arterial',
                    'elementType': 'geometry.fill',
                    'stylers': {
                        'visibility': 'off',
                        'color': '#000000'
                    }
                },
                {
                    'featureType': 'arterial',
                    'elementType': 'geometry.stroke',
                    'stylers': {

                        'color': '#0b3d51'
                    }
                },
                {
                    'featureType': 'local',
                    'elementType': 'geometry',
                    'stylers': {

                        'color': '#000000'
                    }
                },
                {
                    'featureType': 'railway',
                    'elementType': 'geometry.fill',
                    'stylers': {
                        'color': '#000000',


                    }
                },
                {
                    'featureType': 'park',
                    'elementType': 'labels',
                    'stylers': {
                        'color': '#000000',


                    }
                },
                {
                    'featureType': 'railway',
                    'elementType': 'geometry.stroke',
                    'stylers': {
                        'color': '#08304b',

                    }
                },
                {
                    'featureType': 'subway',
                    'elementType': 'geometry',
                    'stylers': {

                        'lightness': -170
                    }
                },
                {
                    'featureType': 'building',
                    'elementType': 'geometry.fill',
                    'stylers': {
                        'visibility': 'off',
                        'color': '#000000'
                    }
                },
                {
                    'featureType': 'all',
                    'elementType': 'labels.text.fill',
                    'stylers': {
                           'visibility': 'off',
                        'color': '#857f7f'
                    }
                },
                {
                    'featureType': 'all',
                    'elementType': 'labels.text.stroke',
                    'stylers': {

                        'color': '#000000'
                    }
                },
                {
                    'featureType': 'all',
                    'elementType': 'labels.icon',
                    'stylers': {
                    'visibility': 'off',
                        'color': '#000000'
                    }
                },
                {
                    'featureType': 'building',
                    'elementType': 'geometry',
                    'stylers': {

                        'color': '#022338'
                    }
                },
                {
                    'featureType': 'green',
                    'elementType': 'geometry',
                    'stylers': {
                        'color': '#062032'
                    }
                },
                {
                    'featureType': 'boundary',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#465b6c'
                    }
                },
                {
                    'featureType': 'manmade',
                    'elementType': 'all',
                    'stylers': {
                        'visibility': 'off',
                        'color': '#022338'
                    }
                },

                 {
				                    "featureType": "poi",
				                    "elementType": "labels",

				                    "stylers": {

				                              "visibility": "off"
				                    }
				          }
            ]
        }
    },

    tooltip : {
        trigger: 'item',
        alwaysShowContent:false,
        showContent:false,
        enterable:false,
        triggerOn:'click',
        formatter:function (params) {
            console.log(params);
            if(params.value[2]!=undefined){
                return "<span class='box'><h4>"+params.name+"</h4>"+
                    "藏书量：" + params.value[2]+"册</br>"+
                    "学生数："+ params.value[5]+"人</br>"+
                    "生均："+ Math.round(params.value[2]/params.value[5])+"册</br>"+
                    "借阅率："+ params.value[3]+"‰</br>"+
                    '今日借还 : ' + params.value[4]+"本</br><s class='s'><i class='i'></i></s></span>";
            }
            return  params.value;
    },
       position:'top'
    },
    grid: {
        right: 40,
        top: 100,
        bottom: 40,
        width: '20%'
    },
    xAxis: {
        type: 'value',
        scale: true,
        position: 'top',
        boundaryGap: false,
        splitLine: {show: false},
        axisLine: {show: false},
        axisTick: {show: false},
        axisLabel: {margin: 2, textStyle: {color: '#aaa'}},
    },
    yAxis: {
        type: 'category',
        name: 'TOP 20 年平均借阅率(%)',
        nameGap: 19,
        axisLine: {show: false, lineStyle: {color: '#ddd'}},
        axisTick: {show: false, lineStyle: {color: '#ddd'}},
        axisLabel: {interval: 0, textStyle: {color: '#ddd'}},
        data: []
    },

    series : [
        {
            name: 'pm2.5',
            type: 'scatter',
            coordinateSystem: 'bmap',
            data: convertedData[0],
            //symbolSize: 60,
            symbolSize: function (val) {
                //alert()
                return Math.max(val[4] / 10, 8);
            },
            label: {
                normal: {
                    formatter: function (params) {
                    return params.name ;
                },

                       //     '{b}/日活：{c0}',
                    position: 'right',
                    show: false
                },
                emphasis: {
                    show: true
                }
            },
            itemStyle: {
                normal: {
                    color: '#14e925',
                    shadowBlur: 10,
                    shadowColor: '#333'
                }
            }

        },
        {
            name: 'Top 5',
            type: 'effectScatter',
            coordinateSystem: 'bmap',
            data: convertedData[1],
            symbolSize: function (val) {
                return Math.max(35, 12);
            },
            showEffectOn: 'emphasis',
            rippleEffect: {
                brushType: 'stroke'
            },
            hoverAnimation: true,
            label: {
                normal: {
                    formatter: function (params) {
                    return params.name ;
                    },
                    position: 'right',
                    show: true
                }
            },
            itemStyle: {
                normal: {
                    color: '#14e925',
                    shadowBlur: 10,
                    shadowColor: '#333'
                }
            },
            zlevel: 5
        },
        {
            id: 'bar',
            zlevel: 2,
            type: 'bar',
            symbol: 'none',
            itemStyle: {
                normal: {
                    color: '#fff'
                }
            },
            data: []
        }
    ]
};
console.log("myChart.map")
    console.log(myChart)
//myChart.on('brushselected', renderBrushed);
//    myChart.on('click', renderClick);
//
////myChart.on(option.EVENT.CLICK, renderClick);
//    function renderClick(params){
//        //componentType: "series", componentSubType: "bar", seriesType: "bar", seriesIndex: 2, seriesName:
//        console.log(params)
//
//    }




function renderBrushed(params) {
    var mainSeries = params.batch[0].selected[0];

    console.log(mainSeries)
    var selectedItems = [];
    var categoryData = [];
    var barData = [];
    var maxBar = 30;
    var sum = 0;
    var count = 0;

    for (var i = 0; i < mainSeries.dataIndex.length; i++) {
        var rawIndex = mainSeries.dataIndex[i];
        var dataItem = convertedData[0][rawIndex];
        var pmValue = dataItem.value[2];

        sum += pmValue;
        count++;

        selectedItems.push(dataItem);
    }
    console.log("selectedItems")
    console.log(selectedItems)

    selectedItems.sort(function (a, b) {
        return a.value[2] - b.value[2];
    });

    for (var i = 0; i < Math.min(selectedItems.length, maxBar); i++) {
        categoryData.push(selectedItems[i].name);
        barData.push(selectedItems[i].value[2]);
    }


    this.setOption({
        yAxis: {
            data: categoryData
        },
        xAxis: {
            axisLabel: {show: !!count}
        },
        title: {
            id: 'statistic',
            text: count ? '年平均借阅率%: ' + (sum / count).toFixed(4) : ''
        },
        series: {
            id: 'bar',
            data: barData
        }
    });
};



    function renderBrushed2(params,myChart) {
   // var mainSeries = params.batch[0].selected[0];

   // console.log(mainSeries)
    var selectedItems = [];
    var categoryData = [];
    var barData = [];
    var maxBar = 30;
    var sum = 0;
    var count = 0;
//
//    for (var i = 0; i < mainSeries.dataIndex.length; i++) {
//        var rawIndex = mainSeries.dataIndex[i];
//        var dataItem = convertedData[0][rawIndex];
//        var pmValue = dataItem.value[2];
//
//        sum += pmValue;
//        count++;
//
//        selectedItems.push(dataItem);
//    }
//
//    selectedItems.sort(function (a, b) {
//        return a.value[2] - b.value[2];
//    });

        selectedItems = params;
    for (var i = 0; i < Math.min(selectedItems.length, maxBar); i++) {
        categoryData.push(selectedItems[i].name);
        barData.push(selectedItems[i].value[3]);
    }


    myChart.setOption({
        yAxis: {
            data: categoryData
        },
        xAxis: {
            axisLabel: {show: !!count}
        },
        title: {
            id: 'statistic',
            text: count ? '年平均借阅率%: ' + (sum / count).toFixed(4) : ''
        },
        series: {
            id: 'bar',
            data: barData
        }
    });
};





if (option && typeof option === "object") {
   myChart.setOption(option, true);

myChart.on('click', function (params) {

    if(params.seriesIndex==2)
    {
        return false;
    }

    var city = params.name;
    var city_id=params.data.value[2]
    window.location.href='/statistics/town/'+city_id
    //console.log(params.data.value[2])
    //loadChart(city);
});




    $.get('http://114.215.82.219:8081/api/library/statistics').done(function (data) {
         var dataArray=eval("("+data+")");


        //top20
   var data2 =  dataArray.sort(function (a, b) {
        return b.value[3] - a.value[3];
    }).slice(0, 20);


       // option.series[1].data=data1;
         renderBrushed2(data2,myChart)
         maxBar=20
         categoryData=[]
          barData=[]
        var count=0
        var sum=0
         for (var i = 0; i < Math.min(data2.length, maxBar); i++) {
             count++;
            categoryData.unshift(data2[i].name);
            barData.unshift(data2[i].value[3]);
             sum+=data2[i].value[3];
        }



        option.title[1].text=count ? '全区年平均借阅率: ' + (sum / count).toFixed(2) +"%\n": '';
        option.series[2].data=barData;
         option.yAxis.data=categoryData
         myChart.setOption(option,true);


        var htmls='<button class="previewAll" onclick="gotopreview();">全区预览</button>';
               // $(htmls).insertBefore('#container');
         $('#container').append($(htmls));

//        $.get('http://114.215.82.219:8069/api/library/statistics2').done(function (data) {
//
//
//            var htmls='<div class="infoTip"></div>';
//  //  $(htmls).insertBefore('#container');
//
//           // $('.ec-extension-bmap').append($(htmls));
//
//
//           // var datar=eval("("+data+")");
//           // var htmlr='<p>总图书册书:'+format(datar['book_amounts'])+'册</br>总学生数:'+format(datar['students_amounts'])+'人</br>总生均册数:'+format(datar['avg_books'])+'册/人</p>'
//
//            $(".infoTip").append($(htmlr));
//
//    });





     });


//       setInterval(function () {
//    // 异步加载数据
//    $.get('http://localhost:8001/api/library/statistics').done(function (data) {
//        console.log(data)
//       // data.shift();
//    //  console.log(data);
//        option.series[0].data=data[0];
//        option.xAxis.data=data[0];
//        console.log(myChart.getOption);
//      //  data[0]['value']++;
//      //  myChart.setOption(option, true);
//        // 填入数据
//        myChart.setOption(option);
//
//    });
//    }, 5000);
 //   setInterval(function () {
//        addData(true);
//        myChart.setOption({
//            xAxis: {
//                data: date
//            },
//            series: [{
//                name:'成交',
//                data: data
//            }]
//        });
 //       myChart.setOption(option, true);
//    }, 10000);
//http://blog.csdn.net/ID_Kong/article/details/50722312
    //http://blog.csdn.net/yc_1993/article/details/52432005?mType=Group
    //http://doc.okbase.net/wzgj/archive/251763.html
    //http://blog.csdn.net/kenhins/article/details/43273621





//            var htmls='<div class="previewAll">22222222</div>';
//
//            $(".infoTip").append($(htmls));




    //http://echarts.baidu.com/option.html#title 文档
}
})

function gotopreview(){
    window.location.href='/statistics/all';

}