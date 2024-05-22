@CARDS @REGRESSION
Feature: Cards
"""
  As a user
    I want to manage my credit cards
    So that i can use them for payments
  """

  Background: Login
	Given el usuario "usuario_app" con identificador "935100051" y contraseña "122222"
	When el usuario "usuario_app" inicia sesion con sus credenciales
	Then el usuario "usuario_app" accede a la aplicacion

  @critical
  @allure.label.suite:PaymentMethods
  @allure.labels.story:GetUserCards
  @84147
  Scenario: Obtener tarjetas del usuario
	When el usuario "usuario_app" desea ver el listado de tarjetas agregadas
	Then se retorna el listado de tarjetas para el usuario "usuario_app"