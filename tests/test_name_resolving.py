import unittest
from unittest.mock import MagicMock, call

import sys
sys.path.insert(0, '..')
from pyhomematic import HMConnection
import time

import logging
FORMAT = "[%(filename)10s:%(lineno)5s - %(funcName)10s() ] %(message)s"
#logging.basicConfig(format=FORMAT, level=logging.DEBUG)


class TestNameResolving(unittest.TestCase):
    def setUp(self):
        pyhm = HMConnection(interface_id="myserver",
                                   autostart=False,
                                   systemcallback=False,
                                   remotes={"wired":{
                                       "resolvenames":"json",
                                       "username":"nobody",
                                       "password":"nix",
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
    def test_single_dev(self):
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

        def jsonRpcPost(ip, funcname, *args):
#            print(ip, funcname)
            if funcname == 'Session.login':
                return {'error': None, 'id': 0, 'result': 'Q90KKhFQ48', 'version': '1.1'}
            elif funcname == 'Interface.listInterfaces':
                return {'error': None,
                         'id': 0,
                         'result': [{'info': 'BidCoS-Wired', 'name': 'BidCos-Wired', 'port': 2000},
                                    {'info': 'BidCos-RF', 'name': 'BidCos-RF', 'port': 2001},
                                    {'info': 'Virtual Devices', 'name': 'VirtualDevices', 'port': 9292},
                                    {'info': 'HmIP-RF', 'name': 'HmIP-RF', 'port': 2010}],
                         'version': '1.1'}
            elif funcname == 'Session.logout':
                return {'error': None,
                         'id': 0,
                         'version': '1.1'}
            elif funcname == 'Device.listAllDetail':
                return {'error': None,
                         'id': 0,
                         'result': [
                                    {'address': 'LEQ1181667',
                                     'channels': [{'address': 'LEQ1181667:1',
                                                   'category': 'CATEGORY_SENDER',
                                                   'channelType': 'KEY',
                                                   'deviceId': '1875',
                                                   'id': '1889',
                                                   'index': 1,
                                                   'isAesAvailable': False,
                                                   'isEventable': True,
                                                   'isLogable': True,
                                                   'isLogged': True,
                                                   'isReadable': False,
                                                   'isReady': True,
                                                   'isUsable': True,
                                                   'isVirtual': False,
                                                   'isVisible': True,
                                                   'isWritable': True,
                                                   'mode': 'MODE_DEFAULT',
                                                   'name': 'Kanal1',
                                                   'partnerId': ''},
                                                  {'address': 'LEQ1181667:2',
                                                   'category': 'CATEGORY_SENDER',
                                                   'channelType': 'KEY',
                                                   'deviceId': '1875',
                                                   'id': '1893',
                                                   'index': 2,
                                                   'isAesAvailable': False,
                                                   'isEventable': True,
                                                   'isLogable': True,
                                                   'isLogged': True,
                                                   'isReadable': False,
                                                   'isReady': True,
                                                   'isUsable': True,
                                                   'isVirtual': False,
                                                   'isVisible': True,
                                                   'isWritable': True,
                                                   'mode': 'MODE_DEFAULT',
                                                   'name': 'Kanal2',
                                                   'partnerId': ''},
                                                  {'address': 'LEQ1181667:3',
                                                   'category': 'CATEGORY_RECEIVER',
                                                   'channelType': 'BLIND',
                                                   'deviceId': '1875',
                                                   'id': '1897',
                                                   'index': 3,
                                                   'isAesAvailable': False,
                                                   'isEventable': True,
                                                   'isLogable': True,
                                                   'isLogged': True,
                                                   'isReadable': True,
                                                   'isReady': True,
                                                   'isUsable': True,
                                                   'isVirtual': False,
                                                   'isVisible': True,
                                                   'isWritable': True,
                                                   'mode': 'MODE_DEFAULT',
                                                   'name': 'Kanal3',
                                                   'partnerId': ''}],
                                     'id': '1875',
                                     'interface': 'BidCos-Wired',
                                     'name': 'Hauptgerät',
                                     'operateGroupOnly': 'false',
                                     'type': 'HMW-LC-Bl1-DR'}
                                     ],
                         'version': '1.1'}

        self.rpc.jsonRpcPost = jsonRpcPost
        self.rpc.newDevices('myserver-wired', description)

        # for addr,dev in self.pyhm.devices['wired'].items():
        #     print("%-21s (%15s) %s"%(dev.ADDRESS, dev.NAME, type(dev)))
        #     for channelid, channel in dev.CHANNELS.items():
        #         print("  |-- %-15s (%15s) %s"%(channel.ADDRESS, channel.NAME, type(channel)))

        dev = self.pyhm.devices['wired']['LEQ1181667']
        for idx, name in enumerate(['LEQ1181667:0', 'Kanal1', 'Kanal2', 'Kanal3']):
            self.assertEqual(dev.CHANNELS[idx].NAME, name)



#        print(jsonRpcPost.method_calls)


if __name__ == '__main__':
    unittest.main()
