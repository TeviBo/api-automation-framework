from src.lib.api.library_api import BackofficeLib, DADLib
from src.lib.infra.models.external.dad.dad_user_model import DADUserModel


# *** // Backoffice Functions // ***
def get_categories(context, user):
    """
    Retrieves the categories from the Backoffice API for the given user.

    Parameters:
    - context: The context object containing necessary information for API calls.
    - user: The user for which to retrieve the categories.

    Returns:
    - None

    """
    bo_client = BackofficeLib(f'{context.HOST}/{context.BASE_ENV_VARS["paths"]["shop"]["backoffice"]}',
                              client_id=context.VALUES["USER_DATA"]["usuario_tienda"]["session"]['client_id'],
                              access_token=context.VALUES["USER_DATA"]["usuario_tienda"]["session"]["access_token"],
                              firebase_token=context.VALUES["USER_DATA"]["usuario_tienda"]["session"]["firebase_token"],
                              identity_token=context.VALUES["USER_DATA"]["usuario_tienda"]["session"]["identity_token"],
                              token=context.VALUES["USER_DATA"]["usuario_tienda"]["session"]["token"])
    context.get_categories_response = bo_client.get_categories(
        context.VALUES["USER_DATA"]["usuario_tienda"]["session"]["user"]["storeId"])


def assert_get_categories(context):  # NOSONAR
    assert context.get_categories_response.status_code == 200, (
        '[ERROR] No se pudo obtener las categorias'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.get_categories_response.status_code}'
    )

    context.store_user.store.categories = context.get_categories_response.body['result']


def get_child_categories(context, category_id):
    bo_client = BackofficeLib(f'{context.HOST}/{context.PATHS["haert"]}',
                              client_id=context.VALUES["USER_DATA"]["usuario_tienda"]["session"]['client_id'],
                              access_token=context.VALUES["USER_DATA"]["usuario_tienda"]["session"]["access_token"],
                              firebase_token=context.VALUES["USER_DATA"]["usuario_tienda"]["session"]["firebase_token"],
                              identity_token=context.VALUES["USER_DATA"]["usuario_tienda"]["session"]["identity_token"],
                              token=context.VALUES["USER_DATA"]["usuario_tienda"]["session"]["token"])
    context.get_child_categories_response = bo_client.get_child_categories(
        context.VALUES["USER_DATA"]["usuario_tienda"]["session"]["user"]["storeId"], category_id)


def assert_get_child_categories(context):
    assert context.get_child_categories_response.status_code == 200, (
        '[ERROR] No se pudo obtener las categorias'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.get_child_categories_response.status_code}')

    context.child_categories = context.get_child_categories_response.body


# *** // DAD Functions // ***
def dad_login(context, picker_username, picker_password):
    dad_client = DADLib(context.BASE_ENV_VARS["dad"]["host"].format('login'))
    context.dad_login_response = dad_client.login(picker_username, picker_password)


def assert_dad_login(context, user):
    assert context.dad_login_response.status_code == 200, (
        '[ERROR] no se pudo iniciar sesion en el dad'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.dad_login_response.status_code}')

    assert context.dad_login_response.body["username"] != "", '[ERROR] la propiedad username viene vacia'

    assert (context.dad_login_response.body["entity"] is not None
            or context.dad_login_response.body["username"] != {}
            or context.dad_login_response.body["entity"] is not None), (
        '[ERROR] la propiedad entity viene vacia'
    )
    context.dad_user = DADUserModel(**context.dad_login_response.body)
    context.dad_user.user_type = user

    context.VALUES["USER_DATA"].update(context.dad_user.get_user())


def get_orders_to_dispatch(context, user):
    dad_client = DADLib(context.BASE_ENV_VARS["dad"]["host"].format("picking-report"),
                        token=context.VALUES["USER_DATA"][user]["session"]["access_token"])
    context.get_id_dispatch_response = dad_client.get_id_dispatch(context.dad_user.entity["entityId"],
                                                                  context.app_user.selected_order.external_order_number)


def assert_get_orders_to_dispatch(context):
    assert context.get_id_dispatch_response.status_code == 200, (
        '[ERROR] No se pudo obtener el despacho'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.get_id_dispatch_response.status_code}')

    assert context.get_id_dispatch_response.body["totalRecords"] > 0, (
        '[ERROR] no se encontraron registros de despacho'
        '\n [Expected Records Quantity]: > 0'
        f'\n [Received Records Quantity]: {context.get_id_dispatch_response.body["totalRecords"]}'
    )
    context.dad_user.order_to_pick = \
        context.get_id_dispatch_response.body["listResponseOrdersDispatchConsolidation"][0]
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


def get_products_ids_to_dispatch(context, user):
    dad_client = DADLib(context.BASE_ENV_VARS["dad"]["host"].format('picking-report'),
                        token=context.VALUES["USER_DATA"][user]["session"]["access_token"])
    context.get_products_ids_response = dad_client.get_products_ids(
        context.dad_user.order_to_pick.id_order_dispatch)


def assert_get_products_ids_to_dispatch(context):
    assert context.get_products_ids_response.status_code == 200, (
        '[ERROR] No se pudieron obtener los ids de los productos para despachar'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.get_products_ids_response.status_code}'
    )
    assert len(context.get_products_ids_response.body) > 0, (
        '[ERROR] La lista de productos esta vacia'
        '\n [Expected Length]: > 0'
        f'\n [Received Length]: {len(context.get_products_ids_response.body)}'

    )
    context.dad_user.products_to_pick = context.get_products_ids_response.body
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


def assign_order_to_picker(context, user):
    dad_client = DADLib(context.BASE_ENV_VARS["dad"]["host"].format("business-irdgco-picking"),
                        token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                        username=context.VALUES["USER_DATA"][user]["username"])
    context.assign_order_to_picker_response = dad_client.assign_order_to_picker(
        context.dad_user.get_user()[user]["products_to_pick"])


def assert_assign_order_to_picker(context):
    assert context.assign_order_to_picker_response.status_code == 200, (
        '[ERROR] El pedido no pudo ser asignado al picker'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.assign_order_to_picker_response.status_code}'
    )
    assert len(context.assign_order_to_picker_response.body["numberOrderList"]) > 0, (
        '[ERROR] El listado de ordenes a pickear esta vacio'
        '\n [Expected Quantity]: > 0'
        f'\n [Received Quantity]: {len(context.assign_order_to_picker_response.body["numberOrderList"])}'
    )


def manual_picking(context, user, amount_to_pick, product_to_pick):
    dad_client = DADLib(context.BASE_ENV_VARS["dad"]["host"].format("business-irdgco-picking"),
                        token=context.VALUES["USER_DATA"][user]["session"]["access_token"])
    context.dad_user.find_product(product_to_pick, context.dad_user.products_to_pick)
    context.dad_user.selected_product.amount_to_pick = int(amount_to_pick)
    context.manual_picking_response = dad_client.manual_picking(
        context.dad_user.entity["company"]["code"],
        context.dad_user.entity["entityId"],
        f'{context.app_user.selected_order.external_order_number}-1',
        context.dad_user.selected_product.sku,
        context.dad_user.username,
        context.dad_user.selected_product.amount_to_pick)


def assert_manual_picking(context):
    assert context.manual_picking_response.status_code == 200, (
        '[ERROR] no se pudo realizar el pickeo manual de los productos'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.manual_picking_response.status_code}'
        f'\n [Product]: \nSKU: {context.dad_user.selected_product.sku} \n[Label]: {context.picked_product["label"]}'
    )
    assert context.manual_picking_response.body["entityId"] == context.dad_user.entity["entityId"], (
        '[ERROR] el id de la entidad difiere con el enviado'
        f'\n [Expected Entity ID]: {context.dad_user.entity["entityId"]}'
        f'\n [Received Entity ID]: {context.manual_picking_response.body["entityId"]}'
    )
    assert context.manual_picking_response.body["skuCode"] == context.dad_user.selected_product.sku, (
        '[ERROR] el SKU del producto difiere con el enviado'
        f'\n [Expected SKU]: {context.dad_user.selected_product.sku}'
        f'\n [Received SKU]: {context.manual_picking_response.body["skuCode"]}'
    )
    assert context.manual_picking_response.body["amount"] == context.dad_user.selected_product.amount_to_pick, (
        '[ERROR] la cantidad pickeada recibida difiere con la enviada'
        f'\n [Expected Quantity]: {context.picked_amount}'
        f'\n [Received Quantity]: {context.manual_picking_response.body["amount"]}'
    )
    context.dad_user.picked_products.append(context.dad_user.selected_product)


def synchronize_order(context, user):
    dad_client = DADLib(context.BASE_ENV_VARS["dad"]["host"].format("business-irdgco-picking"),
                        token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                        username=context.dad_user.username,
                        company_code=context.dad_user.entity["company"]["code"])
    context.synchronize_order_response = dad_client.synchronize_orders(
        context.dad_user.order_to_pick.id_order_dispatch,
        context.app_user.selected_order.external_order_number,
        [product.get_product() for product in context.dad_user.picked_products])


def assert_synchronize_order(context):
    assert context.synchronize_order_response.status_code == 200, (
        '[ERROR] la orden no ha podido sincronizarse correctamente'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.synchronize_order_response.status_code}'
    )

    products_dict = {product.sku: product for product in context.dad_user.picked_products}
    for product in context.app_user.cart.items:
        prod = products_dict[product["product"]["productSku"]]
        if prod and prod.amount_to_pick < int(product["product"]["unitCount"]):
            product["product"]["unitCount"] = float(prod.amount_to_pick)


def complete_picking(context, **kwargs):
    dad_login(context, kwargs.get("picker_username", "QAEBOBBIESISPSA"), kwargs.get("picker_password", "Aa38796212$"))
    assert_dad_login(context, kwargs.get("user"))
    get_orders_to_dispatch(context, kwargs.get("user"))
    assert_get_orders_to_dispatch(context)
    get_products_ids_to_dispatch(context, kwargs.get("user"))
    assert_get_products_ids_to_dispatch(context)
    assign_order_to_picker(context, kwargs.get("user"))
    assert_assign_order_to_picker(context)
    for row in context.table:
        manual_picking(context, kwargs.get("user"), row["amount_to_pick"], row["product_to_pick"])
        assert_manual_picking(context)

    synchronize_order(context, kwargs.get("user"))
