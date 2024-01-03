import uvicorn
import mysql.connector
import random
import os
import jinja2
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
	'port': 3306,
    'database': 'Ospedale'
}

# Creazione dell'app FastAPI
webapp = FastAPI(
	title='🏥 Fanta Ospedale',
	description= "Crea un archivio di pazienti con malattie immaginarie!"
)

# Configurazione dei template Jinja2
templates = Jinja2Templates(
	directory='templates',
	autoescape=False,
	auto_reload=True
)

# Montaggio della cartella 'static' per i file statici
webapp.mount(
	'/static',
	app=StaticFiles(directory='static'),
	name='static'
)

# Definizione dell'oggetto Person utilizzando pydantic (altrimenti dovevamo usare dataclasses)
class Pazienti(BaseModel):
	id: int
	nome: str
	cognome: str
	sesso: str
	dataNascita: datetime
	def calcolaEta(self) -> int:
		oggi = datetime.now().date()
		differenza_anni = oggi.year - self.dataNascita.year
		if (oggi.month, oggi.day) < (self.dataNascita.month, self.dataNascita.day):
			differenza_anni -= 1
		return differenza_anni

# Lista di esempio di persone esempio
"""
listaPazienti = [
    Pazienti(id=1, nome="Mario", cognome="Rossi", eta=35, sesso="M", dataNascita=datetime(1988, 5, 15), dataRicovero=datetime.now()),
    Pazienti(id=2, nome="Maria", cognome="Bianchi", eta=28, sesso="F", dataNascita=datetime(1995, 10, 22), dataRicovero=datetime.now()),
    Pazienti(id=3, nome="Giovanni", cognome="Verdi", eta=45, sesso="M", dataNascita=datetime(1978, 3, 7), dataRicovero=datetime.now()),
    Pazienti(id=4, nome="Luigi", cognome="Gialli", eta=60, sesso="M", dataNascita=datetime(1963, 12, 18), dataRicovero=datetime.now()),
    Pazienti(id=5, nome="Chiara", cognome="Neri", eta=20, sesso="F", dataNascita=datetime(2002, 8, 30), dataRicovero=datetime.now()),
    Pazienti(id=6, nome="Paolo", cognome="Rosa", eta=55, sesso="M", dataNascita=datetime(1968, 6, 5), dataRicovero=datetime.now()),
    Pazienti(id=7, nome="Alessia", cognome="Verdi", eta=32, sesso="F", dataNascita=datetime(1990, 4, 12), dataRicovero=datetime.now()),
    Pazienti(id=8, nome="Marco", cognome="Marroni", eta=42, sesso="M", dataNascita=datetime(1981, 9, 25), dataRicovero=datetime.now()),
    Pazienti(id=9, nome="Elena", cognome="Blu", eta=25, sesso="F", dataNascita=datetime(1998, 7, 17), dataRicovero=datetime.now()),
    Pazienti(id=10, nome="Federico", cognome="Arancioni", eta=38, sesso="M", dataNascita=datetime(1985, 11, 9), dataRicovero=datetime.now()),
    # Aggiungi altri pazienti con le loro informazioni di data di nascita e di ricovero
]
"""

# QUI INSERITE LE FUNZIONI
def getAllPazienti():
	conn = mysql.connector.connect(**config)
	if conn.is_connected():
		print('Okay')
		# Creazione di un cursore per eseguire le query
		cursor = conn.cursor()
		# Esempio di esecuzione di una query
		query = "SELECT * FROM Patients"
		cursor.execute(query)
		# Ottenere i risultati della query
		results = cursor.fetchall()
		# Crezione Lista
		listaPazienti = []
		for row in results:
			listaPazienti.append(Pazienti(id=int(row[0]), nome=row[1], cognome=row[2], sesso=row[3], dataNascita=row[4]))
		# Chiudi il cursore e la connessione
		cursor.close()
		conn.close()
		return listaPazienti
	else:
		print('Connessione al database fallita.')
		#Rimanda a qualcge pagina
@webapp.get("/", response_class= HTMLResponse)
def home(req: Request):
	return templates.TemplateResponse(
		"root.html",{
		"request": req
		}
	)

@webapp.get("/api/patient")
async def pazientiPage(req: Request):
	return templates.TemplateResponse(
		"pazienti.html", {
			"request": req,
			"listaPazienti": getAllPazienti()
		}
	)

@webapp.delete("/api/patient/{id}")
async def eliminaPaziente(id):
	conn = mysql.connector.connect(**config)
	if conn.is_connected():
		# Esempio di esecuzione di una query
		query = f"DELETE FROM Patients WHERE id = {id}"
		cur = conn.cursor()
		cur.execute(query)
		conn.commit()
		conn.close()

@webapp.get("/api/patient/add")
async def cambiaPag(req: Request):
	return templates.TemplateResponse(
		"aggiungiPaziente.html", {
			"request": req,
		}
	)

@webapp.post("/api/patient/add")
async def aggiungiPaziente(req: Request, p: Pazienti):
	conn = mysql.connector.connect(**config)
	if conn.is_connected():
		# Esempio di esecuzione di una query
		query = "INSERT INTO Patients (Nome, Cognome, Sesso, DataNascita) VALUES (%s, %s, %s, %s)"
		cur = conn.cursor()
		cur.execute(query, (p.nome, p.cognome, p.sesso, p.dataNascita))
		conn.commit()
		conn.close()

# Avvio dell'applicazione utilizzando uvicorn
if __name__ == '__main__':
	uvicorn.run(
		'main:webapp',
		host='0.0.0.0',
		port=3109,
		# use_colors = False,
		http='httptools',
		reload=True
	)