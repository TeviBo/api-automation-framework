@SMOKE_TEST @JKR
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
	When el usuario "usuario_app" busca el producto "Azucar Impalpable Universal 200g"
	Then se retorna el producto "Azucar Impalpable Universal 200g" para el usuario "usuario_app"
	When el usuario "usuario_app" agrega "3" unidades del producto "Azucar Impalpable Universal 200g" al carrito
	Then se agrega "3" unidades del producto "Azucar Impalpable Universal 200g" al carrito del usuario "usuario_app"
	When el usuario "usuario_app" busca el producto "Tor-Tees Clasico 138g"
	Then se retorna el producto "Tor-Tees Clasico 138g" para el usuario "usuario_app"
	When el usuario "usuario_app" agrega "5" unidades del producto "Tor-Tees Clasico 138g" al carrito
	Then se agrega "5" unidades del producto "Tor-Tees Clasico 138g" al carrito del usuario "usuario_app"
	When el usuario "usuario_app" busca el producto "Quinua Costeño 500g"
	Then se retorna el producto "Quinua Costeño 500g" para el usuario "usuario_app"
	When el usuario "usuario_app" agrega "1" unidades del producto "Quinua Costeño 500g" al carrito
	Then se agrega "1" unidades del producto "Quinua Costeño 500g" al carrito del usuario "usuario_app"
	And la cantidad de items agregados coincide con la cantidad de items en el carrito del usuario "usuario_app"
	And el subtotal del carrito coincide con la sumatoria de precios de los productos del carrito del usuario "usuario_app"
	When el usuario "usuario_app" establece la direccion de entrega "AUTOMATION TEST LIM013"
	Then la direccion de entrega "AUTOMATION TEST LIM013" es establecida por el usuario "usuario_app"
	Then la direccion de entrega "AUTOMATION TEST LIM013" es establecida por el usuario "usuario_app"
	When el usuario "usuario_app" selecciona la tarjeta "VISA" terminada en "1112"
	Then la tarjeta "VISA" terminada en "1112" es seleccionada por el usuario "usuario_app"
	And el valor del pedido del usuario "usuario_app" es correcto
	When el usuario "usuario_app" completa el checkout
	Then el pedido es generado exitosamente para el usuario "usuario_app"
	And el usuario "usuario_app" es redireccionado al detalle del pedido
	And el estado de la orden del usuario "usuario_app" es "PENDING_VALIDATION"
	And se valida la "NOTA DE VENTA" generada por el pedido
	And se valida la "AUTORIZACION DE COBRO" generada por el pedido
	When el usuario "usuario_dad" picker "QAEBOBBIESISPSA" se loguea en la app del DAD con contraseña "Aa38796212$"
	Then el usuario "usuario_dad" inicia sesion exitosamente
	When el usuario "usuario_app" captura la nota de venta generada por el pedido de JOKR
	Then la nota de venta es capturada exitosamente por el usuario "usuario_app"
	When el usuario "usuario_dad" obtiene las ordenes de despacho del pedido generado
	Then se obtienen las ordenes de despacho a asignar por el usuario "usuario_dad"
	When el usuario "usuario_dad" obtiene los productos en el dad para asignarlos
	Then los productos son obtenidos exitosamente por el usuario "usuario_dad"
	When el pedido es asignado al usuario "usuario_dad"
	Then el pedido es asignado exitosamente al usuario "usuario_dad"
	And el estado de la orden del usuario "usuario_app" es "PICKING_STARTED"
	When el usuario "usuario_dad" pickea "3" items del producto "Azúcar Impalpable UNIVERSAL Bolsa 200g"
	Then los productos son pickeados exitosamente por el usuario "usuario_dad"
	When el usuario "usuario_dad" pickea "5" items del producto "Piqueos TORTEES con Sal Bolsa 138g"
	Then los productos son pickeados exitosamente por el usuario "usuario_dad"
	When el usuario "usuario_dad" pickea "1" items del producto "Quinua COSTEÑO Bolsa 500g"
	Then los productos son pickeados exitosamente por el usuario "usuario_dad"
	When el usuario "usuario_dad" sincroniza el pedido de JOKR
	Then el pedido es sincronizado exitosamente por el usuario "usuario_dad"
	And el estado de la orden del usuario "usuario_app" es "PICKING_FINISH"
	When se filta el despacho para el pedido del cliente desde beetrack
	Then se retorna resultado
	When creamos la ruta
	Then se crea la ruta
	When el motorizado actualiza el estado de la orden a "Recogido Exitoso"
	Then el estado de la orden es actualizado exitosamente a "Recogido Exitoso"
	And el estado de la orden del usuario "usuario_app" es "DELIVERY_ON_ROUTE"
	When el motorizado actualiza el estado de la orden a "Entrega Exitosa"
	Then el estado de la orden es actualizado exitosamente a "Entrega Exitosa"
	And el estado de la orden del usuario "usuario_app" es "SHIPPED"
	And se valida la "CAPTURA DE COBRO" generada por el pedido
	And se valida la "FACTURA DE COMPRA" generada por el pedido





