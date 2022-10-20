# CTBC-ABC-AutoTest
CTBC-ABC-AutoTest

# Change Python Test Env
conda activate CtbcAbc

# Run Automation Test
'''
python3 -m pytest -m abccollectorapi --env=local Tests/test_abc_collector_api.py
python3 -m pytest -m abcclickapi --env=local Tests/test_abc_click_api.py
python3 -m pytest -m abcididentifyapi --env=local Tests/test_abc_identify.py
'''
