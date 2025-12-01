from loyverse_api.api.endpoints import LoyverseEndpoint
from loyverse_api.models import (
    Category,
    Customer,
    Discount,
    Employee,
    Item,
    PaymentType,
    PosDevice,
    Receipt,
    Store,
)


class LoyverseEndpoints:
    """Entry point for accessing all Loyverse endpoints"""

    CATEGORIES = LoyverseEndpoint(endpoint="categories", model=Category)
    CUSTOMERS = LoyverseEndpoint(endpoint="customers", model=Customer)
    DISCOUNTS = LoyverseEndpoint(endpoint="discounts", model=Discount)
    EMPLOYEES = LoyverseEndpoint(endpoint="employees", model=Employee)
    # INVENTORY = LoyverseEndpoint(endpoint="inventory")
    ITEMS = LoyverseEndpoint(endpoint="items", model=Item)
    PAYMENT_TYPES = LoyverseEndpoint(endpoint="payment_types", model=PaymentType)
    POS_DEVICES = LoyverseEndpoint(endpoint="pos_devices", model=PosDevice)
    RECEIPTS = LoyverseEndpoint(endpoint="receipts", model=Receipt)
    STORES = LoyverseEndpoint(endpoint="stores", model=Store)
    # SHIFTS = LoyverseEndpoint(endpoint="shifts")
    # SUPPLIERS = LoyverseEndpoint(endpoint="suppliers")
    # TAXES = LoyverseEndpoint(endpoint="taxes")
    # WEBHOOKS = LoyverseEndpoint(endpoint="webhooks")
    # VARIANTS = LoyverseEndpoint(endpoint="variants")
