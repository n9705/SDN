# -*- coding: utf-8 -*-
import httplib2
import time
import json
class OdlUtil:
	url = ''
	def __init__(self, host, port):
		self.url = 'http://' + host + ':' + str(port)
	def install_flow(self, container_name='default',username="admin", password="admin"):
		http = httplib2.Http()
		http.add_credentials(username, password)
		headers = {'Accept': 'application/json'}
		flow_name = 'flow_' + str(int(time.time()*1000))
		#s2流表
		#在检测h2发包的时候s2的1口流量空闲时发的流表
		h2_to_s2_1 ='{"flow": [{"id": "0","match": {"ethernet-match":'\
               		'{"ethernet-type": {"type": "2048"}},'\
					'"ipv4-source":"10.0.0.2/32","ipv4-destination": "10.0.0.1/32"},'\
            		'"instructions": {"instruction": [{"order": "0",'\
            		'"apply-actions": {"action": [{"output-action": {'\
                	'"output-node-connector": "1"},"order": "0"}]}}]},'\
            		'"priority": "101","cookie": "1","table_id": "0"}]}'
		#在检测h3发包的时候s2的1口流量空闲时发的流表
		h3_to_s2_1 ='{"flow": [{"id": "1","match": {"ethernet-match":'\
               		'{"ethernet-type": {"type": "2048"}},'\
					'"ipv4-source":"10.0.0.3/32","ipv4-destination": "10.0.0.1/32"},'\
            		'"instructions": {"instruction": [{"order": "0",'\
                	'"apply-actions": {"action": [{"output-action": {'\
                	'"output-node-connector": "1"},"order": "0"}]}}]},'\
            		'"priority": "101","cookie": "1","table_id": "0"}]}'
		mh3_to_s2_1 ='{"flow": [{"id": "1","match": {"ethernet-match":'\
               		'{"ethernet-type": {"type": "2048"}},'\
					'"ipv4-source":"10.0.0.3/32","ipv4-destination": "10.0.0.1/32"},'\
            		'"instructions": {"instruction": [{"order": "0",'\
                	'"apply-actions": {"action": [{"output-action": {'\
                	'"output-node-connector": "1"},"order": "0"}]}}]},'\
            		'"priority": "100","cookie": "1","table_id": "0"}]}'
		#在检测h3发包的时候s2的1口流量满载时发的流表	
		h3_to_s2_2 ='{"flow": [{"id": "2","match": {"ethernet-match":'\
               		'{"ethernet-type": {"type": "2048"}},'\
					'"ipv4-source":"10.0.0.3/32","ipv4-destination": "10.0.0.1/32"},'\
            		'"instructions": {"instruction": [{"order": "0",'\
                	'"apply-actions": {"action": [{"output-action": {'\
                	'"output-node-connector": "2"},"order": "0"}]}}]},'\
            		'"priority": "101","cookie": "1","table_id": "0"}]}'
		mh3_to_s2_2 ='{"flow": [{"id": "2","match": {"ethernet-match":'\
               		'{"ethernet-type": {"type": "2048"}},'\
					'"ipv4-source":"10.0.0.3/32","ipv4-destination": "10.0.0.1/32"},'\
            		'"instructions": {"instruction": [{"order": "0",'\
                	'"apply-actions": {"action": [{"output-action": {'\
                	'"output-node-connector": "2"},"order": "0"}]}}]},'\
            		'"priority": "100","cookie": "1","table_id": "0"}]}'
		#s3流表
		s3_1='{"flow": [{"id": "0","match": {"ethernet-match":'\
            '{"ethernet-type": {"type": "2048"}},'\
			'"ipv4-source":"10.0.0.3/32","ipv4-destination": "10.0.0.1/32"},'\
            '"instructions": {"instruction": [{"order": "0",'\
            '"apply-actions": {"action": [{"output-action": {'\
            '"output-node-connector": "1"},"order": "0"}]}}]},'\
            '"priority": "101","cookie": "1","table_id": "0"}]}'
		#s1流表
		s1_2To1='{"flow": [{"id": "0","match": {"ethernet-match":'\
            	'{"ethernet-type": {"type": "2048"}},'\
				'"ipv4-source":"10.0.0.2/32","ipv4-destination": "10.0.0.1/32"},'\
            	'"instructions": {"instruction": [{"order": "0",'\
            	'"apply-actions": {"action": [{"output-action": {'\
            	'"output-node-connector": "1"},"order": "0"}]}}]},'\
            	'"priority": "101","cookie": "1","table_id": "0"}]}'
		s1_3To1='{"flow": [{"id": "1","match": {"ethernet-match":'\
            	'{"ethernet-type": {"type": "2048"}},'\
				'"ipv4-source":"10.0.0.3/32","ipv4-destination": "10.0.0.1/32"},'\
            	'"instructions": {"instruction": [{"order": "0",'\
            	'"apply-actions": {"action": [{"output-action": {'\
            	'"output-node-connector": "1"},"order": "0"}]}}]},'\
            	'"priority": "101","cookie": "1","table_id": "0"}]}'
		headers = {'Content-type': 'application/json'}
		num=0
		#下发流表，中间的地址可以从ODL控制器页面获得
		#先把s1和s3的流表都下了
		response, content = http.request(uri='http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/flow-node-inventory:table/0/flow/0', body=s1_2To1, method='PUT',headers=headers)	
		response, content = http.request(uri='http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/flow-node-inventory:table/0/flow/1', body=s1_3To1, method='PUT',headers=headers)
		response, content = http.request(uri='http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:3/flow-node-inventory:table/0/flow/0', body=s3_1, method='PUT',headers=headers)
		#s2调用h2到1的流表			
		response, content = http.request(uri='http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:2/flow-node-inventory:table/0/flow/0', body=h2_to_s2_1, method='PUT',headers=headers)
		while num < 4 :
			#获取s2端口1的流量
			uri = 'http://127.0.0.1:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:2/node-connector/openflow:2:1'
			response, content = http.request(uri=uri, method='GET')
			content = json.loads(content)
			statistics = content['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']
			bytes1 = statistics['bytes']['transmitted']
			#1秒后再次获取
			time.sleep(1)
			response, content = http.request(uri=uri, method='GET')
			content = json.loads(content)
			statistics = content['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']
			bytes2 = statistics['bytes']['transmitted']
			#在检测到s2的1口流量空闲时发的流表
			speed=float(bytes2-bytes1)/1
			if speed !=0 :#获取有效的速度
				if speed < 1000 :
					print('s2端口1空闲，h3数据包改为往1口通过')
					response, content = http.request(uri='http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:2/flow-node-inventory:table/0/flow/1', body=h3_to_s2_1, method='PUT',headers=headers)
					response, content = http.request(uri='http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:2/flow-node-inventory:table/0/flow/2', body=mh3_to_s2_2, method='PUT',headers=headers)
				#在检测到s2的1口流量满载时发的流表
				else :
					print('s2端口1满载，h3数据包改为往2口通过')
					response, content = http.request(uri='http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:2/flow-node-inventory:table/0/flow/1', body=mh3_to_s2_1, method='PUT',headers=headers)
					response, content = http.request(uri='http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:2/flow-node-inventory:table/0/flow/2', body=h3_to_s2_2, method='PUT',headers=headers)
odl = OdlUtil('127.0.0.1', '8181')
odl.install_flow()

