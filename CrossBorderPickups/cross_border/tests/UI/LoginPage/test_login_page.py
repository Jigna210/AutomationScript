import pytest

from CrossBorderPickups.cross_border.lib.locators.locators import Locators
from CrossBorderPickups.cross_border.lib.messages.message import NotificationMessages
from CrossBorderPickups.cross_border.page_objects.UI.HeaderPage.header_page import HeaderPage
from CrossBorderPickups.cross_border.page_objects.UI.LoginPage.login_page import LoginPage
from CrossBorderPickups.cross_border.page_objects.UI.ShopAndShip.PackagesPage.packages_page import PackagesPage


@pytest.mark.usefixtures("login")
class TestLoginPage:
    """ Covers tests related to user login """

    def test_user_can_login_with_default_credentials(self):
        """
        Test Steps:
        1. Enter correct username or email id
        2. Enter correct password
        3. Click on Login button

        Scenario Tested:
        [x] User do login successfully in product with default credentials.
        """
        shipment_page = PackagesPage(self.driver)
        page_title = shipment_page.get_element_text(by_locator=Locators.ShipmentPage.page_title)

        assert page_title == "Shipments", "User can not be login successfully"

    @pytest.mark.parametrize('input_username, input_password', [
        ('xxx985@gmail.com', '123456'), ('test@cbp.com', '123456')])
    def test_user_can_login_with_credentials(self, input_username, input_password):
        """
        Test Steps:
        1. Enter correct username or email id
        2. Enter correct password
        3. Click on Login button

        Scenario Tested:
        [x] User should do login successfully in product.
        """
        HeaderPage(self.driver).do_logout()

        login_page = LoginPage(self.driver)
        login_page.login_with_credentials(input_username, input_password)

        shipment_page = PackagesPage(self.driver)
        page_title = shipment_page.get_element_text(by_locator=Locators.ShipmentPage.page_title)

        assert page_title == "Shipments", "User can not be login successfully"

    @pytest.mark.disable_logout
    def test_login_blank_credentials(self):
        """
        Test Steps:
        1. Keep blank Email
        2. Keep blank Password
        3. Click on Login Button

        Scenario Tested:
        [x] User should not do login in application with blank credentials.
        """
        HeaderPage(self.driver).do_logout()

        login_page = LoginPage(self.driver)
        login_page.login_with_credentials('', '')

        assert login_page.get_element_text(by_locator=Locators.LoginPage.email_msg) == \
               NotificationMessages.LoginPageValidation.email_required
        assert login_page.get_element_text(by_locator=Locators.LoginPage.password_msg) == \
               NotificationMessages.LoginPageValidation.password_required

    @pytest.mark.disable_logout
    @pytest.mark.parametrize('input_username, input_password', [
        ('XXX985@gmail.com', '12345'), ('test@cbp', '123456'), ('XX21029', '123456')])
    def test_login_invalid_credentials(self, input_username, input_password):
        """
        Test Steps:
        1. Keep blank Email
        2. Keep blank Password
        3. Click on Login Button

        Scenario Tested:
        [x] User should not do login in application with invalid credentials.
        """
        HeaderPage(self.driver).do_logout()

        login_page = LoginPage(self.driver)
        login_page.login_with_credentials(input_username, input_password)

        if '@' in input_username:
            assert login_page.get_element_text(by_locator=Locators.LoginPage.credentials_msg) == \
                   NotificationMessages.LoginPageValidation.invalid_credentials
        else:
            assert login_page.get_element_text(by_locator=Locators.LoginPage.invalid_email_error) == \
                   NotificationMessages.LoginPageValidation.invalid_email_error

    @pytest.mark.parametrize('username, password', [
        ("xxx985@gmail.com", "123456"), ("xx21029@gmail.com", "123456")])
    def test_user_can_login_successfully(self, username, password):
        """
        Test Steps:
        1. Enter correct username or email id
        2. Enter correct password
        3. Click on Login button

        Scenario Tested:
        [x] User should do login successfully in product.
        """
        HeaderPage(self.driver).do_logout()

        login_page = LoginPage(self.driver)
        login_page.login_with_credentials(username=username, password=password)

        packages_page = PackagesPage(self.driver)
        page_title = packages_page.get_element_text(by_locator=Locators.PackagesPage.page_title)
        expected_page_title = "Dashboard" if username == "xx21029@gmail.com" else "Shipments"

        assert page_title == expected_page_title, "User can not be login successfully"
