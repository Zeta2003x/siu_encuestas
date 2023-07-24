from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time
import chromedriver_autoinstaller
from easygui import multenterbox
from easygui import enterbox
from easygui import msgbox


def obtenerUserYPass():
	msg = "Ingresa tu usuario y contraseña del SIU"
	title = "Ingreso SIU Guarani"
	fieldNames = ["Usuario", "Contraseña"]
	fieldValues = multenterbox(msg, title, fieldNames)
	while True:
		errmsg = ""
		for i, name in enumerate(fieldNames):
			if fieldValues[i].strip() == "":
				errmsg += "{} es un campo necesario.\n\n".format(name)
		if errmsg == "":
			break # sin problemas
		fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
		if fieldValues is None:
			break
	return fieldValues

def login():
	# Ingresar al siu
	driver.get("https://guarani.frba.utn.edu.ar/autogestion/grado/")
	driver.maximize_window()
	driver.implicitly_wait(5)

	driver.find_element(By.ID, 'usuario').send_keys(UTN_USER)
	driver.find_element(By.ID, 'password').send_keys(UTN_PASS)
	driver.find_element(By.XPATH, '/html/body/div[6]/div/div[1]/div').find_element(By.ID, 'login').click()

def obtener_encuestas():
	# Obtengo cantidad de encuestas
	encuestas = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div[1]/div/div[2]/div').find_elements_by_tag_name('a')
	for encuesta in encuestas: # Recorro todas las encuestas
		lista_encuestas.append(encuesta.get_attribute('href')) # Link a la encuesta
		puntaje = enterbox(msg='Ingresa el puntaje (del 1 al 10) que quieres asignarle al profesor/a de esta materia: %s' % encuesta.text, title='Ingresar puntaje')
		try:puntaje = int(puntaje)
		except:
			puntaje = enterbox(msg='Ingresa solo valores enteros del 1 al 10 por favor.', title='Ingresar puntaje')
			puntaje = int(puntaje)
		puntaje = (puntaje - 10) * (-1) # Calculo para transformar puntaje en elemento correspondiente del DOM
		if (puntaje > 0) and (puntaje <= 10):lista_puntajes.append(puntaje+1)
		else: lista_puntajes.append(11) # Elemento del DOM que significa "No opina"

def completar_encuesta(enc):
	# Ingresar a la encuesta
	driver.get(enc)
	driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
	
	# Contesta todas las encuestas
	for i in range(1,24):
		valor = driver.find_element(By.XPATH, f'/html/body/div/div/div/form/div[1]/div/div/div[2]/div[2]/div[{i}]/div/div/div/div[{lista_puntajes[enc]}]/label/input')
		valor.click()
		time.sleep(0.5)
		valor.click()
		time.sleep(0.5)

	boton = driver.find_element(By.ID, "btn-terminar")
	boton.click()
	boton.click()
	Alert(driver).accept()
	time.sleep(10) #Tiempo para que cargue la encuesta porque sino se pierde


lista_encuestas = []
lista_puntajes = []
UTN_USER, UTN_PASS = obtenerUserYPass()

chromedriver_autoinstaller.install()
driver = webdriver.Chrome()

login()
obtener_encuestas()

for enc in lista_encuestas:
	try:
		completar_encuesta(enc)
	except:
		print(f"No se pudo completar la encuesta: {enc}")

driver.quit()
msgbox("Se han completado las encuestas")