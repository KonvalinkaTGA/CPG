
def cislo_text_desitky(cislo):
    # funkce zkonvertuje desítkové místo čísla do jeho textove reprezentace
    # napr: "25" -> "dvacet"

    if(int(cislo)//10==2):
        return "dvacet"
    elif(int(cislo)//10==3):
        return "třicet"
    elif(int(cislo)//10==4):
        return "čtyřicet"
    elif(int(cislo)//10==5):
        return "padesát"
    elif(int(cislo)//10==6):
        return "šedesát"
    elif(int(cislo)//10==7):
        return "sedmdesát"
    elif(int(cislo)//10==8):
        return "osmdesát"
    elif(int(cislo)//10==9):
        return "devadesát"
    else:
        return ""
    

def mezera(cislo): #nenapíše mezeru, pokud je cislo jednociferne, nebo "divne cislo"
    if(int(cislo)//10==0)or(int(cislo)//10==1)or(int(cislo)==100):
        return ""
    else:
        return " "
    
    
def cislo_text_jednotky(cislo):#kontroluje cislo na jednotkové pozici
    if(int(cislo)//10==1):
        return ""#udělá aby funkce nejela, pokud pracujeme s čísly 10 až 19
    elif(int(cislo)%10==1):
        return "jedna"
    elif(int(cislo)%10==2):
        return "dva"
    elif(int(cislo)%10==3):
        return "tři"
    elif(int(cislo)%10==4):
        return "čtyři"
    elif(int(cislo)%10==5):
        return "pět"
    elif(int(cislo)%10==6):
        return "šest"
    elif(int(cislo)%10==7):
        return "sedm"
    elif(int(cislo)%10==8):
        return "osm"
    elif(int(cislo)%10==9):
        return "devět"
    else:
        return ""
        

def cislo_text_divne(cislo):#přepisuce čísla, která nešla zapsat pomocí ostatních příkazů
    if(int(cislo)==10):
        return "deset"
    elif(int(cislo)==11):
        return "jedenáct"
    elif(int(cislo)==12):
        return "dvanáct"
    elif(int(cislo)==13):
        return "třináct"
    elif(int(cislo)==14):
        return "čtrnáct"
    elif(int(cislo)==15):
        return "patnáct"
    elif(int(cislo)==16):
        return "šestnáct"
    elif(int(cislo)==17):
        return "sedmnáct"
    elif(int(cislo)==18):
        return "osmnáct"
    elif(int(cislo)==19):
        return "devatenáct"
    elif(int(cislo)==100):
        return "sto"
    elif(int(cislo)==0):
        return "nula"
    else:
        return ""

if __name__ == "__main__":
    x=0
    cislo = input("Zadej číslo: ")
    if(x=="1"):
        text=cislo_text_jednotky(cislo)
    else:text = cislo_text_desitky(cislo)+mezera(cislo)+cislo_text_jednotky(cislo)+cislo_text_divne(cislo)
    print(text)
