
from Bio import Entrez
from Bio import Medline
import pymysql

TERM1 = input("Geef de stof op: ")
TERM2 = input("Geef het organisme op: ")
TERMS = ('(' +TERM1 + ')' + 'AND'+ '('+TERM2 + ')')

Entrez.email = "A.N.Other@example.com"     # Always tell NCBI who you are
handle = Entrez.egquery(term=TERMS)
record = Entrez.read(handle)
for row in record["eGQueryResult"]:
     if row["DbName"]=="pubmed":
          print(row["Count"])
         
handle = Entrez.esearch(db="pubmed", term=TERMS, retmax=463)
record = Entrez.read(handle)
idlist = record["IdList"]

handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline",
                           retmode="text")
records = Medline.parse(handle)
records = list(records)

for record in records:
    print("title:", record.get("TI", "?"))
    print("authors:", record.get("AU", "?"))
    print("source:", record.get("SO", "?"))
    print("abstract:", record.get("AB", "?"))
    print("date:", record.get("DA", "?"))
    print("")

# Open database connection
db=pymysql.connect(host="cytosine.nl", # your host, usually localhost
user="bi2_pg4", # your username
passwd="blaat1234", # your password
database="bi2_pg4") # name of the data base

# prepare a cursor object using cursor() method
cursor = database.cursor()
    
# Prepare SQL query to UPDATE required records
stat1 = ("INSERT INTO publication (title, authors, magazine, year, abstact) VALUES ('"+title+"', '"+authors+"', '"+source+"', '"+date+"', '"+abstact+"')")
stat2 = ("INSERT INTO organisms VALUES (%s) ", (TERM2))
stat3 = ("INSERT INTO substances VALUES (%s) ", (TERM1))

# 
if exists(("SELECT * FROM organisms WHERE Key =(%s) ", (TERM2)), cursor) and exists(("SELECT * FROM organisms WHERE Key =(%s) ", (TERM1)),cursor):
     print ('Zit al in de database')
else:
     print ('Zit nog niet in de database.')
     try:
       # Execute the SQL command
          cursor.execute(stat1)
          cursor.execute(stat2)
          cursor.execute(stat3)

       # Commit your changes in the database
          database.commit()

     except pymysql.Error:
          print ("ERROR IN CONNECTION")
     except:
       # Rollback in case there is any error
<<<<<<< HEAD
          db.rollback()  
=======
          database.rollback()

   
>>>>>>> d3306560c16806324f948cfa11079a51c0f95cac


# disconnect from server
cursor.close
database.close()

def exists(query, cursor):
     for result in cursor.execute(query):
          return result.with_rows


