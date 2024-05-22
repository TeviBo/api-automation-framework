@CHECKOUT @REGRESSION @MRK
Feature: Checkout
"""
  As a user
      I want to checkout
      So that I can pay for my items
  """

  Background: Login y armado de carrito
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
	When el usuario "usuario_app" busca el producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)"
	Then se retorna el producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)" para el usuario "usuario_app"
	When el usuario "usuario_app" agrega "3" unidades del producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)" al carrito
	Then se agrega "3" unidades del producto "Gatorade Rehidratante Tropical Bt 500 ml (Pack x12 und)" al carrito del usuario "usuario_app"
	When el usuario "usuario_app" busca el producto "Saman Arroz Extra Tacuari Saco 50Kg  (1 und)"
	Then se retorna el producto "Saman Arroz Extra Tacuari Saco 50Kg  (1 und)" para el usuario "usuario_app"
	When el usuario "usuario_app" agrega "5" unidades del producto "Saman Arroz Extra Tacuari Saco 50Kg  (1 und)" al carrito
	Then se agrega "5" unidades del producto "Saman Arroz Extra Tacuari Saco 50Kg  (1 und)" al carrito del usuario "usuario_app"
	And la cantidad de items agregados coincide con la cantidad de items en el carrito del usuario "usuario_app"
	And el subtotal del carrito coincide con la sumatoria de precios de los productos del carrito del usuario "usuario_app"

  @allure.label.suite:Checkout
  @allure.labels.story:Checkout
  @RESET_VALUES
  @87015 @87017 @88893 @NEW_ORDER
  Scenario: Realizar Pedido - Happy Path
	Given el usuario "usuario_app" selecciona la direccion de entrega "AUTOMATION TEST LIM014"
	And el usuario "usuario_app" selecciona la forma de pago "CASH_ON_DELIVERY"
	Then la direccion de entrega "AUTOMATION TEST LIM014" es seleccionada por el usuario "usuario_app"
	And la forma de pago "CASH_ON_DELIVERY" es seleccionada por el usuario "usuario_app"
	And el valor del pedido del usuario "usuario_app" es el correcto
	When el usuario "usuario_app" completa el checkout
	Then el pedido es generado exitosamente para el usuario "usuario_app"
	And el usuario "usuario_app" es redireccionado al detalle del pedido
	And el estado de la orden del usuario "usuario_app" es "PENDING_VALIDATION"

  @allure.label.suite:Checkout
  @allure.labels.story:Discounts
  @RESET_VALUES
  @84158 @DISCOUNTS
  Scenario: Realizar Pedido con producto con descuento aplicando cupon de descuento de 20 soles
	Given el usuario "usuario_app" busca el producto "Gloria Leche Uht Sin Lactosa Bolsa 900Ml  (1 Und)"
	Then se retorna el producto "Gloria Leche Uht Sin Lactosa Bolsa 900Ml  (1 Und)" para el usuario "usuario_app"
	When el usuario "usuario_app" agrega "3" unidades del producto "Gloria Leche Uht Sin Lactosa Bolsa 900Ml  (1 Und)" al carrito
	Then se agrega "3" unidades del producto "Gloria Leche Uht Sin Lactosa Bolsa 900Ml  (1 Und)" al carrito del usuario "usuario_app"
	And la cantidad de items agregados coincide con la cantidad de items en el carrito del usuario "usuario_app"
	And el subtotal del carrito coincide con la sumatoria de precios de los productos del carrito del usuario "usuario_app"
	When el usuario "usuario_app" selecciona la direccion de entrega "AUTOMATION TEST LIM014"
	And el usuario "usuario_app" selecciona la forma de pago "CASH_ON_DELIVERY"
	Then la direccion de entrega "AUTOMATION TEST LIM014" es seleccionada por el usuario "usuario_app"
	And la forma de pago "CASH_ON_DELIVERY" es seleccionada por el usuario "usuario_app"
	And el valor del pedido del usuario "usuario_app" es el correcto
	When el usuario "usuario_app" aplica el cupon de descuento "PIKACHU"
	Then el cupon de descuento "PIKACHU" es aplicado por el usuario "usuario_app"
	And la cantidad de soles a descontar al usuario "usuario_app" es "20"
	And el valor del pedido del usuario "usuario_app" es el correcto
	When el usuario "usuario_app" completa el checkout
	Then el pedido es generado exitosamente para el usuario "usuario_app"
	And el usuario "usuario_app" es redireccionado al detalle del pedido
	And el estado de la orden del usuario "usuario_app" es "PENDING_VALIDATION"

  @allure.label.suite:Checkout
  @allure.labels.story:CheckoutExceptions
  @RESET_VALUES
  @94073
  Scenario: Aplicar cupon de descuento invalido
	Given el usuario "usuario_app" selecciona la direccion de entrega "AUTOMATION TEST LIM014"
	And el usuario "usuario_app" selecciona la forma de pago "CASH_ON_DELIVERY"
	Then la direccion de entrega "AUTOMATION TEST LIM014" es seleccionada por el usuario "usuario_app"
	And la forma de pago "CASH_ON_DELIVERY" es seleccionada por el usuario "usuario_app"
	When el usuario "usuario_app" aplica el cupon de descuento "test"
	Then el sistema devuelve un mensaje de error por cupon invalido

  @allure.label.suite:Checkout
  @allure.labels.story:CheckoutExceptions
  @RESET_VALUES
  @normal
  @105918 @EXCEPTIONS @CHECKOUT_EXCEPTIONS @NOT_LIM014
  Scenario: Realizar Pedido - Tarjeta invalida
	Given el usuario "usuario_app" establece la direccion de entrega "AUTOMATION TEST LIM014"
	Then la direccion de entrega "AUTOMATION TEST LIM014" es establecida por el usuario "usuario_app"
	Then la direccion de entrega "AUTOMATION TEST LIM014" es establecida por el usuario "usuario_app"
	When el usuario "usuario_app" selecciona la tarjeta "VISA" terminada en "9826"
	Then la tarjeta "VISA" terminada en "9826" es seleccionada por el usuario "usuario_app"
	And el valor del pedido del usuario "usuario_app" es el correcto
	When el usuario "usuario_app" completa el checkout
	Then se muestra un mensaje de error al usuario "usuario_app" indicando que su revise los datos de su tarjeta
