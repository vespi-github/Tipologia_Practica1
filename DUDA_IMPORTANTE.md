
Escribimos este pequeño fichero para preguntarle sobre una cuestión que nos inquieta.

Al usar los 13300 links de cada una de las descripciones de los teléfonos para bajar el dataset final, resulta que hemos obtenido muchísimos datos menos (entorno a 4000).
Por lo que hemos estado observando, creemos que se debe a que:

* Hay una gran mayoría de artículos de telefonía camuflados como teléfonos móviles que salen al realizar la búsqueda en amazon y esto no 
podemos evitarlo ya que el vendedor lo hace a propósito. Dichos productos carecen de la descripción técnica típica de un teléfono, lo que resulta en obtención de tuplas casi vacías.
En realidad creemos que esto no es un problema ya que estas tuplas simplemente corresponden a objetos que están fuera de nuestro interés, y solo ocasionará tener que limpiar más
el dataset.
* De los productos que sí son teléfonos pueden ocurrir varias cosas:  
  * Descripción por defecto de amazon: no hay problemas la extracción se realiza correctamente.
  * Descripción por defecto pero no introdujo datos, o los introdujo erróneamente: estamos con las manos atadas.
  * La descripción consiste en una imagen que se corresponde con un folleto informativo: no podemos hacer nada ahí.
  * Descripción personalizada: el vendedor ha embebido el código html sin ningún tipo de estándar, datos totalmente desestructurados,
  en distintos idiomas y muchas veces con errores. Muy difícil proceder si no imposible.
  
Esta serie de situaciones creemos que han llevado a la reducción considerable de la cantidad de información que en una primera instancia creíamos que íbamos a poder sacar.
Hemos llegado a esta conclusión estudiando la lista de teléfonos ofertada por amazon manualmente. De las 400 páginas que aparecen (30 teléfonos por página) , en las últimas 150 páginas
todos son productos sin apenas información, algunos sin precio y otros que nunca llegaron a estar en venta realmente y carecen de foto, suponemos que los vendedores los pusieron con
el objetivo de ganar algún tipo de ventaja en la indexación de amazon. De las 250 restantes, hay gran cantidad de anuncios que sufren alguna de las situaciones comentadas con anterioridad.  

Me temo que esto es típico del web Scrapping y hay que acostumbrarse a ello.
  

