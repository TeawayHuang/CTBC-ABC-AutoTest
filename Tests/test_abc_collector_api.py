"""abc collector api"""
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
TIMEOUT = 10


@pytest.mark.apis
class TestClassAbcCollectorAPI:
    """TestClassAbcCollectorAPI"""

    def random_oid(self):
        """random_oid"""
        return ''.join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 1) + random.sample(string.digits, 9))

    def get_datetime(self):
        """get_datetime"""
        now = datetime.now()
        return now.strftime("%Y-%m-%dT%H:%M:%S")

    def verify_success_response_body(self, response_json):
        """verify_success_response_body"""
        assert 'apiVersion' in response_json
        assert 'apiTxno' in response_json
        assert 'success' in response_json
        assert 'message' in response_json['success']
        assert 'resource created' in response_json['success']['message']

    def verify_error_response_body(self, response_json):
        """verify_error_response_body"""
        assert 'apiVersion' in response_json
        assert 'apiTxno' in response_json
        assert 'error' in response_json
        assert 'code' in response_json['error']
        assert 'message' in response_json['error']

    @classmethod
    def setup_class(cls):
        """setup_class"""

        logging.info("setup_class")
        logging.info("setup_class BASEURL: %s", os.environ.get('BASEURL'))
        logging.info("setup_class Admin: %s", os.environ.get('ADMIN'))
        logging.info("setup_class password: %s", os.environ.get('PASSWORD'))

    @pytest.mark.debug
    @pytest.mark.abccollectorapi
    def test_abc_collector_api_1_001_1(self, request):
        """ test_abc_collector_api_1_001_1 """
        """ Normal test case """
        """ Expected 200 """

        item = "test_abc_collector_api_1_001_1"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        oid = self.random_oid()
        clickdatetime = self.get_datetime()

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

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 200
        self.verify_success_response_body(response_json)

    @pytest.mark.abccollectorapi
    def test_abc_collector_api_1_001_2(self, request):
        """ test_abc_collector_api_1_001_2 """
        """ Normal test case """
        """ Request Body without productName, productDesc, branchCode and depositNumber"""
        """ Expected 200 """

        item = "test_abc_collector_api_1_001_2"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        oid = self.random_oid()
        clickdatetime = self.get_datetime()

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
                    "clickUrl": "string"
                }
            }
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 200
        self.verify_success_response_body(response_json)

    @pytest.mark.abccollectorapi
    def test_abc_collector_api_1_001_3(self, request):
        """ test_abc_collector_api_1_001_3 """
        """ Normal test case """
        """ Request Body - productName, productDesc, branchCode and depositNumber are empty string"""
        """ Expected 200 """

        item = "test_abc_collector_api_1_001_3"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        oid = self.random_oid()
        clickdatetime = self.get_datetime()

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
                    "productName": "",
                    "productDesc": "",
                    "branchCode": "",
                    "depositNumber": ""
                }
            }
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 200
        self.verify_success_response_body(response_json)

    @pytest.mark.abccollectorapi
    def test_abc_collector_api_1_002(self, request):
        """ test_abc_collector_api_1_002 """
        """ Error Handling """
        """ Request Header without X-SOURCE-ID """
        """ Expected 400 and message is 'No Source Id' """

        item = "test_abc_collector_api_1_002"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        oid = self.random_oid()
        clickdatetime = self.get_datetime()

        req_headers = {
            "Content-Type": "application/json",
            "X-APP-ID": "X-APP-ID",
            "X-APP-KEY": "X-APP-KEY",
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

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        self.verify_error_response_body(response_json)
        assert '4001' in str(response_json['error']['code'])
        assert "No Source Id" in response_json['error']['message']

    @pytest.mark.abccollectorapi
    def test_abc_collector_api_1_003(self, request):
        """ test_abc_collector_api_1_003 """
        """ Error Handling """
        """ Request Header without api_txno """

        item = "test_abc_collector_api_1_003"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        oid = self.random_oid()
        clickdatetime = self.get_datetime()

        req_headers = {
            "Content-Type": "application/json",
            "X-APP-ID": "X-APP-ID",
            "X-APP-KEY": "X-APP-KEY",
            "X-SOURCE-ID": "X-SOURCE-ID",
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

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        assert '4000' in str(response_json['error']['code'])
        assert "No Transaction Number" in response_json['error']['message']

    @pytest.mark.abccollectorapi
    def test_abc_collector_api_1_004_1(self, request):
        """ test_abc_collector_api_1_004_1 """
        """ Error Handling """
        """ Request Body without OID """
        """ Expected 400 and code is '4002' and message is 'Misformed Request Body' """

        item = "test_abc_collector_api_1_004_1"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        clickdatetime = self.get_datetime()

        req_headers = {
            "Content-Type": "application/json",
            "X-APP-ID": "X-APP-ID",
            "X-APP-KEY": "X-APP-KEY",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "data": {
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

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        self.verify_error_response_body(response_json)
        assert '4002' in str(response_json['error']['code'])
        assert 'Misformed Request Body' in response_json['error']['message']

    @pytest.mark.abccollectorapi
    def test_abc_collector_api_1_004_2(self, request):
        """t est_abc_collector_api_1_004_2 """
        """ Error Handling """
        """ Request Header without clickDateTime """
        """ Expected 400 and code is '4002' and message is 'Misformed Request Body' """

        item = "test_abc_collector_api_1_004_2"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        oid = self.random_oid()

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
                    "clickUrl": "string",
                    "productName": "string",
                    "productDesc": "string",
                    "branchCode": "string",
                    "depositNumber": "string"
                }
            }
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        self.verify_error_response_body(response_json)
        assert '4002' in str(response_json['error']['code'])
        assert 'Misformed Request Body' in response_json['error']['message']

    @pytest.mark.abccollectorapi
    def test_abc_collector_api_1_004_3(self, request):
        """ test_abc_collector_api_1_004_3 """
        """ Error Handling """
        """ Request Body without clickUrl """
        """ Expected 400 and code is '4002' and message is 'Misformed Request Body' """

        item = "test_abc_collector_api_1_004_3"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        oid = self.random_oid()
        clickdatetime = self.get_datetime()

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
                    "productName": "string",
                    "productDesc": "string",
                    "branchCode": "string",
                    "depositNumber": "string"
                }
            }
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        self.verify_error_response_body(response_json)
        assert '4002' in str(response_json['error']['code'])
        assert 'Misformed Request Body' in response_json['error']['message']

    @pytest.mark.abccollectorapi
    def test_abc_collector_api_1_004_4(self, request):
        """ test_abc_collector_api_1_004_4 """
        """ Error Handling """
        """ Request Body with OID is incorrect """
        """ Expected 400 and code is '4002' and message is 'Misformed Request Body' """

        item = "test_abc_collector_api_1_004_3"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        oid = self.random_oid()
        clickdatetime = self.get_datetime()

        req_headers = {
            "Content-Type": "application/json",
            "X-APP-ID": "X-APP-ID",
            "X-APP-KEY": "X-APP-KEY",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "data": {
                "OIDs": oid,
                "clickInfo": {
                    "clickDateTime": clickdatetime,
                    "clickUrl": "https://www.google.com",
                    "productName": "string",
                    "productDesc": "string",
                    "branchCode": "string",
                    "depositNumber": "string"
                }
            }
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        self.verify_error_response_body(response_json)
        assert '4002' in str(response_json['error']['code'])
        assert 'Misformed Request Body' in response_json['error']['message']

    @pytest.mark.abccollectorapi
    def test_abc_collector_api_1_004_5(self, request):
        """ test_abc_collector_api_1_004_5 """
        """ Error Handling """
        """ Request Body with clickDateTime is incorrect """
        """ Expected 400 and code is '4002' and message is 'Misformed Request Body' """

        item = "test_abc_collector_api_1_004_3"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        oid = self.random_oid()
        clickdatetime = self.get_datetime()

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
                    "clickDateTimes": clickdatetime,
                    "clickUrl": "https://www.google.com",
                    "productName": "string",
                    "productDesc": "string",
                    "branchCode": "string",
                    "depositNumber": "string"
                }
            }
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        self.verify_error_response_body(response_json)
        assert '4002' in str(response_json['error']['code'])
        assert 'Misformed Request Body' in response_json['error']['message']

    @pytest.mark.abccollectorapi
    def test_abc_collector_api_1_004_6(self, request):
        """ test_abc_collector_api_1_004_6 """
        """ Error Handling """
        """ Request Body with clickUrls is incorrect """
        """ Expected 400 and code is '4002' and message is 'Misformed Request Body' """

        item = "test_abc_collector_api_1_004_3"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        oid = self.random_oid()
        clickdatetime = self.get_datetime()

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
                    "clickUrls": "https://www.google.com",
                    "productName": "string",
                    "productDesc": "string",
                    "branchCode": "string",
                    "depositNumber": "string"
                }
            }
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        self.verify_error_response_body(response_json)
        assert '4002' in str(response_json['error']['code'])
        assert 'Misformed Request Body' in response_json['error']['message']

    def test_abc_collector_api_1_005(self, request):
        """ test_abc_collector_api_1_005 """

        item = "test_abc_collector_api_1_005"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        oid = self.random_oid()
        clickdatetime = self.get_datetime()

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

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        # response_json = json.loads(response.text)
        assert response.status_code == 504

    def test_abc_collector_api_1_006(self, request):
        """ test_abc_collector_api_1_006 """

        item = "test_abc_collector_api_1_006"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        oid = self.random_oid()
        clickdatetime = self.get_datetime()

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

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCCONTROLLPORT+ABCCONTROLLAPIPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        # response_json = json.loads(response.text)
        assert response.status_code == 500
