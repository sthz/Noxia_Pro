import sys
sys.path.append('/home/bi2_pg4/public_html/NoxiaPro/')
from Bio import Entrez
from Bio import Medline
import MySQLdb as con
import logging
logging.basicConfig(filename='/home/bi2_pg4/public_html/python/app.log',level=logging.DEBUG)

#if form.has_key('Substance'and'Organism')
#    TERM1 = '%s' %form['Substance']
#    TERM2 = '%s'%form['Organism']
#    TERMS = ('(' +TERM1 + ')' + 'AND'+ '('+TERM2 + ')')

TERM1 = "formaldehyde"
TERM2 = "dictyostelium discoideum"
TERMS = ('(' +TERM1 + ')' + 'AND'+ '('+TERM2 + ')')

Entrez.email = "A.N.Other@example.com"     # Always tell NCBI who you are
handle = Entrez.egquery(term=TERMS)
record = Entrez.read(handle)
for row in record["eGQueryResult"]:
    if row["DbName"]=="pubmed":
        print(row["Count"])
		 
handle = Entrez.esearch(db="pubmed", term=TERMS, retmax=463)
record = Entrez.read(handle)

handle = Entrez.efetch(db="pubmed", id=record["IdList"], rettype="medline")
records = Medline.parse(handle)
records = list(records)

for record in records:
    title = []
    authors = []
    source = []
    abstract = []
    date = []
    title.append(record.get("TI", "?"))
    authors.append(record.get("AU", "?"))
    source.append(record.get("SO", "?"))
    abstract.append(record.get("AB", "?"))
    date.append(record.get("DA", "?"))
	 

# Open database connection
dataB=con.connect(host="localhost", # your host, usually localhost
user="bi2_pg4", # your username
passwd="blaat1234", # your password
db="bi2_pg4") # name of the data base

# prepare a cursor object using cursor() method
cursor1 = dataB.cursor()

try:
# Execute the SQL command
    cursor1.execute("INSERT INTO substances(substance) VALUES ('"+TERM1+"')")
    cursor1.close()
    cursor1 = dataB.cursor()
    cursor1.execute("INSERT INTO organisms (organism) VALUES ('"+TERM2+"')")    
    cursor1.close()
    cursor1 = dataB.cursor()
    cursor1.execute("SELECT substance_id FROM substances WHERE substance = '"+TERM1+"'")
    Term1ID = cursor1.fetchone()[0]
    logging.debug(Term1ID)
    cursor1.close()
    cursor1 = dataB.cursor()
    cursor1.execute("SELECT organism_id FROM organisms WHERE organism = '"+TERM2+"'")
    Term2ID = cursor1.fetchone()[0]
    logging.debug(Term2ID)
    cursor1.close()
    cursor1 = dataB.cursor()
    dataB.commit()

    cursor1.execute("""INSERT INTO publications (organism, substance, title, authors, magazine, date, abstract) VALUES ('"+Term2ID+"','"+Term1ID+"','test', 'test', 'test', 'today', 'test')""")
    dataB.commit()    

	   # Commit your changes in the database
    dataB.commit()

except con.Error, e:
    logging.debug(e)
#except:
	   # Rollback in case there is any error
    #dataB.rollback()
# disconnect from server
cursor1.close()
dataB.close()
