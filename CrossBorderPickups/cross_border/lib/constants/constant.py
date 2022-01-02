from enum import Enum


class BaseConstants:
    """ Common application constants """
    # DEFAULT_BASE_URL = "https://cbp-customer-qa.crossborderpickups.ca/"
    DEFAULT_BASE_URL = "http://crossborderui.s3-website.us-east-2.amazonaws.com/#/login"
    CUSTOMER_USER_NAME = "qa_test12@yopmail.com"
    DEFAULT_PASSWORD = "123456"
    OPERATION_PORTAL_URL = "https://cbp-ops-qa.crossborderpickups.ca/"
    OPERATION_PORTAL_USERNAME = "operation@cbp.com"
    OPERATION_PORTAL_PASSWORD = "operation"
    BUSINESS_USERNAME = "jr21029@gmail.com"
    DEFAULT_TIMEOUT = 30
    CHROME_BROWSER = "Chrome"
    CHROME_BINARY_LOCATION = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    FIREFOX_BROWSER = "Firefox"
    LOCAL = "Local"
    GRID = "Grid"
    WINDOWS_SYSTEM = "Windows"
    DISCARD_CHARGE_PER_PACKAGE = 2
    ERROR_COLOR_CODE = "#F44336"
    SCREENSHOT_EXTENSION = "png"

    class Status(Enum):
        """ Test statuses Value represents abbreviated prefix """
        Skipped = 'S'
        Failed = 'F'
        Error = 'E'
        Passed = ''
        XFailed = 'XF'
        XPassed = 'XP'

    class Urls:
        """ Constants related to application page URL's """
        GRID_HUB_URL = "http://ec2-3-16-166-56.us-east-2.compute.amazonaws.com:4444/wd/hub"
        LOGIN_PAGE_URL = "account/auth/login"
        PACKAGES_PAGE_URL = "packages"
        DASHBOARD_PAGE_URL = "customerDashboard"
        ORDERS_PAGE_URL = "orders"
        PROFILE_PAGE_URL = "profile"
        SHIPPING_ORDERS_PAGE_URL = "ecommerce/orders"
        NEW_PACKAGES_PAGE_URL = "packages/add"
        OPS_PACKAGES_PAGE_URL = "packages"
        CUSTOMS_FORM_PAGE_URL = "customsForms"
        SCANNING_TOOL_PAGE_URL = "scanningTool"
        RATES_PAGE_URL = "rates"


class PageConstants:
    """ Constants related to different application web pages """

    class PackagesPage:
        """ Constants related to Packages Page """
        NO_RECORD_MESSAGE = "No Records"
        PACKAGE_ID = "Package Id"
        PACKAGE_STATUS = "Status"
        PACKAGE_RECEIVED = "Received"
        PACKAGE_RECEIVED_FROM = "Received From"
        PACKAGE_SIZE = "Size"
        PACKAGE_TRACKING_NUMBER = "Incoming Carrier Tracking Number"
        PACKAGE_CARRIER = "Incoming Carrier"
        PACKAGE_CONTENTS = "PACKAGE CONTENTS"
        CANADIAN_PROVINCES = ["Alberta", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland and Labrador",
                              "Northwest Territories", "Nova Scotia", "Nunavut", "Ontario", "Prince Edward Island",
                              "Quebec", "Saskatchewan", "Yukon"]
        CANADIAN_CITIES = ["Airdrie", "Beaumont", "Brooks", "Calgary", "Camrose", "Chestermere", "Cold Lake",
                           "Edmonton", "Fort Saskatchewan", "Grande Prairie", "Lacombe", "Leduc", "Lethbridge",
                           "Lloydminster", "Medicine Hat", "Red Deer", "Spruce Grove", "St. Albert", "Wetaskiwin"]
        POSTAL_CODES = ["M1B5P1", "C1B1Y5", "V7J3M6"]

        class PackageStatus:
            """ Constants related to Packages Status """
            AVAILABLE_FOR_PICKUP = "Available for Pickup"
            INFORMATION_REQUIRED = "Information Required"
            IN_TRANSIT = "In Transit"
            PENDING_PAYMENT = "Pending Payment"
            READY_FOR_TRANSPORT = "Ready for Transport"

        class AddContent:
            """ Constants related to Packages Content table """
            CONTENT_QTY = "Qty"
            CONTENT_VALUE = "Value"
            CONTENT_TOTAL_VALUE = "Total Value"
            CONTENT_TOTAL_VALUE_CAD = "Total Value(CAD)"
            CONTENT_EST_DUTIES = "Est. Duties"
            CONTENT_EST_TAX = "Est. Tax"
            DUTY_CATEGORY = "Duty Category"
            COUNTRY_OF_ORIGIN = "Country of Origin"

        class CreateOrder:
            """ Constants related to Create Order modal """
            PACKAGE_RECEIVE_METHOD_MESSAGE = "How would you like to receive the package ?"
            PACKAGE_RECEIVE_BY_MAIL = "Mail"
            PACKAGE_RECEIVE_BY_PICKUP = "Pickup"
            PACKAGE_PICKUP_LOCATION_MISSISSAUGA = "Mississauga"
            PACKAGE_PICKUP_LOCATION_MARKHAM = "Markham"
            PAYMENT_CARD_NUMBERS = ["3782822463100050", "5555555555554444", "4242424242424242"]
            INVALID_ADDRESS_ERROR = "Service available only in Canada"
            COUNTRY = "Country"
            PROVINCE = "Province"

        class DiscardPackages:
            """ Constants related to Discard packages modal """
            NUMBER_OF_DISCARDS = "Number of Discards"
            TOTAL_CHARGE = "Total Charge"

    class NewPackagePage:
        """ Constants related to New Package page """
        FULL_NAME = "Full Name"
        STATUS_FOR_POSTING = "Status for Posting"
        DATE_RECEIVED = "Date Received"
        CARRIER = "Carrier"
        TRACKING_NUMBER = "Tracking Number"
        VENDOR = "Vendor"
        WEIGHT = "Weight"
        REQUIRED_FIELDS = [FULL_NAME, STATUS_FOR_POSTING, DATE_RECEIVED, CARRIER, TRACKING_NUMBER, VENDOR, WEIGHT]

        class PackageStatus:
            """ Constants related to Package Status from New Package page """
            INFORMATION_REQUIRED = "Information Required"
            PENDING_PAYMENT = "Pending Payment"
            STATUSES_FOR_POSTING = [INFORMATION_REQUIRED, PENDING_PAYMENT]

        class PackageCarrier:
            """ Constants related to Package Carrier from New Package page """
            UPS = "UPS"
            USPS = "USPS"
            FED_EX = "FedEx"
            DHL = "DHL"
            AMAZON_LOGISTICS = "AMAZON LOGISTICS"
            FREIGHT = "FREIGHT"
            CENTRAL_TRANSPORT = "Central Transport"
            WALK_IN = "Walk-In"
            LASER_SHIP = "Laser Ship"
            CARRIERS = [UPS, USPS, FED_EX, DHL, AMAZON_LOGISTICS, FREIGHT, CENTRAL_TRANSPORT, WALK_IN, LASER_SHIP]

        class PackageVendors:
            """ Constants related to Package Vendors from New Package page """
            UA = "UA"
            MACY = "MACY"
            WALMART_COM = "WALMART.COM"
            AOSOM = "AOSOM"
            JLS = "JUSTIFIED LOGISTICS SOLUTIONS"
            FULL_MOON_EMPIRE = "FULL MOON EMPIRE"
            KRAFT_WERKS = "KRAFT WERKS"
            BOB_KING = "BOB KING"
            MERCOLA_COM = "MERCOLA.COM"
            BAY_LAKE = "BAY LAKE"
            VENDORS = [UA, MACY, WALMART_COM, AOSOM, JLS, FULL_MOON_EMPIRE, KRAFT_WERKS, BOB_KING, MERCOLA_COM,
                       BAY_LAKE]

        class PackageType:
            """ Constants related to Package type from New Package page """
            LARGE = "Large"
            LIGHT = "Light"
            OVERSIZE = "Oversize"
            REGULAR = "Regular"
            SKID = "Skid"

        class PackageCondition:
            """ Constants related to Package condition from New Package page """
            NEW = "New"
            USED = "Used"
            RETURNS = "Returns"
            PACKAGE_CONDITIONS = [NEW, USED, RETURNS]

        class AddContent:
            """ Constants related to "Add Content" form from New Package page """
            CATEGORY_DESCRIPTION = "Category/Description"
            QUANTITY = "Quantity"
            VALUE = "Value(each in USD)"
            ADD_BUTTON = "Add"
            CANCEL_BUTTON = "Cancel"
            REQUIRED_FIELDS = [CATEGORY_DESCRIPTION, QUANTITY, VALUE]

            PRINTER_FILAMENT = "3D Printer Filament"
            PRINTERS = "Printers"
            ACNE_PATCHES = "Acne patches"
            ACNE_TREATMENTS = "Acne treatments"
            ACOUSTIC_FOAM = "Acoustic Foam in plates and sheets"
            ACOUTIC_GUITAR = "Acoutic Guitar"
            ACRYLIC_DISPLAY = "Acrylic Display"
            CONTENT_CATEGORY = [PRINTER_FILAMENT, PRINTERS, ACNE_PATCHES, ACNE_TREATMENTS, ACOUSTIC_FOAM,
                                ACOUTIC_GUITAR, ACRYLIC_DISPLAY]

    class SideNavigationPanel:
        """ Constants related to Side navigation panel """
        SHOP_AND_SHIP = "Shop & Ship"
        OPS_SHOP_AND_SHIP = "Shop and Ship"
        ECOMMERCE = "Ecommerce"
        ECOMMERCE_SHIPPING = "Ecommerce shipping"
        PROFILE = "Profile"
        OPERATIONS = "Operations"
        CUSTOMER_SERVICE = "Customer Service"
        ADMIN_PANEL = "Admin Panel"

        class ShopAndShip:
            """ Constants related to Shop & Ship menu """
            DASHBOARD = "Dashboard"
            PACKAGES = "Packages"
            ORDERS = "Orders"
            NEW_PACKAGE = "New Package"
            SCANNING_TOOL = "Scanning Tool"
            CUSTOMS_FORMS = "Customs Forms"
            REPORTS = "Reports"
            OUTGOING_PALLET_REPORT = "Outgoing Pallet Report"
            SCANNING_CHECK_MISSING_REPORT = "Scanning Check - Missing (US) Report"
            SCANNING_CHECK_EXTRA_REPORT = "Scanning Check - Extra (US) Report"
            EMPTY_SHELF_REPORT = "Empty Shelf Report"
            PROCESSOR = "Processor"
            SHELF_REPORT = "Shelf Report"
            OPS_SHOP_AND_SHIP_OPTIONS = [NEW_PACKAGE, PACKAGES, ORDERS, CUSTOMS_FORMS, SCANNING_TOOL, REPORTS,
                                         OUTGOING_PALLET_REPORT, SCANNING_CHECK_MISSING_REPORT,
                                         SCANNING_CHECK_EXTRA_REPORT, EMPTY_SHELF_REPORT, PROCESSOR, SHELF_REPORT]

        class Ecommerce:
            """ Constants related to Ecommerce menu """
            DASHBOARD = "Dashboard"
            ORDERS = "Orders"
            SHIPMENT_BATCHES = "Shipment Batches"

        class EcommerceShipping:
            """ Constants related to Ecommerce shipping menu """
            SHIPMENTS = "Shipments"
            BATCHES = "Batches"
            RATES = "Rates"
            ECOMMERCE_SHIPPING_OPTIONS = [SHIPMENTS, BATCHES, RATES]

        class CustomerService:
            """ Constants related to Customer Service menu """
            CUSTOMER_ACCOUNT = "Customer Account"

        class AdminPanel:
            """ Constants related to Admin Panel menu """
            USER_ACCOUNT_MANAGEMENT = "User Account Management"
