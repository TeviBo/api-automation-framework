@PROMOTIONS @PACKS @REGRESSION @JKR @PRODUCTS
Feature: Promotion Pack

  Background: Login de usuario app y tienda
	Given el usuario "usuario_app" con identificador "958596485" y contraseña "122222"
	Given el usuario de tienda "usuario_tienda"
	When el usuario "usuario_app" inicia sesion con sus credenciales
	Then el usuario "usuario_app" accede a la aplicacion
	When el usuario de tienda "usuario_tienda" inicia sesion con sus credenciales
	Then el usuario de tienda "usuario_tienda" inicia sesion exitosamente
	When el usuario de tienda "usuario_tienda" ingresa al listado de hubs
	Then el usuario de tienda "usuario_tienda" visualiza el listado de hubs
	When el usuario de tienda "usuario_tienda" selecciona el hub "LIM013"
	Then el hub "LIM013" es seleccionado por el usuario de tienda "usuario_tienda"
	When el usuario de tienda "usuario_tienda" visualiza el listado de categorias para la tienda "LIM013"
	Then se retornan las categorias para la tienda "LIM013" para el usuario de tienda "usuario_tienda"
	And sus categorias hijas

  @normal
  @allure.label.suite:Promotions
  @allure.labels.story:Packs
  @103617
  Scenario: Listar Packs
	When el usuario "usuario_tienda" el usuario accede al modulo de promociones
	Then se listan en una tabla todas las promociones para el usuario "usuario_tienda"

  @normal
  @allure.label.suite:Promotions
  @allure.labels.story:Packs
  @96008
  Scenario: Obtener Pack
	Given el usuario de tienda "usuario_tienda"
	When el usuario de tienda "usuario_tienda" inicia sesion con sus credenciales
	Then el usuario de tienda "usuario_tienda" inicia sesion exitosamente
	When el usuario de tienda "usuario_tienda" ingresa al listado de hubs
	Then el usuario de tienda "usuario_tienda" visualiza el listado de hubs
	When el usuario de tienda "usuario_tienda" selecciona el hub "LIM013"
	Then el hub "LIM013" es seleccionado por el usuario de tienda "usuario_tienda"
	When el usuario "usuario_tienda" ingresa al detalle del pack "K000465"
	Then se retorna la informacion de la promocion pack "K000465" para el usuario "usuario_tienda"

  @critical
	@allure.label.suite:Promotions
	@allure.labels.story:Packs
	@93804 @96044
	@RESET_VALUES
  Scenario Outline: Crear promocion pack de 2 skus
	Given un set de productos para crear un kit de promocion
	  | sku      | requiredQuantity | unitPrice |
	  | 69991    | 2                | 23.13     |
	  | 20236222 | 3                | 29.66     |
	When el usuario "usuario_tienda" crea un nuevo kit de promociones con productos
	Then el kit de promociones es creado exitosamente por el usuario "usuario_tienda"
	When el usuario "usuario_tienda" realiza la carga del kit de promociones
	Then el kit de promocion es cargado exitosamente por el usuario "usuario_tienda"
	When el usuario "usuario_tienda" crea un nuevo producto pack para la categoria "<category>" subcategoria "<subcategory>"
	When el usuario "usuario_tienda" realiza la carga del pack
	Then el pack es cargado exitosamente por el usuario "usuario_tienda"
	Examples:
	  | category         | subcategory       |
	  | Despensa         | Arroz y Menestras |
	  | Bebidas          | Energizantes      |
	  | Lacteos y Huevos | Leche             |

  @critical
	@allure.label.suite:Promotions
	@allure.labels.story:Packs
	@RESET_VALUES
  Scenario Outline: Crear promocion pack de 1 sku
	Given un set de productos para crear un kit de promocion
	  | sku   | requiredQuantity | unitPrice |
	  | 69991 | 2                | 15.37     |
	When el usuario "usuario_tienda" crea un nuevo kit de promociones con productos
	Then el kit de promociones es creado exitosamente por el usuario "usuario_tienda"
	When el usuario "usuario_tienda" realiza la carga del kit de promociones
	Then el kit de promocion es cargado exitosamente por el usuario "usuario_tienda"
	When el usuario "usuario_tienda" crea un nuevo producto pack para la categoria "<category>" subcategoria "<subcategory>"
	When el usuario "usuario_tienda" realiza la carga del pack
	Then el pack es cargado exitosamente por el usuario "usuario_tienda"
	Examples:
	  | category            | subcategory              |
	  | Carnes y Aves       | Aves                     |
	  | Pescados y Mariscos | Congelados y Empanizados |
	  | Cervezas            | Packs de Cervezas        |

  @critical
  @allure.label.suite:Promotions
  @allure.labels.story:Packs
  @103622
  @RESET_VALUES
  Scenario: Editar Pack
	Given el usuario "usuario_tienda" selecciona una promocion pack vigente
	When el usuario "usuario_tienda" edita la promocion pack
	Then la promocion pack es editado exitosamente por el usuario "usuario_tienda"