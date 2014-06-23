#   author  Jurriaan
#	date	05-06-14

from Bio import Entrez
from Bio import Medline

def main(substance):
    return ("edges = ["+edgewriter(substance)+"];")
    print("done")



	
def edgewriter(substance):
    
    edges = ""
    organisms = {"C.Elegans","D.Discoideum","Danio rerio"}
    c = 0
    for i in organisms:
        print("test")
        c += 1
        aantalpubmedartikelen = pubcheck(i,substance)
        if aantalpubmedartikelen == "0":
            pass
        else:
            pass
            edges += ",{from: "+str(c)+", to: 4, value: "+str(aantalpubmedartikelen)+", title: '"+str(aantalpubmedartikelen)+" Matching publications'}"
    return(edges[1:])
	
def pubcheck(i,substance):
    TERM = (i+" AND "+substance)
    MAX_COUNT = 10
    Entrez.email = "A.N.Other@example.com"
    h = Entrez.esearch(db="pubmed", retmax=MAX_COUNT, term=TERM)
    result = Entrez.read(h)
    return(result["Count"])