import os
import random
from random import randint

import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from CrossBorderPickups.cross_border.lib.constants.constant import PageConstants, BaseConstants
from CrossBorderPickups.cross_border.lib.helpers.helpers import sleep_execution
from CrossBorderPickups.cross_border.lib.locators.locators import Locators
from CrossBorderPickups.cross_border.lib.messages.message import NotificationMessages
from CrossBorderPickups.cross_border.lib.utility.notification import Notifications
from CrossBorderPickups.cross_border.page_objects.UI.ShopAndShip.PackagesPage.packages_page import PackagesPage, \
    PackagesList, CreateOrderDropDown, AddContentModal, DiscardPackagesDropDown

app_url = BaseConstants.DEFAULT_BASE_URL
app_user_name = BaseConstants.CUSTOMER_USER_NAME
app_password = BaseConstants.DEFAULT_PASSWORD


@pytest.mark.usefixtures("login")
class TestPackagesPage:
    """
    Covers tests related to packages page

    Pre-requisite:
        1. Enter url 
        2. Click on login button
        3. Enter username
        4. Enter password
        5. Click on login button
    """
    package_constant = PageConstants.PackagesPage
    create_order_constants = package_constant.CreateOrder
    status_constant = package_constant.PackageStatus

    def select_packages_from_packages_list_table(self, select_action: str = "single", return_ids: bool = False,
                                                 package_status: str = status_constant.PENDING_PAYMENT) -> list:
        """
        Helper function to select packages from packages list table

        :param str select_action: action value like single/multiple
        :param bool return_ids: True if selected package ids needed else False
        :param str package_status: status of package that id needs to be select
        :return: selected package's id
        :rtype: list
        """
        expected_ids = []
        packages_page = PackagesPage(self.driver)
        packages_page.wait_for_element(lambda: packages_page.is_element_visible(
            by_locator=Locators.PackagesPage.checkout_button), waiting_for="packages page gets loaded")

        packages_list = PackagesList(self.driver)
        package_ids_of_given_status = packages_list.get_package_id_from_other_field_value(
            package_header=self.package_constant.PACKAGE_STATUS, values=[package_status])

        if len(package_ids_of_given_status) > 0:
            number_of_package = 1 if (select_action == "single" or len(package_ids_of_given_status) == 1) else \
                random.randint(2, len(package_ids_of_given_status))
            expected_ids = random.sample(package_ids_of_given_status, k=number_of_package)

            for p_id in expected_ids:
                packages_list.select_package_by_id(package_id=p_id)

        return expected_ids if return_ids else None

    @pytest.mark.parametrize('create_new_package', [{"pkg_count": 2}], indirect=True)
    def test_visibility_of_create_order_link_unlink_discard_buttons(self, create_new_package):
        """
        Test Steps:
            1. Go to Packages page

        Scenario Tested:
        [x] User can see "Create Order", "Link", "Unlink" and "Discard" buttons on Packages page.
        [x] "Create Order" and "Discard" buttons only should show enabled.
        [x] "Link" and "Unlink" buttons should show disabled initially.
        [x] "Unlink" button should get enabled if user select any single package from list.
        [x] "Link" button should get enabled only if user select more than one package from list.
        """
        packages_page = PackagesPage(self.driver)
        packages_page.load_url(url=os.path.join(app_url, BaseConstants.Urls.PACKAGES_PAGE_URL))
        packages_page.wait_for_element(lambda: packages_page.is_element_visible(
            by_locator=Locators.PackagesPage.checkout_button), waiting_for="packages page gets loaded")

        package_page_locator = Locators.PackagesPage

        for element in [package_page_locator.checkout_button, package_page_locator.link_button,
                        package_page_locator.unlink_button, package_page_locator.discard_button]:
            assert packages_page.is_element_visible(by_locator=element), \
                "Any one from 'Create Order', 'Link', 'Unlink' or 'Discard' buttons are missing or it's text mismatch."

            if element in [package_page_locator.checkout_button, package_page_locator.discard_button]:
                assert packages_page.is_element_enabled(by_locator=element), \
                    "Any one from 'Create Order' or 'Discard' buttons are showing disabled which should be " \
                    "enabled instead."
            else:
                assert not packages_page.is_element_enabled(by_locator=element), \
                    "Any one from 'Link' or 'Unlink' buttons are showing enabled which should be disabled instead."

        package_list = PackagesList(self.driver)
        status_constant = self.package_constant.PackageStatus
        all_packages_id = package_list.get_package_id_from_other_field_value(
            package_header=self.package_constant.PACKAGE_STATUS, values=[status_constant.PENDING_PAYMENT,
                                                                         status_constant.INFORMATION_REQUIRED])

        enable_disable_buttons = [package_page_locator.link_button, package_page_locator.unlink_button]

        for element in enable_disable_buttons:
            number_of_package_to_select = 1 if element == package_page_locator.link_button else \
                random.randint(2, int(len(all_packages_id) / 2))

            package_ids_to_select = random.sample(all_packages_id, k=number_of_package_to_select)

            for package_id in package_ids_to_select:
                package_list.select_package_by_id(package_id=package_id)

            is_enabled = packages_page.is_element_enabled(by_locator=element)

            if number_of_package_to_select == 1:
                assert all([not is_enabled, not packages_page.is_element_enabled(
                    by_locator=enable_disable_buttons[-1])]), \
                    "'Link' and 'Unlink' buttons are showing enabled even if user select only one package."
            else:
                assert all([packages_page.is_element_enabled(by_locator=enable_disable_buttons[0]), not is_enabled]), \
                    "'Link' button is showing disabled and 'Unlink' button is showing enabled even if user select " \
                    "more than one package."

            for p_id in package_ids_to_select:
                package_list.select_package_by_id(package_id=p_id, is_select=False)

    @pytest.mark.xfail
    def test_verify_empty_record_message_while_no_records(self):
        """
        Test Steps:
            1. Go to Packages page
            2. Enter value in Search textbox

        Scenario Tested:
        [x] Verify if no record is exist then "no record" message should appear
        """
        packages_page = PackagesPage(self.driver)
        expected_message = packages_page.get_element_text(by_locator=Locators.PackagesPage.no_record_msg)

        assert expected_message == PageConstants.PackagesPage.NO_RECORD_MESSAGE, \
            "'No Records' message is not showing even if there is no records found."

    @pytest.mark.parametrize('select_action', ['single', 'multiple'])
    def test_user_can_select_single_or_multiple_packages(self, select_action):
        """
        Test Steps:
            1. Go to Packages page
            2. Select single or multiple packages from packages list table

        Scenario Tested:
        [x] User should select single and multiple packages that, we want to ship
        """
        selected_ids = self.select_packages_from_packages_list_table(select_action=select_action, return_ids=True)

        for package_id in selected_ids:
            assert PackagesList(self.driver).get_element_of_package_checkbox(package_id=package_id).is_selected(), \
                "Failed to select package by using checkbox."

    @pytest.mark.parametrize('select_action', ['single', 'multiple'])
    def test_user_can_create_order_by_selecting_single_or_multiple_packages(self, create_new_package, select_action):
        """
        Test Steps:
            1. Go to Packages page
            2. Select single or multiple packages from packages list table

        Scenario Tested:
        [x] User should select single and multiple packages that, we want to ship
        """
        selected_ids = self.select_packages_from_packages_list_table(select_action=select_action, return_ids=True)

        packages_page = PackagesPage(self.driver)
        packages_page.click(by_locator=Locators.PackagesPage.checkout_button)

        create_order = CreateOrderDropDown(self.driver)
        create_order_locators = Locators.PackagesPage.CreateOrder

        assert packages_page.is_element_visible(by_locator=Locators.modal), \
            "'Create Order' modal is not getting displayed after clicking on 'Create Order' button by selecting " \
            "single or multiple packages."

        create_order.wait_for_element(lambda: create_order.is_element_visible(
            by_locator=create_order_locators.send_to_canada_button), waiting_for="create order modal gets loaded")

        assert not create_order.is_element_enabled(by_locator=create_order_locators.send_to_canada_button), \
            "'Send to Canada' button is showing enabled even if no package selected there."

        for package_id in selected_ids:
            PackagesList(self.driver).select_package_by_id(package_id=package_id, element_on_modal=True)

        assert create_order.is_element_enabled(by_locator=create_order_locators.send_to_canada_button), \
            "'Send to Canada' button is not showing enabled even after selecting the packages."

        create_order.click(by_locator=create_order_locators.send_to_canada_button)
        create_order.wait_for_element(lambda: create_order.is_element_visible(
            by_locator=create_order_locators.email_field), waiting_for="order details page gets loaded")

        create_order.click(by_locator=create_order_locators.create_order_modal_close_icon)
        sleep_execution(2)

    def test_user_can_view_content_declaration_block(self):
        """
        Test Steps:
            1. Go to Packages page
            2. Select any record from packages list

        Scenario Tested:
        [x] Verify that user should view content declaration blocks
        [x] Verify that User should view package details by selecting a records
        """
        package_list = PackagesList(self.driver)
        status_constant = self.package_constant.PackageStatus

        all_packages_id = package_list.get_package_id_from_other_field_value(
            package_header=self.package_constant.PACKAGE_STATUS, values=[
                status_constant.PENDING_PAYMENT, status_constant.AVAILABLE_FOR_PICKUP,
                status_constant.READY_FOR_TRANSPORT])

        selected_id = all_packages_id[0]
        package_list.select_package_by_id(package_id=selected_id)
        package_list.click_on_row(row_to_be_select=selected_id)

        package_content_title_element = package_list.get_element_of_content_block_title(package_id=selected_id)
        package_content_table_element = package_list.get_element_of_package_content_table(package_id=selected_id)

        assert package_content_title_element.text == PageConstants.PackagesPage.PACKAGE_CONTENTS, \
            "'Package Contents' block title is missing or getting mismatch."

        for locator in [package_content_title_element, package_content_table_element,
                        Locators.PackagesPage.add_content_button]:
            assert package_list.is_element_visible(by_locator=locator), \
                "'Package Contents' block does not getting opened after selecting package from package list."

    def test_user_can_add_content_in_package_content_block(self):
        """
        Test Steps:
            1. Go to Packages page
            2. Select any record from packages list
            3. Add content from Content declaration block

        Scenario Tested:
        [x] User should view and edit value in a textbox inside a content declaration blocks
        [x] Verify that user can select category from content declaration blocks
        [x] Verify that user can enter quantity details from content declaration blocks
        [x] Verify that user can click and save add content details in a content declaration blocks
        """
        package_list = PackagesList(self.driver)
        status_constant = self.package_constant.PackageStatus

        all_packages_id = package_list.get_package_id_from_other_field_value(
            package_header=self.package_constant.PACKAGE_STATUS, values=[
                status_constant.PENDING_PAYMENT, status_constant.AVAILABLE_FOR_PICKUP,
                status_constant.READY_FOR_TRANSPORT, status_constant.INFORMATION_REQUIRED])

        selected_id = random.sample(all_packages_id, k=1)[0]
        package_list.select_package_by_id(package_id=selected_id)
        package_list.click_on_row(row_to_be_select=selected_id)

        package_list.click(by_locator=Locators.PackagesPage.add_content_button)
        sleep_execution(2)

        add_content = AddContentModal(self.driver)
        add_content_locators = Locators.PackagesPage.AddContent
        add_content.wait_for_element(lambda: add_content.is_element_visible(
            by_locator=add_content_locators.add_button), waiting_for="create order modal gets loaded")

        assert package_list.is_element_visible(by_locator=Locators.modal), \
            "'Add content' modal is not getting displayed after clicking on 'Add content' button from " \
            "selected package."

        add_content_constant = PageConstants.PackagesPage.AddContent
        add_content.click_on_drop_down_arrow(field_name=add_content_constant.DUTY_CATEGORY)

        for locator in [Locators.modal, add_content_constant.DUTY_CATEGORY, add_content_constant.COUNTRY_OF_ORIGIN,
                        add_content_locators.quantity_field, add_content_locators.value_usd_field]:
            if locator in [add_content_constant.DUTY_CATEGORY, add_content_constant.COUNTRY_OF_ORIGIN]:
                locator = add_content.get_element_of_add_content_modal_drop_downs(field_label=locator)

            assert add_content.is_element_visible(by_locator=locator), \
                "'Add content' modal is not getting displayed properly after clicking on 'Add content' button."

        assert not add_content.is_element_enabled(by_locator=add_content_locators.add_button), \
            "'Add' button in 'Add content' modal button is showing enabled even if no package details entered there."

        package_content_details = {"duty_category": "Acne patches", "country_origin": "India",
                                   "quantity": randint(1, 5), "content_value": randint(2, 10)}
        add_content.fill_add_content_form(**package_content_details)

        notification = Notifications(self.driver)
        success_notification = notification.get_notification_message()

        assert success_notification == NotificationMessages.PackagesPage.add_content_success_msg, \
            "Success notification message is missing or mismatched."

        notification.clear_notification()
        add_content.wait_for_element(lambda: add_content.is_element_visible(
            by_locator=Locators.HeaderPage.user_avatar), waiting_for="notification message to be disappear")

    def test_user_can_edit_added_content_declaration_block_under_package(self):
        """
        Test Steps:
            1. Go to Packages page
            2. Select any package from packages list table

        Scenario Tested:
        [x] Verify user can view and edit total value in a textbox inside a content declaration blocks
        """
        package_to_be_select = self.select_packages_from_packages_list_table(return_ids=True)[0]

        package_list = PackagesList(self.driver)
        sleep_execution(time_seconds=2)

        package_list.click_on_row(row_to_be_select=package_to_be_select)
        sleep_execution(time_seconds=2)
        added_content_categories = package_list.get_categories_from_package_content_table(
            package_id=package_to_be_select)[:-1]

        category_to_be_edited = random.sample(added_content_categories, k=1)[0]
        package_list.get_element_of_content_edit_delete_icon(
            package_id=package_to_be_select, category=category_to_be_edited,
            locator_value=Locators.PackagesPage.edit_content_icon).click()

        package_content_details = {"country_origin": "Canada", "quantity": 2, "content_value": 15,
                                   "content_description": "Herbal and Ayurvedic medicines"}

        add_content = AddContentModal(self.driver)
        add_content.fill_add_content_form(edit_content=True, **package_content_details)

        notification = Notifications(self.driver)
        success_notification = notification.get_notification_message()

        assert success_notification == NotificationMessages.PackagesPage.update_content_success_msg, \
            "Success notification message is missing or mismatched after editing package content."

        notification.clear_notification()
        add_content.wait_for_element(lambda: add_content.is_element_visible(
            by_locator=Locators.HeaderPage.user_avatar), waiting_for="notification message to be disappear")

    def test_create_order_modal_shows_only_pending_order_creation_packages_id(self):
        """
        Test Steps:
            1. Go to Packages page
            2. Click on "Create Order"

        Scenario Tested:
        [x] "Create Order" modal should show only those packages id whose status is "Pending order creation"
        """
        package_list = PackagesList(self.driver)
        pending_order_creation_ids = package_list.get_package_id_from_other_field_value(
            package_header=self.package_constant.PACKAGE_STATUS, values=[self.status_constant.PENDING_PAYMENT])

        packages_page_locators = Locators.PackagesPage
        PackagesPage(self.driver).click(by_locator=packages_page_locators.checkout_button)

        create_order = CreateOrderDropDown(self.driver)
        create_order.wait_for_element(lambda: create_order.is_element_visible(
            by_locator=packages_page_locators.CreateOrder.send_to_canada_button),
                                      waiting_for="create order modal gets loaded")

        package_ids_from_create_modal = package_list.get_all_packages_id(table_on_modal=True)

        assert pending_order_creation_ids == package_ids_from_create_modal, \
            "'Create Order' modal shows all packages id instead of to show only package id which status has " \
            "'Pending order creation'."

        create_order.click(by_locator=packages_page_locators.CreateOrder.create_order_modal_close_icon)
        sleep_execution(2)

    @pytest.mark.parametrize('package_receive_method', [create_order_constants.PACKAGE_RECEIVE_BY_MAIL,
                                                        create_order_constants.PACKAGE_RECEIVE_BY_PICKUP])
    def test_visibility_of_fields_under_create_order_modal(self, package_receive_method):
        """
        Test Steps:
            1. Go to Packages page
            2. Click on "Create Order" button

        Scenario Tested:
        [x] Verify user can view "how would you like to receive package details" screen after step 1
        [x] Verify user can view line 1 address textbox in a order details
        [x] Verify user can view line 2 address textbox in a order details
        [x] Verify user can view province textbox in a order details
        [x] Verify user can view post code data textbox in a order details
        """
        packages_page = PackagesPage(self.driver)
        packages_page.click(by_locator=Locators.PackagesPage.checkout_button)

        package_list = PackagesList(self.driver)
        pending_order_creation_ids = package_list.get_package_id_from_other_field_value(
            package_header=self.package_constant.PACKAGE_STATUS, values=[self.status_constant.PENDING_PAYMENT])
        package_id = random.sample(pending_order_creation_ids, k=1)[0]

        create_order = CreateOrderDropDown(self.driver)
        create_order_locators = Locators.PackagesPage.CreateOrder
        create_order.wait_for_element(lambda: create_order.is_element_visible(
            by_locator=create_order_locators.send_to_canada_button), waiting_for="create order modal gets loaded")

        package_list.select_package_by_id(package_id=package_id, element_on_modal=True)
        create_order.click(by_locator=create_order_locators.send_to_canada_button)
        sleep_execution(2)
        create_order_modal_constant = self.create_order_constants

        assert all([create_order.is_element_visible(by_locator=create_order_locators.receive_package_method_message),
                    create_order.get_element_text(by_locator=create_order_locators.receive_package_method_message) ==
                    create_order_modal_constant.PACKAGE_RECEIVE_METHOD_MESSAGE]), \
            "'{}' message is missing or mismatch on 'Order Details' panel.".format(
                create_order_modal_constant.PACKAGE_RECEIVE_METHOD_MESSAGE)

        # TO DO: Radio buttons visibilities are not working
        # for receive_method in [create_order_modal_constant.PACKAGE_RECEIVE_BY_MAIL,
        #                        create_order_modal_constant.PACKAGE_RECEIVE_BY_PICKUP]:
        #     package_receive_method_element = create_order.get_element_of_package_receive_radio_button(
        #         locator_value=receive_method)
        #
        #     assert create_order.is_element_visible(by_locator=package_receive_method_element), \
        #         "Package receive radio button for '{}' method is missing on 'Order Details' panel.".format(
        #             receive_method)

        create_order.click_element_by_javascript(element=create_order.get_element_of_package_receive_radio_button(
            locator_value=package_receive_method))

        if package_receive_method == create_order_modal_constant.PACKAGE_RECEIVE_BY_MAIL:
            elements_to_be_verify = [create_order_locators.shipping_address_name,
                                     create_order_locators.select_mail_address]

            for element in elements_to_be_verify:
                assert create_order.is_element_visible(by_locator=element), \
                    "Shipping address form is not getting displayed after clicking on package receive " \
                    "method '{}'.".format(package_receive_method)
        else:
            for pickup_location in [create_order_modal_constant.PACKAGE_PICKUP_LOCATION_MISSISSAUGA,
                                    create_order_modal_constant.PACKAGE_PICKUP_LOCATION_MARKHAM]:
                package_pickup_location_element = create_order.get_element_of_package_receive_radio_button(
                    locator_value=pickup_location)

                create_order.click_element_by_javascript(element=package_pickup_location_element)

                assert create_order.is_element_selected(element=package_pickup_location_element), \
                    "Package pickup location radio button for '{}' location is missing under 'Order Details' " \
                    "panel.".format(pickup_location)

        create_order.click_element_by_javascript(element=create_order.get_element_of_package_receive_radio_button(
            locator_value=create_order_locators.add_new_card_radio_button))

        assert create_order.is_element_visible(by_locator=create_order_locators.email_field), \
            "Email field is missing in 'Order Details' panel."

        card_and_billing_address_elements = [
            create_order_locators.name_on_card_field, create_order_locators.card_number_field,
            create_order_locators.exp_date_field, create_order_locators.cvc_field, create_order_locators.address_field,
            create_order_locators.city_field, create_order_locators.postal_code_field,
            create_order_locators.country_field, create_order_locators.pay_ca_button]

        for field_element in card_and_billing_address_elements:
            assert create_order.is_element_visible(by_locator=field_element), \
                "'Card Information' or 'Billing Address' fields are not getting displayed properly on " \
                "'Order Details' panel."

        assert not create_order.is_element_enabled(by_locator=create_order_locators.pay_ca_button), \
            "'Pay CA' button is showing enabled even though no information entered in the form."

        create_order.click(by_locator=create_order_locators.create_order_modal_close_icon)
        sleep_execution(2)

    @pytest.mark.parametrize('select_action', ['single', 'multiple'])
    @pytest.mark.parametrize('shipping_method', [create_order_constants.PACKAGE_RECEIVE_BY_MAIL,
                                                 create_order_constants.PACKAGE_RECEIVE_BY_PICKUP])
    def test_create_order_by_filling_order_and_payment_details_with_single_and_multiple_packages(
            self, select_action, shipping_method):
        """
        Test Steps:
            1. Go to Packages page
            2. Select single or multiple packages from packages list table

        Scenario Tested:
        [x] User should be able to create order by selecting single and multiple packages that, we want to ship
        [x] Verify user can proceed from step 2 a order details
        [x] Verify user can proceed to do a payment via various mode
        [x] Verify user can able to view the order confirmation details
        """
        selected_ids = self.select_packages_from_packages_list_table(select_action=select_action, return_ids=True)

        if len(selected_ids) != 0:
            packages_page = PackagesPage(self.driver)
            packages_page.click(by_locator=Locators.PackagesPage.checkout_button)

            create_order = CreateOrderDropDown(self.driver)
            create_order_locators = Locators.PackagesPage.CreateOrder
            create_order.wait_for_element(lambda: create_order.is_element_visible(
                by_locator=create_order_locators.send_to_canada_button), waiting_for="create order modal gets loaded")

            for package_id in selected_ids:
                PackagesList(self.driver).select_package_by_id(package_id=package_id, element_on_modal=True)

            create_order.click(by_locator=create_order_locators.send_to_canada_button)
            create_order.wait_for_element(lambda: create_order.is_element_visible(
                by_locator=create_order_locators.email_field), waiting_for="order details page gets loaded")

            create_order.click_element_by_javascript(element=create_order.get_element_of_package_receive_radio_button(
                locator_value=shipping_method))
            sleep_execution(2)

            select_address_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                create_order_locators.select_mail_address))
            select_address = Select(select_address_element)

            all_shipping_address = [address.text for address in select_address.options]
            address_from_canada_only = [address for address in all_shipping_address if "US" not in address]
            address_to_be_select = random.sample(address_from_canada_only[1:], k=1)[0]
            select_address.select_by_visible_text(text=address_to_be_select)

            create_order.click_element_by_javascript(element=create_order.get_element_of_package_receive_radio_button(
                locator_value=create_order_locators.add_new_card_radio_button))
            sleep_execution(2)

            same_billing_address_checkbox_element = create_order.find_element_by_css_selector(
                locator_value=create_order_locators.same_billing_address_checkbox)
            create_order.click_element_by_javascript(element=same_billing_address_checkbox_element)

            # is_same_address = create_order.is_element_selected(element=same_billing_address_checkbox_element)
            package_shipping_info = create_order.create_billing_and_payment_info_dict(
                shipping_method=shipping_method, is_same_address=True)

            create_order.fill_order_details(**package_shipping_info)
            create_order.click(by_locator=create_order_locators.pay_ca_button)

            notification = Notifications(self.driver)
            success_notification = notification.get_notification_message()

            assert success_notification == NotificationMessages.PackagesPage.create_order_success_msg, \
                "Success notification message is missing or mismatched after creating order with '{}' package " \
                "using '{}' method.".format(select_action, shipping_method)

            create_order.click(by_locator=create_order_locators.create_order_modal_close_icon)
            notification.clear_notification()
            packages_page.wait_for_element(lambda: packages_page.is_element_visible(
                by_locator=Locators.HeaderPage.user_avatar), waiting_for="notification message to be disappear")
        else:
            pytest.mark.skip("No packages found with pending payment status")

    @pytest.mark.parametrize('select_action', ['single', 'multiple'])
    def test_user_can_discard_package_from_packages_list(self, select_action):
        """
        Test Steps:
            1. Go to Packages page
            2. Select single or multiple packages from packages list table
            3. Click on "Discard" button

        Scenario Tested:
        [x] Verify user can Discard a selected records
        """
        selected_ids = self.select_packages_from_packages_list_table(select_action=select_action, return_ids=True)

        packages_page = PackagesPage(self.driver)
        packages_page.click(by_locator=Locators.PackagesPage.discard_button)

        discard_package = DiscardPackagesDropDown(self.driver)
        discard_package_locators = Locators.PackagesPage.DiscardPackage

        assert packages_page.is_element_visible(by_locator=Locators.modal), \
            "'Discard Packages' modal is not getting displayed after clicking on 'Discard' button by selecting " \
            "single or multiple packages."

        discard_package.wait_for_element(lambda: discard_package.is_element_visible(
            by_locator=discard_package_locators.discard_button), waiting_for="discard packages modal gets loaded")

        assert not discard_package.is_element_enabled(by_locator=discard_package_locators.discard_button), \
            "'Discard' button is showing enabled even if no package selected there."

        for package_id in selected_ids:
            PackagesList(self.driver).select_package_by_id(package_id=package_id, element_on_modal=True)

        assert discard_package.is_element_enabled(by_locator=discard_package_locators.discard_button), \
            "'Discard' button is not showing enabled even after selecting the packages."

        discard_package.click(by_locator=discard_package_locators.discard_button)
        sleep_execution(2)

        discard_package.click(by_locator=Locators.PackagesPage.CreateOrder.create_order_modal_close_icon)
        sleep_execution(2)

    @pytest.mark.parametrize('select_action', ['single', 'multiple'])
    def test_discard_packages_by_filling_discard_and_payment_details_with_single_and_multiple_packages(
            self, select_action):
        """
        Test Steps:
            1. Go to Packages page
            2. Select single or multiple packages from packages list table
            3. Click on "Discard" button

        Scenario Tested:
        [x] Verify user can remove all the changes with discard option
        [x] User should be able to create order by selecting single and multiple packages that, we want to ship
        [x] Verify user can proceed from step 2 a order details
        [x] Verify user can proceed to do a payment via various mode
        [x] Verify user can able to view the order confirmation details
        """
        selected_ids = self.select_packages_from_packages_list_table(
            select_action=select_action, return_ids=True, package_status=self.status_constant.INFORMATION_REQUIRED)

        if len(selected_ids) != 0:
            packages_page = PackagesPage(self.driver)
            packages_page.click(by_locator=Locators.PackagesPage.discard_button)

            discard_package = DiscardPackagesDropDown(self.driver)
            discard_package_locators = Locators.PackagesPage.DiscardPackage
            discard_package.wait_for_element(lambda: discard_package.is_element_visible(
                by_locator=discard_package_locators.discard_button), waiting_for="discard packages modal gets loaded")

            for package_id in selected_ids:
                PackagesList(self.driver).select_package_by_id(package_id=package_id, element_on_modal=True)

            discard_package.click(by_locator=discard_package_locators.discard_button)
            sleep_execution(2)
            discard_package_constant = PageConstants.PackagesPage.DiscardPackages
            create_order_locators = Locators.PackagesPage.CreateOrder

            assert int(discard_package.get_element_of_discard_package_count_and_total_charge_value(
                element_for=discard_package_constant.NUMBER_OF_DISCARDS).text) == len(selected_ids), \
                "'Number of Discards' count is getting incorrect after selecting '{}' package.".format(select_action)

            expected_total_charge = discard_package.get_expected_total_charge(discard_package_count=len(selected_ids))

            assert int(discard_package.get_element_of_discard_package_count_and_total_charge_value(
                element_for=discard_package_constant.TOTAL_CHARGE).text) == expected_total_charge, \
                "'Total Charge' value is getting incorrect after selecting '{}' package.".format(select_action)

            create_order = CreateOrderDropDown(self.driver)
            discard_package.click_element_by_javascript(
                element=create_order.get_element_of_package_receive_radio_button(
                    locator_value=create_order_locators.add_new_card_radio_button))
            sleep_execution(2)

            package_shipping_info = create_order.create_billing_and_payment_info_dict(
                shipping_method=self.create_order_constants.PACKAGE_RECEIVE_BY_PICKUP, is_same_address=False)

            discard_package.fill_discard_details(**package_shipping_info)
            discard_package.click(by_locator=create_order_locators.pay_ca_button)
            success_notification = Notifications(self.driver).get_notification_message()

            assert success_notification == NotificationMessages.PackagesPage.discard_package_success_msg, \
                "Success notification message is missing or mismatched after discarding packages with '{}' " \
                "package.".format(select_action)

            discard_package.click(by_locator=Locators.PackagesPage.CreateOrder.create_order_modal_close_icon)
            sleep_execution(2)
        else:
            pytest.mark.skip("No packages found with information required status")

    def test_verify_error_message_on_selecting_us_address_as_shipping_address(self):
        """
        Test Steps:
            1. Go to Packages page
            2. Click on "Create Order" button
            3. Select any package from packages list table
            4. Click on "Send to Canada" button and wait until it gets redirect to "Order Details" tab
            5. Select package receive method "Mail"
            6. Select address of outside the Canada as shipping address

        Scenario Tested:
        [x] Verify that it should give error message "Service available only in Canada" while selecting the address
            of outside the Canada.
        """
        selected_ids = self.select_packages_from_packages_list_table(return_ids=True)

        packages_page = PackagesPage(self.driver)
        packages_page.click(by_locator=Locators.PackagesPage.checkout_button)

        create_order = CreateOrderDropDown(self.driver)
        create_order_locators = Locators.PackagesPage.CreateOrder

        try:
            create_order.wait_for_element(lambda: create_order.is_element_visible(
                by_locator=create_order_locators.send_to_canada_button), waiting_for="create order modal gets loaded")

            for package_id in selected_ids:
                PackagesList(self.driver).select_package_by_id(package_id=package_id, element_on_modal=True)

            create_order.click(by_locator=create_order_locators.send_to_canada_button)
            create_order.wait_for_element(lambda: create_order.is_element_visible(
                by_locator=create_order_locators.email_field), waiting_for="order details page gets loaded")

            create_order.click_element_by_javascript(element=create_order.get_element_of_package_receive_radio_button(
                locator_value=self.create_order_constants.PACKAGE_RECEIVE_BY_MAIL))
            sleep_execution(2)

            select_address_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                create_order_locators.select_mail_address))
            select_address = Select(select_address_element)
            all_shipping_address = [address.text for address in select_address.options]
            address_outside_of_canada = [address for address in all_shipping_address if "US" in address]
            address_to_be_select = random.sample(address_outside_of_canada, k=1)[0]

            select_address.select_by_visible_text(text=address_to_be_select)
            create_order.wait_for_element(lambda: create_order.is_element_visible(
                by_locator=create_order_locators.invalid_address_error_msg), waiting_for="error message gets displayed")

            error_message = create_order.get_element_text(by_locator=create_order_locators.invalid_address_error_msg)

            assert error_message == self.create_order_constants.INVALID_ADDRESS_ERROR, \
                "Error message is either missing or mismatched after selecting address of outside the canada as " \
                "shipping address."
        finally:
            create_order.click(by_locator=create_order_locators.create_order_modal_close_icon)
            sleep_execution(2)

    @pytest.mark.parametrize("keyword_type", [
        package_constant.PACKAGE_ID, package_constant.PACKAGE_STATUS, package_constant.PACKAGE_RECEIVED,
        package_constant.PACKAGE_RECEIVED_FROM, package_constant.PACKAGE_SIZE, package_constant.PACKAGE_CARRIER,
        package_constant.PACKAGE_TRACKING_NUMBER])
    def test_verify_search_package_feature_functioning_properly(self, keyword_type):
        """
        Test Steps:
            1. Go to Packages page
            2. Enter any keyword from packages list tables into search field

        Scenario Tested:
        [x] Verify that search package feature should functioning properly for below listed package headers:
            - Package Id
            - Status
            - Received
            - Received From
            - Size
            - Incoming Carrier Tracking Number
            - Incoming Carrier
        """
        packages_page = PackagesPage(self.driver)
        packages_page.wait_for_element(lambda: packages_page.is_element_visible(
            by_locator=Locators.PackagesPage.search_package_field), waiting_for="create order modal gets loaded")

        header_constant = self.package_constant
        package_header_index_dict = {
            header_constant.PACKAGE_ID: 1, header_constant.PACKAGE_STATUS: 2, header_constant.PACKAGE_RECEIVED: 3,
            header_constant.PACKAGE_RECEIVED_FROM: 4, header_constant.PACKAGE_SIZE: 5,
            header_constant.PACKAGE_TRACKING_NUMBER: 6, header_constant.PACKAGE_CARRIER: 7}

        package_list = PackagesList(self.driver)
        all_values = [row.find_elements_by_tag_name("td")[package_header_index_dict[keyword_type]].text.split("\n")[0]
                      for row in package_list.table_rows]
        value_to_be_enter = random.sample(all_values, k=1)[0]

        packages_page.enter_text(by_locator=Locators.PackagesPage.search_package_field, value=value_to_be_enter)
        sleep_execution(time_seconds=5)
        search_results = [row.text for row in package_list.table_rows]

        assert all([value_to_be_enter in result for result in search_results]), \
            "Search package feature is not functioning properly for '{}' package header.".format(keyword_type)

    def test_verify_user_cannot_link_packages_from_different_vendors(self):
        """
        Test Steps:
            1. Go to Packages page
            2. Select any packages id of different vendors
            3. Click on "Link" button from top of packages list table

        Scenario Tested:
        [x] Verify that user can not link packages of different vendors.
        """
        packages_page = PackagesPage(self.driver)
        packages_page.wait_for_element(lambda: packages_page.is_element_visible(
            by_locator=Locators.PackagesPage.search_package_field), waiting_for="create order modal gets loaded")

        package_list = PackagesList(self.driver)
        status_constant = self.package_constant.PackageStatus
        packages_ids = package_list.get_package_id_from_other_field_value(
            package_header=self.package_constant.PACKAGE_STATUS, values=[status_constant.PENDING_PAYMENT,
                                                                         status_constant.INFORMATION_REQUIRED])

        package_vendor = package_list.get_package_details_by_id(package_id=packages_ids[0],
                                                                fields=[self.package_constant.PACKAGE_RECEIVED_FROM])
        temp_package_vendor = package_vendor[self.package_constant.PACKAGE_RECEIVED_FROM]
        package_list.select_package_by_id(package_id=packages_ids[0])

        for package_id in packages_ids[1:]:
            other_vendor = package_list.get_package_details_by_id(package_id=package_id,
                                                                  fields=[self.package_constant.PACKAGE_RECEIVED_FROM])

            if temp_package_vendor != other_vendor['Received From']:
                package_list.select_package_by_id(package_id=package_id)
                break

        packages_page.click(by_locator=Locators.PackagesPage.link_button)
        sleep_execution(1)
        notification = Notifications(self.driver)
        error_notification = notification.get_notification_message()

        assert error_notification == NotificationMessages.PackagesPage.link_packages_error_msg, \
            "Error notification message is either missing or mismatched after linking packages of different vendors."

        notification.clear_notification()
        packages_page.wait_for_element(lambda: packages_page.is_element_visible(
            by_locator=Locators.HeaderPage.user_avatar), waiting_for="notification message to be disappear")

    def test_verify_user_can_link_same_vendors_packages_successfully(self):
        """
        Test Steps:
            1. Go to Packages page
            2. Select any packages id of same vendors
            3. Click on "Link" button from top of packages list table

        Scenario Tested:
        [x] Verify that user can link packages of same vendors.
        """
        packages_page = PackagesPage(self.driver)
        packages_page.wait_for_element(lambda: packages_page.is_element_visible(
            by_locator=Locators.PackagesPage.search_package_field), waiting_for="create order modal gets loaded")

        package_list = PackagesList(self.driver)
        status_constant = self.package_constant.PackageStatus
        packages_ids = package_list.get_package_id_from_other_field_value(
            package_header=self.package_constant.PACKAGE_STATUS, values=[status_constant.PENDING_PAYMENT,
                                                                         status_constant.INFORMATION_REQUIRED])

        notification = Notifications(self.driver)

        try:
            package_vendor = package_list.get_package_details_by_id(
                package_id=packages_ids[0], fields=[self.package_constant.PACKAGE_RECEIVED_FROM])
            temp_package_vendor = package_vendor[self.package_constant.PACKAGE_RECEIVED_FROM]
            package_list.select_package_by_id(package_id=packages_ids[0])

            for package_id in packages_ids[1:]:
                same_vendor = package_list.get_package_details_by_id(
                    package_id=package_id, fields=[self.package_constant.PACKAGE_RECEIVED_FROM])

                if temp_package_vendor == same_vendor['Received From']:
                    package_list.select_package_by_id(package_id=package_id)
                    break

            packages_page.click(by_locator=Locators.PackagesPage.link_button)
            success_notification = notification.get_notification_message()

            assert success_notification == NotificationMessages.PackagesPage.link_packages_success_msg, \
                "Success notification message is either missing or mismatched after linking packages of same vendors."

            notification.clear_notification()
        finally:
            package_list.select_package_by_id(package_id=packages_ids[0])
            packages_page.click(by_locator=Locators.PackagesPage.unlink_button)
            packages_page.wait_for_element(lambda: packages_page.is_element_visible(
                by_locator=Locators.Notification.notification_msg_text), waiting_for="success notification for unlink")

            notification.clear_notification()
            packages_page.wait_for_element(lambda: packages_page.is_element_visible(
                by_locator=Locators.HeaderPage.user_avatar), waiting_for="notification message to be disappear")

    def test_verify_billing_address_should_same_as_shipping_address(self):
        """
        Test Steps:
            1. Go to Packages page
            2. Click on "Create Order" button
            3. Select any package from packages list table
            4. Click on "Send to Canada" button and wait until it gets redirect to "Order Details" tab
            5. Select package receive method "Mail"
            6. Select any address from Canada as shipping address

        Scenario Tested:
        [x] Verify that billing address should be same as shipping address after clicking on billing address checkbox.
        """
        selected_ids = self.select_packages_from_packages_list_table(return_ids=True)

        packages_page = PackagesPage(self.driver)
        create_order_locators = Locators.PackagesPage.CreateOrder

        try:
            packages_page.click(by_locator=Locators.PackagesPage.checkout_button)

            create_order = CreateOrderDropDown(self.driver)
            create_order.wait_for_element(lambda: create_order.is_element_visible(
                by_locator=create_order_locators.send_to_canada_button), waiting_for="create order modal gets loaded")

            for package_id in selected_ids:
                PackagesList(self.driver).select_package_by_id(package_id=package_id, element_on_modal=True)

            create_order.click(by_locator=create_order_locators.send_to_canada_button)
            sleep_execution(time_seconds=5)
            create_order.click_element_by_javascript(element=create_order.get_element_of_package_receive_radio_button(
                locator_value=self.create_order_constants.PACKAGE_RECEIVE_BY_MAIL))

            select_address_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                create_order_locators.select_mail_address))
            select_address = Select(select_address_element)
            all_shipping_address = [address.text for address in select_address.options]
            address_outside_of_canada = [address for address in all_shipping_address if "CA" in address]
            address_to_be_select = random.sample(address_outside_of_canada, k=1)[0]

            select_address.select_by_visible_text(text=address_to_be_select)
            sleep_execution(time_seconds=3)

            create_order.click_element_by_javascript(element=create_order.get_element_of_package_receive_radio_button(
                locator_value=create_order_locators.add_new_card_radio_button))
            sleep_execution(2)

            same_billing_address_checkbox_element = create_order.find_element_by_css_selector(
                locator_value=create_order_locators.same_billing_address_checkbox)
            create_order.click_element_by_javascript(element=same_billing_address_checkbox_element)
            sleep_execution(time_seconds=3)
            create_order.click_element_by_javascript(element=same_billing_address_checkbox_element)

            selected_address = select_address.all_selected_options[0].text.split(",")

            province_dict = {"ON": "Ontario", "PE": "Prince Edward Island", "BC": "British Columbia", "YT": "Yukon",
                             "CA": "Canada"}
            address_field_locator = {
                "City": create_order_locators.city_field, "Province": create_order_locators.province_field,
                "Postal Code": create_order_locators.postal_code_field, "Country": create_order_locators.country_field}

            for field_name, field_locator in address_field_locator.items():
                expected_attribute = "title" if field_name in ["Province", "Country"] else "value"
                postal_code_and_country = selected_address[2].split()

                expected_value_dict = {
                    "City": selected_address[0], "Province": province_dict[selected_address[1].strip()],
                    "Postal Code": postal_code_and_country[0], "Country": province_dict[postal_code_and_country[1]]}

                assert create_order.get_attribute_value(
                    by_locator=field_locator, attribute_name=expected_attribute) == expected_value_dict[field_name], \
                    "'{}' is not getting same as per the address selected in shipping address.".format(field_name)
        finally:
            packages_page.click(by_locator=create_order_locators.create_order_modal_close_icon)
            sleep_execution(2)
