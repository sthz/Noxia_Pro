#import
from Bio import Entrez
from Bio import Medline

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
