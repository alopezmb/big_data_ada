# Práctica Big Data: Docker + Docker-Compose + Spark-Submit (v1.0; 7puntos)

El escenario ha sido configurado y desplegado bajo las siguientes condiciones y versiones:

- Ubuntu 18.04 y 20.04
- Versión Docker utilizada: 19.03.13
- Versión docker-compose utilizada: 1.25.5

Con esta configuración se ha comprobado su correcto funcionamiento.

## Configuración Inicial

Antes de poder arrancar los contenedores que componen el escenario, es necesario prepararlo. Para ello, necesitamos entrenar un modelo de datos para realizar las predicciones y también requerimos generar un JAR del proyecto spark-scala para poder pasarle dicho archivo a spark-submit.

**NOTA: Este apartado SOLO se realizará la primera vez que se quiere desplegar el escenario. En las sucesivas ocasiones no será necesario hacerlo pues el modelo de datos y el .jar ya estarán generados y situados en los adecuados directorios para que funcione el escenario.** 

Nos situamos en el directorio raíz del proyecto e introducimos los siguientes comandos en un terminal para realizar la configuración inicial:

```bash
cd initial_configs
sudo docker-compose up
```

Se arrancan 2 contenedores. Uno corresponde al que entrenará el modelo mediante PySpark (contenedor pyspark). El otro (jarbuilder) genera un JAR del proyecto que se le indica. 

Al contenedor jarbuilder se le pasa una variable de entorno llamada  `PROJECT_NAME`. Aquí se ha de indicar el nombre del directorio raíz del proyecto spark-scala. En nuestro caso le indicamos que se llama `flight_prediction`. El  directorio raíz del proyecto, en este caso, `flight_prediction`, debe ser colocado dentro del directorio `scala_projects`, situado en `initial_configs/jar_builder/scala_projects`.  En este repositorio ya viene incluido el proyecto en dicha ruta; no obstante se indican estos detalles por si se desea editar el proyecto o añadir otro.

Una vez los contenedores terminen de hacer sus tareas, se necesita copiar los archivos generados (modelo entrenado + jar) a sus respectivos directorios del escenario. Para ello se ha de ejecutar el script `scenario_initial_config.sh` :

```bash
sh scenario_initial_config.sh
```

En este script además se pedirá al usuario que introduzca el nombre del paquete JAR que se ha generado. Esto se realiza para poder tener fácilmente distintas versiones del JAR (porque por ejemplo hemos modificado la main class de Scala) y así tener distintos nombres.

Una vez ejecutado el script, la configuración inicial ha terminado.

## Arranque del Escenario

Desde el directorio raíz del repositorio abrimos un terminal e introducimos  los siguientes comandos:

```bash
cd scenario
sudo docker-compose up
```

Con esto, se levanta gran parte de la aplicación. Concretamente
- servidor web (flask)
- _cluster_ (spark)
- _pipeline_ de datos (kafka + zookeeper)
- almacenamiento (mongodb)

Queda pendiente lanzar la aplicación con spark-submit. Antes de hacerlo, se debe actualizar el _argumento_ `JAR_NAME` definido en `docker-compose-spark-submit` con el nombre del  fichero `.jar` generado en la configuración inicial.
Una vez hecho esto ya podemos añadir a la aplicación final el contenedor restante con el siguiente comando

```bash
sudo docker-compose -f docker-compose-spark-submit.yaml up
```

Hemos separado el escenario en dos ficheros yaml docker-compose porque `spark-submit` genera una enorme cantidad de mensajes. Por tanto, si se incluye este contenedor en la especificación con los otros, una vez se arranquen no podremos ver los logs por el terminal ya que unicamente veremos los mensajes de spark-submit. Con esta separación podremos ver adecuadamente los mensajes de log de todos los contenedores.

**TODO: cambiar nivel de logging de spark-submit para poder aunar los contenedores en un único yaml.** 

Una vez se arranquen todos los contenedores, podremos acceder al servicio web de predicción de retraso de vuelos mediante la siguiente URL:  http://localhost:1212/flights/delays/predict_kafka

Se accede por el puerto **1212** al servicio web porque se ha indicado así en el puerto expuesto al host para el *webserver* en el fichero docker-compose.yaml. Se puede cambiar el puerto y utilizar cualquier otro, siempre y cuando no esté siendo utilizado por otro servicio o aplicación.

# Despliegue en GCP

Hemos seguido los pasos descritos en [este tutorial](https://cloud.google.com/community/tutorials/docker-compose-on-container-optimized-os). A continuación, exponemos cuáes han sido para nuestro proyecto.

## Configuración de la VM en GCP

1. Crear una instancia de VM de Compute Engine.
2. Seleccionar la zona deseada (dónde está el centro de datos del que vamos a usar recursos). Elegimos la opción de Bélgica por cercanía.
3. Seleccionamos tipo de máquina: C2-Standar-4 (suficiente RAM y CPU como para que no pete el entrenamiento del modelo. Esto se podría elegir mejor).
4. Cambiamos el "Boot disk" a "Container-Optimized OS stable".
5. Permitimos el tráfico HTTP (marcar checkbox)
6. Botón crear. Tarda algunos minutillos, pero cuando termine tendremos nuestra instancia en la lista de instancias de Computer Engine, con una IP interna, IP externa y opción a conectarnos a la instancia por SSH. 

## Configuración para iniciar nuestro sistema

1. Click en el botón SSH para abrir un terminal en nuestra instancia.
2. Clonamos nuestro proyecto:
    ```
    git clone https://github.com/alopezmb/big_data_ada.git 
    cd big_data_ada
    ```
    Nota: En estos pasos, hemos desplegado al versión con MongoDB. Podemos desplegar la versión con Cassandra clonando el repo con la rama adecuada.
    
3. No podemos instalar docker-compose en la instancia, por lo que nos descargaremos una imagen para usarlo:
  3.1 Descargar y correr la imagen de Docker Compose y mostrar la versión de la misma.
  ```
  docker run docker/compose version 
  ```
  3.2 Asegúrate de que estás en un directorio con permisos de escritura, como tu ```/home```.
  ```
  $ pwd
  /home/username/big_data_ada
  ```
4. El comando a ejecutar equivalente a docker-compose up es:
  ```
  docker run --rm -it\
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "$PWD:$PWD" \
    -w="$PWD" \
    docker/compose up
  ```
  So that the Docker Compose container has access to the Docker daemon, mount the Docker socket with the -v /var/run/docker.sock:/var/run/docker.sock option.
  To make the current directory available to the container, use the -v "$PWD:$PWD" option to mount it as a volume and the -w="$PWD" to change the working directory.
  -it para poder interacturar con el contenedor desde el terminal.
  
  5. Como este comando es demasiado alrgo como para hacerlo constantemente, creamos un alias:
  ```
  echo alias docker-compose="'"'docker run --rm -it \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "$PWD:$PWD" \
    -w="$PWD" \
    docker/compose'"'" >> ~/.bashrc
   ```
   Recargamos la configuración de bash:
   ```
   source ~/.bashrc
   ```
   6. Ya podemos hacer docker-compose up :)
   
 ## Iniciando el sistema
 
 Seguiremos las instrucciones expuestas más arriba, ya que deberemos entrenar el modelo de nuevo ya que no se encuentra entrenado en el repo.
 (Para más detalle, ver arriba)
 
 1.- Desde la carpeta initial-configs ejecutamos el comando ```docker-compose up```. Esto entrenará el modelo y hará las funciones descritas más arriba. Tarda bastante rato.
 2. Ejecutamos el script correspondiente para preparar la ejecución del escenario
 ``` 
 sh scenario_initial_config.sh
 ```
 3. Cambiamos a la carpeta /scenario y ejecutamos de nuevo ```docker-compose up```
 4. Desde otro terminal, ejecutamos el comando ```docker-compose -f docker-compose-spark-submit.yaml up```. Nota: Recuerda actualizar el nombre de la variable
 5. El sistema ya debería estar accesible y funcional en ```<dir IP externa asignada a tu instancia>/:1212/flights/delays/predict_kafka```
