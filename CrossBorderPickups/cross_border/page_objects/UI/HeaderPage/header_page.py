from CrossBorderPickups.cross_border.lib.locators.locators import Locators
from CrossBorderPickups.cross_border.page_objects.BasePage import BasePage


class HeaderPage(BasePage):
    """ Page Object class for Header Page """

    def __init__(self, driver):
        super().__init__(driver)

    def do_logout(self) -> None:
        """
        Helper function to perform logout from Product

        :return: None
        """
        self.click(by_locator=Locators.HeaderPage.user_avatar)
        self.click(by_locator=Locators.HeaderPage.logout_option)
