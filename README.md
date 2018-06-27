# supreme-funicular

Aplicación de Internet de las cosas: **Invernadero**

**Joaquín Fernández y Mercedes Alonso**

## Interfaces con los sensores y actuadores
Programas en python que publican los datos de los sensores y controlan los actuadores.

#### dhtPub, ldrPub
Publican los datos de temperatura, humedad (dht11) y luminosidad (ldr), junto con un histórico de los últimos N datos. Cada uno es publicado en un tópico utilizando mosquitto. Los tópicos son */etsidi/tmp* y *etsidi/tmpH* para la termperatura, */etsidi/hum* y *etsidi/humH* para la humedad y */etsidi/ldr* y *etsidi/tldrH* para la luminosidad.

#### ldrSub, tmpSub, humSub
Estos programas están suscritos a los datos publicados por los sensores y por la interfaz con el usuario. Cada uno se suscribe a su respectivo topic de dato y al topic de */etsidi/params*, que publica la información sobre los márgenes aceptables de cada magnitud.

#### watersub, lightsub, coversub, fansub
Permite accionar los actuadores directamente desde la interfaz. Están suscritos a los tópicos de */etsidi/water*, */etsidi/light*, */etsidi/cover* y */etsidi/fan* respectivamente. Cuando por el tópico se publica un **on** se activa el actuador, y cuando se recibe un **off** se apaga.

## Interfaz con el usuario
La interfaz está suscrita a los topics de históricos de todos los sensores (acabados en "H"). Utiliza los datos para representar gráficas de los datos en tiempo real de los sensores. Es capaz de publicar órdenes directas a los sensores a través de sus topics correspondientes. Además, se pueden cambiar los parámetros de funcionamiento para mantener las variables del sistema entre valores determinados.

La interfaz está creada en python con ayuda de las librerías *tkinter* y *matplotlib*.


## Script de lanzamiento startApp.sh
Ejecuta un módulo o todos juntos. Lanza cada programa en una terminal individual. Para lanzarlo: `./startApp.sh <module>`
donde módulo es ldr, tmp, hum o all (para toda la aplicación).

## carriots
El programa carriots.py envía a la página web de carriots un mensaje cuando se considera que la luz pasa de *on* a *off*. En la herramienta, hay un *listener*, que envía un correo cuando se recibe este dato.
