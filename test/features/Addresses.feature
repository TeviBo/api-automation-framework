@ADDRESSES @REGRESSION
Feature: Addresses
"""
  As a user
    I want to add my addresses and select which one i want to use
  """

  Background: Login
	Given el usuario "usuario_app" con identificador "958596485" y contraseña "122222"
	When el usuario "usuario_app" inicia sesion con sus credenciales
	Then el usuario "usuario_app" accede a la aplicacion

  @critical
  @allure.label.suite:Addresses
  @allure.labels.story:AddAddress
  @85777
  Scenario: Agregar nueva direccion
	When el usuario "usuario_app" añade una nueva direccion para el hub "LIM013"
	Then la direccion del usuario "usuario_app" es añadida exitosamente
	When el usuario "usuario_app" añade una nueva direccion para el hub "LIM014"
	Then la direccion del usuario "usuario_app" es añadida exitosamente

  @normal
  @allure.label.suite:Addresses
  @allure.labels.story:GetAddresses
  @85778
  Scenario: Obtener direcciones del usuario
	When el usuario "usuario_app" solicita sus direcciones
	Then se retornan todas las direcciones del usuario "usuario_app"

  @normal
  @allure.label.suite:Addresses
  @allure.labels.story:AddressDetail
  @85779
  Scenario: Obtener detalle de una direccion
	When el usuario "usuario_app" selecciona la direccion "AUTOMATION TEST LIM013"
	Then se retona el detalle de la direccion "AUTOMATION TEST LIM013" del usuario "usuario_app"

  @normal
  @allure.label.suite:Addresses
  @allure.labels.story:DeleteAddress
  @85852
  Scenario: Eliminar direccion
	When el usuario "usuario_app" solicita sus direcciones
	Then se retornan todas las direcciones del usuario "usuario_app"
	When el usuario "usuario_app" elimina la direccion con nombre "AUTOMATION TEST LIM014"
	Then la direccion del usuario "usuario_app" es eliminada exitosamente

#   *** Exceptions ***

  @normal
  @allure.label.suite:Addresses
  @allure.labels.story:Exceptions
  @ADDRESS_EXCEPTIONS @85848
  Scenario: Eliminar direccion principal
	When el usuario "usuario_app" solicita sus direcciones
	Then se retornan todas las direcciones del usuario "usuario_app"
	When el usuario "usuario_app" elimina la direccion asignada como direccion principal
	Then el sistema devuelve un mensaje de error al "usuario_app" indicando que no puede eliminar la direccion principal

  @normal
  @allure.label.suite:Addresses
  @allure.labels.story:Exceptions
  @ADDRESS_EXCEPTIONS @86038
  Scenario: Limite maximo de direcciones
	When el usuario "usuario_app" solicita sus direcciones
	Then se retornan todas las direcciones del usuario "usuario_app"
	When el usuario "usuario_app" alcanzo el maximo de direcciones permitidas
	And el usuario "usuario_app" desea agregar una nueva direccion
	Then el sistema devuelve un mensaje de error al usuario "usuario_app" indicando que alcanzo el maximo de direcciones permitidas


