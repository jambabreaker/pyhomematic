import unittest
from unittest.mock import MagicMock, call

import sys
sys.path.insert(0, '..')
from pyhomematic import HMConnection
import time

import logging
FORMAT = "[%(filename)10s:%(lineno)5s - %(funcName)10s() ] %(message)s"
#logging.basicConfig(format=FORMAT, level=logging.INFO)


class TestDevs(unittest.TestCase):
    def setUp(self):
        pyhm = HMConnection(interface_id="myserver",
                                   autostart=False,
                                   systemcallback=False,
                                   remotes={"wired":{
                                       "resolvenames":"none",
                                       "ip":"192.168.178.126",
                                       "port": 2000}})
        proxy = MagicMock()
        proxy._localip = "0.0.0.0"
        pyhm._server._localport = 110
        pyhm._server.proxies['myserver-wired'] = proxy
        rpc = pyhm._server._rpcfunctions
        rpc._proxies = pyhm._server.proxies

        pyhm.start()
        proxy.init.assert_called_with("http://0.0.0.0:110", 'myserver-wired')
        self.pyhm = pyhm
        self.rpc = rpc
        self.proxy = proxy
    def tearDown(self):
        self.pyhm.stop()
    def test_blinds(self):
        #Now we emulate CCU init
        self.rpc.listDevices('myserver-wired')
        description = [
            {'AVAILABLE_FIRMWARE': '3.06', 'TYPE': 'HMW-LC-Bl1-DR', 'VERSION': 14, 'ADDRESS': 'LEQ1181667', 'FLAGS': 1, 'FIRMWARE': '3.06', 'UPDATABLE': 1, 'PARENT': '', 'PARAMSETS': ['MASTER'], 'CHILDREN': ['LEQ1181667:0', 'LEQ1181667:1', 'LEQ1181667:2', 'LEQ1181667:3']}
            ,
            {'PARENT_TYPE': 'HMW-LC-Bl1-DR', 'PARENT': 'LEQ1181667', 'DIRECTION': 0, 'PARAMSETS': ['MASTER', 'VALUES'], 'FLAGS': 3, 'AES_ACTIVE': 0, 'TYPE': 'MAINTENANCE', 'INDEX': 0, 'LINK_SOURCE_ROLES': '', 'LINK_TARGET_ROLES': '', 'VERSION': 14, 'ADDRESS': 'LEQ1181667:0'}
            ,
            {'PARENT_TYPE': 'HMW-LC-Bl1-DR', 'PARENT': 'LEQ1181667', 'DIRECTION': 1, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'KEY', 'INDEX': 1, 'LINK_SOURCE_ROLES': 'SWITCH', 'LINK_TARGET_ROLES': '', 'VERSION': 14, 'ADDRESS': 'LEQ1181667:1'}
            ,
            {'PARENT_TYPE': 'HMW-LC-Bl1-DR', 'PARENT': 'LEQ1181667', 'DIRECTION': 1, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'KEY', 'INDEX': 2, 'LINK_SOURCE_ROLES': 'SWITCH', 'LINK_TARGET_ROLES': '', 'VERSION': 14, 'ADDRESS': 'LEQ1181667:2'}
            ,
            {'PARENT_TYPE': 'HMW-LC-Bl1-DR', 'PARENT': 'LEQ1181667', 'DIRECTION': 2, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'BLIND', 'INDEX': 3, 'LINK_SOURCE_ROLES': '', 'LINK_TARGET_ROLES': 'SWITCH', 'VERSION': 14, 'ADDRESS': 'LEQ1181667:3'}
        ]
        self.rpc.newDevices('myserver-wired', description)


        dev = self.pyhm.devices['wired']['LEQ1181667']
        dev.get_level()
        self.proxy.getValue.assert_called_with('LEQ1181667:3', 'LEVEL')
        dev.set_level(0.6)
        self.proxy.setValue.assert_called_with('LEQ1181667:3', 'LEVEL', 0.6)
        dev.move_up()
        self.proxy.setValue.assert_called_with('LEQ1181667:3', 'LEVEL', 1.0)
        dev.move_down()
        self.proxy.setValue.assert_called_with('LEQ1181667:3', 'LEVEL', 0.0)
        dev.stop()
        self.proxy.setValue.assert_called_with('LEQ1181667:3', 'STOP', True)

    def test_contact(self):
        self.rpc.listDevices('myserver-wired')
        description = [
{'PARAMSETS': ['MASTER'], 'FIRMWARE': '3.01', 'PARENT': '', 'ADDRESS': 'KEQ0054656', 'VERSION': 7, 'UPDATABLE': 1, 'AVAILABLE_FIRMWARE': '3.01', 'FLAGS': 1, 'TYPE': 'HMW-Sen-SC-12-DR', 'CHILDREN': ['KEQ0054656:0', 'KEQ0054656:1', 'KEQ0054656:2', 'KEQ0054656:3', 'KEQ0054656:4', 'KEQ0054656:5', 'KEQ0054656:6', 'KEQ0054656:7', 'KEQ0054656:8', 'KEQ0054656:9', 'KEQ0054656:10', 'KEQ0054656:11', 'KEQ0054656:12']},
{'PARENT': 'KEQ0054656', 'INDEX': 0, 'FLAGS': 3, 'TYPE': 'MAINTENANCE', 'AES_ACTIVE': 0, 'PARAMSETS': ['MASTER', 'VALUES'], 'LINK_TARGET_ROLES': '', 'LINK_SOURCE_ROLES': '', 'ADDRESS': 'KEQ0054656:0', 'VERSION': 7, 'DIRECTION': 0, 'PARENT_TYPE': 'HMW-Sen-SC-12-DR'},
{'PARENT': 'KEQ0054656', 'INDEX': 1, 'FLAGS': 1, 'TYPE': 'SENSOR', 'AES_ACTIVE': 0, 'PARAMSETS': ['MASTER', 'VALUES'], 'LINK_TARGET_ROLES': '', 'LINK_SOURCE_ROLES': '', 'ADDRESS': 'KEQ0054656:1', 'VERSION': 7, 'DIRECTION': 0, 'PARENT_TYPE': 'HMW-Sen-SC-12-DR'},
{'PARENT': 'KEQ0054656', 'INDEX': 2, 'FLAGS': 1, 'TYPE': 'SENSOR', 'AES_ACTIVE': 0, 'PARAMSETS': ['MASTER', 'VALUES'], 'LINK_TARGET_ROLES': '', 'LINK_SOURCE_ROLES': '', 'ADDRESS': 'KEQ0054656:2', 'VERSION': 7, 'DIRECTION': 0, 'PARENT_TYPE': 'HMW-Sen-SC-12-DR'},
{'PARENT': 'KEQ0054656', 'INDEX': 3, 'FLAGS': 1, 'TYPE': 'SENSOR', 'AES_ACTIVE': 0, 'PARAMSETS': ['MASTER', 'VALUES'], 'LINK_TARGET_ROLES': '', 'LINK_SOURCE_ROLES': '', 'ADDRESS': 'KEQ0054656:3', 'VERSION': 7, 'DIRECTION': 0, 'PARENT_TYPE': 'HMW-Sen-SC-12-DR'},
{'PARENT': 'KEQ0054656', 'INDEX': 4, 'FLAGS': 1, 'TYPE': 'SENSOR', 'AES_ACTIVE': 0, 'PARAMSETS': ['MASTER', 'VALUES'], 'LINK_TARGET_ROLES': '', 'LINK_SOURCE_ROLES': '', 'ADDRESS': 'KEQ0054656:4', 'VERSION': 7, 'DIRECTION': 0, 'PARENT_TYPE': 'HMW-Sen-SC-12-DR'},
{'PARENT': 'KEQ0054656', 'INDEX': 5, 'FLAGS': 1, 'TYPE': 'SENSOR', 'AES_ACTIVE': 0, 'PARAMSETS': ['MASTER', 'VALUES'], 'LINK_TARGET_ROLES': '', 'LINK_SOURCE_ROLES': '', 'ADDRESS': 'KEQ0054656:5', 'VERSION': 7, 'DIRECTION': 0, 'PARENT_TYPE': 'HMW-Sen-SC-12-DR'},
{'PARENT': 'KEQ0054656', 'INDEX': 6, 'FLAGS': 1, 'TYPE': 'SENSOR', 'AES_ACTIVE': 0, 'PARAMSETS': ['MASTER', 'VALUES'], 'LINK_TARGET_ROLES': '', 'LINK_SOURCE_ROLES': '', 'ADDRESS': 'KEQ0054656:6', 'VERSION': 7, 'DIRECTION': 0, 'PARENT_TYPE': 'HMW-Sen-SC-12-DR'},
{'PARENT': 'KEQ0054656', 'INDEX': 7, 'FLAGS': 1, 'TYPE': 'SENSOR', 'AES_ACTIVE': 0, 'PARAMSETS': ['MASTER', 'VALUES'], 'LINK_TARGET_ROLES': '', 'LINK_SOURCE_ROLES': '', 'ADDRESS': 'KEQ0054656:7', 'VERSION': 7, 'DIRECTION': 0, 'PARENT_TYPE': 'HMW-Sen-SC-12-DR'},
{'PARENT': 'KEQ0054656', 'INDEX': 8, 'FLAGS': 1, 'TYPE': 'SENSOR', 'AES_ACTIVE': 0, 'PARAMSETS': ['MASTER', 'VALUES'], 'LINK_TARGET_ROLES': '', 'LINK_SOURCE_ROLES': '', 'ADDRESS': 'KEQ0054656:8', 'VERSION': 7, 'DIRECTION': 0, 'PARENT_TYPE': 'HMW-Sen-SC-12-DR'},
{'PARENT': 'KEQ0054656', 'INDEX': 9, 'FLAGS': 1, 'TYPE': 'SENSOR', 'AES_ACTIVE': 0, 'PARAMSETS': ['MASTER', 'VALUES'], 'LINK_TARGET_ROLES': '', 'LINK_SOURCE_ROLES': '', 'ADDRESS': 'KEQ0054656:9', 'VERSION': 7, 'DIRECTION': 0, 'PARENT_TYPE': 'HMW-Sen-SC-12-DR'},
{'PARENT': 'KEQ0054656', 'INDEX': 10, 'FLAGS': 1, 'TYPE': 'SENSOR', 'AES_ACTIVE': 0, 'PARAMSETS': ['MASTER', 'VALUES'], 'LINK_TARGET_ROLES': '', 'LINK_SOURCE_ROLES': '', 'ADDRESS': 'KEQ0054656:10', 'VERSION': 7, 'DIRECTION': 0, 'PARENT_TYPE': 'HMW-Sen-SC-12-DR'},
{'PARENT': 'KEQ0054656', 'INDEX': 11, 'FLAGS': 1, 'TYPE': 'SENSOR', 'AES_ACTIVE': 0, 'PARAMSETS': ['MASTER', 'VALUES'], 'LINK_TARGET_ROLES': '', 'LINK_SOURCE_ROLES': '', 'ADDRESS': 'KEQ0054656:11', 'VERSION': 7, 'DIRECTION': 0, 'PARENT_TYPE': 'HMW-Sen-SC-12-DR'},
{'PARENT': 'KEQ0054656', 'INDEX': 12, 'FLAGS': 1, 'TYPE': 'SENSOR', 'AES_ACTIVE': 0, 'PARAMSETS': ['MASTER', 'VALUES'], 'LINK_TARGET_ROLES': '', 'LINK_SOURCE_ROLES': '', 'ADDRESS': 'KEQ0054656:12', 'VERSION': 7, 'DIRECTION': 0, 'PARENT_TYPE': 'HMW-Sen-SC-12-DR'},
            ]
        self.rpc.newDevices('myserver-wired', description)
        dev = self.pyhm.devices['wired']['KEQ0054656']
        for channel in range(12):
            dev.is_open(channel)
            self.proxy.getValue.assert_called_with('KEQ0054656:%d'%channel, 'SENSOR')

#        print(self.proxy.method_calls)
    def test_switch(self):

        #Now we emulate CCU init
        self.rpc.listDevices('myserver-wired')
        description = [
            {'AVAILABLE_FIRMWARE': '3.06', 'TYPE': 'HMW-IO-12-Sw7-DR', 'VERSION': 11, 'ADDRESS': 'MEQ0064363', 'FLAGS': 1, 'FIRMWARE': '3.06', 'UPDATABLE': 1, 'PARENT': '', 'PARAMSETS': ['MASTER'], 'CHILDREN': ['MEQ0064363:0', 'MEQ0064363:1', 'MEQ0064363:2', 'MEQ0064363:3', 'MEQ0064363:4', 'MEQ0064363:5', 'MEQ0064363:6', 'MEQ0064363:7', 'MEQ0064363:8', 'MEQ0064363:9', 'MEQ0064363:10', 'MEQ0064363:11', 'MEQ0064363:12', 'MEQ0064363:13', 'MEQ0064363:14', 'MEQ0064363:15', 'MEQ0064363:16', 'MEQ0064363:17', 'MEQ0064363:18', 'MEQ0064363:19']},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 0, 'PARAMSETS': ['MASTER', 'VALUES'], 'FLAGS': 3, 'AES_ACTIVE': 0, 'TYPE': 'MAINTENANCE', 'INDEX': 0, 'LINK_SOURCE_ROLES': '', 'LINK_TARGET_ROLES': '', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:0'},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 1, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'KEY', 'INDEX': 1, 'LINK_SOURCE_ROLES': 'SWITCH', 'LINK_TARGET_ROLES': '', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:1'},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 1, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'KEY', 'INDEX': 2, 'LINK_SOURCE_ROLES': 'SWITCH', 'LINK_TARGET_ROLES': '', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:2'},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 1, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'KEY', 'INDEX': 3, 'LINK_SOURCE_ROLES': 'SWITCH', 'LINK_TARGET_ROLES': '', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:3'},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 1, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'KEY', 'INDEX': 4, 'LINK_SOURCE_ROLES': 'SWITCH', 'LINK_TARGET_ROLES': '', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:4'},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 1, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'KEY', 'INDEX': 5, 'LINK_SOURCE_ROLES': 'SWITCH', 'LINK_TARGET_ROLES': '', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:5'},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 1, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'KEY', 'INDEX': 6, 'LINK_SOURCE_ROLES': 'SWITCH', 'LINK_TARGET_ROLES': '', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:6'},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 1, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'KEY', 'INDEX': 7, 'LINK_SOURCE_ROLES': 'SWITCH', 'LINK_TARGET_ROLES': '', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:7'},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 1, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'KEY', 'INDEX': 8, 'LINK_SOURCE_ROLES': 'SWITCH', 'LINK_TARGET_ROLES': '', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:8'},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 1, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'KEY', 'INDEX': 9, 'LINK_SOURCE_ROLES': 'SWITCH', 'LINK_TARGET_ROLES': '', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:9'},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 1, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'KEY', 'INDEX': 10, 'LINK_SOURCE_ROLES': 'SWITCH', 'LINK_TARGET_ROLES': '', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:10'},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 1, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'KEY', 'INDEX': 11, 'LINK_SOURCE_ROLES': 'SWITCH', 'LINK_TARGET_ROLES': '', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:11'},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 1, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'KEY', 'INDEX': 12, 'LINK_SOURCE_ROLES': 'SWITCH', 'LINK_TARGET_ROLES': '', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:12'},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 2, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'SWITCH', 'INDEX': 13, 'LINK_SOURCE_ROLES': '', 'LINK_TARGET_ROLES': 'SWITCH', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:13'},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 2, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'SWITCH', 'INDEX': 14, 'LINK_SOURCE_ROLES': '', 'LINK_TARGET_ROLES': 'SWITCH', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:14'},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 2, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'SWITCH', 'INDEX': 15, 'LINK_SOURCE_ROLES': '', 'LINK_TARGET_ROLES': 'SWITCH', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:15'},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 2, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'SWITCH', 'INDEX': 16, 'LINK_SOURCE_ROLES': '', 'LINK_TARGET_ROLES': 'SWITCH', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:16'},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 2, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'SWITCH', 'INDEX': 17, 'LINK_SOURCE_ROLES': '', 'LINK_TARGET_ROLES': 'SWITCH', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:17'},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 2, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'SWITCH', 'INDEX': 18, 'LINK_SOURCE_ROLES': '', 'LINK_TARGET_ROLES': 'SWITCH', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:18'},
            {'PARENT_TYPE': 'HMW-IO-12-Sw7-DR', 'PARENT': 'MEQ0064363', 'DIRECTION': 2, 'PARAMSETS': ['LINK', 'MASTER', 'VALUES'], 'FLAGS': 1, 'AES_ACTIVE': 0, 'TYPE': 'SWITCH', 'INDEX': 19, 'LINK_SOURCE_ROLES': '', 'LINK_TARGET_ROLES': 'SWITCH', 'VERSION': 11, 'ADDRESS': 'MEQ0064363:19'}
            ]
        self.rpc.newDevices('myserver-wired', description)
        dev = self.pyhm.devices['wired']['MEQ0064363']

        for channel in range(13, 20):
            dev.on(channel)
            self.proxy.setValue.assert_called_with('MEQ0064363:%d'%channel, 'STATE', True)
            dev.off(channel)
            self.proxy.setValue.assert_called_with('MEQ0064363:%d'%channel, 'STATE', False)
            dev.is_on(channel)
            self.proxy.getValue.assert_called_with('MEQ0064363:%d'%channel, 'STATE')


if __name__ == '__main__':
    unittest.main()
