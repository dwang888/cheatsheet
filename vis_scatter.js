import React from 'react';
import echarts from 'echarts/lib/echarts';
// import echarts from 'echarts/dist/echarts.common';
import 'echarts/lib/chart/graph';//must import to activate certain type of chart
import 'echarts/lib/chart/scatter';
import 'echarts/lib/chart/line';
import 'echarts/lib/component/tooltip';
import 'echarts/lib/component/title';
import 'echarts/lib/chart/scatter';
//require('echarts/lib/component/tooltip');//another way of import
//require('echarts/lib/component/title');
// import 'dat.gui';
import * as dat from 'dat.gui';

let dataJson = require('./data/nutrients.json');
// console.log('12345');
export default class VisScatter extends React.Component {
    
    initChart(){
        let ct = echarts.init(document.getElementById('main'));
        return ct;
    };
    
    componentDidMount() {
        var indices = {
            name: 0,
            group: 1,
            id: 16
        };
        var schema = [
            {name: 'name', index: 0},
            {name: 'group', index: 1},
            {name: 'protein', index: 2},
            {name: 'calcium', index: 3},
            {name: 'sodium', index: 4},
            {name: 'fiber', index: 5},
            {name: 'vitaminc', index: 6},
            {name: 'potassium', index: 7},
            {name: 'carbohydrate', index: 8},
            {name: 'sugars', index: 9},
            {name: 'fat', index: 10},
            {name: 'water', index: 11},
            {name: 'calories', index: 12},
            {name: 'saturated', index: 13},
            {name: 'monounsat', index: 14},
            {name: 'polyunsat', index: 15},
            {name: 'id', index: 16}
        ];
        
        var fieldIndices = schema.reduce(function (obj, item) {
            obj[item.name] = item.index;
            return obj;
        }, {});
        
        var groupCategories = [];
        var groupColors = [];
        var data;
        // var app;

        function normalizeData(originData) {
            var groupMap = {};
            originData.forEach(function (row) {
                var groupName = row[indices.group];
                if (!groupMap.hasOwnProperty(groupName)) {
                    groupMap[groupName] = 1;
                }
            });
        
            originData.forEach(function (row) {
                row.forEach(function (item, index) {
                    if (index !== indices.name
                        && index !== indices.group
                        && index !== indices.id
                    ) {
                        // Convert null to zero, as all of them under unit "g".
                        row[index] = parseFloat(item) || 0;
                    }
                });
            });
        
            for (var groupName in groupMap) {
                if (groupMap.hasOwnProperty(groupName)) {
                    groupCategories.push(groupName);
                }
            }
            var hStep = Math.round(300 / (groupCategories.length - 1));
            for (var i = 0; i < groupCategories.length; i++) {
                groupColors.push(echarts.color.modifyHSL('#5A94DF', hStep * i));
            }
            
        
            return originData;
        }
        function getOption(data) {
            return {
                backgroundColor: '#2c343c',
                tooltip: {
                    padding: 10,
                    backgroundColor: '#222',
                    borderColor: '#777',
                    borderWidth: 1
                },
                xAxis: {
                    name: 'protein',
                    splitLine: {show: false},
                    axisLine: {
                        lineStyle: {
                            color: '#fff'
                        }
                    },
                    axisLabel: {
                        textStyle: {
                            color: '#fff'
                        }
                    },
                    axisTick: {
                        lineStyle: {
                            color: '#fff'
                        }
                    }
                },
                yAxis: {
                    name: 'calcium',
                    splitLine: {show: false},
                    axisLine: {
                        lineStyle: {
                            color: '#fff'
                        }
                    },
                    axisLabel: {
                        textStyle: {
                            color: '#fff'
                        }
                    },
                    axisTick: {
                        lineStyle: {
                            color: '#fff'
                        }
                    }
                },
                visualMap: [{
                    show: false,
                    type: 'piecewise',
                    categories: groupCategories,
                    dimension: 2,
                    inRange: {
                        color: groupColors //['#d94e5d','#eac736','#50a3ba']
                    },
                    outOfRange: {
                        color: ['#ccc'] //['#d94e5d','#eac736','#50a3ba']
                    },
                    top: 20,
                    textStyle: {
                        color: '#fff'
                    },
                    realtime: false
                }, {
                    show: false,
                    dimension: 3,
                    max: 1000,
                    inRange: {
                        colorLightness: [0.15, 0.6]
                    }
                }],
                series: [
                    {
                        zlevel: 1,
                        name: 'nutrients',
                        type: 'scatter',
                        data: data.map(function (item, idx) {
                            return [item[2], item[3], item[1], idx];
                        }),
                        animationThreshold: 5000,
                        progressiveThreshold: 5000
                    }
                ],
                animationEasingUpdate: 'cubicInOut',
                animationDurationUpdate: 2000
            };
        }

        var fieldNames = schema.map(function (item) {
            return item.name;
        }).slice(2);

///////////////////////////////////////////////
        var obj = {
            message: 'Please Select hazard and BCP',
            xAxis: 'calcium',
            yAxis: 'fiber',
            maxSize: 6.0,
            speed: 5,
            height: 10,
            noiseStrength: 10.2,
            growthSpeed: 0.2,
            reset: function () {window.alert('Bang!');
                },
        };
        var gui = new dat.gui.GUI();
        
        gui.add(obj, 'message');
        gui.add(obj, 'xAxis', ['protein','calcium', 'fiber']).onChange(function () {
            // window.alert(obj.xAxis + obj.yAxis);
              myChart.setOption({
                xAxis: {
                    name: obj.xAxis
                },
                yAxis: {
                    name: obj.yAxis
                },
                series: {
                    data: data.map(function (item, idx) {
                        return [
                            item[fieldIndices[obj.xAxis]],
                            item[fieldIndices[obj.yAxis]],
                            item[1],
                            idx
                        ];
                    })
                }
                });
            });
        gui.add(obj, 'yAxis', ['protein','calcium', 'fiber']).onChange(function () {
            // window.alert(obj.xAxis + obj.yAxis);
              myChart.setOption({
                xAxis: {
                    name: obj.xAxis
                },
                yAxis: {
                    name: obj.yAxis
                },
                series: {
                    data: data.map(function (item, idx) {
                        return [
                            item[fieldIndices[obj.xAxis]],
                            item[fieldIndices[obj.yAxis]],
                            item[1],
                            idx
                        ];
                    })
                }
                });
            });
        
        gui.add(obj, 'reset');
        gui.add(obj, 'maxSize').min(-10).max(10).step(0.25);
        gui.add(obj, 'height').step(5); // Increment amount
        gui.add(obj, 'speed', { Stopped: 0, Slow: 0.1, Fast: 5 } );


// //////////////////////////////////
        data = normalizeData(dataJson).slice(0, 1000);
        // let opt = getOption(data);
        let myChart = this.initChart();
        console.log('Successfully run: data normalization!');
        console.log('Successfully run: created option!');
        myChart.setOption(getOption(data));

    }

    render() {
        return (
            <div id="main" style={{ width: 800, height: 600 }}></div>
        );
    }

}
