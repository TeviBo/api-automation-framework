@STOCK @REGRESSION @JKR
Feature: Stock

  Background: Backoffice Login
	Given el usuario "usuario_app" con identificador "958596485" y contraseña "122222"
	Given el usuario de tienda "usuario_tienda"
	Given el usuario de pmm "usuario_pmm" con permisos para cargar stock
	When el usuario "usuario_app" inicia sesion con sus credenciales
	Then el usuario "usuario_app" accede a la aplicacion
	And el usuario "usuario_app" no tiene carrito
	When el usuario de tienda "usuario_tienda" inicia sesion con sus credenciales
	Then el usuario de tienda "usuario_tienda" inicia sesion exitosamente
	When el usuario de tienda "usuario_tienda" ingresa al listado de hubs
	Then el usuario de tienda "usuario_tienda" visualiza el listado de hubs
	And el usuario de tienda "usuario_tienda" selecciona el hub "LIM013"
	When el usuario de pmm "usuario_pmm" inicia sesion con sus credenciales
	Then el usuario de pmm "usuario_pmm" inicia sesion exitosamente

  @critical
  @allure.label.suite:Stock
  @allure.labels.story:NewProductsBulk
  @91463 @NEW_PRODUCTS
  Scenario: Carga de nuevos productos desde Backoffice mediante excel
	Given el usuario "usuario_tienda" crea un set de "10" productos nuevos
	When el usuario "usuario_tienda" realiza la carga masiva de los productos mediante un archivo excel
	Then los productos deben cargarse correctamente con los datos

  @critical
	@allure.label.suite:Stock
	@allure.labels.story:NewProductsPrice&StockBulk
	@92129 @NEW_PRODUCTS
  Scenario Outline: Actualizacion de stock y precio de nuevos productos desde Backoffice mediante excel
	Given un set de productos para actualizar
	When se realiza la actualizacion de stock y precio mediante un excel desde Backoffice para el hub "<hub>"
	Then los productos deben actualizarse correctamente con los datos
	Examples:
	  | hub    |
	  | LIM014 |
	  | LIM013 |

  @critical
	@allure.label.suite:Stock
	@allure.labels.story:PMMStockUpdate
	@91191 @PMM
  Scenario Outline: Carga de inventario desde PMM
	Given un set de "10" productos para actualizar desde PMM por el usuario "usuario_pmm" para el hub "<hub>"
	When el usuario "usuario_pmm" realiza la actualizacion de stock y precio desde PMM
	Then el stock y precio de los "10" productos debe ser el enviado desde PMM
	Examples:
	  | hub    |
	  | LIM001 |
	  | LIM012 |
	  | LIM013 |

  @critical
	@allure.label.suite:Stock
	@allure.labels.story:PMMStockUpdate
	@91066 @91065 @PMM
  Scenario Outline: Carga de stock 0 desde PMM
	Given un set de "10" productos para actualizar desde PMM por el usuario "usuario_pmm" para el hub "<hub>"
	When el usuario "usuario_pmm" realiza la actualizacion de stock 0 y precio desde PMM
	Then el stock y precio de los "10" productos debe ser el enviado desde PMM
	Examples:
	  | hub    |
	  | LIM001 |
	  | LIM012 |
	  | LIM013 |

  @critical
  @allure.label.suite:Stock
  @allure.label.story:DaDStockDiscountNotification
  @91193
  Scenario: Descuento de stock luego de compra
	Given el usuario "usuario_app" con carrito
	  | product                          | quantity |
	  | Azucar Impalpable Universal 200g | 5        |
	  | Tor-Tees Clasico 138g            | 10       |
	  | Dulce de leche Gloria 200g       | 3        |
	When el usuario "usuario_app" genera la orden para la direccion "AUTOMATION TEST LIM013" con metodo de pago "VISA" terminado en "1112"
	Then la orden es generada exitosamente por el usuario "usuario_app"
	When el usuario "usuario_dad" con credenciales "QAEBOBBIESISPSA", "Aa38796212$" completa el picking de la orden
	  | product_to_pick                        | amount_to_pick |
	  | Azúcar Impalpable UNIVERSAL Bolsa 200g | 5              |
	  | Piqueos TORTEES con Sal Bolsa 138g     | 10             |
	  | Dulce de Leche GLORIA Doypack 200g     | 3              |
	Then el picking es completado exitosamente
	When el usuario "usuario_beetrack" completa el delivery de la orden
	Then el delivery es completado exitosamente