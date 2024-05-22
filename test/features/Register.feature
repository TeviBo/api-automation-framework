@REGISTER @REGRESSION
Feature: Register
"""
    As a user
     I want to be able to register in the application to be able to make purchases
    """"

  @critical
  @allure.label.suite:Register
  @allure.labels.story:RegisterNewUser
  @84142 @NEW_USER
  Scenario: Registro exitoso
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

  @normal
  @allure.label.suite:Register
  @allure.labels.story:Exceptions
  @84143 @REGISTER_EXCEPTIONS
  Scenario: Registro - Excepciones
	Given un nuevo usuario "usuario_app"
	And el usuario "usuario_app" registra un telefono que no tiene 9 caracteres de extension
	Then el sistema devuelve un mensaje indicando que el telefono debe tener 9 caracteres de extension
	When el usuario "usuario_app" registra un telefono que no comienza con 9
	Then el sistema devuelve un mensaje indicando que el telefono debe comenzar con 9
	When el usuario "usuario_app" registra un telefono valido
	Then el telefono del usuario "usuario_app" es registrado exitosamente
	And se genera un codigo otp para el usuario "usuario_app" que recibira por mensaje para la activacion de su cuenta
	When el usuario "usuario_app" ingresa un codigo invalido
	Then el sistema devuelve un mensaje indicando que el codigo es invalido
	When el usuario "usuario_app" ingresa el codigo otp recibido
	Then el codigo otp del usuario "usuario_app" es validado
	When el usuario "usuario_app" ingresa una contraseña de 6 digitos para su cuenta
	Then la contraseña para el usuario "usuario_app" es registrada exitosamente
	When el usuario "usuario_app" ingresa un numero de documento invalido
	Then el sistema devuelve un mensaje de error para el usuario "usuario_app" indicando que el documento es invalido

  @normal
  @allure.label.suite:Register
  @allure.labels.story:Exceptions
  @REGISTER_EXCEPTIONS @94187
  Scenario: Registro Excepciones - Validacion otp vencido
	Given un nuevo usuario "usuario_app"
	When el usuario "usuario_app" registra un telefono valido
	Then el telefono del usuario "usuario_app" es registrado exitosamente
	And se genera un codigo otp para el usuario "usuario_app" que recibira por mensaje para la activacion de su cuenta
	When el usuario "usuario_app" ingresa el codigo otp vencido
	Then el sistema devuelve un mensaje de error indicando que el otp se ha vencido

  @normal
  @allure.label.suite:Register
  @allure.labels.story:Exceptions
  @REGISTER_EXCEPTIONS @95855
  Scenario: Registro Excepciones - Numero de telefono ya registrado
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
	When el usuario "usuario_app" registra un telefono que ya posee cuenta
	Then el telefono del usuario "usuario_app" es registrado exitosamente
	And se genera un codigo otp para el usuario "usuario_app" que recibira por mensaje para la activacion de su cuenta
	When el usuario "usuario_app" ingresa el codigo otp recibido
	Then el sistema devuelve un mensaje de error para el usuario "usuario_app" indicando que el telefono esta registrado