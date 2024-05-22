@SEARCH @REGRESSION @MRK
Feature: Search
"""
  As a user
    I want to search for products
  """

  Background: Login
	Given el usuario "usuario_app" con identificador "958596485" y contraseña "122222"
	Given el usuario de tienda "usuario_tienda"
	When el usuario "usuario_app" inicia sesion con sus credenciales
	Then el usuario "usuario_app" accede a la aplicacion
	When el usuario de tienda "usuario_tienda" inicia sesion con sus credenciales
	Then el usuario de tienda "usuario_tienda" inicia sesion exitosamente
	When el usuario de tienda "usuario_tienda" ingresa al listado de hubs
	Then el usuario de tienda "usuario_tienda" visualiza el listado de hubs
	When el usuario de tienda "usuario_tienda" selecciona el hub "LIM014"

  @critical
	@allure.label.suite:Search
	@allure.labels.story:Categories
	@84152
  Scenario Outline: Busqueda de productos por categoria
	When el usuario "usuario_app" busca productos por categoria "<category>"
	Then se muestran los productos para la busqueda por "<category>"
	Examples:
	  | category            |
	  | Abarrotes Granel    |
	  | Abarrotes           |
	  | Mundo Desayuno      |
	  | Bebidas y Refrescos |
	  | Bebidas Alcoholica  |
	  | Confiteria y Snacks |
	  | Limpieza y Aseo     |
	  | Higiene Personal    |
	  | Mundo Bebe          |

  @normal
  @allure.label.suite:Search
  @allure.labels.story:Exceptions
  @SEARCH_EXCEPTIONS @91220
  Scenario: Buscar producto inexistente
	When el usuario "usuario_app" busca el producto inexistente "cemento"
	Then el sistema devuelve un mensaje de error indicando que el producto "cemento" no existe


