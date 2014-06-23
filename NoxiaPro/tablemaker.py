def main(substance):
	table = "<table>"
	table += "<tr>"\
  			"<td>title			</td>"\
  			"<td>authors		</td>"\
  			"<td>source			</td>"\
  			"<td>Abstract 		</td>"\
  			"<td>date			</td>"\
    		"<td>country		</td>"\
      		"<td>year			</td>"\
        	"<td>pubmed			</td>"\
			"</tr>"
	link = '<a href="www.pubmed.com">pubmed</a>'
	for i in range (10):
		table += pubmed(substance)
	
	table += "</table>"	
	return table	

	




def pubmed(substance):
	from Bio import Entrez
from Bio import Medline


TERM1 = substance
TERM2 = ("c.elegans")
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
    title = record.get("TI", "?")
    authors = record.get("AU", "?")
    source = record.get("SO", "?")
    abstract = record.get("AB", "?")
    date = record.get("DA", "?")
    pmid = record.get("PMID","?")
    mash = record.get("MH","?")
    country = record.get("PL","?")
    link = ("http://www.pubmed.com/"+pmid)
    return("<tr><td>"+''.join(title)+"</td><td>"+', '.join(authors)+"</td><td>"+source+"</td><td>"+abstract+"</td><td>"+date+"</td><td>"+country+"</td><td>"+', '.join(mash)+"</td><td>"+link+"</td></tr>") 

	
	
	
	
	
	
	
	
	
	
	


