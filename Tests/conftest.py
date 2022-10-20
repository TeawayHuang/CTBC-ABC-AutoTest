import logging
import pytest
import os

@pytest.fixture()
def login():
    logging.info("login()")
    yield
    logging.info("exit login()")

@pytest.fixture()
def get_env(pytestconfig):
    logging.info("get_env(): " + pytestconfig.getoption("env"))
    return pytestconfig.getoption("env")

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    logging.info("pytest_runtest_makereport")
    outcome = yield
    report = outcome.get_result()
    pytest_html = item.config.pluginmanager.getplugin('html')
    extra = getattr(report, 'extra', [])

    main_script_dir = os.path.dirname(__file__)
    rel_path = "Topological/CloudComputing.png"
    image = pytest_html.extras.image(os.path.join(main_script_dir, rel_path))

    if report.when == "call":
        extra.append(image)
        report.extra = extra

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="stage")
