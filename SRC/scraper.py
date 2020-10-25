import requests
from bs4 import BeautifulSoup
import threading
import multiprocessing
import os
import csv
import time
import copy
import random
from random import randint


# declaración de una pequeña lista de user agents para poder rotarlos con el objetivo de pasar desapercibidos ante amazon.
user_agents = [
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
	"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
	"Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
	"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.110 Safari/537.36",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.43",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.43",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 OPR/71.0.3770.271",
	"Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 OPR/71.0.3770.271",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.110 Safari/537.36 OPR/71.0.3770.271",
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 OPR/71.0.3770.271",
	"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; Trident/4.0;)",
	"Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
	"Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko",
	"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 YaBrowser/20.9.0 Yowser/2.5 Safari/537.36"
]

# declaración de la lista de proxies
# el objetivo es poder rotar ips para pasar desapercibidos y poder incrementar la velocidad del scrapper.
proxies = []
enlaces = []


# carga los proxies del fichero proxies_list.csv al vector proxies
def cargar_proxies():
	global proxies
	with open('proxies_list.csv', 'r') as f:
		for proxy in csv.reader(f):
			proxies.append(proxy[0]) 

# carga los enlaces de los móviles ya obtenidos (fichero moviles_links.csv) al vector enlaces
def cargar_enlaces():
	global enlaces
	with open('moviles_links.csv', 'r') as f:
		for enlace in csv.reader(f):
			enlaces.append(enlace[0])



def obtener_links_hebra(id):
	global proxies,user_agents

	#con las variables pag y pag_ini controlaremos la cantidad de páginas del búscador de amazon que esta hebra procesará
	pag = 1
	pag_ini = id*30

	#preparamos el archivo temporal para almacenar los links scrapeados.
	#Lo creamos y cerramos el flujo, no debería ser necesario pero me estaba dando problemas y no quería perder tiempo con esto.
	f = open( "temp/"+str(id)+"moviles_links.txt", "w+")
	f.close()

	# generamos una secuencia distinta de servidores proxy para la hebra shuffleando la lista inicial.

	shuffled_proxies = copy.deepcopy(proxies)
	random.shuffle(shuffled_proxies)

	# Lo ideal es repartir los servidores proxies entre las hebras pero al ser públicos son altamente inestables, mayoritariamente bloqueados y no tenemos acceso a muchos de manera que
	# la probabilidad de acabar con una hebra sufriendo inanición de proxies es muy alta. 
	# Esta es una solución relativamente sencilla para que las hebras "no suelan" hacer peticiones con el mismo proxy a la vez, y se basa en tener una lista lo más grande posible de proxys.


	# Teniendo proxies privados, la solución sería asignar la misma cantidad de proxies a cada hebra de manera disjunta y en el caso de que los proxies de una hebra fueran baneados todos, el resto de hebras cederían
	# proxies para que esa hebra pueda seguir trabajando. De esa manera se podría también aumentar muchísimo la velocidad de extracción al no perder tiempo checkeando servidores caídos o baneados.

	# Supongamos que tuviésemos 100 proxies, 20 hebras, 5 proxies por hebra, con esperas de entre 1 y 5 segundos llegaríamos a realizar unas 12 peticiones por hebra en 1 minuto, lo que serían unas 2 peticiones por 
	# IP en ese tiempo (difícil acabar bloqueados). En total en un minuto extraeríamos 240 teléfonos, 14400 teléfonos en 1h. 

	# Imaginemos que se puede hacer con un supercomputador con 300 núcleos y un paquete de 4000 IPs como he visto en alguna web.



	# generamos la cabecera para las peticiones que realice esta hebra, usará un user agent de la lista aleatoriamente escogido.
	headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
	*/*;q=0.8",
	"Accept-Encoding": "gzip, deflate, sdch, br",
	"Accept-Language": "en-US,en;q=0.8",
	"Cache-Control": "no-cache",
	"dnt": "1",
	"Pragma": "no-cache",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": user_agents[randint(0,19)]
	}

	# mientras no hayamos obtenido 20 páginas (20x30 = 600 links a teléfonos)
	while pag < 30:
		for proxy in shuffled_proxies: # vamos variando el proxy

			print("Hilo "+str(id)+" probando proxy: "+proxy)
			
			proxi_cons_request = 0 #número de peticiones exitosas seguidas a un mismo proxy
			responde = True
            
			while responde and proxi_cons_request < 2 and pag < 30:# mientras el proxy responda y le hallamos hecho menos de 2 peticiones
				try:
					time.sleep(randint(0, 10)) #espera aleatoria entre 0 y 10 segundos
					#pedimos la pagina deseada
					web = requests.get( "https://www.amazon.es/s?k=smartphone&i=electronics&page="+str(pag_ini+pag)+"&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1603579092&ref=sr_pg_3"+str(pag_ini+pag) , headers = headers, proxies = {'http':proxy,'https': proxy}, timeout=5 )
					soup = BeautifulSoup(web.content,"lxml")
					pag = pag + 1
					proxi_cons_request = proxi_cons_request + 1

					#abrimos el fichero temporal y añadimos las urls encontradas
					
					f = open( "temp/"+str(id)+"moviles_links.txt", "a")
					for a_price in soup.find_all('span', class_="a-price"): # recorremos todos los enlaces de la clase a-price encontrados y almacenamos su href.
						if 'a-text-price' not in a_price.attrs['class']:
							f.write("www.amazon.es/"+a_price.parent['href']+"\n")

					f.close()
					#feedback para el programador, permite saber si el proxy probado responde o no (para darse cuenta de la inanición y cortar el proceso)
					print("OK")
				except:
					responde = False #cualquier error de conexión se descarta y se indica que el servidor proxy no responde para pasar a probar el siguiente.

					# se podría proceder eliminando el proxy que ya está baneado de la lista de proxies, pero al ser compartida esta lista tendríamos que establecer pre y post protocolos de 
					# exclusión mutua que forzaría muchas esperas y degeneraría en gran medida la solución paralela.
	
	


# esta función integra los ficheros temporales para generar el definitivo. Sirve para los dos procesos.
def integrar_ficheros(NUM_WORKERS,fich_name):
	w = open(fich_name+".csv", "w+")
	if fich_name == "moviles_datos":
		 w.write(' "Marca","Fabricante","Modelo","Sistema operativo","Capacidad de la memoria","Memoria extraíble","Resolución del sensor óptico","Valoración","Valoraciones","Precio","Imagen"\n')

	for i in range(0,NUM_WORKERS):
		r = open("temp/"+str(i)+fich_name+".txt", "r+") 
		w.write(r.read())
		r.close()
		os.remove("temp/"+str(i)+fich_name+".txt")
	w.close()





# esta función elimina carácteres indeseados presentes en la mayoría de los datos scrapeados
def clean_feature(feature):
	return feature.replace('\n','').replace('\t','')



#función que descarga una imagen EXTRAÍDA DEL TEMARIO DE LA ASIGNATURA y modificada para cambiar el user_agent y el proxy.
def load_requests(source_url,headers,proxy):
	global user_agents

	ruta=""

	try:
		r = requests.get(source_url,headers = headers, stream = True, proxies = {'http':proxy,'https': proxy})
		if r.status_code == 200:
			aSplit = source_url.split('/')
			ruta = "Pictures/"+aSplit[len(aSplit)-1]
			with open(ruta,"wb") as output:
				for chunk in r:
					output.write(chunk)
	except:
		pass

	return ruta





def extraccion_telefonos_hebra(id):
	global proxies,user_agents,enlaces

	enlace = 1
	enlace_ini = id*444


	f = open( "temp/"+str(id)+"moviles_datos.txt", "w+")
	f.close()

	# generamos una secuencia distinta de servidores proxy para la hebra
	shuffled_proxies = copy.deepcopy(proxies)
	random.shuffle(shuffled_proxies)

	# generamos el user agent para esta hebra
	headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
	*/*;q=0.8",
	"Accept-Encoding": "gzip, deflate, sdch, br",
	"Accept-Language": "en-US,en;q=0.8",
	"Cache-Control": "no-cache",
	"dnt": "1",
	"Pragma": "no-cache",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": user_agents[randint(0,19)]
	}

	#forzamos la obtención de 800 teléfonos
	while enlace < 444:
		for proxy in shuffled_proxies:

			print("hilo "+str(id)+" probando proxy: "+proxy)

			proxi_cons_request = 0
			responde = True #flag que indica si el proxy responde

			while responde and proxi_cons_request < 1 and enlace < 444 : # en este caso solo quiero una petición cada vez (ya que la imagen realiza otra)
				
				try:

					time.sleep(randint(0, 5))

					# realizamos la petición al enlace correspondiente
					web = requests.get( "https://"+enlaces[enlace_ini+enlace], headers = headers, proxies = {'http':proxy,'https': proxy}, timeout=5 )
					print("OK")
					soup = BeautifulSoup(web.content,"lxml")
					enlace = enlace + 1
					proxi_cons_request = proxi_cons_request + 1



					# aquí el scrapping de los datos
					#########################################################################################################
					mobile_json = {}

					# la mayoría de datos están en una estructura tabular y por cada th hay un td, esto ha facilitado mucho la extracción, con este simple bucle cargamos casi todos.
					# el try/except permite ignorar errores (si no puedes agarrar un dato, intenta agarrar los demás).
					for feature in soup.find_all("th",class_="prodDetSectionEntry"):
						try:
							mobile_json[clean_feature(feature.get_text())] = clean_feature(feature.findNext('td').get_text())
						except:
							pass

					# Los datos correspondientes a la valoración, el número de valoraciones y el precio se hallan en otras secciones.
					# Son fácilemte localizables gracias a clases muy restringidas y el uso de ids.
					# Hacemos un pequeño preprocesado de ellos para eliminar datos no numéricos.

					try:
						mobile_json["Valoración"] = clean_feature(soup.find("span",class_=['reviewCountTextLinkedHistogram', 'noUnderline'])['title']).replace(",",".")
						mobile_json["Valoración"] = mobile_json["Valoración"][0:mobile_json["Valoración"].find(" ")]
					except:
						pass

					try:
						mobile_json["Valoraciones"] = clean_feature(soup.find("a",href="#customerReviews").get_text())
						mobile_json["Valoraciones"] = (mobile_json["Valoraciones"][0:mobile_json["Valoraciones"].find(" ")])
					except:
						pass

					try:
						mobile_json["Precio"] = clean_feature(soup.find("span",id="priceblock_ourprice").get_text()).replace(",",".")
						mobile_json["Precio"] = mobile_json["Precio"][0:mobile_json["Precio"].find("\xa0")]
					except:
						pass
					
					# Por último descargamos la imagen y añadimos el nombre de donde ha sido guardada al JSON.
					# Como se va a realizar otra petición, se hace una pequeña espera extra antes.
					try:
						time.sleep(randint(0, 3))
						mobile_json["Imagen"] = load_requests(soup.find("img",id="landingImage")['data-old-hires'],headers,proxy)
					except:
						pass
					

					# ahora simplemente volcamos los datos de interés del JSON en un string, separando los mismo con comas, para posteriormente escribirla en fichero.
					linea = ""
					

					for feature in ["Marca","Fabricante","Modelo","Sistema operativo","Capacidad de la memoria","Memoria extraíble","Resolución del sensor óptico","Valoración","Valoraciones","Precio","Imagen"]:
						if feature not in mobile_json:
							linea+= '" ",'
						else:
							linea+= '"'+mobile_json[feature]+'",'

					# debido a cuestiones de formato y codificación primero eliminamos algunos tipos de carácteres especiales y luego recortamos para ignorar la última coma añadida en el bucle.
					linea = str(linea.encode("utf-8"))
					linea = linea[2:len(linea)-2]

					f = open( "temp/"+str(id)+"moviles_datos.txt", "a")
					f.write(linea+'\n')
					f.close()

					#########################################################################################################


				except Exception as e:
					responde = False

					# se podría proceder eliminando el proxy que ya está baneado de la lista de proxies, pero al ser compartida esta lista tendríamos que establecer pre y post protocolos de 
					# exclusión mutua que forzaría muchas esperas y degeneraría en gran medida la solución paralela.
					
	f.close()				
   
# esta función lanza 12 hebras que ejecutarán la función "obtener_links_hebra" en paralelo.
# la función obtener_links_hebra se encarga de extraer una cantidad de enlaces de teléfonos de amazon a partir de la lista de búsqueda.
def obtener_links_paralelo():
	NUM_WORKERS = 12
	threads = [threading.Thread(target=obtener_links_hebra,args=(i,)) for i in range(0,NUM_WORKERS)]
	[thread.start() for thread in threads]
	[thread.join() for thread in threads]
	integrar_ficheros(NUM_WORKERS,"moviles_links")				


# esta función lanza 12 hebras que ejecutarán la función "extraccion_telefonos_hebra" en paralelo.
# la función extraccion_telefonos_hebra se encarga de extraer la información relativa a un teléfono de su página de descripción en amazon.
def obtener_información_telefonos_paralelo():
	NUM_WORKERS = 12
	threads = [threading.Thread(target=extraccion_telefonos_hebra,args=(i,)) for i in range(0,NUM_WORKERS)]
	[thread.start() for thread in threads]
	[thread.join() for thread in threads]
	integrar_ficheros(NUM_WORKERS,"moviles_datos")



#######################################################################################
####################################   MAIN CODE   ####################################
#######################################################################################

cargar_proxies()

# EJECUTAR PRIMERO ESTA SECCIÓN
"""
# obtenemos los links de las descripciones de cada teléfono
start_time = time.time()
obtener_links_paralelo()
end_time = time.time()

print("Tiempo total en horas =", (end_time - start_time)/3600 )
"""

# EJECUTAR ESTA SECCIÓN DESPUÉS

"""
# usamos los enlaces obtenidos en el proceso anterior para extraer la información de los móviles
cargar_enlaces()
start_time = time.time()
obtener_información_telefonos_paralelo()
end_time = time.time()
print("Tiempo total en horas =", (end_time - start_time)/3600  )
"""





















