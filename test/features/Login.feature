@LOGIN @REGRESSION
Feature: Login
"""
As a user
	I want to login to the application
	So that I can access the application's features
"""

  @critical
  @allure.label.suite:Login
  @allure.labels.story:Login
  @84145
  Scenario: Login Exitoso
	Given el usuario "usuario_app" con identificador "958596485" y contraseña "122222"
	And con direccion en rango del hub "LIM013"
	When el usuario "usuario_app" inicia sesion con sus credenciales
	Then el usuario "usuario_app" accede a la aplicacion
	And se valida si el usuario "usuario_app" acepto los terminos y condiciones
	And se verifica si el usuario "usuario_app" completo el registro
	And se obtiene el perfil del usuario "usuario_app"
	And se obtienen las direcciones del usuario "usuario_app"
	And se obtiene la informacion del hub "LIM013" para el usuario "usuario_app"
	And se obtienen los segmentos del usuario "usuario_app"
	And se obtiene el carrito de compras del usuario "usuario_app"
	And se obtienen las campañas del home para el usuario "usuario_app" en el hub "LIM013"
	And se obtienen las categorias de la tienda para el usuario "usuario_app"
	Then el usuario "usuario_app" accede al home de la aplicacion


  @normal
  @allure.label.suite:Login
  @allure.labels.story:Exceptions
  @84161 @LOGIN_EXCEPTIONS
  Scenario: Login fallido por contraseña incorrecta
	Given el usuario "usuario_app" con identificador "958596485" y contraseña "144444"
	When el usuario "usuario_app" inicia sesion con sus credenciales
	Then el sistema retorna un mensaje de error indicando que los datos son incorrectos

  @normal
  @allure.label.suite:Login
  @allure.labels.story:Exceptions
  @84161 @LOGIN_EXCEPTIONS
  Scenario: Login fallido por identificador incorrecto
	Given el usuario "usuario_app" con identificador "random_phone" y contraseña "122222"
	When el usuario "usuario_app" inicia sesion con sus credenciales
	Then el sistema retorna un mensaje de error indicando que los datos son incorrectos

  @critical
  @allure.label.suite:Login
  @allure.labels.story:Exceptions
  @103734 @LOGIN_EXCEPTIONS
  Scenario: Bloqueo de cuenta por maximo de intentos con credenciales invalidas
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
	When el usuario "usuario_app" inicia sesion con sus credenciales 3 veces y contraseña incorrecta
	Then el sistema bloquea la cuenta del usuario "usuario_app" por 24 horas

