

pmodel={
    "LM":{
            "className": "LocationMark",
            "instanceName": "LM1",
            "pos": {
                "x": -73.491,
                "y": -41.442
            },
            "property": [
                {
                    "key": "spin",
                    "type": "bool",
                    "value": "ZmFsc2U=",
                    "boolValue": False
                }
            ],
            "ignoreDir": True
        },
    "PP": {
            "className": "ParkPoint",
            "instanceName": "PP2",
            "pos": {
                "x": -74.978,
                "y": -39.854
            },
            "property": [
                {
                    "key": "spin",
                    "type": "bool",
                    "value": "ZmFsc2U=",
                    "boolValue": False
                }
            ],
            "ignoreDir": True
        },
    "AP":{
            "className": "ActionPoint",
            "instanceName": "AP3",
            "pos": {
                "x": -73.491,
                "y": -39.854
            },
            "property": [
                {
                    "key": "spin",
                    "type": "bool",
                    "value": "ZmFsc2U=",
                    "boolValue": False
                }
            ],
            "ignoreDir": True
        },
    "CP": {
            "className": "ChargePoint",
            "instanceName": "CP4",
            "pos": {
                "x": -75.089,
                "y": -41.221
            },
            "property": [
                {
                    "key": "spin",
                    "type": "bool",
                    "value": "ZmFsc2U=",
                    "boolValue": False
                }
            ],
            "ignoreDir": True
        },
    "SM":{
            "className": "SwitchMap",
            "instanceName": "SM5",
            "pos": {
                "x": -72.04,
                "y": -39.854
            },
            "property": [
                {
                    "key": "spin",
                    "type": "bool",
                    "value": "ZmFsc2U=",
                    "boolValue": False
                }
            ]
        },
    "DegenerateBezier":{  # 高阶贝塞尔，两个控制点
            "className": "DegenerateBezier",
            "instanceName": "",
            "startPos": {
                "instanceName": "",
                "pos": {
                    "x": 0,
                    "y": 0
                }
            },
            "endPos": {
                "instanceName": "AP3",
                "pos": {
                    "x": 0,
                    "y": 0
                }
            },
            "controlPos1": {
                "x": 0,
                "y": 0
            },
            "controlPos2": {
                "x": 0,
                "y": 0
            },
            "property": [
                {
                    "key": "direction",
                    "type": "int",
                    "value": "MA==",
                    "int32Value": 0
                },
                {
                    "key": "movestyle",
                    "type": "int",
                    "value": "MA==",
                    "int32Value": 0
                }
            ]
        },
    "NURBS6":{"className": "NURBS6",  # "NURBS6" 四个控制点,点位坐标包含 x,y,z
            "instanceName": "",
            "startPos": {
                "instanceName": "",
                "pos": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                }
            },
            "endPos": {
                "instanceName": "",
                "pos": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                }
            },
            "controlPos1": {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "controlPos2": {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "property": [
                {
                    "key": "direction",
                    "type": "int",
                    "value": "MA==",
                    "int32Value": 0
                },
                {
                    "key": "movestyle",
                    "type": "int",
                    "value": "MA==",
                    "int32Value": 0
                }
            ],
            "controlPos3": {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "controlPos4": {
                "x": 0,
                "y": 0,
                "z": 0
            }
        },
    "BezierPath":{  # 三阶贝塞尔
        "className": "BezierPath",
        "instanceName": "",
        "startPos": {
            "instanceName": "",
            "pos": {
                "x": 0,
                "y": 0
            }
        },
        "endPos": {
            "instanceName": "",
            "pos": {
                "x": 0,
                "y": 0
            }
        },
        "controlPos1": {
            "x": 0,
            "y": 0
        },
        "controlPos2": {
            "x": 0,
            "y": 0
        },
        "property": [
            {
                "key": "direction",
                "type": "int",
                "value": "MA==",
                "int32Value": 0
            },
            {
                "key": "movestyle",
                "type": "int",
                "value": "MA==",
                "int32Value": 0
            }
        ]
    },
    "StraightPath":{
            "className": "StraightPath",  # 直线
            "instanceName": "",
            "startPos": {
                "instanceName": "",
                "pos": {
                    "x": 0,
                    "y": 0
                }
            },
            "endPos": {
                "instanceName": "",
                "pos": {
                    "x": 0,
                    "y": 0
                }
            },
            "property": [
                {
                    "key": "direction",
                    "type": "int",
                    "value": "MA==",
                    "int32Value": 0
                },
                {
                    "key": "movestyle",
                    "type": "int",
                    "value": "MA==",
                    "int32Value": 0
                }
            ]
        },
}