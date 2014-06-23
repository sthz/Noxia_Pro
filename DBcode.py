## DB code.py ontwikkeld door bio informatica groep 4, leerjaar 2
## naam auteurs: Janneke van den End, Wouter Sanderse, Mariska Windhouwer en Jurriaan Jansen
## Deze code zoekt met behulp van een aanroep vanuit app.py in de pubmed
## database naar artikelen, daarna connecteerd hij aan de database en vult deze
## met de gevonden artikelen, hij vult substance met de stof en een auto ID
## hij vult organism met het organisme waarop is gezocht en voegt er een auto ID
## aan toe, en bij publications voegt hij de ID's van substance en organisme toe.
## en titel, schrijvers, abstract, datum en bron van het gevonden artikel.
## bekende bugs: als je via de internet site organisme en substantie invult dan
## neemt het programma app deze nog niet mee naar dit python script.
## versie 1.7
## datum: 16-09-2014

#import van biopython, mysql database en app.
import sys
#sys.path.end('/home/bi2_pg4/public_html/NoxiaPro/')
import app
import cgi, cgitb
form=cgi.FieldStorage()
organism = form.getvalue('organism')
substance = form.getvalue('substance')
from Bio import Entrez
from Bio import Medline
import MySQLdb as con
import logging

# aanmaken van een class
class bla():

# zoeken met de meegegeven terms vanuit app.py in de pubmed database.
	def __init__(self):
		logging.basicConfig(filename='/home/bi2_pg4/public_html/python/app.log',level=logging.DEBUG)
		
		if True:
                        self.TERMS = '(' +substance + ')' + 'AND'+ '('+organism + ')'
		        self.TERM1 = '%s' %form['substance']
                        self.TERM2 = '%s'%form['organism']
		logging.debug(form.keys)
# meegeven van gegevens aan NCBI, aanroepen van de zoekfunctie.
		Entrez.email = "A.N.Other@example.com"     # Always tell NCBI who you are
		handle = Entrez.egquery (term=self.TERMS)
		record = Entrez.read(handle)
		for row in record["eGQueryResult"]:
			if row["DbName"]=="pubmed":
				print(row["Count"])
				
		handle = Entrez.esearch(db="pubmed", term=self.TERMS, retmax=463)
		record = Entrez.read(handle)
		
		handle = Entrez.efetch(db="pubmed", id=record["IdList"], rettype="medline")
		records = Medline.parse(handle)
		records = list(records)
		
# het aanmaken van listen voor Titel, auteur, bron, abstract en date.
		self.title = []
		self.authors = []
		self.source = []
		self.abstract = []
		self.date = []
# het vullen van de aangemaakte listen met de gevonden resultaten.
		for record in records:
			self.title.append(record.get("TI", "?"))
			self.authors.append(record.get("AU", "?"))
			self.source.append(record.get("SO", "?"))
			self.abstract.append(record.get("AB", "?"))
			self.date.append(record.get("DA", "?"))   
				 
		# Open database connection
		self.dataB=con.connect(host="localhost", # your host, usually localhost
		user="bi2_pg4", # your username
		passwd="blaat1234", # your password
		db="bi2_pg4") # name of the data base

		# prepare a cursor object using cursor() method
		cursor1 = self.dataB.cursor()

		try:
		# Execute the SQL command
			cursor1.execute("SELECT substance_id FROM substances WHERE substance = '"+self.TERM1+"'")
			substanceExists = cursor1.rowcount > 0
			cursor1.close()
			cursor1 = self.dataB.cursor()
			cursor1.execute("SELECT organism_id FROM organisms WHERE organism = '"+self.TERM2+"'")
			organismExists = cursor1.rowcount > 0
			cursor1.close()
# aanroepen van verschillende functies afhankelijk van de hierboven SQL commands.
			if not substanceExists and not organismExists:
				self.insertsubstance()
				self.insertorganism()
				self.insertPublications()
				self.dataB.commit()
			elif not substanceExists:
				self.insertsubstance()        
				self.insertPublications()
				self.dataB.commit()
			elif not organismExists:
				self.insertorganism()
				self.insertPublications()
				self.dataB.commit()
				
		except con.Error, e:
			logging.debug(e)
		#except:
				   # Rollback in case there is any error
			#dataB.rollback()
		# disconnect from server
		cursor1.close()
		self.dataB.close()
# insert substance voegt de substance toe aan de database
	def insertsubstance(self):
		cursor = self.dataB.cursor()
		cursor.execute("INSERT INTO substances(substance) VALUES ('"+self.TERM1+"')")
		cursor.close()
# insert organism voegt de organisme toe aan de database
	def insertorganism(self):
		cursor = self.dataB.cursor()
		cursor.execute("INSERT INTO organisms (organism) VALUES ('"+self.TERM2+"')")  
		cursor.close()
# insert publications voegt de titel, auteur, source, abstract en datum toe aan de database
	def insertPublications(self):
		cursor = self.dataB.cursor()
		cursor.execute("SELECT substance_id FROM substances WHERE substance = '"+self.TERM1+"'")
		Term1ID = cursor.fetchone()[0]
		cursor.close()
		cursor = self.dataB.cursor()
		cursor.execute("SELECT organism_id FROM organisms WHERE organism = '"+self.TERM2+"'")
		Term2ID = cursor.fetchone()[0]
		i=0
		while(i<len(self.title)):
			#logging.debug(i)
			cursor.close()
			cursor = self.dataB.cursor()
			_title = self.title[i].replace("'","")
			_authors = ','.join(self.authors[i]).replace("'","")
			magazine = self.source[i].replace("'","")
			_date = self.date[i].replace("'","")
			_abstract = self.abstract[i].replace("'","")
			command = 'INSERT INTO publications (organism, substance, title, authors, magazine, date, abstract) VALUES ({0},{1},{2},{3},{4},{5},{6})'.format(Term2ID, Term1ID, "'"+_title+"'", "'"+_authors+"'", "'"+magazine+"'", "'"+_date+"'", "'"+_abstract+"'")
			#logging.debug(command)
			cursor.execute(command)
			i+=1
# aanmaken van de mainfunctie met daarin de aanroep naar de class		
def main():
	b = bla()
# aanroep van de main functie.	
main()



