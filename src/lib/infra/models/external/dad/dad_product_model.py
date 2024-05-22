class DADProductModel:
    def __init__(self, **kwargs):
        self._data = kwargs

    @property
    def id(self) -> int:
        return self._data.get("id")

    @property
    def label(self) -> str:
        return self._data.get("description").split(" - ")[1]

    @property
    def sku(self) -> str:
        return self._data.get("description").split(" - ")[0]

    @property
    def amount_requested(self) -> int:
        return self._data.get("amountRequested")

    @property
    def amount_consolidated(self) -> int:
        return self._data.get("amountConsolidated")

    @property
    def amount_cancelled(self) -> int:
        return self._data.get("amountCancelled")

    @property
    def amount_missing(self) -> int:
        return self._data.get("amountMissing")

    @property
    def amount_total(self) -> int:
        return self._data.get("amountTotal")

    @property
    def state(self) -> dict:
        return self._data.get("state")

    @property
    def id_order_dispatch(self) -> int:
        return self._data.get("idOrderDispatch")

    @property
    def ean_code(self) -> str:
        return self._data.get("eanCode")

    @property
    def amount_to_pick(self) -> int:
        return self._data.get("amount_to_pick")

    @amount_to_pick.setter
    def amount_to_pick(self, value: int) -> None:
        self._data["amount_to_pick"] = value

    def get_product(self):
        return self._data
