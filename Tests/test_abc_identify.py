"""abc id identify api"""
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
ABCIDIDENTIFYPORT = os.environ.get('ABCIDIDENTIFYPORT')
ABCIDIDENTIFYPATH = apis.abcIdIdentifyAPI
TIMEOUT = 10


@pytest.mark.apis
class TestAbcIdentifyAPI:
    """TestClassAbcIdIdentifyAPI"""

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
        assert oid in response_json['data']['items'][0]['sourceId']
        assert 'OID' in response_json['data']['items'][0]['sourceIdType']

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

    @pytest.mark.abcididentifyapi
    def test_abc_identify_3_001_1(self, request):
        """ test_abc_id_identify_api_3_001_1 """
        """ Normal test case """
        """ Set 1 data into DB than post abc_id_identify to get the data """
        """ Expected 200 """

        item = "test_abc_id_identify_api_3_001_1"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        oid = "K333352999"

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "sourceIds": [oid],
            "sourceIdType":"OID"
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 200
        self.verify_success_response_body(response_json, oid)
        assert oid in response_json['data']['items'][0]['custId']

    @pytest.mark.abcididentifyapi
    def test_abc_identify_3_001_2(self, request):
        """ test_abc_id_identify_api_3_001_2 """
        """ Normal test case """
        """ There is OID not exist in DB"""
        """ Expected 200 """

        item = "test_abc_id_identify_api_3_001_2"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        oid =["A123456789"]

        req_body = {
            "sourceIds": oid,
            "sourceIdType":"OID"
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 200
        self.verify_success_response_body(response_json, oid[0])
        assert '4040' in str(response_json['data']['items'][0]['error']['code'])
        assert 'User Not found' in response_json['data']['items'][0]['error']['message']

    @pytest.mark.abcididentifyapi
    def test_abc_identify_3_001_3(self, request):
        """ test_abc_id_identify_api_3_001_3 """
        """ Normal test case """
        """ Data into DB have mulit count than post abc_id_identify to get the data """
        """ Expected 200 """

        item = "test_abc_id_identify_api_3_001_1"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        oid = "Q123456789"

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "sourceIds": [oid],
            "sourceIdType":"OID"
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 200
        self.verify_success_response_body(response_json, oid)
        assert oid in response_json['data']['items'][0]['custId']

    @pytest.mark.abcididentifyapi
    def test_abc_identify_3_002_1(self, request):
        """ test_abc_id_identify_api_3_002_1 """
        """ Normal test case """
        """ Set 1 data into DB than post abc_id_identify to get the data """
        """ There are some OID not exist in DB"""
        """ Expected 200 """

        item = "test_abc_id_identify_api_3_002_1"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        list_oid = ["K333352999", "A123456789"]

        req_body = {
            "sourceIds": list_oid,
            "sourceIdType":"OID"
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 200
        self.verify_multiple_oids_in_success_response_body(response_json, list_oid)
        assert list_oid[0] in response_json['data']['items'][0]['sourceId']
        assert 'OID' in response_json['data']['items'][0]['sourceIdType']
        assert list_oid[0] in response_json['data']['items'][0]['custId']
        assert list_oid[1] in response_json['data']['items'][1]['sourceId']
        assert 'OID' in response_json['data']['items'][1]['sourceIdType']
        assert '4040' in str(response_json['data']['items'][1]['error']['code'])
        assert 'User Not found' in response_json['data']['items'][1]['error']['message']

    @pytest.mark.abcididentifyapi
    def test_abc_identify_3_002_2(self, request):
        """ test_abc_id_identify_3_002_2 """
        """ Normal test case """
        """ Set 50 data into DB than post abc_id_identify to get the data """
        """ Expected 200 """

        item = "test_abc_id_identify_3_002_2"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        list_oid = ["K295874063", "X960375124", "F829140657", "X523194780", "C149526873",
        "A472108369", "A638791450", "W384970521", "X627908145", "Y846193527",
        "A089413627", "G685392074", "L093248561", "D214357690", "D984613072", 
        "M740153689", "B964807132", "D065143892", "Y492160853", "L403192785",
        "X682190753", "X408163952", "J417368905", "W857694130", "Z763910584", 
        "D185263907", "O735942086", "D896274310", "Q254107389", "Y316872509",
        "P073542986", "Y051863247", "Y382169470", "Z216379084", "G961834205",
        "C832519076", "F985610274", "U028674359", "N803241976", "J180475936",
        "A753168029", "Z608491275", "P735041968", "L547291830", "L325198647",
        "D051247938", "N946578102", "N847531092", "Z894152360", "T849162350"]

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "sourceIds": list_oid,
            "sourceIdType":"OID"
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 200
        self.verify_multiple_oids_in_success_response_body(response_json, list_oid)

    @pytest.mark.abcididentifyapi
    def test_abc_identify_3_003(self, request):
        """ test_abc_id_identify_api_3_003 """
        """ Error Handling """
        """ Request Header without X-SOURCE-ID """
        """ Expected 400 """

        item = "test_abc_id_identify_api_3_003"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        req_headers = {
            "Content-Type": "application/json",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "sourceIds": "T123456789",
            "sourceIdType":"OID"
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        assert '4001' in str(response_json['error']['code'])
        assert "No Source Id" in response_json['error']['message']

    @pytest.mark.abcididentifyapi
    def test_abc_identify_3_004(self, request):
        """ test_abc_id_identify_api_3_004 """
        """ Error Handling """
        """ Request Header without api_txno """
        """ Expected 400 """

        item = "test_abc_id_identify_api_3_004"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            }

        req_body = {
            "sourceIds": "T123456789",
            "sourceIdType":"OID"
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        assert '4000' in str(response_json['error']['code'])
        assert "No Transaction Number" in response_json['error']['message']

    @pytest.mark.abcididentifyapi
    def test_abc_identify_3_005(self, request):
        """ test_abc_id_identify_api_3_005 """
        """ Error Handling """
        """ Request Body format is not correct """
        """ Expected 400 and message is 'Misformed Request Body' """

        item = "test_abc_id_identify_api_3_005"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "sourceId": "T123456789",
            "sourceIdType":"OID"
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        assert '4002' in str(response_json['error']['code'])
        assert 'Misformed Request Body' in response_json['error']['message']

    @pytest.mark.abcididentifyapi
    def test_abc_identify_3_005_1(self, request):
        """ test_abc_identify_3_005_1 """
        """ Error Handling """
        """ Request Body format is not correct """
        """ Expected 400 and message is 'Misformed Request Body' """

        item = "test_abc_id_identify_api_3_005"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "sourceIdType":"OID"
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        assert '4002' in str(response_json['error']['code'])
        assert 'Misformed Request Body' in response_json['error']['message']

    @pytest.mark.abcididentifyapi
    def test_abc_identify_3_005_2(self, request):
        """ test_abc_identify_3_005_2 """
        """ Error Handling """
        """ Request Body format is not correct """
        """ Expected 400 and message is 'Misformed Request Body' """

        item = "test_abc_id_identify_api_3_005"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "sourceIds": [],
            "sourceIdType":"OID"
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        assert '4002' in str(response_json['error']['code'])
        assert 'Misformed Request Body' in response_json['error']['message']

    @pytest.mark.abcididentifyapi
    def test_abc_identify_3_005_3(self, request):
        """ test_abc_identify_3_005_3 """
        """ Error Handling """
        """ Request Body format is not correct """
        """ Expected 400 and message is 'Misformed Request Body' """

        item = "test_abc_id_identify_api_3_005"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "sourceIds": ["T456567890", "V345567890", "467"],
            "sourceIdTypes":"OID"
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        assert '4002' in str(response_json['error']['code'])
        assert 'Misformed Request Body' in response_json['error']['message']

    @pytest.mark.abcididentifyapi
    def test_abc_identify_3_005_4(self, request):
        """ test_abc_identify_3_005_4 """
        """ Error Handling """
        """ Request Body format is not correct """
        """ Expected 400 and message is 'Misformed Request Body' """

        item = "test_abc_id_identify_api_3_005"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "sourceIds": ["T456567890", "V345567890", "467"]
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        assert '4002' in str(response_json['error']['code'])
        assert 'Misformed Request Body' in response_json['error']['message']

    @pytest.mark.abcididentifyapi
    def test_abc_identify_3_006(self, request):
        """ test_abc_id_identify_api_3_006 """
        """ Error Handling """
        """ Request Body OID array length is over 50 """
        """ Expected 400 and message is 'Query exceeded limit' """

        item = "test_abc_id_identify_api_3_006"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        list_oid = ["K295874063", "X960375124", "F829140657", "X523194780", "C149526873",
        "A472108369", "A638791450", "W384970521", "X627908145", "Y846193527",
        "A089413627", "G685392074", "L093248561", "D214357690", "D984613072", 
        "M740153689", "B964807132", "D065143892", "Y492160853", "L403192785",
        "X682190753", "X408163952", "J417368905", "W857694130", "Z763910584", 
        "D185263907", "O735942086", "D896274310", "Q254107389", "Y316872509",
        "P073542986", "Y051863247", "Y382169470", "Z216379084", "G961834205",
        "C832519076", "F985610274", "U028674359", "N803241976", "J180475936",
        "A753168029", "Z608491275", "P735041968", "L547291830", "L325198647",
        "D051247938", "N946578102", "N847531092", "Z894152360", "T849162350", 
        "P920641783"]

        req_headers = {
            "Content-Type": "application/json",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "sourceIds": list_oid,
            "sourceIdType":"OID"
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        response_json = json.loads(response.text)
        assert response.status_code == 400
        assert '4003' in str(response_json['error']['code'])
        assert 'Query exceeded limit' in response_json['error']['message']

    def test_abc_id_identify_api_3_007(self, request):
        """test_abc_id_identify_api_3_007"""

        item = "test_abc_id_identify_api_3_007"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        req_headers = {
            "Content-Type": "application/json",
            "X-APP-ID": "X-APP-ID",
            "X-APP-KEY": "X-APP-KEY",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "sourceIds": [
                "xxxxxxxx", "xxxxxxxx", "xxxxxxxx", "xxxxxxxx", "xxxxxxxx"
            ],
            "sourceType": "OID"
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        # responseJson = json.loads(response.text)
        assert response.status_code == 504

    def test_abc_id_identify_api_3_008(self, request):
        """test_abc_id_identify_api_3_008"""

        item = "test_abc_id_identify_api_3_008"
        LogHelp.log_test_env(item, request.config.getoption('--env'))

        req_headers = {
            "Content-Type": "application/json",
            "X-APP-ID": "X-APP-ID",
            "X-APP-KEY": "X-APP-KEY",
            "X-SOURCE-ID": "X-SOURCE-ID",
            "api_txno": "YYYYMMDDHHmmssfff"
            }

        req_body = {
            "sourceIds": [
                "xxxxxxxx", "xxxxxxxx", "xxxxxxxx", "xxxxxxxx", "xxxxxxxx"
            ],
            "sourceType": "OID"
        }

        LogHelp.log_url_header_body(item, BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, req_headers, req_body)
        response = requests.post(url=BASEURL+':'+ABCIDIDENTIFYPORT+ABCIDIDENTIFYPATH, headers=req_headers, json=req_body, timeout=TIMEOUT)
        # responseJson = json.loads(response.text)
        assert response.status_code == 500
