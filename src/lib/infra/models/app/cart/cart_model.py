from typing import Optional, Dict, Any

from src.lib.infra.models.app.products.app_product_model import AppProductModel


class CartModel:
    def __init__(self, **kwargs):
        self._data = kwargs
        self._full_data: Optional[Dict[str, Any]] = None

    # Properties
    @property
    def full_data(self) -> Optional[Dict[str, Any]]:
        return self._full_data

    @full_data.setter
    def full_data(self, full_data: Optional[Dict[str, Any]]) -> None:
        self._full_data = full_data

    @property
    def discounts_amount(self) -> float:
        return self._data.get("discounts_amount") if self._data.get("discounts_amount") is not None else 0.0

    @discounts_amount.setter
    def discounts_amount(self, discounts_amount: float) -> None:
        self._data["discounts_amount"] = discounts_amount

    @property
    def expected_total_amount(self) -> float:
        return self._data.get("expected_total_amount") if self._data.get("expected_total_amount") is not None else 0.0

    @expected_total_amount.setter
    def expected_total_amount(self, expected_total_amount: float) -> None:
        self._data["expected_total_amount"] = expected_total_amount

    @property
    def expected_subtotal_amount(self) -> float:
        return self._data.get("expected_subtotal_amount") if self._data.get(
            "expected_subtotal_amount") is not None else 0.0

    @expected_subtotal_amount.setter
    def expected_subtotal_amount(self, expected_subtotal_amount: float) -> None:
        self._data["expected_subtotal_amount"] = expected_subtotal_amount

    @property
    def shopping_cart_id(self) -> str:
        return self._data.get("shoppingCartId")

    @shopping_cart_id.setter
    def shopping_cart_id(self, cart_id: str) -> None:
        self._data["shoppingCartId"] = cart_id

    @property
    def items(self) -> list[dict]:
        return self._data.get("items")

    @items.setter
    def items(self, cart_products: list[dict]) -> None:
        self._data["items"] = cart_products

    @property
    def approximate_delivery_time(self) -> dict:
        return self._data.get("approximateDeliveryTimeResponse")

    @property
    def discounts(self) -> list[dict]:
        return self._data.get("discounts")

    @discounts.setter
    def discounts(self, discounts: list[dict]) -> None:
        self._data["discounts"] = discounts

    @property
    def shipping_address(self) -> dict:
        return self._data.get("shippingAddress")

    @property
    def product_count(self) -> int:
        return self._data.get("productCount")

    @product_count.setter
    def product_count(self, product_count: int) -> None:
        self._data["productCount"] = product_count

    @property
    def subtotal_amount(self) -> float:
        return self._data.get("subTotalAmount")

    @subtotal_amount.setter
    def subtotal_amount(self, sub_total_amount: float) -> None:
        self._data["subTotalAmount"] = sub_total_amount

    @property
    def promotional_price_oh_card_payment(self) -> float:
        return self._data.get("promotionalPriceOhCardPayment")

    @promotional_price_oh_card_payment.setter
    def promotional_price_oh_card_payment(self, promotional_price_oh_card_payment: float) -> None:
        self._data["promotionalPriceOhCardPayment"] = promotional_price_oh_card_payment

    @property
    def promotional_price_agora_card_payment(self) -> float:
        return self._data.get("promotionalPriceAgoraCardPayment")

    @promotional_price_agora_card_payment.setter
    def promotional_price_agora_card_payment(self, promotional_price_agora_card_payment: float) -> None:
        self._data["promotionalPriceAgoraCardPayment"] = promotional_price_agora_card_payment

    @property
    def min_amount_purchase(self) -> float:
        return self._data.get("minAmountPurchase")

    @min_amount_purchase.setter
    def min_amount_purchase(self, min_amount_purchase: float) -> None:
        self._data["minAmountPurchase"] = min_amount_purchase

    @property
    def store(self) -> dict:
        return self._data.get("store")

    @store.setter
    def store(self, store: dict) -> None:
        self._data["store"] = store

    @property
    def store_subsidiary(self) -> dict:
        return self._data.get("storeSubsidiary")

    @store_subsidiary.setter
    def store_subsidiary(self, store_subsidiary: dict) -> None:
        self._data["storeSubsidiary"] = store_subsidiary

    @property
    def order_number(self) -> str:
        return self._data.get("orderNumber")

    @order_number.setter
    def order_number(self, order_number: str) -> None:
        self._data["orderNumber"] = order_number

    @property
    def status(self) -> dict:
        return self._data.get("status")

    @status.setter
    def status(self, status: dict) -> None:
        self._data["status"] = status

    @property
    def shopper_name(self) -> str:
        return self._data.get("shopperName")

    @shopper_name.setter
    def shopper_name(self, shopper_name: str) -> None:
        self._data["shopperName"] = shopper_name

    @property
    def address(self) -> dict:
        return self._data.get("address")

    @address.setter
    def address(self, address: dict) -> None:
        self._data["address"] = address

    @property
    def payment(self) -> dict:
        return self._data.get("payment")

    @payment.setter
    def payment(self, payment: dict) -> None:
        self._data["payment"] = payment

    @property
    def time_slot(self) -> dict:
        return self._data.get("timeSlot")

    @time_slot.setter
    def time_slot(self, time_slot: dict) -> None:
        self._data["timeSlot"] = time_slot

    @property
    def coupon(self) -> dict:
        return self._data.get("coupon")

    @coupon.setter
    def coupon(self, coupon: dict) -> None:
        self._data["coupon"] = coupon

    @property
    def invoice(self) -> dict:
        return self._data.get("invoice")

    @invoice.setter
    def invoice(self, invoice: dict) -> None:
        self._data["invoice"] = invoice

    @property
    def bill(self) -> dict:
        return self._data.get("bill")

    @bill.setter
    def bill(self, bill: dict) -> None:
        self._data["bill"] = bill

    @property
    def customer(self) -> dict:
        return self._data.get("customer")

    @customer.setter
    def customer(self, customer: dict) -> None:
        self._data["customer"] = customer

    @property
    def message(self) -> dict:
        return self._data.get("message")

    @message.setter
    def message(self, message: dict) -> None:
        self._data["message"] = message

    @property
    def transaction_payment_list(self) -> list[dict]:
        return self._data.get("transactionPaymentList")

    @transaction_payment_list.setter
    def transaction_payment_list(self, transaction_payment_list: list[dict]) -> None:
        self._data["transactionPaymentList"] = transaction_payment_list

    @property
    def club_reward(self) -> dict:
        return self._data.get("clubReward")

    @club_reward.setter
    def club_reward(self, club_rewards: dict) -> None:
        self._data["clubReward"] = club_rewards

    def get_cart(self):
        return {
            "shoppingCartId": self.shopping_cart_id,
            "items": self.items,
            "approximateDeliveryTimeResponse": self.approximate_delivery_time,
            "discounts": self.discounts,
            "shippingAddress": self.shipping_address,
            "productCount": self.product_count,
            "subTotalAmount": self.subtotal_amount,
            "promotionalPriceOhCardPayment": self.promotional_price_oh_card_payment,
            "promotionalPriceAgoraCardPayment": self.promotional_price_agora_card_payment,
            "minAmountPurchase": self.min_amount_purchase,
            "store": self.store,
            "storeSubsidiary": self.store_subsidiary,
            "orderNumber": self.order_number,
            "status": self.status,
            "shopperName": self.shopper_name,
            "address": self.address,
            "payment": self.payment,
            "timeSlot": self.time_slot,
            "coupon": self.coupon,
            "invoice": self.invoice,
            "bill": self.bill,
            "customer": self.customer,
            "message": self.message,
            "transactionPaymentList": self.transaction_payment_list,
            "clubReward": self.club_reward,
            "discounts_amount": self.discounts_amount,
            "expected_total_amount": self.expected_total_amount,
            "expected_subtotal_amount": self.expected_subtotal_amount,
            "full_data": self.full_data
        }

    def assert_items_quantity_added(self, purchased_products: list[AppProductModel]) -> bool:
        """
        Assert if the quantity of items added to the cart is the same as the quantity of items picked by the user
        :param purchased_products: items picked by the user
        :return: True if all quantities match, False otherwise
        """
        if len(purchased_products) != len(self.items):
            return False  # If the lengths of the lists don't match, quantities can't match

        # Create a dictionary mapping product IDs to their quantities in the cart
        cart_items = {item["product"]["productId"]: item["product"]["unitCount"] for item in self.items}

        for purchased_product in purchased_products:
            # Check if the product is in the cart and the quantities match
            if cart_items.get(purchased_product.product_id) != purchased_product.quantity_purchased:
                return False

        return True  # If all items match, return True

    def assert_cart_subtotal(self, purchased_products: list[(AppProductModel, dict)]) -> float:
        """
        Calculate cart subtotal
        :param purchased_products: Items picked by user
        :return: Cart subtotal (float)
        """
        subtotal: float = 0.0
        for product in purchased_products:
            if len(product.promotions) > 0:
                subtotal += product.promotions[0]["promotionalPrice"] * product.quantity_purchased
                self.discounts_amount += round((product.product_subsidiary[0]["price"] - product.promotions[0][
                    "promotionalPrice"]) * product.quantity_purchased, 2)

            elif int(product.quantity_purchased) > 1:
                subtotal += (product.quantity_purchased * product.product_subsidiary[0][
                    "price"])
            else:
                subtotal += product.product_subsidiary[0]["price"]
        self.expected_subtotal_amount = subtotal
        return round(subtotal, 2) == round(self.subtotal_amount, 2)

    def assert_cart_total_amount(self, cart: dict) -> bool:
        """
        Calculate order total amount
        :param cart: Cart object received from response
        :return: (float) order value
        """
        self.expected_subtotal_amount = sum(
            float(item["product"]["unitPriceAmount"]) * float(item["product"]["unitCount"]) for item in self.items)
        discount_sum = sum(round(float(item["product"]["unitPriceAmount"]) - float(promo["discount"]), 2) * float(
            item["product"]["unitCount"]) for item in self.items if len(item["promotions"]) > 0 for promo in
                           item["promotions"])

        assert round(self.expected_subtotal_amount, 2) == float(cart["bill"]["subTotalAmount"]), (
            "Subtotals do not match."
            f"\n[Trace]: 'assert_cart_total_amount' method in class: '{self.__class__.__name__}'")

        assert f'{discount_sum:.2f}' == f'{cart["bill"]["discountAmount"]:.2f}', (
            "Discounts do not match."
            f"\n[Trace]: 'assert_cart_total_amount' method in class: '{self.__class__.__name__}'")

        service_cost = float(cart["bill"]["serviceCostAmount"]) - (
            float(cart["bill"]["serviceDiscountAmount"]) if cart["bill"]["serviceDiscountAmount"] else 0.0)
        delivery_cost = float(cart["bill"]["deliveryCostAmount"]) - (
            float(cart["bill"]["deliveryDiscountAmount"]) if cart["bill"]["deliveryDiscountAmount"] else 0.0)

        self.expected_total_amount = round(
            float((self.expected_subtotal_amount + delivery_cost + service_cost) - discount_sum), 2)

        return round(self.expected_total_amount, 2) == round(cart["bill"]["totalAmount"], 2)

    def assert_cart_total_amount_with_discount(self, cart: dict, method: str = "") -> bool:
        if self.bill["serviceDiscountAmount"] is None:
            self.bill["serviceDiscountAmount"] = 0.0
        if self.bill["deliveryDiscountAmount"] is None:
            self.bill["deliveryDiscountAmount"] = 0.0
        service_cost = float(self.bill["serviceCostAmount"]) - float(self.bill["serviceDiscountAmount"])
        delivery_cost = float(self.bill["deliveryCostAmount"]) - float(self.bill["deliveryDiscountAmount"])
        expected_total_amount = self.expected_subtotal_amount + service_cost + delivery_cost
        self.expected_total_amount = round(expected_total_amount, 2)

        def received_total_amount_lower_than_actual():
            return round(expected_total_amount + self.discounts_amount, 2) > cart["bill"]["totalAmount"]

        def received_total_amount_equal_to_actual():
            return round(expected_total_amount - self.bill["discountAmount"], 2) == cart["totalAmount"]

        if method.lower() == "equals":
            return received_total_amount_equal_to_actual()
        return received_total_amount_lower_than_actual()
