# Práctica Big Data: Docker + Docker-Compose + Spark-Submit + Cassandra (v2.0; 9puntos)

El escenario ha sido configurado y desplegado bajo las siguientes condiciones y versiones:

- Ubuntu 18.04 y 20.04
- Versión Docker utilizada: 19.03.13
- Versión docker-compose utilizada: 1.25.5

Con esta configuración se ha comprobado su correcto funcionamiento.



## Consideraciones con Cassandra

Los pasos a seguir son prácticamente los mismos que antes. Por tanto se recomienda seguir los pasos ya conocidos. Hay que tener en cuenta que:

- La **configuración inicial se hace de la misma manera.** La clase de Scala ha cambiado para adaptarla a Cassandra pero al final lo que queremos en este primer paso es generar el JAR, que se hace como ya se conoce.
- La **primera vez** que se vaya a arrancar el escenario (Arranque del Escenario), primero debemos configurar el keyspace y familias de columnas a utilizar en Cassandra (no se pueden crear dinámicamente y si se levanta el escenario entero la primera vez, dará error).  Luego ya se pueden levantar el resto. En sucesivas ocasiones, se podrán arrancar todos los contenedores a la vez sin ningún problema. 

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

1. **SI ES LA PRIMERA VEZ QUE SE ARRANCA EL ESCENARIO, SEGUIR ESTOS PASOS:**

```bash
cd scenario
sudo docker-compose up cassandra-1 cassandra-2
```

La primera vez sólo se levantará en primer lugar el cluster de cassandra porque es necesario configurar el modelo de datos a utilizar.

A través de un nuevo terminal, acceder al bash del contenedor cassandra-1 y configurar los keyspaces, familias de columnas y demás  configuraciones iniciales de cassandra:

```bash
sudo docker-compose exec cassandra-1 bash #Acceso al bash de cassandra-1
$cassandra-1> cqlsh -f /config_db/flights.cql #Comando cqlsh dentro del bash de cassandra-1
$cassandra-1> exit #Salimos del bash de cassandra-1
sudo docker-compose down #Paramos el cluster de cassandra
```

Ahora, una vez configurado Cassandra, ya procedemos al paso 2:

2. **ARRANQUE EN SUCESIVAS OCACIONES (IR AL PASO 1 SI ES LA PRIMERA VEZ QUE SE VA A ARRANCAR EL ESCENARIO):**

Será tan simple como abrir un nuevo terminal en el directorio raíz e introducir los siguientes comandos

```bash
cd scenario # Si ya estamos en el directorio scenario, omitir.
sudo docker-compose up #Levantamos todo el escenario
```

Con esto, se  levantan todos los contenedores. Concretamente:

- servidor web (flask)
- cluster de procesamiento (spark) + spark-submit **Ya se ha integrado en el mismo docker-compose y se ha modificado el nivel de Logging para evitar esos mensajes tan molestos.**
- _pipeline_ de datos (kafka + zookeeper)
- almacenamiento (cassandra)

Una vez se arranquen todos los contenedores, podremos acceder al servicio web de predicción de retraso de vuelos mediante la siguiente URL:  http://localhost:1212/flights/delays/predict_kafka

Se accede por el puerto **1212** al servicio web porque se ha indicado así en el puerto expuesto al host para el *webserver* en el fichero docker-compose.yaml. Se puede cambiar el puerto y utilizar cualquier otro, siempre y cuando no esté siendo utilizado por otro servicio o aplicación.
