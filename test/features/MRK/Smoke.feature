@SMOKE_TEST @MRK
Feature: Smoke Tests
"""
  Test suite to verify that the application is up and running
  """

  Background: Login Backoffice
	Given el usuario de tienda "usuario_tienda"
	When el usuario de tienda "usuario_tienda" inicia sesion con sus credenciales
	Then el usuario de tienda "usuario_tienda" inicia sesion exitosamente
	When el usuario de tienda "usuario_tienda" ingresa al listado de hubs
	Then el usuario de tienda "usuario_tienda" visualiza el listado de hubs
	When el usuario de tienda "usuario_tienda" selecciona el hub "LIM013"
	When el usuario "usuario_dad" picker "QAEBOBBIESISPSA" se loguea en la app del DAD con contraseña "Aa38796212$"
	Then el usuario "usuario_dad" inicia sesion exitosamente

  @critical
  @RESET_VALUES
  @REGISTER_SMOKE
  Scenario: Registro, Login y Armado de Carrito
	Given un nuevo usuario "usuario_app"
	When el usuario "usuario_app" registra un telefono valido
	Then el telefono del usuario "usuario_app" es registrado exitosamente
	And se genera un codigo otp para el usuario "usuario_app" que recibira por mensaje para la activacion de su cuenta
	When el usuario "usuario_app" ingresa el codigo otp recibido
	Then el codigo otp del usuario "usuario_app" es validado
	When el usuario "usuario_app" ingresa una contraseña de 6 digitos para su cuenta
	Then la contraseña para el usuario "usuario_app" es registrada exitosamente
	When el usuario "usuario_app" completa sus datos personales
	Then el sistema registra los datos del usuario "usuario_app" exitosamente
	When el usuario "usuario_app" inicia sesion con sus credenciales
	Then el usuario "usuario_app" accede a la aplicacion
	When el usuario "usuario_app" añade una nueva direccion para el hub "LIM013"
	Then la direccion del usuario "usuario_app" es añadida exitosamente
	When el usuario "usuario_app" ingresa a la vista de pedidos
	Then el usuario "usuario_app" no tiene pedidos
	When el usuario "usuario_app" busca el producto "Tor-Tees Clasico 138g"
	Then se retorna el producto "Tor-Tees Clasico 138g" para el usuario "usuario_app"
	When el usuario "usuario_app" agrega "3" unidades del producto "Tor-Tees Clasico 138g" al carrito
	Then se agrega "3" unidades del producto "Tor-Tees Clasico 138g" al carrito del usuario "usuario_app"
	When el usuario "usuario_app" busca el producto "Azucar Impalpable Universal 200g"
	Then se retorna el producto "Azucar Impalpable Universal 200g" para el usuario "usuario_app"
	When el usuario "usuario_app" agrega "10" unidades del producto "Azucar Impalpable Universal 200g" al carrito
	Then se agrega "10" unidades del producto "Azucar Impalpable Universal 200g" al carrito del usuario "usuario_app"
	And la cantidad de items agregados coincide con la cantidad de items en el carrito del usuario "usuario_app"
	And el subtotal del carrito coincide con la sumatoria de precios de los productos del carrito del usuario "usuario_app"
	When el usuario "usuario_app" vacia el carrito
	Then el carrito del usuario "usuario_app" queda vacio

  @critical
  @RESET_VALUES
  @ORDER_SMOKE
  Scenario: Login y Compra
	Given el usuario "usuario_app" con identificador "958596485" y contraseña "122222"
	When el usuario "usuario_app" inicia sesion con sus credenciales
	Then el usuario "usuario_app" accede a la aplicacion
	And el usuario "usuario_app" no tiene carrito
	When el usuario "usuario_app" selecciona la direccion de entrega "AUTOMATION TEST LIM014"
	And el usuario "usuario_app" selecciona la forma de pago "CASH_ON_DELIVERY"
	Then la direccion de entrega "AUTOMATION TEST LIM014" es seleccionada por el usuario "usuario_app"
	And la forma de pago "CASH_ON_DELIVERY" es seleccionada por el usuario "usuario_app"
	And el valor del pedido del usuario "usuario_app" es el correcto
	When el usuario "usuario_app" completa el checkout
	Then el pedido es generado exitosamente para el usuario "usuario_app"
	And el usuario "usuario_app" es redireccionado al detalle del pedido
	And el estado de la orden del usuario "usuario_app" es "PENDING_VALIDATION"





