class DADOrderModel:

    def __init__(self, **kwargs):
        self._data = kwargs

    # Properties
    @property
    def customer(self) -> dict:
        return self._data.get("customer")

    @property
    def receiver(self) -> dict:
        return self._data.get("receiver")

    @property
    def state(self) -> dict:
        return self._data.get("state")

    @property
    def retirement_date(self) -> str:
        return self._data.get("retirementDate")

    @property
    def consolidated_date(self) -> str:
        return self._data.get("consolidatedDate")

    @property
    def number_packages(self) -> int:
        return self._data.get("numberPackages")

    @property
    def id_order_dispatch(self) -> int:
        return self._data.get("idOrderDispatch")

    @property
    def order_number(self) -> str:
        return self._data.get("orderNumber")

    @property
    def serial_number(self) -> str:
        return self._data.get("serialNumber")

    @property
    def payment_method_name(self) -> str:
        return self._data.get("paymentMethodName")

    @property
    def method_delivery_name(self) -> str:
        return self._data.get("methodDeliveryName")

    @property
    def dispatch_type_code(self) -> str:
        return self._data.get("dispatchTypeCode")

    @property
    def start_date_delivery_window(self) -> str:
        return self._data.get("startDateDeliveryWindow")

    @property
    def end_date_delivery_window(self) -> str:
        return self._data.get("endDateDeliveryWindow")

    @property
    def picking_client(self) -> bool:
        return self._data.get("pickingClient")

    @property
    def entity_code(self) -> str:
        return self._data.get("entityCode")

    @property
    def number_phone(self) -> str:
        return self._data.get("numberPhone")

    @property
    def district(self) -> str:
        return self._data.get("district")

    @property
    def sale_channel(self) -> str:
        return self._data.get("saleChannel")

    @property
    def amount_requested(self) -> float:
        return self._data.get("amountRequested")

    @property
    def ecommerce_id(self) -> str:
        return self._data.get("ecommerceId")

    def get_order(self):
        return {
            "customer": self.customer,
            "receiver": self.receiver,
            "state": self.state,
            "retirementDate": self.retirement_date,
            "consolidatedDate": self.consolidated_date,
            "numberPackages": self.number_packages,
            "idOrderDispatch": self.id_order_dispatch,
            "orderNumber": self.order_number,
            "serialNumber": self.serial_number,
            "paymentMethodName": self.payment_method_name,
            "methodDeliveryName": self.method_delivery_name,
            "dispatchTypeCode": self.dispatch_type_code,
            "startDateDeliveryWindow": self.start_date_delivery_window,
            "endDateDeliveryWindow": self.end_date_delivery_window,
            "pickingClient": self.picking_client,
            "entityCode": self.entity_code,
            "numberPhone": self.number_phone,
            "district": self.district,
            "saleChannel": self.sale_channel,
            "amountRequested": self.amount_requested,
            "ecommerceId": self.ecommerce_id,
        }
