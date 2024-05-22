@CART @REGRESSION @MRK
Feature: Cart
"""
  As a user
    I want to add items to my cart
    So that I can purchase them
  """

  Background: Login
	Given el usuario "usuario_app" con identificador "958596485" y contraseña "122222"
	Given el usuario de tienda "usuario_tienda"
	When el usuario "usuario_app" inicia sesion con sus credenciales
	Then el usuario "usuario_app" accede a la aplicacion
	And el usuario "usuario_app" no tiene carrito
	When el usuario de tienda "usuario_tienda" inicia sesion con sus credenciales
	Then el usuario de tienda "usuario_tienda" inicia sesion exitosamente
	When el usuario de tienda "usuario_tienda" ingresa al listado de hubs
	Then el usuario de tienda "usuario_tienda" visualiza el listado de hubs
	When el usuario de tienda "usuario_tienda" selecciona el hub "LIM014"

  @critical
  @allure.label.suite:Cart
  @allure.labels.story:AddItem
  @84154
  Scenario: Agregar item al carrito
	Given el usuario "usuario_app" busca el producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)"
	Then se retorna el producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)" para el usuario "usuario_app"
	When el usuario "usuario_app" agrega "3" unidades del producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)" al carrito
	Then se agrega "3" unidades del producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)" al carrito del usuario "usuario_app"
	When el usuario "usuario_app" busca el producto "Saman Arroz Extra Tacuari Saco 50Kg  (1 und)"
	Then se retorna el producto "Saman Arroz Extra Tacuari Saco 50Kg  (1 und)" para el usuario "usuario_app"
	When el usuario "usuario_app" agrega "5" unidades del producto "Saman Arroz Extra Tacuari Saco 50Kg  (1 und)" al carrito
	Then se agrega "5" unidades del producto "Saman Arroz Extra Tacuari Saco 50Kg  (1 und)" al carrito del usuario "usuario_app"
	And la cantidad de items agregados coincide con la cantidad de items en el carrito del usuario "usuario_app"
	And el subtotal del carrito coincide con la sumatoria de precios de los productos del carrito del usuario "usuario_app"

  @critical
	@allure.label.suite:Cart
	@allure.labels.story:GetCart
	@84155
  Scenario Outline: Obtener carrito por usuario
	Given el usuario "<identifier>" con identificador "<identifier>" y contraseña "122222"
	When el usuario "<identifier>" abre el carrito
	Then se obtiene el carrito del usuario "<identifier>"
	Examples:
	  | identifier |
	  | 935100037  |
	  | 935100042  |
	  | 958596485  |


  @critical
  @allure.label.suite:Cart
  @allure.labels.story:EmptyCart
  @RESET_VALUES
  @86258
  Scenario: Vaciar carrito
	Given el usuario "usuario_app" busca el producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)"
	Then se retorna el producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)" para el usuario "usuario_app"
	When el usuario "usuario_app" agrega "3" unidades del producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)" al carrito
	Then se agrega "3" unidades del producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)" al carrito del usuario "usuario_app"
	And la cantidad de items agregados coincide con la cantidad de items en el carrito del usuario "usuario_app"
	And el subtotal del carrito coincide con la sumatoria de precios de los productos del carrito del usuario "usuario_app"
	When el usuario "usuario_app" vacia el carrito
	Then el carrito del usuario "usuario_app" queda vacio


  @critical
  @allure.label.suite:Cart
  @allure.labels.story:RemoveProduct
  @RESET_VALUES
  @86257
  Scenario: Eliminar producto del carrito
	Given el usuario "usuario_app" busca el producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)"
	Then se retorna el producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)" para el usuario "usuario_app"
	When el usuario "usuario_app" agrega "3" unidades del producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)" al carrito
	Then se agrega "3" unidades del producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)" al carrito del usuario "usuario_app"
	When el usuario "usuario_app" busca el producto "Saman Arroz Extra Tacuari Saco 50Kg  (1 und)"
	Then se retorna el producto "Saman Arroz Extra Tacuari Saco 50Kg  (1 und)" para el usuario "usuario_app"
	When el usuario "usuario_app" agrega "5" unidades del producto "Saman Arroz Extra Tacuari Saco 50Kg  (1 und)" al carrito
	Then se agrega "5" unidades del producto "Saman Arroz Extra Tacuari Saco 50Kg  (1 und)" al carrito del usuario "usuario_app"
	And la cantidad de items agregados coincide con la cantidad de items en el carrito del usuario "usuario_app"
	And el subtotal del carrito coincide con la sumatoria de precios de los productos del carrito del usuario "usuario_app"
	When el usuario "usuario_app" elimina el product "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)" del carrito
	Then el producto es eliminado del carrito del usuario "usuario_app"
	And la cantidad de items agregados coincide con la cantidad de items en el carrito del usuario "usuario_app"
	And el subtotal del carrito coincide con la sumatoria de precios de los productos del carrito del usuario "usuario_app"


  @critical
  @allure.label.suite:Cart
  @allure.labels.story:Exceptions
  @86739 @CART_EXCEPTIONS
  Scenario: Eliminar carrito de compras vacio
	Given el usuario "usuario_app" busca el producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)"
	Then se retorna el producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)" para el usuario "usuario_app"
	When el usuario "usuario_app" agrega "3" unidades del producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)" al carrito
	Then se agrega "3" unidades del producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)" al carrito del usuario "usuario_app"
	When el usuario "usuario_app" elimina el carrito
	Then el carrito del usuario "usuario_app" es eliminado
	When el usuario "usuario_app" intenta eliminar nuevamente el carrito
	Then el sistema devuelve un error indicando que el carrito no existe


  @critical
  @allure.label.suite:Cart
  @allure.labels.story:Exceptions
  @86738 @CART_EXCEPTIONS
  Scenario: Agregar producto con cantidad mayor al stock existente
	Given el usuario "usuario_app" busca el producto "Frugos Fresh Fruit Punch Bt 500 ml (Pack x12 und)"
	When el usuario "usuario_app" agrega "30" unidades del producto "Frugos Fresh Fruit Punch Bt 500 ml (Pack x12 und)" al carrito
	Then el sistema devuelve un error indicando que no hay stock suficiente


  @critical
  @allure.label.suite:Cart
  @allure.labels.story:Exceptions
  @86905 @CART_EXCEPTIONS
  Scenario: Limite maximo de producto por compra
	Given el usuario "usuario_app" busca el producto "Colgate Pasta Dental Triple Accion 150Ml (Pack x 12 Und)"
	When el usuario "usuario_app" agrega "200" unidades del producto "Colgate Pasta Dental Triple Accion 150Ml (Pack x 12 Und)" al carrito
	Then el sistema devuelve un error indicando que se excedio la cantidad maxima de producto por compra