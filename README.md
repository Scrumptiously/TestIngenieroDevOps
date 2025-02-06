# Test Ingeniero DevOps - Gabriel Flores

A continuación se explicará el sistema desarrollado para la prueba de implementación de pipeline CI/CD con despliegue a servicio Cloud (AWS).

## Aplicación
La aplicación utilizada para la demostración se desarrolló bajo el framework web Django, y solo cuenta con una vista, en la cúal se consume el endpoint especificado en las instrucciones y luego, a través de una respuesta HTTP, muestra los datos recuperados. También cuenta con una prueba unitaria que verifica la integración de la API con la aplicación.

## Contenedores
En la carpeta raíz se encuentra un archivo Docker-Compose, el cúal tiene configurada la creación de los servicios, basandose en la imagen especificada en el Dockerfile de la carpeta main, y la creación de los volumenes necesarios para el funcionamiento de la app.

## Github Flow
Siguiendo Github Flow, para realizar cambios se debe crear una nueva rama "feature", basada en la rama main, donde el desarrollador realiza cambios. El servidor jenkins está a la escucha de un webhook, por lo que al realizar cambios en el repositorio se ejecutará automaticamente la pipeline, pero como no queremos desplegar a producción al hacer push a la rama "feature", las etapas de la pipeline se encuentran condicionadas, por lo que cuando se hace push a la rama "feature" solo se ejecutaran las etapas relacionadas a pruebas unitarias, de integración y de seguridad, y la etapa de despliegue se ejecutará solo al hacer merge con la rama main.

## Pipeline CI/CD
Para la pipeline CI/CD se escribió en un archivo Jenkinsfile. Para efectos de esta prueba, consideraremos que la maquina de pruebas es la misma maquina en la que se encuentra instalado Jenkins, mientras que la maquina de producción será una maquina EC2 de AWS. A continuación se explica brevemente las etapas:
* Etapa 0 (Checkout): Al detectar un commit, Jenkins ejecuta la pipeline, y por defecto, clona el repositorio en el WorkSpace, por lo que no es necesario incluir esto en el Jenkinsfile.
* Etapa 1 (Preparar ambiente): Se prepara el ambiente para la ejecución de pruebas, para lo cual es necesario descargar la versión mas reciente de Dastardly, se copia en el WorkSpace el archivo de ambiente que se encuentra almacenado en boveda, y se ejecuta el archivo Docker-Compose para montar la imagen y correr el contenedor con la app en el puerto 8000.
* Etapa 2 (Análisis SAST): Utilizando una instalación de SonarQube previamente configurada en el servidor Jenkins, se ejecuta el análisis SAST para realizar pruebas de código estático.
* Etapa 3 (Análisis SCA): Utilizando una instalación de OWASP Dependency Check previamente configurada en el servidor Jenkins, se ejecuta el análisis SCA para comprobar que las dependencias no cuenten con vulnerabilidades.
* Etapa 4 (Pruebas unitarias): Se ejecutan las pruebas unitarias programadas en la app Django, la cúal como se mencionó anteriormente, solo es una.
* Etapa 5 (Análisis DAST): Con la imagen Dastardly de docker descargada en la primera etapa, se ejecutan pruebas dinamicas en el puerto 8000, que es donde el contenedor está recibiendo peticiones.
* Etapa 6 (Despliegue) (Solo al realizar cambios en branch main): Una vez que la aplicación pasó todas las pruebas, se establece una conexión SSH con la maquina EC2 de AWS y se realizan todos los pasos necesarios para desplegar la aplicación.
* Acciones post-ejecución
  * Limpieza del Workspace: Luego de finalizar la pipeline, se limpia el WorkSpace para no dejar archivos residuales que puedan interferir en futuras ejecuciones
  * Notificación vía e-mail: Gracias a una configuración previa de un servidor SMTP, la pipeline puede enviar correos electrónicos indicando si la pipeline se ejecutó correctamente, o si se detuvo debido a errores. 
