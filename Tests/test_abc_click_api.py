"""abc click api"""
import logging
import os
import random
import string
import json
from datetime import datetime
import pytest
import requests
import apis

from Util.logtool import LogHelp

BASEURL = os.environ.get('BASEURL')
CLICKURL = os.environ.get('CLICKURL')
ABCCONTROLLPORT = os.environ.get('ABCCONTROLLPORT')
ABCCONTROLLAPIPATH = apis.abcControllAPI
ABCCLICKPORT = os.environ.get('ABCCLICKPORT')
ABCCLICKAPIPATH = apis.abcClickAPI
TIMEOUT = 10


@pytest.mark.apis
class TestClassAbcClickAPI:
    """ TestClassAbcClickAPI """

    def random_oid(self):
        """random_oid"""
        return ''.join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 1) + random.sample(string.digits, 9))

    def random_multiple_oids(self, oids_count):
        """random_multiple_oids"""
        list_oids = []

        for i in range(oids_count):
            list_oids.append(''.join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 1) + random.sample(string.digits, 9)))

        return list_oids

    def get_datetime(self):
        """get_datetime"""
        now = datetime.now()
        return now.strftime("%Y-%m-%dT%H:%M:%S")

    def set_data_into_db(self, oid, clickdatetime):
        """set_data_into_db"""
        req_headers = {
            "Content-Type": "application/json",
            "X-APP-ID": "X-APP-ID",
            "X-APP-KEY": "X-APP-KEY",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "data": {
                "OID": oid,
                "clickInfo": {
                    "clickDateTime": clickdatetime,
                    "clickUrl": CLICKURL,
                    "productName": "string",
                    "productDesc": "string",
                    "branchCode": "string",
                    "depositNumber": "string"
                }
            }
        }

        response = requests.post(url=BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 200

    def set_multiple_data_into_db(self, list_oid, clickdatetime):
        """set_multiple_data_into_db"""
        req_headers = {
            "Content-Type": "application/json",
            "X-APP-ID": "X-APP-ID",
            "X-APP-KEY": "X-APP-KEY",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        for i in range(len(list_oid)):
            oid = list_oid[i]
            req_body = {
                "data": {
                    "OID": oid,
                    "clickInfo": {
                        "clickDateTime": clickdatetime,
                        "clickUrl": CLICKURL,
                        "productName": "string",
                        "productDesc": "string",
                        "branchCode": "string",
                        "depositNumber": "string"
                    }
                }
            }

            response = requests.post(url=BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)

    def verify_success_response_body(self, response_json, oid):
        """verify_success_response_body"""
        assert 'apiVersion' in response_json
        assert 'apiTxno' in response_json
        assert '1' in str(response_json['data']['totalItems'])
        assert oid in response_json['data']['items'][0]['OID']

    def verify_multiple_oids_in_success_response_body(self, response_json, list_oid):
        """verify_multiple_oids_in_success_response_body"""
        assert 'apiVersion' in response_json
        assert 'apiTxno' in response_json
        assert str(len(list_oid)) in str(response_json['data']['totalItems'])

    @classmethod
    def setup_class(cls):
        """setup_class"""

        logging.info("setup_class")
        logging.info("setup_class Admin: %s", os.environ.get('ADMIN'))
        logging.info("setup_class password: %s", os.environ.get('PASSWORD'))

    @pytest.mark.abcclickapi
    def test_abc_click_api_2_001_1(self, request):
        """ test_abc_click_api_2_001 """
        """ Normal test case """
        """ Set 1 data into DB than post abc_click to get the data """
        """ Expected 200 """

        item = "test_abc_click_api_2_001"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        oid = self.random_oid()
        clickdatetime = self.get_datetime()

        self.set_data_into_db(oid, clickdatetime)

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "OID": [
                oid
            ]
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 200
        self.verify_success_response_body(response_json, oid)

    @pytest.mark.abcclickapi
    def test_abc_click_api_2_001_2(self, request):
        """ test_abc_click_api_2_001_2 """
        """ Normal test case """
        """ There is OID not exist in DB"""
        """ Expected 200 """

        item = "test_abc_click_api_2_001_2"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        oid =["T123456789"]

        req_body = {
            "OID": oid
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 200
        self.verify_success_response_body(response_json, oid[0])
        assert '4040' in str(response_json['data']['items'][0]['error']['code'])
        assert 'User Not found' in response_json['data']['items'][0]['error']['message']

    @pytest.mark.abcclickapi
    def test_abc_click_api_2_002_1(self, request):
        """ test_abc_click_api_2_002_1 """
        """ Normal test case """
        """ Set 1 data into DB than post abc_click to get the data """
        """ There are some OID not exist in DB"""
        """ Expected 200 """

        item = "test_abc_click_api_2_002_1"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        oid = self.random_oid()
        clickdatetime = self.get_datetime()

        self.set_data_into_db(oid, clickdatetime)

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        list_oid = [oid, "T123456789"]

        req_body = {
            "OID": list_oid
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 200
        self.verify_multiple_oids_in_success_response_body(response_json, list_oid)
        assert list_oid[0] in response_json['data']['items'][0]['OID']
        assert list_oid[1] in response_json['data']['items'][1]['OID']
        assert '4040' in str(response_json['data']['items'][1]['error']['code'])
        assert 'User Not found' in response_json['data']['items'][1]['error']['message']

    @pytest.mark.abcclickapi
    def test_abc_click_api_2_002_2(self, request):
        """ test_abc_click_api_2_002_2 """
        """ Normal test case """
        """ Set 50 data into DB than post abc_click to get the data """
        """ Expected 200 """

        item = "test_abc_click_api_2_002_2"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        list_oid = self.random_multiple_oids(50)
        clickdatetime = self.get_datetime()

        self.set_multiple_data_into_db(list_oid, clickdatetime)

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "OID": list_oid
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 200
        self.verify_multiple_oids_in_success_response_body(response_json, list_oid)

    @pytest.mark.abcclickapi
    def test_abc_click_api_2_003(self, request):
        """ test_abc_click_api_2_003 """
        """ Error Handling """
        """ Request Header without X-SOURCE-ID """
        """ Expected 400 """

        item = "test_abc_click_api_2_003"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        req_headers = {
            "Content-Type": "application/json",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "OID": [
                "T123456789"
            ]
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        assert '4001' in str(response_json['error']['code'])
        assert "No Source Id" in response_json['error']['message']


    @pytest.mark.abcclickapi
    def test_abc_click_api_2_004(self, request):
        """ test_abc_click_api_2_004 """
        """ Error Handling """
        """ Request Header without api_txno """
        """ Expected 400 """

        item = "test_abc_click_api_2_004"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            }

        req_body = {
            "OID": [
                "T123456789"
            ]
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        assert '4000' in str(response_json['error']['code'])
        assert "No Transaction Number" in response_json['error']['message']

    @pytest.mark.abcclickapi
    def test_abc_click_api_2_005(self, request):
        """ test_abc_click_api_2_005 """
        """ Error Handling """
        """ Request Body format is not correct """
        """ Expected 400 and message is 'Misformed Request Body' """

        item = "test_abc_click_api_2_005"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "OIDs": [
                "T123456789"
            ]
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        assert '4002' in str(response_json['error']['code'])
        assert 'Misformed Request Body' in response_json['error']['message']

    @pytest.mark.abcclickapi
    def test_abc_click_api_2_006(self, request):
        """ test_abc_click_api_2_006 """
        """ Error Handling """
        """ Request Body OID array length is over 50 """
        """ Expected 400 and message is 'Query exceeded limit' """

        item = "test_abc_click_api_2_006"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        list_oid = self.random_multiple_oids(51)
        clickdatetime = self.get_datetime()

        self.set_multiple_data_into_db(list_oid, clickdatetime)

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "OID": list_oid
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        assert '4003' in str(response_json['error']['code'])
        assert 'Query exceeded limit' in response_json['error']['message']

    def test_abc_click_api_2_007(self, request):
        """ test_abc_click_api_2_007 """

        item = "test_abc_click_api_2_007"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "OID": [
                "T123456789", "T123456780", "T123456781", "T123456782", "T123456783"
            ]
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        # response_json = json.loads(response.text)
        assert response.status_code == 504

    def test_abc_click_api_2_008(self, request):
        """ test_abc_click_api_2_008 """

        item = "test_abc_click_api_2_008"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "OIDS": [
                "T123456789", "T123456780", "T123456781", "T123456782", "T123456783"
            ]
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCLICKPORT+ABCCLICKAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        # response_json = json.loads(response.text)
        assert response.status_code == 500
