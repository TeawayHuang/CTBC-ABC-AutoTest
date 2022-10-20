import logging

class LogHelp:

    @classmethod
    def log_test_env(self, item, testenv):
        logging.info("%s env: %s", item, testenv)

    @classmethod
    def log_url_header_body(self, item, baseurl, header, body):
        logging.info("test item:" + str(item))
        logging.info("baseurl:" + str(baseurl))
        logging.info("header:" + str(header))
        logging.info("body:" + str(body))