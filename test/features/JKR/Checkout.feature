@CHECKOUT @REGRESSION @JKR
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
	When el usuario de tienda "usuario_tienda" selecciona el hub "LIM013"
	When el usuario "usuario_app" busca el producto "Azucar Impalpable Universal 200g"
	Then se retorna el producto "Azucar Impalpable Universal 200g" para el usuario "usuario_app"
	When el usuario "usuario_app" agrega "3" unidades del producto "Azucar Impalpable Universal 200g" al carrito
	Then se agrega "3" unidades del producto "Azucar Impalpable Universal 200g" al carrito del usuario "usuario_app"
	When el usuario "usuario_app" busca el producto "Tor-Tees Clasico 138g"
	Then se retorna el producto "Tor-Tees Clasico 138g" para el usuario "usuario_app"
	When el usuario "usuario_app" agrega "5" unidades del producto "Tor-Tees Clasico 138g" al carrito
	Then se agrega "5" unidades del producto "Tor-Tees Clasico 138g" al carrito del usuario "usuario_app"
	And la cantidad de items agregados coincide con la cantidad de items en el carrito del usuario "usuario_app"
	And el subtotal del carrito coincide con la sumatoria de precios de los productos del carrito del usuario "usuario_app"

  @critical
  @allure.label.suite:Checkout
  @allure.labels.story:Checkout
  @RESET_VALUES
  @87015 @87017 @88893 @NEW_ORDER
  Scenario: Realizar Pedido - Happy Path
	Given el usuario "usuario_app" establece la direccion de entrega "AUTOMATION TEST LIM013"
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
	When el usuario "usuario_dad" sincroniza el pedido de JOKR
	Then el pedido es sincronizado exitosamente por el usuario "usuario_dad"
	And el estado de la orden del usuario "usuario_app" es "PICKING_FINISH"
	When se filta el despacho para el pedido del cliente desde beetrack
	Then se retorna resultado
	When creamos la ruta de entrega
	Then se crea la ruta de entrega
	When el motorizado actualiza el estado de la orden a "Recogido Exitoso"
	Then el estado de la orden es actualizado exitosamente a "Recogido Exitoso"
	And el estado de la orden del usuario "usuario_app" es "DELIVERY_ON_ROUTE"
	When el motorizado actualiza el estado de la orden a "Entrega Exitosa"
	Then el estado de la orden es actualizado exitosamente a "Entrega Exitosa"
	And el estado de la orden del usuario "usuario_app" es "SHIPPED"
	And se valida la "CAPTURA DE COBRO" generada por el pedido
	And se valida la "FACTURA DE COMPRA" generada por el pedido

  @critical
  @allure.label.suite:Checkout
  @allure.labels.story:Discounts
  @RESET_VALUES
  @84158 @DISCOUNTS
  Scenario: Realizar Pedido con producto con descuento aplicando cupon de descuento de 20 soles
	Given el usuario "usuario_app" busca el producto "Dulce de leche Gloria 200g"
	Then se retorna el producto "Dulce de leche Gloria 200g" para el usuario "usuario_app"
	When el usuario "usuario_app" agrega "3" unidades del producto "Dulce de leche Gloria 200g" al carrito
	Then se agrega "3" unidades del producto "Dulce de leche Gloria 200g" al carrito del usuario "usuario_app"
	And la cantidad de items agregados coincide con la cantidad de items en el carrito del usuario "usuario_app"
	And el subtotal del carrito coincide con la sumatoria de precios de los productos del carrito del usuario "usuario_app"
	When el usuario "usuario_app" establece la direccion de entrega "AUTOMATION TEST LIM013"
	Then la direccion de entrega "AUTOMATION TEST LIM013" es establecida por el usuario "usuario_app"
	When el usuario "usuario_app" selecciona la tarjeta "VISA" terminada en "1112"
	Then la tarjeta "VISA" terminada en "1112" es seleccionada por el usuario "usuario_app"
	When el usuario "usuario_app" aplica el cupon de descuento "SR20X20"
	Then el cupon de descuento "SR20X20" es aplicado por el usuario "usuario_app"
	And la cantidad de soles a descontar al usuario "usuario_app" es "20"
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
	When el usuario "usuario_dad" pickea "3" items del producto "Dulce de Leche GLORIA Doypack 200g"
	Then los productos son pickeados exitosamente por el usuario "usuario_dad"
	When el usuario "usuario_dad" sincroniza el pedido de JOKR
	Then el pedido es sincronizado exitosamente por el usuario "usuario_dad"
	And el estado de la orden del usuario "usuario_app" es "PICKING_FINISH"
	When se filta el despacho para el pedido del cliente desde beetrack
	Then se retorna resultado
	When creamos la ruta de entrega
	Then se crea la ruta de entrega
	When el motorizado actualiza el estado de la orden a "Recogido Exitoso"
	Then el estado de la orden es actualizado exitosamente a "Recogido Exitoso"
	And el estado de la orden del usuario "usuario_app" es "DELIVERY_ON_ROUTE"
	When el motorizado actualiza el estado de la orden a "Entrega Exitosa"
	Then el estado de la orden es actualizado exitosamente a "Entrega Exitosa"
	And el estado de la orden del usuario "usuario_app" es "SHIPPED"
	And se valida la "CAPTURA DE COBRO" generada por el pedido
	And se valida la "FACTURA DE COMPRA" generada por el pedido

  @allure.label.suite:Checkout
  @allure.labels.story:PartialPicking
  @critical
  @RESET_VALUES
  @91166 @PARTIAL_ORDER @PICKING_PARTIAL
  Scenario: Picking partial - Pickear cantidad menor a la solicitada
	Given el usuario "usuario_app" establece la direccion de entrega "AUTOMATION TEST LIM013"
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
	When el usuario "usuario_dad" pickea "2" items del producto "Azúcar Impalpable UNIVERSAL Bolsa 200g"
	Then los productos son pickeados exitosamente por el usuario "usuario_dad"
	When el usuario "usuario_dad" pickea "5" items del producto "Piqueos TORTEES con Sal Bolsa 138g"
	Then los productos son pickeados exitosamente por el usuario "usuario_dad"
	When el usuario "usuario_dad" sincroniza el pedido de JOKR
	Then el pedido es sincronizado exitosamente por el usuario "usuario_dad"
	And el estado de la orden del usuario "usuario_app" es "PICKING_FINISH"
	When se filta el despacho para el pedido del cliente desde beetrack
	Then se retorna resultado
	When creamos la ruta de entrega
	Then se crea la ruta de entrega
	When el motorizado actualiza el estado de la orden a "Recogido Exitoso"
	Then el estado de la orden es actualizado exitosamente a "Recogido Exitoso"
	And el estado de la orden del usuario "usuario_app" es "DELIVERY_ON_ROUTE"
	When el motorizado actualiza el estado de la orden a "Entrega Exitosa"
	Then el estado de la orden es actualizado exitosamente a "Entrega Exitosa"
	And el estado de la orden del usuario "usuario_app" es "SHIPPED"
	And se valida la "CAPTURA DE COBRO" generada por el pedido
	And se valida la "FACTURA DE COMPRA" generada por el pedido

  @critical
  @allure.label.suite:Checkout
  @allure.labels.story:PartialPicking
  @RESET_VALUES @PICKING_PARTIAL @NULL_PICKING
  Scenario: Picking partial - Pickeo total de un producto y nulo de otro
	Given el usuario "usuario_app" establece la direccion de entrega "AUTOMATION TEST LIM013"
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
	When el usuario "usuario_dad" pickea "0" items del producto "Piqueos TORTEES con Sal Bolsa 138g"
	Then los productos son pickeados exitosamente por el usuario "usuario_dad"
	When el usuario "usuario_dad" sincroniza el pedido de JOKR
	Then el pedido es sincronizado exitosamente por el usuario "usuario_dad"
	And el estado de la orden del usuario "usuario_app" es "PICKING_FINISH"
	When se filta el despacho para el pedido del cliente desde beetrack
	Then se retorna resultado
	When creamos la ruta de entrega
	Then se crea la ruta de entrega
	When el motorizado actualiza el estado de la orden a "Recogido Exitoso"
	Then el estado de la orden es actualizado exitosamente a "Recogido Exitoso"
	And el estado de la orden del usuario "usuario_app" es "DELIVERY_ON_ROUTE"
	When el motorizado actualiza el estado de la orden a "Entrega Exitosa"
	Then el estado de la orden es actualizado exitosamente a "Entrega Exitosa"
	And el estado de la orden del usuario "usuario_app" es "SHIPPED"
	And se valida la "CAPTURA DE COBRO" generada por el pedido
	And se valida la "FACTURA DE COMPRA" generada por el pedido

  @critical
  @allure.label.suite:Checkout
  @allure.labels.story:CheckoutExceptions
  @RESET_VALUES
  @94073
  Scenario: Aplicar cupon de descuento invalido
	Given el usuario "usuario_app" establece la direccion de entrega "AUTOMATION TEST LIM013"
	Then la direccion de entrega "AUTOMATION TEST LIM013" es establecida por el usuario "usuario_app"
	When el usuario "usuario_app" selecciona la tarjeta "VISA" terminada en "1112"
	Then la tarjeta "VISA" terminada en "1112" es seleccionada por el usuario "usuario_app"
	When el usuario "usuario_app" aplica el cupon de descuento "test"
	Then el sistema devuelve un mensaje de error por cupon invalido

  @critical
  @allure.label.suite:Checkout
  @allure.labels.story:CheckoutExceptions
  @RESET_VALUES
  @105918 @EXCEPTIONS @CHECKOUT_EXCEPTIONS
  Scenario: Realizar Pedido - Tarjeta invalida
	Given el usuario "usuario_app" establece la direccion de entrega "AUTOMATION TEST LIM013"
	Then la direccion de entrega "AUTOMATION TEST LIM013" es establecida por el usuario "usuario_app"
	When el usuario "usuario_app" selecciona la tarjeta "VISA" terminada en "9826"
	Then la tarjeta "VISA" terminada en "9826" es seleccionada por el usuario "usuario_app"
	And el valor del pedido del usuario "usuario_app" es correcto
	When el usuario "usuario_app" completa el checkout
	Then se muestra un mensaje de error al usuario "usuario_app" indicando que su revise los datos de su tarjeta
