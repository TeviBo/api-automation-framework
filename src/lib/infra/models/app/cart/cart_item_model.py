class CartItemModel:

    def __init__(self, **kwargs):
        self._data = kwargs

    @property
    def shopping_cart_item_id(self) -> str:
        return self._data.get("shoppingCartItemId")

    @shopping_cart_item_id.setter
    def shopping_cart_item_id(self, shopping_cart_item_id: str) -> None:
        self._data["shoppingCartItemId"] = shopping_cart_item_id

    @property
    def status(self) -> str:
        return self._data.get("status")

    @status.setter
    def status(self, status: str) -> None:
        self._data["status"] = status

    @property
    def change_status(self) -> str:
        return self._data.get("changeStatus")

    @change_status.setter
    def change_status(self, change_status: str) -> None:
        self._data["changeStatus"] = change_status

    @property
    def product(self) -> dict:
        return self._data.get("product")

    @property
    def is_kit(self) -> bool:
        return self._data.get("isKit")

    @is_kit.setter
    def is_kit(self, is_kit: bool) -> None:
        self._data["isKit"] = is_kit

    @property
    def product_stock_price(self) -> list[dict]:
        return self._data.get("productStockPrice")

    @product_stock_price.setter
    def product_stock_price(self, product_stock_price: list[dict]) -> None:
        self._data["productStockPrice"] = product_stock_price

    @property
    def promotions(self) -> list[dict]:
        return self._data.get("promotions")

    @promotions.setter
    def promotions(self, promotions: list[dict]) -> None:
        self._data["promotions"] = promotions

    def get_cart_item(self) -> dict:
        return self._data

    def clean(self) -> None:
        self._data = {}
