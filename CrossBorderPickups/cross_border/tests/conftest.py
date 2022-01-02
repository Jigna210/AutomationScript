import os
import platform

import pytest
from _pytest.fixtures import SubRequest
from _pytest.reports import TestReport
from _pytest.runner import CallInfo
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from CrossBorderPickups.cross_border.lib.configs import config
from CrossBorderPickups.cross_border.lib.configs.environmental_variables import CBP
from CrossBorderPickups.cross_border.lib.constants.constant import BaseConstants
from CrossBorderPickups.cross_border.lib.locators.locators import Locators
from CrossBorderPickups.cross_border.page_objects.UI.HeaderPage.header_page import HeaderPage
from CrossBorderPickups.cross_border.page_objects.UI.LoginPage.login_page import LoginPage


web_driver = None

def get_driver_instance():
    """ Returns driver instance """
    return web_driver

@pytest.fixture()
def login(request: 'SubRequest', init_driver):
    """ Automatically logs into product with configured username and password before each test """
    driver = init_driver
    perform_logout = True

    if request.node.get_closest_marker('disable_logout'):
        perform_logout = False

    try:
        login_page = LoginPage(driver)
        login_page.do_login()

        expected_locator = Locators.HeaderPage.operation_button if "-ops-" in driver.current_url else \
            Locators.HeaderPage.user_avatar
        login_page.wait_for_element(lambda: WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            expected_locator)), waiting_for="dashboard gets displayed after login")
        yield
    finally:
        if perform_logout:
            HeaderPage(driver).do_logout()

def get_screenshot_filename(test_name: str, test_status: BaseConstants.Status = None) -> str:
    """
    Return test's screenshot filename

    :param str test_name: test case name
    :param str test_status: test case status
    :return: screenshot filename
    :rtype: str
    """
    filename_prefix = '{}-'.format(test_status.value) if test_status != BaseConstants.Status.Passed else ''
    screenshot_filename = ".".join([os.path.split(test_name)[1], BaseConstants.SCREENSHOT_EXTENSION])

    return "{}{}".format(filename_prefix, screenshot_filename)
