@PRODUCTS @REGRESSION @JKR
Feature: Products
"""
  As a user
    I want to see the available products for purchase
  """

  Background: Login
	Given el usuario "usuario_app" con identificador "958596485" y contraseña "122222"
	When el usuario "usuario_app" inicia sesion con sus credenciales
	Then el usuario "usuario_app" accede a la aplicacion
	When el usuario "usuario_app" visualiza el listado de categorias para la tienda "LIM013"
	Then se retornan las categorias para la tienda "LIM013" para el usuario "usuario_app"

  @critical
	@allure.label.suite:Products
	@allure.labels.story:Categories
	@84148
  Scenario Outline: Obtener productos por categoria
	When el usuario "usuario_app" ingresa a la categoria "<category>" para el hub "LIM013"
	Then se listan los productos relacionados a la categoria "<category>" para el usuario "usuario_app"
	Examples:
	  | category             |
	  | Despensa             |
	  | Bebidas              |
	  | Lacteos y Huevos     |
	  | Frutas y Verduras    |
	  | Carnes y Aves        |
	  | Pescados y Mariscos  |
	  | Cervezas             |
	  | Licores              |
	  | Vinos                |
	  | Panaderia y Cereales |
	  | Snacks               |
	  | Dulces y Helados     |
	  | Galletas             |
	  | Listo en Minutos     |
	  | Quesos y Fiambres    |
	  | Limpieza del Hogar   |
	  | Cuidado Personal     |
	  | Bebes y Niños        |
	  | Salud Sexual         |
	  | Farmacia             |
	  | Mascotas             |
	  | Hogar y Tecnología   |

  @critical
	@allure.label.suite:Products
	@allure.labels.story:Campaigns
	@84149
  Scenario Outline: Obtener productos por campaña por hub
	When el usuario "usuario_app" visualiza el listado de campañas para el hub "<hub>"
	Then se retornan las campañas  para el hub "<hub>" para el usuario "usuario_app"
	When el usuario "usuario_app" ingresa a la campaña "<campaign>"
	Then se retorna el listado de productos para la campaña "<campaign>" para el usuario "usuario_app"
	Examples:
	  | hub    | campaign     |
	  | LIM013 | bannerXLarge |
	  | LIM013 | bannerLarge1 |
	  | LIM013 | bannerLarge2 |
	  | LIM013 | swimlane5    |


