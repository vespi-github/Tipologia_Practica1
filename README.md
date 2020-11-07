# Smartphones Scraper
Este scraper extrae información de todos los smartphones en venta en 4m4z0n.es actualmente.  Ha sido realizado por Diego Martín Montoro y Javier Hernández Hernández.

Para la ejecución del scraper es necesario instalar los siguientes paquetes:  

* BeautifulSoup
* threading
* multiprocessing
* os
* csv
* time
* copy
* random

Para ello se puede usar el comando pip:  
```
  pip install package_name
```


Para ejecutar el script deberemos ejecutar la siguiente instrucción:
```
  python scraper.py
```
__NOTA IMPORTANTE__: es necesaria la presencia en la misma carpeta de los siguientes archivos/carpetas:

1. proxies_list.csv : contiene una lista de servidores proxy.
2. Carpeta temp : en ella se crear archivos temporales necesarios para la correcta paralelización del script.
3. Carpeta Pictures: es donde se almacenarán las imágenes de los teléfonos.

La ejecución se divide en dos procesos: uno que genera un archivo llamado moviles_links.csv que contiene el resultado de un primer raspado de datos de 4m4z0n ; y otro que generará el conjunto de datos final, llamado moviles_datos.csv, que será extraído usando los enlaces del fichero moviles_links.csv.

Los datos contenidos en el fichero final corresponden a las siguientes características de cada teléfono:
* Marca: marca del teléfono, suele coincidir con el fabricante.
* Fabricante: empresa fabricadora del teléfono.
* Modelo: nombre del modelo del teléfono, suele contener la gama y el número dentro de la misma. Ej: Xiaomi MI 3
* Sistema operativo: Indica el nombre del sistema operativo instalado de fábrica en el teléfono.
* Capacidad de la memoria: cantidad de memoria secundaria que tiene el teléfono.
* Memoria extraíble: indica el nombre de la tecnología de memoria extraíble que tiene el teléfono, en el caso que goce de ella.
* Resolución del sensor óptico: indica los megapíxeles de la cámara trasera del teléfono.
* Valoración: valoración media de los clientes sobre 5.
* Valoraciones: número total de valoraciones de cliente que ha recibido el teléfono.
* Precio: precio actual del teléfono.
* Imagen: ruta de la imagen del teléfono en la carpeta pictures.

__El DOI: 10.5281/zenodo.4135053__

La carpeta SRC contiene todos los ficheros necesarios para la ejecución:   
    scraper.py: contiene el código del scraper  
    proxies_list.csv: contiene la lista de servidores proxy.  
    Las carpetas temp y Pictures necesarias para la ejecución del script.  

El archivo proceso.md contiene información sobre como realizar correctamente la extracción de datos usando el script.
