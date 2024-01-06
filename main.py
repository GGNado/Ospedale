from typing import List

import uvicorn
import mysql.connector
import random
import os
import jinja2
import aiofiles
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

# Definizione dell'oggetto Pazienti utilizzando pydantic
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

	def getCondizioni(self) -> str:
		listaMalattie = getPazienteMalattie(self.id)
		if len(listaMalattie) < 2:
			return "Eccellenti"
		elif len(listaMalattie) < 6:
			return "Stabili"
		else:
			return "Gravi"



class Malattie(BaseModel):
	id: int
	nome: str
	descrizione: str

class MalattieLista(BaseModel):
	malattieIds: List[int]

# QUI INSERITE LE FUNZIONI
def getAllPazienti(filtro = None):
	conn = mysql.connector.connect(**config)
	if conn.is_connected():
		cursor = conn.cursor()
		if filtro == None:
			query = "SELECT * FROM Patients"
			cursor.execute(query)
		else:
			query = "SELECT * FROM Patients WHERE nome LIKE %s OR cognome LIKE %s"
			cursor.execute(query, (filtro, filtro))
		results = cursor.fetchall()
		listaPazienti = []
		for row in results:
			listaPazienti.append(Pazienti(id=int(row[0]), nome=row[1], cognome=row[2], sesso=row[3], dataNascita=row[4]))
		cursor.close()
		conn.close()
		return listaPazienti
	else:
		print('Connessione al database fallita.')

def getPazienteById(id):
	conn = mysql.connector.connect(**config)
	if conn.is_connected():
		cursor = conn.cursor()
		query = "SELECT * FROM Patients WHERE id = %s"
		cursor.execute(query, (id,))
		results = cursor.fetchall()
		p = None
		for row in results:
			p = Pazienti(id=int(row[0]), nome=row[1], cognome=row[2], sesso=row[3], dataNascita=row[4])
		cursor.close()
		conn.close()
		return p
	else:
		print('Connessione al database fallita.')

def getAllMalattie():
	conn = mysql.connector.connect(**config)
	if conn.is_connected():
		cursor = conn.cursor()
		query = "SELECT * FROM Illnesses"
		cursor.execute(query)
		results = cursor.fetchall()
		listaMalattie = []
		for row in results:
			listaMalattie.append(Malattie(id=int(row[0]), nome=row[1], descrizione=row[2]))
		cursor.close()
		conn.close()
		return listaMalattie
	else:
		print('Connessione al database fallita.')

def getPazienteMalattie(idPaziente: int):
	conn = mysql.connector.connect(**config)
	if conn.is_connected():
		cursor = conn.cursor()
		query = "SELECT FK_Malattia FROM PatientsIllnesses WHERE FK_Paziente = %s AND dataCura IS NULL"
		cursor.execute(query, (idPaziente,))
		results = cursor.fetchall()
		listaMalattie = []
		for row in results:
			listaMalattie.append(row[0])
		cursor.close()
		conn.close()
		return listaMalattie
	else:
		print('Connessione al database fallita.')


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

@webapp.get("/api/patientFiltro/{f}")
async def pazientiPage(req: Request, f: str):
	return templates.TemplateResponse(
		"pazienti.html", {
			"request": req,
			"listaPazienti": getAllPazienti(f)
		}
	)


@webapp.delete("/api/patient/{id}")
async def eliminaPaziente(id):
	conn = mysql.connector.connect(**config)
	if conn.is_connected():
		queryForein = "DELETE FROM PatientsIllnesses WHERE FK_Paziente = %s"
		query = "DELETE FROM Patients WHERE id = %s"
		cur = conn.cursor()
		cur.execute(queryForein, (id,))
		conn.commit()
		cur.execute(query, (id,))
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
async def aggiungiPaziente(p: Pazienti):
	conn = mysql.connector.connect(**config)
	if conn.is_connected():
		query = "INSERT INTO Patients (Nome, Cognome, Sesso, DataNascita) VALUES (%s, %s, %s, %s)"
		cur = conn.cursor()
		cur.execute(query, (p.nome, p.cognome, p.sesso, p.dataNascita))
		conn.commit()
		conn.close()

@webapp.post('/api/patient/uploadImage/{nome}/{cognome}/{data}')
async def uploadImg(data:datetime, nome: str, cognome: str, imgFile: UploadFile = File(...)):
	filename = f'{nome}_{cognome}_{data.strftime("%Y-%m-%d")}.jpg'

	async with aiofiles.open(os.path.join("static", filename), "wb") as out_file:
		content = await imgFile.read()  # Leggi il contenuto del file caricato
		await out_file.write(content)   # Scrivi il contenuto nel nuovo file

@webapp.put("/api/patient/{id}/")
async def aggiornaPaziente(p: Pazienti):
	conn = mysql.connector.connect(**config)
	if conn.is_connected():
		query = '''UPDATE Patients
				   SET Nome = %s, Cognome = %s, Sesso = %s, DataNascita = %s
				   WHERE id = %s'''
		cur = conn.cursor()
		cur.execute(query, (p.nome, p.cognome, p.sesso, p.dataNascita, p.id))
		conn.commit()
		conn.close()

@webapp.get("/api/patient/{id}")
async def cambiaPag(req: Request, id: int):
	return templates.TemplateResponse(
		"aggiornaPaziente.html", {
			"request": req,
			"pazienteCorrente": getPazienteById(id)
		}
	)

@webapp.get("/api/patient/{id}/aggiungiIlness")
async def cambiaPag(req: Request, id: int):
	return templates.TemplateResponse(
		"malattieAggiungi.html", {
			"request": req,
			"listaMalattie": getAllMalattie(),
			"pMalattie": getPazienteMalattie(id),
			"paziente": getPazienteById(id)
		}
	)

@webapp.get("/api/patient/{id}/ilness")
async def cambiaPag(req: Request, id: int):
	return templates.TemplateResponse(
		"malattieIndex.html", {
			"request": req,
			"paziente": getPazienteById(id)
		}
	)

@webapp.post("/api/patient/{id}/aggiungiIlness/")
async def aggiungiMalattie(id: int, malattie_ids: MalattieLista):
	malattie_selezionate = malattie_ids.malattieIds
	conn = mysql.connector.connect(**config)
	if conn.is_connected():
		for ids in malattie_selezionate:
			query = '''INSERT INTO PatientsIllnesses (dataCont, FK_Paziente, FK_Malattia) VALUES (%s, %s, %s)'''
			cur = conn.cursor()
			cur.execute(query, (datetime.now(), id, ids))
			conn.commit()

		conn.close()

@webapp.get("/api/patient/{id}/eliminaIlness")
async def cambiaPag(req: Request, id: int):
	return templates.TemplateResponse(
		"eliminaMalattie.html", {
			"request": req,
			"listaMalattie": getAllMalattie(),
			"pMalattie": getPazienteMalattie(id),
			"paziente": getPazienteById(id)
		}
	)
@webapp.delete("/api/patient/{id}/eliminaIlness/")
async def eliminaMalattie(id: int, malattie_ids: MalattieLista):
	malattie_selezionate = malattie_ids.malattieIds
	conn = mysql.connector.connect(**config)
	if conn.is_connected():
		for ids in malattie_selezionate:
			query = '''DELETE FROM PatientsIllnesses WHERE FK_Paziente = %s AND FK_Malattia = %s'''
			cur = conn.cursor()
			cur.execute(query, (id, ids))
			conn.commit()

		conn.close()

@webapp.get("/api/patient/{id}/modificaIlness")
async def cambiaPag(req: Request, id: int):
	return templates.TemplateResponse(
		"modificaMalattie.html", {
			"request": req,
			"listaMalattie": getAllMalattie(),
			"pMalattie": getPazienteMalattie(id),
			"paziente": getPazienteById(id)
		}
	)

@webapp.put("/api/patient/{id}/modificaIlness")
async def modificaMalattie(id: int, malattie_ids: MalattieLista):
	malattie_selezionate = malattie_ids.malattieIds
	conn = mysql.connector.connect(**config)
	if conn.is_connected():
		for ids in malattie_selezionate:
			query = '''UPDATE PatientsIllnesses
							   SET dataCura = %s
							   WHERE FK_Malattia = %s AND FK_Paziente = %s'''
			cur = conn.cursor()
			cur.execute(query, (datetime.now(), ids, id))
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