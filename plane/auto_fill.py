def autofill(type_):
    """give me the type, and I'll return the model name and the cat/class"""
    type_ = type_.upper()
    model = None
    
    if type_.startswith("C"):
        if   "120" in type_: model="";c=1
        elif "140" in type_: model="";c=1
        elif "150" in type_: model="";c=1
        elif "152" in type_: model="";c=1
        elif "162" in type_: model="Skycatcher";c=1
        elif "165" in type_: model="Airmaster";c=1
        elif "170" in type_: model="";c=1
        elif "172" in type_: model="Skyhawk";c=1
        elif "175" in type_: model="Skylark";c=1
        elif "177" in type_: model="Cardinal";c=1
        elif "180" in type_: model="";c=1
        elif "182" in type_: model="Skylane";c=1
        elif "185" in type_: model="";c=1
        elif "190" in type_: model="";c=1
        elif "195" in type_: model="";c=1
        elif "210" in type_: model="Centurion";c=1
        elif "206" in type_: model="Stationair";c=1
        elif "207" in type_: model="";c=1
        elif "208" in type_: model="Caravan";c=1
        elif "303" in type_: model="Crusader";c=2
        elif "310" in type_: model="";c=2
        elif "320" in type_: model="Skyknight";c=2
        elif "335" in type_: model="";c=2
        elif "336" in type_: model="Skymaster";c=2
        elif "337" in type_: model="Skymaster";c=2
        elif "340" in type_: model="";c=2
        elif "350" in type_: model="Corvalis";c=1
        elif "400" in type_: model="Corvalis TT";c=1
        elif "401" in type_: model="";c=2
        elif "402" in type_: model="";c=2
        elif "404" in type_: model="Titan";c=2
        elif "406" in type_: model="Caravan II";c=2
        elif "411" in type_: model="";c=2
        elif "414" in type_: model="Conquest II";c=2
        elif "421" in type_: model="Golden Eagle";c=2
        elif "425" in type_: model="Conquest";c=2
        elif "441" in type_: model="Conquest II";c=2
        elif "500" in type_: model="Citation I";c=2
        elif "501" in type_: model="Citation I";c=2
        elif "510" in type_: model="Citation Mustang";c=2
        elif "525" in type_: model="CitationJet";c=2
        elif "550" in type_: model="Citation II";c=2
        elif "560" in type_: model="Citation V";c=2
        elif "650" in type_: model="Citation III";c=2
        elif "680" in type_: model="Citation Sovereign";c=2
        elif "750" in type_: model="Citation X";c=2
        elif "850" in type_: model="Citation Columbus";c=2
        
        if model is not None:
            return ("Cessna", model, c)
        else:
            return None
    
    elif type_.startswith("PA"):
        if "6" in type_: model="Sky Sedan";c=1
        if "7" in type_: model="Skycoupe";c=1
        if "8" in type_: model="Skycycle";c=1
        if "9" in type_: model="";c=1
        elif "10" in type_: model="";c=1
        elif "11" in type_: model="Cub Special";c=1
        elif "12" in type_: model="Super Cruiser";c=1
        elif "14" in type_: model="Family Cruiser";c=1
        elif "15" in type_: model="Vagabond";c=1
        elif "16" in type_: model="Clipper";c=1
        elif "17" in type_: model="Vagabond";c=1
        elif "18" in type_: model="Super Cub";c=1
        elif "19" in type_: model="Super Cub";c=1
        elif "20" in type_: model="Pacer";c=1
        elif "21" in type_: model="";c=1
        elif "22" in type_: model="Tri-Pacer";c=1
        elif "23" in type_: model="Apache";c=2
        elif "24" in type_: model="Comanche";c=1
        elif "25" in type_: model="Pawnee";c=1
        elif "26" in type_: model="";c=1
        elif "27" in type_: model="Aztec";c=2
        elif "28R" in type_: model="Arrow";c=1
        elif "28-235" in type_: model="Dakota";c=1
        elif "28" in type_: model="Cherokee";c=1
        elif "29" in type_: model="Papoose";c=1
        elif "30" in type_: model="Twin Comanche";c=2
        elif "31T" in type_: model="Cheyenne";c=2
        elif "31P" in type_: model="Mojave";c=2
        elif "31-350" in type_: model="Chieftain";c=2
        elif "31" in type_: model="Navajo";c=2
        elif "32R" in type_: model="Lance";c=1
        elif "32" in type_: model="Cherokee Six";c=1
        elif "33" in type_: model="Comanche";c=1
        elif "34" in type_: model="Seneca";c=2
        elif "35" in type_: model="Pocono";c=2
        elif "36" in type_: model="Pawnee Brave";c=1
        elif "37" in type_: model="Comanche";c=1
        elif "38" in type_: model="Tomahawk";c=1
        elif "39" in type_: model="Twin Comanche";c=2
        elif "40" in type_: model="Arapaho";c=2
        elif "41" in type_: model="Aztec";c=2
        elif "42" in type_: model="Cheyenne";c=2
        elif "43" in type_: model="Cheyenne";c=2
        elif "44" in type_: model="Seminole";c=2
        elif "45" in type_: model="";c=1
        elif "46" in type_: model="Malibu";c=1
        elif "47" in type_: model="PiperJet";c=1
        elif "48" in type_: model="Enforcer";c=2
        elif "60" in type_: model="Aerostar";c=2

        if model is not None:
            return ("Piper", model, c)
        else:
            return None
    
    elif type_.startswith("BE"):
        if "16" in type_: model="";c=1
        elif "17" in type_: model="Staggerwing";c=1
        elif "18" in type_: model="Twin Beech";c=2
        elif "19" in type_: model="Sport";c=1
        elif "23" in type_: model="Musketeer";c=1
        elif "24" in type_: model="Sierra";c=1
        elif "34" in type_: model="Twin-Quad";c=1
        elif "33" in type_: model="Debonair";c=1
        elif "35" in type_: model="Bonanza";c=1
        elif "36" in type_: model="Bonanza";c=1
        elif "40" in type_: model="";c=2
        elif "50" in type_: model="";c=2
        elif "55" in type_: model="Baron";c=2
        elif "56" in type_: model="Baron";c=2
        elif "58" in type_: model="Baron";c=2
        elif "60" in type_: model="Duke";c=2
        elif "65" in type_: model="Queen Air";c=2
        elif "70" in type_: model="Queen Air";c=2
        elif "80" in type_: model="Queen Air";c=2
        elif "88" in type_: model="Queen Air";c=2
        elif "76" in type_: model="Duchess";c=2
        elif "77" in type_: model="Skipper";c=1
        elif "90" in type_: model="King Air";c=2
        elif "200" in type_: model="Super King Air";c=2
        elif "300" in type_: model="Super King Air";c=2       
        elif "100" in type_: model="King Air";c=2
        elif "95" in type_: model="Travel Air";c=2
        elif "99" in type_: model="Airliner";c=2
        elif "390" in type_: model="Premier";c=2
        elif "1900" in type_: model="Airliner";c=2
        elif "2000" in type_: model="Starship";c=2

        if model is not None:
            return ("Beechcraft", model, c)
        else:
            return None











        
