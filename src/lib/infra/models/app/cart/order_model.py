from typing import Dict, Any, List


class OrderModel:
    def __init__(self, **kwargs):
        self._data = kwargs
        self._external_order_number: str = ""

    @property
    def external_order_number(self) -> str:
        return self._external_order_number

    @external_order_number.setter
    def external_order_number(self, external_order_number: str) -> None:
        self._external_order_number = external_order_number

    @property
    def order_number(self) -> int:
        return self._data.get("orderNumber")

    @order_number.setter
    def order_number(self, order_number: int) -> None:
        self._data["orderNumber"] = order_number

    @property
    def total_amount(self) -> float:
        return self._data.get("totalAmount")

    @total_amount.setter
    def total_amount(self, total_amount: float) -> None:
        self._data["totalAmount"] = total_amount

    @property
    def delivery_date(self) -> str:
        return self._data.get("deliveryDate")

    @delivery_date.setter
    def delivery_date(self, delivery_date: str) -> None:
        self._data["deliveryDate"] = delivery_date

    @property
    def club_reward_used(self) -> bool:
        return self._data.get("clubRewardUsed")

    @club_reward_used.setter
    def club_reward_used(self, club_reward_used: bool) -> None:
        self._data["clubRewardUsed"] = club_reward_used

    @property
    def club_reward_used_formatted(self) -> str:
        return self._data.get("clubRewardUsedFormatted")

    @club_reward_used_formatted.setter
    def club_reward_used_formatted(self, club_reward_used_formatted: str) -> None:
        self._data["clubRewardUsedFormatted"] = club_reward_used_formatted

    @property
    def status(self) -> str:
        return self._data.get("status")

    @status.setter
    def status(self, status: str) -> None:
        self._data["status"] = status

    @property
    def address(self) -> str:
        return self._data.get("address")

    @address.setter
    def address(self, address: Dict[str, Any]) -> None:
        self._data["address"] = address

    @property
    def time_slot(self) -> str:
        return self._data.get("timeSlot")

    @time_slot.setter
    def time_slot(self, time_slot: Dict[str, Any]) -> None:
        self._data["timeSlot"] = time_slot

    @property
    def payment(self) -> Dict[str, Any]:
        return self._data.get("payment")

    @payment.setter
    def payment(self, payment: Dict[str, Any]) -> None:
        self._data["payment"] = payment

    @property
    def coupon(self) -> Dict[str, Any]:
        return self._data.get("coupon")

    @coupon.setter
    def coupon(self, coupon: Dict[str, Any]) -> None:
        self._data["coupon"] = coupon

    @property
    def invoice(self) -> Dict[str, Any]:
        return self._data.get("invoice")

    @invoice.setter
    def invoice(self, invoice: Dict[str, Any]) -> None:
        self._data["invoice"] = invoice

    @property
    def cart(self) -> Dict[str, Any]:
        return self._data.get("cart")

    @cart.setter
    def cart(self, cart: Dict[str, Any]) -> None:
        self._data["cart"] = cart

    @property
    def bill(self) -> Dict[str, Any]:
        return self._data.get("bill")

    @bill.setter
    def bill(self, bill: Dict[str, Any]) -> None:
        self._data["bill"] = bill

    @property
    def transaction_payment_list(self) -> List:
        return self._data.get("transactionPaymentList")

    @transaction_payment_list.setter
    def transaction_payment_list(self, transaction_payment_list: List) -> None:
        self._data["transactionPaymentList"] = transaction_payment_list

    def get_order(self):
        return self._data

    def clean(self):
        self._data = {}
        self.external_order_number = ""
