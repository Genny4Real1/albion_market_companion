# versione 0.1
import os.path
import os
import json
import requests

print("Benvenuto in Albion Market Companion!")
print("made by Genny4Real")

oggetti = [] #crea una lista vuota di dizionari di oggetti

i = 1
while True:
    filename = f"report vendita {i:03}.txt"
    if not os.path.exists(filename):
        break
    i = i + 1 

while True:
    premiumInput = input("Hai il premium? (sì/no): ").lower() #inserisci se hai il premium o no per calcolare prezzo di vendita lordo
    
    if premiumInput == "sì" or premiumInput == "si" or premiumInput == "yes" or premiumInput == "true":
        premium = True
        break
    elif premiumInput == "false" or premiumInput == "no":
        premium = False
        break
    else:
        print("Input non valido. Scrivi esattamente 'true' o 'false': ")

idOggetto = 0

while True: #loop infinito
    nome = input("Nome dell'oggetto (oppure 'fine' per terminare): ") #inserisci nome oggetto
    
    if nome.lower() == "fine": #inserisci fine per rompere il loop
        break
    
    prezzoVenditaLordo = int(input("Prezzo di vendita per unità non tassato: ")) #inserisci il prezzo di vendita lordo, le tasse verrano calcolate successivamente
    quantita = int(input("Quantità da vendere: ")) #inserisci quantità di vendita

    if premium == True:
        tasse = int(round(prezzoVenditaLordo * 0.065,0)) #se hai il premium le tasse equivalgono a 4% + setup fee di 2.5%
    else:
        tasse = int(round(prezzoVenditaLordo * 0.105,0))  #se non hai il premium le tasse equivalgono a 8% + setup fee di 2.5%

    prezzoVenditaNetto = prezzoVenditaLordo - tasse #calcoliamo il prezzo di vendita netto

    guadagno = prezzoVenditaNetto * quantita #calcoliamo il guadagno netto
    oggetti.append({ #aggiungiamo un dizionario alla lista per ogni oggetto con le informazioni salvate
    "id": idOggetto,
    "nome": nome,
    "prezzo netto": prezzoVenditaNetto,
    "quantità": quantita,
    "tasse": tasse,
    "guadagno": guadagno
    })
    idOggetto = idOggetto + 1

with open(filename, "w") as f: 
    print("\n--- Report Vendite ---", file=f) #intestazione report vendite
    print("Premium? = " + premiumInput, file=f) #status del premium
    for o in oggetti: #ciclo for che scorre per tutti gli oggetti dela lista
        print(f"\n{o['nome']}: {o['quantità']:,} unità a {o['prezzo netto']:,} argento ciascuna -> Guadagno totale: {o['guadagno']:,} argento, Tasse totali: {round(o['tasse']*o['quantità'],0):,} argento.", file=f)


def cercaMiglioreOggetto(oggetti):
        oggettoMigliore = oggetti[1] #creo una variabile in cui inserisco l'id del primo oggetto(dizionario) della lista oggetti
        guadagnoOggettoMigliore = oggetti[1]['guadagno'] #creo una variabile in cui inserisco il guadagno del primo oggetto(dizionario) della lista oggetti
        for o in oggetti: #oggetti è una lista di o
            if guadagnoOggettoMigliore < o['guadagno']:
                guadagnoOggettoMigliore = o['guadagno']
                oggettoMigliore = o
        return(oggettoMigliore)

listaFinale = cercaMiglioreOggetto(oggetti)
with open(filename, "a") as f: 
    print(f"\nIl miglior profitto è dato dalla vendita dell'oggetto {listaFinale["nome"]} con un guadagno di {listaFinale['guadagno']:,} argento.", file=f)

market_comparison = input("Vuoi comparare il tuo ordine di vendita con il mercato? (sì/no)")
if market_comparison == "sì" or market_comparison == "si":
        api_url = "https://west.albion-online-data.com/api/v2/stats/prices/"

        items = ['T4_SOUL','T5_SOUL']
        item_name = ','.join(items)     

        locations = ['Bridgewatch']
        location_name = ','.join(locations)     

        #qualities = ['1','2']
        #quality = ','.join(qualities)          

        price_request = requests.get(api_url + item_name + ".json?locations=" + location_name + r"&qualities=0")       

        # pretty_json = json.dumps(price_request.json(), indent=2)
        # print (pretty_json)       

        item_price_info_a = []
        item_price_info_a.append({
            "item_id" : price_request.json()[0]["item_id"],
            "quality" : price_request.json()[0]["quality"],
            "sell_price_min" : price_request.json()[0]["sell_price_min"]
        })

        item_price_info_b = []
        item_price_info_b.append({
            "item_id" : price_request.json()[1]["item_id"],
            "quality" : price_request.json()[1]["quality"],
            "sell_price_min" : price_request.json()[1]["sell_price_min"]
        })

        print("Queste sono le informazioni prese dall'API di Albion per l'item da te richiesto")

        print(f"\n{item_price_info_a[0]['item_id']}: {oggetti[0]['quantità']:,} unità a {item_price_info_a[0]['sell_price_min']:,} argento ciascuna -> Guadagno totale: {oggetti[0]['quantità'] * item_price_info_a[0]['sell_price_min']:,} argento, differenza: {oggetti[0]['guadagno'] - (oggetti[0]['quantità'] * item_price_info_a[0]['sell_price_min']):,} argento.")
        print(f"\n{item_price_info_b[0]['item_id']}: {oggetti[1]['quantità']:,} unità a {item_price_info_b[0]['sell_price_min']:,} argento ciascuna -> Guadagno totale: {oggetti[1]['quantità'] * item_price_info_b[0]['sell_price_min']:,} argento, differenza: {oggetti[1]['guadagno'] - (oggetti[1]['quantità'] * item_price_info_b[0]['sell_price_min']):,} argento.")
        print("Grazie per aver usato Albion Market Comparison.")
else:
    print("Grazie per aver usato Albion Market Comparison.")




        



