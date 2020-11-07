En esta pequeña nota queremos explicar brevemente como es el proceso de extracción de datos.    

Procedemos a ejecutar el scraper descomentado solo el primer grupo de líneas del código principal.  

En primer lugar se extraen todos los enlaces a las descripciones de producto de una búsqueda con la keyword "smartphone" en 4m4z0n:  

<img align="center" width="1200" height="500" src="/imagenes wiki/am4z0n_2.png">


Una vez descargados los enlaces, de manera manual eliminamos aquellos enlaces que no correspondan con teléfonos.  
Para ello usamos expresiones regulares
(leer el archivo duda_importante.md, ahí viene explicado por que se da esta situación)  

<img align="center"  width="1200" height="500" src="/imagenes wiki/limpiado_enlaces.png">


Ahora procedemos a ejecutar el script descomentando solo el segundo grupo e líneas del código principal.  
Comenzará la descarga de toda la información de los teléfonos.

Una vez acabada, eliminamos datos no deseados mediante expresiones regulares.  
(leer el archivo duda_importante.md, ahí viene explicado por que se da esta situación)  


<img align="center"  width="1200" height="500" src="/imagenes wiki/limpiado_datos_incompletos.png">

<img align="center" width="1200" height="500" src="/imagenes wiki/limpiado_datos_incompletos2.png">

Ya tenemos el dataset completo, para una mayor calidad de los datos habría que hacer un preprocesado más a fondo, pero eso queda fuera del alcance.
