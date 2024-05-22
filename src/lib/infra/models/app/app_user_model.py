from typing import List, Dict, Any

from src.lib.infra.models.app.cart.cart_item_model import CartItemModel
from src.lib.infra.models.app.cart.cart_model import CartModel
from src.lib.infra.models.app.cart.order_model import OrderModel
from src.lib.infra.models.app.products.app_product_model import AppProductModel
from src.lib.infra.models.app.products.pack_product import PackProductModel
from src.lib.infra.models.base.base_user_model import UserModel


class AppUserModel(UserModel):
    def __init__(self):
        super().__init__()
        self._contact_key: str = ""
        self._identifier: str = ""
        self._phone: str = self._identifier
        self._document: str = ""
        self._cards: List[Dict[str, Any]] = []
        self._cart: (CartModel, Dict[str, Any]) = {}
        self._orders: List[(OrderModel, Dict[str, Any])] = []
        self._selected_order: (OrderModel, Dict[str, Any]) = {}
        self._selected_product: (AppProductModel, Dict[str, Any]) = {}
        self._purchased_products: List[(AppProductModel, Dict[str, Any])] = []
        self._selected_payment_method: Dict[str, Any] = {}
        self._selected_address: Dict[str, Any] = {}
        self._new_order: (OrderModel, Dict[str, Any]) = OrderModel()
        self._purchased_pack_products: List[(PackProductModel, Dict[str, Any])] = []
        self._selected_pack_product: (PackProductModel, Dict[str, Any]) = {}
        self._selected_category: Dict[str, Any] = {}
        self._selected_child_category: Dict[str, Any] = {}
        self._application: str = ""
        self._segments: List[Dict[str, Any]] = []

    #  // *** Properties *** //

    @property
    def application(self) -> str:
        return self._application

    @application.setter
    def application(self, application: str) -> None:
        self._application = application

    @property
    def selected_child_category(self) -> Dict[str, Any]:
        return self._selected_child_category

    @selected_child_category.setter
    def selected_child_category(self, selected_child_category: Dict[str, Any]) -> None:
        self._selected_child_category = selected_child_category

    @property
    def selected_category(self) -> Dict[str, Any]:
        return self._selected_category

    @selected_category.setter
    def selected_category(self, selected_category: Dict[str, Any]) -> None:
        self._selected_category = selected_category

    @property
    def selected_pack_product(self) -> (PackProductModel, Dict[str, Any]):
        return self._selected_pack_product

    @selected_pack_product.setter
    def selected_pack_product(self, selected_pack_product: (PackProductModel, Dict[str, Any])) -> None:
        self._selected_pack_product = PackProductModel(**selected_pack_product) if type(
            selected_pack_product) is Dict[str, Any] else selected_pack_product

    @property
    def purchased_pack_products(self) -> List[PackProductModel]:
        return self._purchased_pack_products

    @purchased_pack_products.setter
    def purchased_pack_products(self, pack_products: List[Dict[str, Any]]) -> None:
        self._purchased_pack_products = [PackProductModel(**pack_product) for pack_product in pack_products]

    @property
    def new_order(self) -> OrderModel:
        return self._new_order

    @new_order.setter
    def new_order(self, order: (OrderModel, Dict[str, Any])) -> None:
        self._new_order = OrderModel(**order) if type(order) is Dict[str, Any] else order

    @property
    def selected_payment_method(self) -> Dict[str, Any]:
        return self._selected_payment_method

    @selected_payment_method.setter
    def selected_payment_method(self, selected_method: Dict[str, Any]) -> None:
        self._selected_payment_method = selected_method

    @property
    def selected_address(self) -> Dict[str, Any]:
        return self._selected_address

    @selected_address.setter
    def selected_address(self, selected_address: Dict[str, Any]) -> None:
        self._selected_address = selected_address

    @property
    def selected_product(self) -> (AppProductModel, Dict[str, Any]):
        return self._selected_product

    @selected_product.setter
    def selected_product(self, selected_product: (AppProductModel, Dict[str, Any])) -> None:
        self._selected_product = AppProductModel(**selected_product) if type(
            selected_product) is Dict[str, Any] else selected_product

    @property
    def contact_key(self) -> str:
        return self._contact_key

    @contact_key.setter
    def contact_key(self, contact_key: str) -> None:
        self._contact_key = contact_key

    @property
    def identifier(self) -> str:
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str) -> None:
        self._identifier = identifier

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, phone: str) -> None:
        self._phone = phone

    @property
    def document(self) -> str:
        return self._document

    @document.setter
    def document(self, document: str) -> None:
        self._document = document

    @property
    def cards(self) -> List[Dict[str, Any]]:
        return self._cards

    @cards.setter
    def cards(self, cards: List[Dict[str, Any]]) -> None:
        self._cards = cards

    @property
    def cart(self) -> (CartModel, Dict[str, Any]):
        return self._cart

    @cart.setter
    def cart(self, cart: (CartModel, Dict[str, Any])) -> None:
        if isinstance(cart, dict):
            if cart != {}:
                # Create a backup of the current cart data
                backup_cart = self._cart.get_cart() if isinstance(self._cart, CartModel) else self._cart
                # Merge the new cart data with the backup data (if needed)
                backup_cart.update(**cart)
                self._cart = CartModel(**backup_cart)
            else:
                self._cart = cart
        else:
            self._cart = cart

    @property
    def orders(self) -> List[OrderModel | Dict[str, Any]]:
        return self._orders

    @orders.setter
    def orders(self, orders: List[OrderModel | Dict[str, Any]]) -> None:
        self._orders = [OrderModel(**order) if type(order) is dict else order for order in orders]

    @property
    def selected_order(self) -> (OrderModel, Dict[str, Any]):
        return self._selected_order

    @selected_order.setter
    def selected_order(self, selected_order: (OrderModel, Dict[str, Any])) -> None:
        self._selected_order = OrderModel(**selected_order) if type(selected_order) is dict else selected_order

    @property
    def purchased_products(self) -> List[AppProductModel]:
        return self._purchased_products

    @purchased_products.setter
    def purchased_products(self, purchased_products: List[AppProductModel | Dict[str, Any]]) -> None:
        self._purchased_products = [AppProductModel(**purchased_product) if type(
            purchased_product) is Dict[str, Any] else purchased_product for purchased_product in purchased_products]

    @property
    def segments(self) -> List[Dict[str, Any]]:
        return self._segments

    @segments.setter
    def segments(self, segments: List[Dict[str, Any]]) -> None:
        self._segments = segments

    # // *** Methods *** //

    def get_user(self) -> Dict[str, Any]:
        user_data = super().get_user()
        app_user_data = {
            'contactKey': self.contact_key,
            'identifier': self.identifier,
            'phone': self.phone,
            'document': self.document,
            'cards': self.cards,
            'cart': self.cart.get_cart() if type(self.cart) is CartModel else self.cart,
            'orders': [order.get_order() for order in self.orders] if self.orders else [],
            'selectedOrder': self.selected_order.get_order() if type(
                self.selected_order) is OrderModel else self.selected_order,
            'selectedProduct': self.selected_product.get_product() if type(
                self.selected_product) is AppProductModel else self.selected_product,
            'purchasedProducts': [purchased.get_product() for purchased in self.purchased_products],
            'selectedPaymentMethod': self.selected_payment_method,
            'selectedAddress': self.selected_address,
            'newOrder': self.new_order.get_order() if type(self.new_order) is OrderModel else self.new_order,
            'purchasedPackProducts': [purchased.get_product() for purchased in self.purchased_pack_products if
                                      type(purchased) is PackProductModel] if self.purchased_pack_products else [],
            'selectedPackProduct': self.selected_pack_product.get_product() if type(
                self.selected_pack_product) is PackProductModel else self.selected_pack_product,
            'selectedCategory': self.selected_category,
            'selectedChildCategory': self.selected_child_category,
            'application': self.application

        }

        user_data[self.user_type].update(app_user_data)
        return user_data

    def get_purchased_product_quantity(self, product_id: str) -> float:
        for prod in self.purchased_products:
            if prod.product_id == product_id:
                return float(prod.quantity_purchased)

    def get_address(self, address_name: str) -> Dict[str, Any]:
        for address in self.addresses:
            if address['title'] == address_name:
                return address

    def get_order(self, order_number: str) -> None:
        for order in self._orders:
            if order.order_number == order_number:
                self.selected_order = order
                break

    def find_product(self, product: Dict[str, Any], products: Dict[str, Any]) -> None:
        for prod in products:
            if isinstance(prod, dict):
                if prod["label"] == product:
                    self.selected_product = AppProductModel(**prod)
                    break
            else:
                if prod.label == product:
                    self.selected_product = prod
                    break

    def find_product_in_cart(self, product: AppProductModel) -> None:
        for prod in self.cart.items:
            if prod["product"]["productLabel"] == product:
                self.selected_product = CartItemModel(**prod)
                break

    def select_payment_method(self, payment_method: Dict[str, Any]) -> None:
        for card in self.cards:
            if (card['branch'] == payment_method['branch'] and
                    card['pan'].split(' ')[-1] == payment_method['last_4_digits']):
                self.selected_payment_method = card
                break
            else:
                self.selected_payment_method = payment_method

    def find_category(self, category: str, categories: List[Dict[str, Any]]) -> None:
        for cat in categories:
            if cat["name"] == category:
                self.selected_category = cat
                break

    def find_child_category(self, child_category: str, child_categories: List[Dict[str, Any]]) -> None:
        for child_cat in child_categories:
            if child_cat["label"] == child_category:
                self.selected_child_category = child_cat
                break

    def clean(self) -> None:
        super().clean()
        self.selected_child_category = {}
        self.selected_category = {}
        self.purchased_pack_products = []
        self.new_order = {}
        self.selected_address = {}
        self.cart = {}
        self.selected_payment_method = {}
        self.purchased_products = []
        self.selected_product = {}
        self.selected_order = {}
        self.orders = []
        self.document = 0
        self.phone = ""
        self.identifier = ""
        self.contact_key = ""

    def delete_cart(self) -> None:
        self.cart = {}
