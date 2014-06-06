import sys
sys.path.append('/home/bi2_pg4/public_html/NoxiaPro/')
from Bio import Entrez
from Bio import Medline
import MySQLdb as con
import logging

class bla():

    def __init__(self):
        logging.basicConfig(filename='/home/bi2_pg4/public_html/python/app.log',level=logging.DEBUG)

        if form.has_key('Substance'and'Organism')
            TERM1 = '%s' %form['Substance']
            TERM2 = '%s'%form['Organism']
            TERMS = ('(' +TERM1 + ')' + 'AND'+ '('+TERM2 + ')')

##        self.TERM1 = "formaldehyde"
##        self.TERM2 = "Caenorhabditis elegans"
##        self.TERMS = ('(' +self.TERM1 + ')' + 'AND'+ '('+self.TERM2 + ')')

        Entrez.email = "A.N.Other@example.com"     # Always tell NCBI who you are
        handle = Entrez.egquery(term=self.TERMS)
        record = Entrez.read(handle)
        for row in record["eGQueryResult"]:
            if row["DbName"]=="pubmed":
                print(row["Count"])
                         
        handle = Entrez.esearch(db="pubmed", term=self.TERMS, retmax=463)
        record = Entrez.read(handle)

        handle = Entrez.efetch(db="pubmed", id=record["IdList"], rettype="medline")
        records = Medline.parse(handle)
        records = list(records)

        self.title = []
        self.authors = []
        self.source = []
        self.abstract = []
        self.date = []

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

            if not substanceExists and not organismExists:
                self.insertSubstance()
                self.insertOrganism()
                self.insertPublications()
                self.dataB.commit()
            elif not substanceExists:
                self.insertSubstance()        
                self.insertPublications()
                self.dataB.commit()
            elif not organismExists:
                self.insertOrganism()
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

    def insertSubstance(self):
        cursor = self.dataB.cursor()
        cursor.execute("INSERT INTO substances(substance) VALUES ('"+self.TERM1+"')")
        cursor.close()

    def insertOrganism(self):
        cursor = self.dataB.cursor()
        cursor.execute("INSERT INTO organisms (organism) VALUES ('"+self.TERM2+"')")  
        cursor.close()

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

def main():
    b = bla()

main()
    
    
