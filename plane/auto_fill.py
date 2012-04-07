def autofill(type_):
    """give me the type, and I'll return the model name and the cat/class"""
    type_ = type_.upper().replace("-","")
    model = None
    t = None
    c = None
    ret = {"manufacturer": None, "model": None, "cat_class": None, "tags": None}
    
    ## ----------------------------------------------------------------
    
    if type_.startswith("C") or type_.startswith("CE"):
        if   "120" in type_: model="";c=1;t="w"
        elif "140" in type_: model="";c=1;t="w"
        elif "150" in type_: model="";c=1
        elif "152" in type_: model="";c=1
        elif "162" in type_: model="Skycatcher";c=1;t="l"
        elif "165" in type_: model="Airmaster";c=1
        elif "170" in type_: model="";c=1;t="w"
        elif "172" in type_: model="Skyhawk";c=1
        elif "175" in type_: model="Skylark";c=1
        elif "177" in type_: model="Cardinal";c=1
        elif "180" in type_: model="";c=1;t="hw"
        elif "182" in type_: model="Skylane";c=1;t="h"
        elif "185" in type_: model="";c=1;t="hw"
        elif "190" in type_: model="";c=1;t="hw"
        elif "195" in type_: model="";c=1;t="hw"
        elif "210" in type_: model="Centurion";c=1;t="ch"
        elif "206" in type_: model="Stationair";c=1;t="ch"
        elif "207" in type_: model="";c=1;t="ch"
        elif "208" in type_: model="Caravan";c=1;t="th"
        elif "303" in type_: model="Crusader";c=2;t="ch"
        elif "310" in type_: model="";c=2;t="ch"
        elif "320" in type_: model="Skyknight";c=2;t="ch"
        elif "335" in type_: model="";c=2;t="ch"
        elif "336" in type_: model="Skymaster";c=2;t="ch"
        elif "337" in type_: model="Skymaster";c=2;t="ch"
        elif "340" in type_: model="";c=2;t="ch"
        elif "350" in type_: model="Corvalis";c=1;t="chg"
        elif "400" in type_: model="Corvalis TT";c=1;t="chg"
        elif "401" in type_: model="";c=2;t="ch"
        elif "402" in type_: model="";c=2;t="ch"
        elif "404" in type_: model="Titan";c=2;t="ch"
        elif "406" in type_: model="Caravan II";c=2;t="tcph"
        elif "411" in type_: model="";c=2;t="ch"
        elif "414" in type_: model="Conquest II";c=2;t="ch"
        elif "421" in type_: model="Golden Eagle";c=2;t="ch"
        elif "425" in type_: model="Conquest";c=2;t="tchp"
        elif "441" in type_: model="Conquest II";c=2;t="tchp"
        elif "500" in type_: model="Citation I";c=2;t="tjch"
        elif "501" in type_: model="Citation I";c=2;t="tjch"
        elif "510" in type_: model="Citation Mustang";c=2;t="tjch"
        elif "525" in type_: model="CitationJet";c=2;t="tjch"
        elif "550" in type_: model="Citation II";c=2;t="tjch"
        elif "560" in type_: model="Citation V";c=2;t="tjch"
        elif "650" in type_: model="Citation III";c=2;t="tjch"
        elif "680" in type_: model="Citation Sovereign";c=2;t="tjch"
        elif "750" in type_: model="Citation X";c=2;t="tjch"
        elif "850" in type_: model="Citation Columbus";c=2;t="tjch"
        
        if model is not None:
            ret["manufacturer"] = "Cessna"
            ret["model"] = model
            ret["cat_class"] = c
        else:
            return ret
    
    ## ----------------------------------------------------------------
    
    elif type_.startswith("PA"):
        type_ = type_.replace('-', '')[2:]
        
        if   type_.startswith("10"): model="";c=1;t="w"
        elif type_.startswith("11"): model="Cub Special";c=1;t="w"
        elif type_.startswith("12"): model="Super Cruiser";c=1;t="w"
        elif type_.startswith("14"): model="Family Cruiser";c=1;t="w"
        elif type_.startswith("15"): model="Vagabond";c=1;t="w"
        elif type_.startswith("16"): model="Clipper";c=1;t="w"
        elif type_.startswith("17"): model="Vagabond";c=1;t="w"
        elif type_.startswith("18"): model="Super Cub";c=1;t="w"
        elif type_.startswith("19"): model="Super Cub";c=1;t="w"
        elif type_.startswith("20"): model="Pacer";c=1;t="w"
        elif type_.startswith("21"): model="";c=1
        elif type_.startswith("22"): model="Tri-Pacer";c=1;t="w"
        elif type_.startswith("23"): model="Apache";c=2;t="hc"
        elif type_.startswith("24"): model="Comanche";c=1;t="ch"
        elif type_.startswith("25"): model="Pawnee";c=1;t="wh"
        elif type_.startswith("26"): model="";c=1;t="ch"
        elif type_.startswith("27"): model="Aztec";c=2;t="ch"
        elif type_.startswith("28R"): model="Arrow";c=1;t="c"
        elif type_.startswith("28235"): model="Dakota";c=1;t="h"
        elif type_.startswith("28161"): model="Warrior";c=1
        elif type_.startswith("28181"): model="Archer";c=1
        elif type_.startswith("28"): model="Cherokee";c=1
        elif type_.startswith("29"): model="Papoose";c=1
        elif type_.startswith("30"): model="Twin Comanche";c=2;t="c"
        elif type_.startswith("31T"): model="Cheyenne";c=2;t="cht"
        elif type_.startswith("31P"): model="Mojave";c=2;t="ch"
        elif type_.startswith("31350"): model="Chieftain";c=2;t="hc"
        elif type_.startswith("31"): model="Navajo";c=2;t="hc"
        elif type_.startswith("32R"): model="Lance";c=1;t="h"
        elif type_.startswith("32"): model="Cherokee Six";c=1;t="h"
        elif type_.startswith("33"): model="Comanche";c=1
        elif type_.startswith("34"): model="Seneca";c=2;t="hc"
        elif type_.startswith("35"): model="Pocono";c=2
        elif type_.startswith("36"): model="Pawnee Brave";c=1;t="w"
        elif type_.startswith("37"): model="Comanche";c=1
        elif type_.startswith("38"): model="Tomahawk";c=1
        elif type_.startswith("39"): model="Twin Comanche";c=2
        elif type_.startswith("40"): model="Arapaho";c=2
        elif type_.startswith("41"): model="Aztec";c=2
        elif type_.startswith("42"): model="Cheyenne";c=2;t="thc"
        elif type_.startswith("43"): model="Cheyenne";c=2;t="thc"
        elif type_.startswith("44"): model="Seminole";c=2;t="c"
        elif type_.startswith("45"): model="";c=1
        elif type_.startswith("46"): model="Malibu";c=1;t="ch"
        elif type_.startswith("47"): model="PiperJet";c=1;t="chjt"
        elif type_.startswith("48"): model="Enforcer";c=2
        elif type_.startswith("60"): model="Aerostar";c=2;t="hc"
        
        elif type_.startswith("6"): model="Sky Sedan";c=1;t="w"
        elif type_.startswith("7"): model="Skycoupe";c=1;t="w"
        elif type_.startswith("8"): model="Skycycle";c=1;t="w"
        elif type_.startswith("9"): model="";c=1;t="w"
        

        if model is not None:
            ret["manufacturer"] = "Piper"
            ret["model"] = model
            ret["cat_class"] = c
        else:
            return ret
    
    ## ----------------------------------------------------------------
    
    elif type_.startswith("BE"):
        if "16" in type_: model="";c=1
        elif "17" in type_: model="Staggerwing";c=1;t="w"
        elif "18" in type_: model="Twin Beech";c=2;t="c"
        elif "19" in type_: model="Sport";c=1
        elif "23" in type_: model="Musketeer";c=1
        elif "24" in type_: model="Sierra";c=1
        elif "34" in type_: model="Twin-Quad";c=1
        elif "33" in type_: model="Debonair";c=1;t="ch"
        elif "35" in type_: model="Bonanza";c=1;t="ch"
        elif "36" in type_: model="Bonanza";c=1;t="ch"
        elif "40" in type_: model="";c=2
        elif "50" in type_: model="";c=2
        elif "55" in type_: model="Baron";c=2;t="ch"
        elif "56" in type_: model="Baron";c=2;t="ch"
        elif "58" in type_: model="Baron";c=2;t="ch"
        elif "60" in type_: model="Duke";c=2;t="ch"
        elif "65" in type_: model="Queen Air";c=2;t="ch"
        elif "70" in type_: model="Queen Air";c=2;t="ch"
        elif "80" in type_: model="Queen Air";c=2;t="ch"
        elif "88" in type_: model="Queen Air";c=2;t="ch"
        elif "76" in type_: model="Duchess";c=2;t="c"
        elif "77" in type_: model="Skipper";c=1
        elif "90" in type_: model="King Air";c=2;t="tcph"
        elif "200" in type_: model="Super King Air";c=2;t="tcph"
        elif "300" in type_: model="Super King Air";c=2;t="tcph"
        elif "100" in type_: model="King Air";c=2;t="tchp"
        elif "95" in type_: model="Travel Air";c=2;t="c"
        elif "99" in type_: model="Airliner";c=2;t="tchp"
        elif "390" in type_: model="Premier";c=2;t="tch"
        elif "1900" in type_: model="Airliner";c=2;t="tchp"
        elif "2000" in type_: model="Starship";c=2;t="tchp"

        if model is not None:
            ret["manufacturer"] = "Beechcraft"
            ret["model"] = model
            ret["cat_class"] = c
        else:
            return ret
    
    ## ----------------------------------------------------------------
        
    elif type_.startswith("TB"):
        if "700" in type_: model="";c=1;t="tchp"
        elif "850" in type_: model="";c=1;t="tchp"
        elif "9" in type_: model="Tampico";c=1
        elif "10" in type_: model="Tobago";c=1
        elif "20" in type_: model="Trinidad";c=1
        elif "21" in type_: model="Trinidad";c=1
        
        if c is not None:
            ret["manufacturer"] = "SOCATA"
            ret["model"] = model
            ret["cat_class"] = c
        else:
            return ret
            
    ## ----------------------------------------------------------------
        
    elif type_.startswith("DA"):
        if "20" in type_ and not "C1" in type_: model="Katana";c=1
        elif "20" in type_ and "C1" in type_: model="Evolution/Eclipse";c=1
        elif "40" in type_: model="Star";c=1
        elif "42" in type_: model="Twin Star";c=2;t="c"
        
        if c is not None:
            ret["manufacturer"] = "Diamond"
            ret["model"] = model
            ret["cat_class"] = c
        else:
            return ret
    
    ## ----------------------------------------------------------------
    
    elif type_ == "SA227":
        return {"manufacturer": "Swearingen",
                "model": "Merlin/Metroliner",
                "cat_class": 2,
                "tags": "Turbine, HP, Turboprop, TR"}
                
    elif type_ == "CH2000" or type_ == "CH2T":
        return {"manufacturer": "AMD",
                "model": "Alarus",
                "cat_class": 1,
                "tags": None}
    
    elif type_ == "SR22":
        return {"manufacturer": "Cirrus",
                "model": "",
                "cat_class": 1,
                "tags": "HP, Glass"}
                
    elif type_ == "SR20":
        return {"manufacturer": "Cirrus",
                "model": "",
                "cat_class": 1,
                "tags": "Glass"}
    
    ## -----------------------------------------------------------------
        
    if not ret['manufacturer']:
        return ret     #plane not found, return None
    
    if not t:
        ret['tags'] = ""
        return ret
    
    tags = []
    if "t" in t:
        tags.append("Turbine")
        
    if "p" in t:
        tags.append("Turboprop")
        
    if "c" in t:
        tags.append("Complex")
        
    if "h" in t:
        tags.append("HP")
        
    if "j" in t:
        tags.append("Jet")

    if "w" in t:
        tags.append("Tailwheel")
    
    if "l" in t:
        tags.append("LSA")
        
    ret["tags"] = ", ".join(tags)
    
    return ret









        
