@STOCK @REGRESSION @MRK
Feature: Stock

  Background: Backoffice Login
	Given el usuario de tienda "usuario_tienda"
	Given el usuario de pmm "usuario_pmm" con permisos para cargar stock
	When el usuario de tienda "usuario_tienda" inicia sesion con sus credenciales
	Then el usuario de tienda "usuario_tienda" inicia sesion exitosamente
	When el usuario de tienda "usuario_tienda" ingresa al listado de hubs
	Then el usuario de tienda "usuario_tienda" visualiza el listado de hubs
	When el usuario de pmm "usuario_pmm" inicia sesion con sus credenciales
	Then el usuario de pmm "usuario_pmm" inicia sesion exitosamente

  @critical
  @allure.label.suite:Stock
  @allure.labels.story:NewProductsBulk
  @91463  @NEW_PRODUCTS
  Scenario: Carga de nuevos productos desde Backoffice mediante excel
	Given el usuario "usuario_tienda" crea un set de "10" productos nuevos
	When el usuario "usuario_tienda" realiza la carga de stock y precio mediante un excel
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
