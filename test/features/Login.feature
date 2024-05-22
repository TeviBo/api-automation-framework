@LOGIN
Feature: Login
"""
As a user
	I want to login to the application
	So that I can access the application's features
"""

  @critical
  @allure.label.suite:Login
  @allure.labels.story:Login
  Scenario: Login Exitoso
	Given el usuario "usuario_app" con identificador "958596485" y contraseña "122222"
	And con direccion en rango del hub "LIM013"
	When el usuario "usuario_app" inicia sesion con sus credenciales
	Then el usuario "usuario_app" accede a la aplicacion