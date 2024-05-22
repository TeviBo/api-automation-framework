@ORDERS @REGRESSION
Feature: Orders
"""
  As a user
    I want to be able to order a product
    And see my order listed in the orders page
    So that I can keep track of my orders
  """

  Background: Login
	Given el usuario "usuario_app" con identificador "958596485" y contraseña "122222"
	When el usuario "usuario_app" inicia sesion con sus credenciales
	Then el usuario "usuario_app" accede a la aplicacion

  @critical
  @allure.label.suite:Orders
  @allure.labels.story:GetOrders
  @87822
  Scenario: Obtener ordenes del usuario
	When el usuario "usuario_app" ingresa a la vista de pedidos
	Then se listan todos los pedidos realizados por el usuario "usuario_app"


  @critical
  @allure.label.suite:Orders
  @allure.labels.story:OrderDetail
  @87823
  Scenario: Obtener detalle de una orden
	When el usuario "usuario_app" ingresa a la vista de pedidos
	Then se listan todos los pedidos realizados por el usuario "usuario_app"
	When el usuario "usuario_app" ingresa al detalle del pedido
	Then se muestra el detalle del pedido para el usuario "usuario_app"