def loadPreset(presetName):
    global charClass
    global charBackground
    global wishDict

    if presetName == "dril":
        charClass = "Monk"
        charBackground = "Folk Hero"
        wishDict =  {
                        "Rations (1 day)":  400,
                        "Abacus":           75,
                        "Tent, two-person": 400,
                        "Candle":           360000,
                        "Barrel":           75
                    }
        return True

    if presetName == "The Jaws of Defeat":
        charClass = "wizard"
        charBackground = "criminal"
        wishDict =  {
                        "hunting trap":     999
                    }
        return True

    if presetName == "Crossbow":
        charClass = "Fighter"
        charBackground = "Criminal"
        wishDict =  {
                        "Crossbow, Hand":           1,
                        "Crossbow, Heavy":          1,
                        "Studded Leather Armor":    1,
                        "Thieves' Tools":           1,
                        "Clothes, Common":          1,
                        "Lantern, Hooded":          1,
                        "Oil (Flask)":              2,
                        "backpack":                 1,
                        "bedroll":                  1,
                        "mess kit":                 1,
                        "rations (1 day)":          5,
                        "tinderbox":                1,
                        "waterskin (full)":         1,
                        "rope, hempen (50 feet)":   1,
                        "Grappling Hook":           1,
                        "Crowbar":                  1,
                        "Hammer":                   1,
                        "Piton":                    10,
                        "Case, Crossbow Bolt":      2,
                        "Crossbow Bolts (20)":      2,
                        "Blanket":                  1,
                        "Pouch":                    1
                    }
        return True
      
    if presetName == "Crossbow2":
        charClass = "Fighter"
        charBackground = "Criminal"
        wishDict =  {
                        "Crossbow, Hand":           1,
                        "Crossbow, Light":          1,
                        "Studded Leather Armor":    1,
                        "Thieves' Tools":           1,
                        "Clothes, Common":          1,
                        "Lantern, Hooded":          1,
                        "Oil (Flask)":              2,
                        "backpack":                 1,
                        "bedroll":                  1,
                        "mess kit":                 1,
                        "rations (1 day)":          5,
                        "tinderbox":                1,
                        "waterskin (full)":         1,
                        "rope, hempen (50 feet)":   1,
                        "Grappling Hook":           1,
                        "Crowbar":                  1,
                        "Hammer":                   1,
                        "Piton":                    10,
                        "Case, Crossbow Bolt":      2,
                        "Crossbow Bolts (20)":      2,
                        "Blanket":                  1,
                        "Pouch":                    1
                    }
        return True   

          
      
    return False

def main():
    global Bank
    global myEquipment
    global wishDict
    global charClass
    global charBackground
    while True:
        Bank = 0
        myEquipment = {}
        wishDict = {}
        print("Class Options:")
        print("| Barbarian |", "Bard |", "Cleric, Knowledge, Light, Trickery |", "Cleric, Life, Nature |", "Cleric, Tempest, War |", "Druid |", "Fighter |", "Monk |", "Paladin |",
              "Ranger |", "Rogue |", "Sorcerer |", "Warlock |", "Wizard |")
        charClass = input("\nCharacter Class: ").strip()
        if loadPreset(charClass):
            
            charClass = charClass.lower()
            charBackground = charBackground.lower()
            uppers = [k for k in wishDict if k!=k.lower()]
            for key in uppers:
                wishDict[key.lower()] = wishDict[key]
                del wishDict[key]

        else:
            charClass = charClass.lower()
            while charClass not in ["barbarian", "bard", "cleric, knowledge, light, trickery", "cleric,  life, nature", "cleric, tempest, war", "druid", "fighter", "monk", "paladin",  "ranger", "rogue", "sorcerer", "warlock", "wizard", "blank"]:
                charClass = input("Character class not recognized. Try again: ").strip().lower()   
            charBackground = input("\nCharacter Background: ").strip().lower()
            while charBackground not in ["acolyte", "charlatan", "criminal", "entertainer", "entertainer, gladiator", "folk hero", "guild artisan", "hermit", "noble", "outlander", "sage", "sailor", "soldier", "urchin", "far traveler", "urban bounty hunter", "city watch", "blank"]:
                charBackground = input("Character background not recognized. Try again: ").strip().lower()
            skipflag = False
            print("\nWish List (input 'item; count' in priority order and 'end' when done):")
            while not skipflag:
                try:
                    raw = input().strip().lower()
                    entry,count = [s.strip() for s in raw.split(";")]
                    count = int(count)
                    if entry in Packs.keys():
                        for item,innerCount in Packs[entry]:
                            if item in wishDict.keys():
                                wishDict[item] += count*innerCount
                            else:
                                wishDict[item] = count*innerCount
                    elif entry in Price.keys():
                        if entry in wishDict.keys():
                            wishDict[entry] += count
                        else:
                            wishDict[entry] = count
                    else:
                        print(f"{entry} not recognized.")
                except:
                    if raw in Price.keys():
                        if raw in wishDict.keys():
                            wishDict[raw] += 1
                        else:
                            wishDict[raw] = 1
                    elif raw == "end":
                        skipflag = True
                    else:
                        print(f"{raw} not recognized.")
        print()
        Bank = 0
        myEquipment = {}
        equip()
        buystuff()
        print("\nMy Equipment:\n", *[f"{c:6.0f} of {recap(i)}\n" for i,c in myEquipment.items() if c!=0])
        print(f"Gold: {Bank:.2f}")
        print("\nMissed Items:\n", *[f"{c:6.0f} of {recap(i)}\n" for i,c in wishDict.items() if c!=0])

def startwith(smackers):
    bank(smackers)
    print(f"Started with{' '*46}{smackers:.2f}")
    return

def bank(moolah):
    global Bank
    Bank += moolah
    return

def spend(legalTender):
    global Bank
    Bank -= legalTender
    return

def addinv(item, count):
    global myEquipment
    if item in myEquipment.keys():
        myEquipment[item] += count
    else:
        myEquipment[item] = count

def value(item, count=1):
    #Returns the subjective value of *count* many *item*s based on if they appear in *wishDict*
    #Be careful, value() can change over time with *wishDict*.
    if item in wishDict.keys(): 
        if wishDict[item] < count:
            subjectiveValue = Price[item]*wishDict[item]+.5*Price[item]*(count-wishDict[item])
        else:
            subjectiveValue = Price[item]*count
    else:
        subjectiveValue = .5*Price[item]*count
    return subjectiveValue

def pickup(item, count=1):
    #Use to pick up *count* many of a single type of item.
    #If passed a pack, it will pick up every item in that pack *count* many times.
    #Do not pass item sets other than packs to this function unless you want it to pick up all of them.
    global myEquipment
    global wishDict
    if type(item) is Pack:
        for innerItem in item:
            pickup(innerItem,count*item[innerItem])
    else:
        if item in wishDict.keys() and wishDict[item]!=0:
            bank(max(0,.5*Price[item]*(count-wishDict[item])))
            addinv(item, min(count,wishDict[item]))
            print(f"Kept\t{min(count,wishDict[item]):.0f}\t{recap(item):30}{'...' if len(item)>30 else ''}")
            wishDict[item] = max(0,wishDict[item]-count)
        elif Price[item]==0:
            addinv(item, count)
            print(f"Kept\t{count:.0f}\t{recap(item):.30}{'...' if len(item)>30 else ''}")
        else:
            bank(.5*count*Price[item])
            print(f"Sold\t{count:.0f}\t{recap(item):.30}{'...' if len(item)>30 else ''}{' '*(33-len(item))}for\t{.5*count*Price[item]:7.2f}")
    return

def choose(*items, itemset=None):
    #Input like so: choose("Crossbow",1,"Short Sword",2,"Crossbow Bolts (20)",1)
    #Where the numbers are the count of the preceding item.
    #Alternatively input like so: choose(itemset=Martial)
    #It will choose one from the given item set.
    if itemset is not None:
        passlist = []
        for item in itemset:
            passlist += [item,1]
        choose(*passlist) 
    else:
        global wishDict
        bestpick = None
        for option in [(items[i],items[i+1]) for i in range(len(items)) if i%2==0]:
            if bestpick is None or value(*bestpick) < value(*option):
                bestpick = option
        pickup(*bestpick)
    return

def chooseAB(*groups, **namedGroups):
    #chooseAB(group1=["item1",count1,Pack,count2], group2=["item3",count3,ItemSet,count4])
    #will pick up either group1 or group2 based on which is more valuable.
    #It will pick up entire packs *count* many times, but only *count* many items from am item set (eg Martial)
    #Can choose between arbitrarily many groups of arbitrary size.
    global wishDict
    bestGroup = None
    for group in list(groups) + [g for name,g in namedGroups.items()]:
        groupVal = 0
        for item,count in [(group[i],group[i+1]) for i in range(len(group)) if i%2==0]:
            if type(item) is dict:
                for i in range(count):
                    best = None
                    for innerItem in item:
                        if best is None or value(innerItem) > value(best):
                            best = innerItem
                    groupVal += value(best)
            elif type(item) is Pack:
                for i in range(count):
                    for innerItem,innerCount in item.items():
                        groupVal += value(innerItem,innerCount)
            else:
                groupVal += value(item,count)
        if bestGroup is None or bestGroup[1] < groupVal:
            bestGroup = (group,groupVal)
    for item,count in [(bestGroup[0][i],bestGroup[0][i+1]) for i in range(len(bestGroup[0])) if i%2==0]:
        if type(item) is dict:
            for i in range(count):
                chooseAB(*[[innerItem,1] for innerItem in item.keys()])
        else:
            pickup(item,count)
    return

def buystuff():
    for necessity in [item for item in wishDict if item in {**FocusDruidic, **FocusArcane, **FocusHolySymbol, **Instruments} or item=="staff"]:
        spend(Price[necessity])
        addinv(necessity, 1)
        wishDict[necessity] -= 1
        print(f"Bought\t{1}\t{recap(necessity):.30}{'...' if len(necessity)>30 else ''}{' '*(33-len(necessity))}for\t{-Price[necessity]:7.2f}")
    for item,count in wishDict.items():
        if Price[item]!=0:
            buyCount = min(count,Bank//Price[item])
            spend(Price[item]*buyCount)
            addinv(item, buyCount)
            wishDict[item] -= buyCount
            if buyCount!=0:
                print(f"Bought\t{buyCount:.0f}\t{recap(item):.30}{'...' if len(item)>30 else ''}{' '*(33-len(item))}for\t{-Price[item]*buyCount:7.2f}")

SimpleMelee =       {"club":0.1, "dagger":2, "greatclub":0.2, "handaxe":5, "javelin":0.5,
                     "light hammer":2, "mace":5, "quarterstaff":0.2, "sickle":1, "spear":1}

SimpleRanged =      {"crossbow, light":25, "dart":0.05, "shortbow":25, "sling":0.1}

MartialMelee =      {"battleaxe":10, "flail":10, "glaive":20, "greataxe":30, "greatsword":50,
                     "halberd":20, "lance":10, "longsword":15, "maul":10, "morningstar":15, "pike":5,
                     "rapier":25, "scimitar":25, "shortsword":10, "trident":5, "war pick":5, "warhammer":15, "whip":2}

MartialRanged =     {"blowgun":10, "crossbow, hand":75, "crossbow, heavy":50, "longbow":50, "net":1}

ArmorLight =        {"padded armor":5, "leather armor":10, "studded leather armor":45}

ArmorMedium =       {"hide armor":10, "chain shirt":50, "scale mail":50, "breastplate":400, "half plate":750}

ArmorHeavy =        {"ring mail":30, "chain mail":75, "splint armor":200, "full plate":1500}

ArmorShield =       {"shield":10}

FocusDruidic =      {"sprig of mistletoe":1, "totem":1, "wooden staff":5, "yew wand":10}

FocusArcane =       {"crystal":10, "orb":20, "rod":10, "staff":5, "wand":10}

FocusHolySymbol =   {"amulet":5, "emblem":5, "reliquary":5}

StuffReal =         {"abacus":2, "acid (vial)":25, "alchemist's fire (flask)":50, "arrows (20)":1,"blowgun needles (50)":1,
                     "crossbow bolts (20)":1, "sling bullets (20)":0.04, "antitoxin (vial)":50, "backpack":2,
                     "ball bearings (bag of 1000)":1, "barrel":2, "basket":0.4, "bedroll":1, "bell":1, "blanket":0.5,
                     "block and tackle":1, "book":25, "bottle, glass":2, "bucket":0.05, "caltrops (bag of 20)":1,
                     "candle":0.01, "case, crossbow bolt":1, "case, map or scroll":1, "chain (10 feet)":5,
                     "chalk (1 piece)":0.01, "chest":5, "climber's kit":25, "clothes, common":0.5, "clothes, costume":5,
                     "clothes, fine":15, "clothes, traveler":2, "component pouch":25, "crowbar":2, "fishing tackle":1,
                     "flask":0.02, "tankard":0.02, "grappling hook":2, "hammer":1, "hammer, sledge":2, "healer's kit":5,
                     "holy water (flask)":25, "hourglass":25, "hunting trap":5, "ink (1 ounce bottle)":10, "ink pen":0.02,
                     "jug":0.02, "pitcher":0.02, "ladder (10-foot)":0.1, "lamp":0.5, "lantern, bullseye":10,
                     "lantern, hooded":5, "lock":10, "magnifying glass":100, "manacles":2, "mess kit":0.2, "mirror, steel":5,
                     "oil (flask)":0.1, "paper (1 sheet)":0.2,"parchment (1 sheet)":0.1, "perfume (vial)":5,
                     "pick, miner's":2, "piton":0.05, "poison, basic (vial)":100, "pole (10-foot)":0.05, "pot, iron":2,
                     "potion of healing":50, "pouch":0.5, "quiver":1, "ram, portable":4, "rations (1 day)":0.5, "robes":1,
                     "rope, hempen (50 feet)":1, "rope, silk (50 feet)":10, "sack":0.01, "scale, merchant's":5,
                     "sealing wax":0.5, "shovel":2, "signal whistle":0.05, "signet ring":5, "soap":0.02, "spellbook":50,
                     "spikes, iron (10)":1, "spyglass":1000, "tent, two-person":2, "tinderbox":0.5, "torch":0.01, "vial":1,
                     "waterskin (full)":0.2, "whetstone":0.01}

StuffFake =         {"book, prayer":25, "incense, stick":0, "bottle of colored liquid":0, "weighted dice":0.1,
                     "marked cards":0.5, "fake duke's signet ring":5, "string (10 feet)":0, "alms box":0, "incense, block":0,
                     "censer":0, "vestments":0, "little bag of sand":0, "knife, small":0, "book, lore":25, "love letter":0,
                     "lock of hair":0, "trinket":0, "guild letter of introduction":0, "purse":0.5, "scroll of pedigree":0,
                     "trophy, animal":0, "trophy, enemy":0, "letter from a dead colleague posing a question you have not yet been able to answer":0,
                     "insignia of rank":0, "map, home city":0, "pet, mouse":0, "a small piece of jewelry in the style of your homeland's craftsmanship":10,
-                    "poorly wrought maps from your homeland that depict where you are in Faerun":0, "clothes, uniform":0}

Instruments =       {"bagpipes":30, "drum":6, "dulcimer":25, "flute":2, "lute":35, "lyre":30, "horn":3, "pan flute":12,
                     "shawm":2, "viol":30}    

Games =             {"dice set":0.1, "dragonchess set":1, "playing card set":0.5, "three-dragon ante set":1,}

ToolsArtisan =      {"alchemist's supplies":50, "brewer's supplies":20, "calligrapher's supplies":10, "carpenter's tools":8,
                     "cartographer's tools":15, "cobbler's tools":5, "cook's utensils":1, "glassblower's tools":30,
                     "jeweler's tools":25, "leatherworker's tools":5, "mason's tools":10, "painter's supplies":10,
                     "potter's tools":10, "smith's tools":20, "tinker's tools":50, "weaver's tools":1, "woodcarver's tools":1}

ToolsOther =        {"navigator's tools":25, "poisoner's kit":50, "thieves' tools":25, "herbalism kit":5, "disguise kit":25,
                     "forgery kit":15}

class Pack(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
BurglarPack =       Pack({"backpack":1, "ball bearings (bag of 1000)":1, "string (10 feet)":1, "bell":1, "candle":5, "crowbar":1, "hammer":1,
                          "piton":10, "lantern, hooded":1, "oil (flask)":2, "rations (1 day)":5, "tinderbox":1, "waterskin (full)":1,
                          "rope, hempen (50 feet)":1})

DiplotmatPack =     Pack({"chest":1, "case, map or scroll":2, "clothes, fine":1, "ink (1 ounce bottle)":1, "ink pen":1, "lamp":1, "oil (flask)":2,
                          "paper (1 sheet)":5, "perfume (vial)":1, "sealing wax":1, "soap":1})

DungeoneerPack =    Pack({"backpack":1, "crowbar":1, "hammer":1, "piton":10, "torch":10, "rations (1 day)":10, "tinderbox":1, "waterskin (full)":1,
                          "rope, hempen (50 feet)":1})

EntertainerPack =   Pack({"backpack":1, "bedroll":1, "clothes, costume":2, "candle":5, "rations (1 day)":5, "waterskin (full)":1, "disguise kit":1})

ExplorerPack =      Pack({"backpack":1, "bedroll":1, "mess kit":1, "torch":10, "rations (1 day)":10, "tinderbox":1, "waterskin (full)":1,
                          "rope, hempen (50 feet)":1})

PriestPack =        Pack({"backpack":1, "blanket":1, "candle":10, "tinderbox":1, "alms box":1, "incense, block":2, "censer":1, "vestments":1,
                          "rations (1 day)":2, "waterskin (full)":1})

ScholarPack =       Pack({"backpack":1, "book, lore":1, "ink (1 ounce bottle)":1, "ink pen":1, "parchment (1 sheet)":10, "little bag of sand":1,
                          "knife, small":1})

Packs =     {"burglar's pack":BurglarPack, "diplomat's pack":DiplotmatPack, "dungeoneer's pack":DungeoneerPack, "entertainer's pack":EntertainerPack,
             "explorer's pack":ExplorerPack, "priest's pack":PriestPack, "scholar's pack":ScholarPack}

Simple =    {**SimpleMelee, **SimpleRanged}
Melee =     {**SimpleMelee, **MartialMelee}
Ranged =    {**SimpleRanged, **MartialRanged}
Martial =   {**MartialMelee, **MartialRanged}

Price =     {**SimpleMelee, **SimpleRanged, **MartialMelee, **MartialRanged, **ArmorLight, **ArmorMedium, **ArmorHeavy, **ArmorShield,
             **FocusDruidic, **FocusArcane, **FocusHolySymbol, **StuffReal, **StuffFake, **Instruments, **Games, **ToolsArtisan, **ToolsOther}
        
def equip():

    #BACKGROUNDS
    print(f"    -{recap(charBackground)} Items-")
    
    if charBackground == "acolyte":
        startwith(15)
        pickup("book, prayer", 1)
        pickup("incense, stick", 5)
        pickup("pouch", 1)
        pickup("vestments", 1)
        pickup("clothes, common", 1)
        choose(itemset=FocusHolySymbol)

    elif charBackground == "charlatan":
        startwith(15)         
        pickup("clothes, fine", 1)
        pickup("disguise kit", 1)
        pickup("pouch", 1)
        choose("bottle of colored liquid", 10, "weighted dice", 1,"marked cards", 1, "fake duke's signet ring", 1)

    elif charBackground == "criminal":
        startwith(15)
        pickup("crowbar", 1)
        pickup("clothes, common", 1)
        pickup("pouch", 1)

    elif charBackground == "entertainer":
        startwith(15)
        pickup("pouch", 1)
        pickup("clothes, costume", 1)
        choose("love letter",1, "lock of hair",1, "trinket",1)
        choose(itemset=Instruments)

    elif charBackground == "entertainer, gladiator":
        startwith(15)
        pickup("pouch", 1)
        pickup("clothes, costume", 1)
        choose("love letter",1, "lock of hair",1, "trinket",1)
        choose("club", 1, "dagger", 1, "greatclub", 1, "handaxe", 1, "javelin", 1, "light hammer", 1, "mace", 1, "quarterstaff", 1,
               "sickle", 1, "spear", 1, "dart", 1, "sling", 1, "pike", 1, "trident", 1, "war pick", 1, "whip", 1, "net", 1)

    elif charBackground == "folk hero":
        startwith(10)
        pickup("pouch", 1)
        pickup("shovel", 1)
        pickup("pot, iron", 1)
        pickup("clothes, common", 1)
        choose(itemset=ToolsArtisan)

    elif charBackground == "guild artisan":         
        startwith(15)
        pickup("pouch", 1)
        pickup("clothes, traveler", 1)
        pickup("guild letter of introduction", 1)
        choose(itemset=ToolsArtisan)

    elif charBackground == "hermit":
        startwith(5)
        pickup("pouch", 1)
        pickup("case, map or scroll", 1)
        pickup("blanket", 1)
        pickup("clothes, common", 1)
        pickup("herbalism kit", 1)

    elif charBackground == "noble":
        startwith(25)
        pickup("purse", 1)
        pickup("scroll of pedigree", 1)
        pickup("clothes, fine", 1)
        pickup("signet ring", 1)

    elif charBackground == "outlander":
        startwith(10)
        pickup("pouch", 1)
        pickup("staff", 1)
        pickup("hunting trap", 1)
        pickup("trophy, animal", 1)
        pickup("clothes, traveler", 1)

    elif charBackground == "sage":
        startwith(10)
        pickup("pouch", 1)
        pickup("ink (1 ounce bottle)", 1)
        pickup("ink pen", 1)
        pickup("clothes, common", 1)
        pickup("letter from a dead colleague posing a question you have not yet been able to answer", 1)

    elif charBackground == "sailor":
        startwith(10)
        pickup("pouch", 1)
        pickup("club", 1)
        pickup("rope, silk (50 feet)", 1)
        pickup("clothes, common", 1)
        pickup("trinket", 1)

    elif charBackground == "soldier":
        startwith(10)
        pickup("pouch", 1)
        pickup("insignia of rank", 1)
        pickup("trophy, enemy", 1)
        pickup("clothes, common", 1)
        choose("dice set", 1, "playing card set", 1)

    elif charBackground == "urchin":
        startwith(15)
        pickup("pouch", 1)
        pickup("knife, small", 1)
        pickup("map, home city", 1)
        pickup("pet, mouse", 1)
        pickup("trinket", 1)
        pickup("clothes, common", 1)
    
    #SCAG
    elif charBackground == "city watch":
        startwith(10)
        pickup("pouch", 1)
        pickup("manacles", 1)
        pickup("clothes, uniform", 1)
        pickup("horn", 1)

    elif charBackground == "far traveler":
        startwith(5)
        pickup("pouch", 1)
        pickup("clothes, traveler", 1)
        pickup("poorly wrought maps from your homeland that depict where you are in Faerun", 1)
        pickup("a small piece of jewelry in the style of your homeland's craftsmanship", 1)
        chooseAB(a=[Instruments,1], b=[Games,1])

    elif charBackground == "urban bounty hunter":
        startwith(20)
        pickup("pouch", 1)
        pickup("clothes, common", 1)

    elif charBackground == "blank":
        #For testing
        pass
      
    #CLASSES
    print(f"    -{recap(charClass)} Items-")
    
    if charClass == "barbarian":
        chooseAB(a=["greataxe",1], b=[MartialMelee,1])
        chooseAB(a=["handaxe", 2], b=[Simple,1])             
        pickup("javelin", 4)
        pickup(ExplorerPack, 1)

    elif charClass == "bard":
        if not any([instrument in wishDict for instrument in Instruments]):
            wishDict["shawm"] = 1
        chooseAB(a=["rapier",1], b=["longsword",1], c=[Simple,1])             
        chooseAB(a=[DiplotmatPack,1], b=[EntertainerPack,1])         
        choose(itemset=Instruments)
        pickup("leather armor", 1)
        pickup("dagger", 1)

    elif charClass == "cleric, knowledge, light, trickery":
        if not any([focus in wishDict for focus in FocusHolySymbol]):
            wishDict["reliquary"] = 1
        pickup("mace", 1)
        choose("scale mail", 1, "leather armor", 1)
        chooseAB(a=["crossbow, light",1, "crossbow bolts (20)",1, "case, crossbow bolt",1], b=[Simple,1])
        chooseAB(a=[preistpack,1], b=[ExplorerPack,1])
        pickup("shield", 1)
        choose(itemset=FocusHolySymbol)

    elif charClass == "cleric, life, nature":
        if not any([focus in wishDict for focus in FocusHolySymbol]):
            wishDict["reliquary"] = 1
        pickup("mace", 1)
        chooseAB(a=["scale mail",1], b=["leather armor",1], c=["chain mail",1])
        chooseAB(a=["crossbow, light",1, "crossbow bolts (20)",1, "case, crossbow bolt",1], b=[Simple,1])
        chooseAB(a=[preistpack,1], b=[ExplorerPack,1])
        pickup("shield", 1)
        choose(itemset=FocusHolySymbol)

    elif charClass == "cleric, tempest, war":
        if not any([focus in wishDict for focus in FocusHolySymbol]):
            wishDict["reliquary"] = 1
        choose("mace", 1, "warhammer", 1)
        chooseAB(a=["scale mail",1], b=["leather armor",1], c=["chain mail",1])
        chooseAB(a=["crossbow, light",1, "crossbow bolts (20)",1, "case, crossbow bolt",1], b=[Simple,1])
        chooseAB(a=[preistpack,1], b=[ExplorerPack,1])
        pickup("shield", 1)
        choose(itemset=FocusHolySymbol)

    elif charClass == "druid":
        if not any([focus in wishDict for focus in FocusDruidic]):
            wishDict["sprig of mistletoe"] = 1
        chooseAB(a=["shield",1], b=[Simple,1])
        chooseAB(a=["scimitar",1], b=[SimpleMelee,1])
        pickup("leather armor", 1)
        pickup(ExplorerPack, 1)
        choose(itemset=FocusDruidic)

    elif charClass == "fighter":
        chooseAB(a=["chain mail",1], b=["leather armor",1, "longbow",1, "arrows (20)",1, "quiver",1])
        chooseAB(a=[Martial,1, "shield",1], b=[Martial,2])
        chooseAB(a=["crossbow, light",1, "crossbow bolts (20)",1, "case, crossbow bolt",1], b=["handaxe",2])
        chooseAB(a=[DungeoneerPack,1], b=[ExplorerPack,1])         

    elif charClass == "monk":
        chooseAB(a=["shortsword",1], b=[Simple,1])
        chooseAB(a=[DungeoneerPack,1], b=[ExplorerPack,1])
        pickup("dart", 10)

    elif charClass == "paladin":
        if not any([focus in wishDict for focus in FocusHolySymbol]):
            wishDict["reliquary"] = 1
        chooseAB(a=[Martial,1, "shield",1], b=[Martial,2])
        chooseAB(a=["javelin",5], b=[SimpleMelee,1])
        chooseAB(a=[PriestPack,1], b=[ExplorerPack,1])
        pickup("chain mail", 1)
        choose(itemset=FocusHolySymbol)

    elif charClass == "ranger":
        choose("scale mail", 1, "leather armor", 1)
        chooseAB(a=["shortsword",2], b=[SimpleMelee,2])         
        chooseAB(a=[DungeoneerPack,1], b=[ExplorerPack,1])
        pickup("longbow", 1)
        pickup("arrows (20)", 1)
        pickup("quiver", 1)

    elif charClass == "rogue":
        choose("rapier", 1, "shortsword", 1)
        chooseAB(a=["shortbow",1, "arrows (20)",1, "quiver",1], b=["shortsword",1])
        chooseAB(a=[DungeoneerPack,1], b=[BurglarPack,1])
        pickup("leather armor", 1)
        pickup("dagger", 2)
        pickup("thieves' tools", 1)

    elif charClass == "sorcerer":
        if not any([focus in wishDict for focus in FocusArcane]):
            wishDict["staff"] = 1
        chooseAB(a=["crossbow, light",1, "crossbow bolts (20)",1, "case, crossbow bolt",1], b=[Simple,1])
        chooseAB(a=["component pouch",1], b=[FocusArcane,1])
        chooseAB(a=[DungeoneerPack,1], b=[ExplorerPack,1])
        pickup("dagger", 2)

    elif charClass == "warlock":
        if not any([focus in wishDict for focus in FocusArcane]):
            wishDict["staff"] = 1
        chooseAB(a=["crossbow, light",1, "crossbow bolts (20)",1, "case, crossbow bolt",1], b=[Simple,1])
        chooseAB(a=["component pouch",1], b=[FocusArcane,1])
        chooseAB(a=[ScholarPack,1], b=[ExplorerPack,1])
        pickup("dagger", 2)
        pickup("leather armor", 1)
        choose(itemset=Simple)

    elif charClass == "wizard":
        if "spellbook" not in wishDict:
            wishDict["spellbook"] = 1
        if not any([focus in wishDict for focus in FocusArcane]):
            wishDict["staff"] = 1
        choose("quarterstaff", 1, "dagger", 1)
        chooseAB(a=["component pouch",1], b=[FocusArcane,1])
        chooseAB(a=[ScholarPack,1], b=[ExplorerPack,1])
        pickup("spellbook", 1)
    
    elif charClass == "blank":
        #For testing
        pass

def recap(stringyboi):
    chad = stringyboi[0].capitalize()
    for i in range(len(stringyboi)-1):
        if not (stringyboi[i].isalpha() or stringyboi[i]=="'") and stringyboi[i+1].isalpha():
            chad += stringyboi[i+1].capitalize()
        else:
            chad += stringyboi[i+1]
    return chad
  
def testing(c, b, w):
    global Bank
    global myEquipment
    global wishDict
    global charClass
    global charBackground
    
    Bank = 0
    myEquipment = {}
    wishDict = w
    charClass = c
    charBackground = b
    
    print(recap(charClass + " " + charBackground))
    print("\nWant:\n", *[f"{c:6.0f} of {recap(i)}\n" for i,c in wishDict.items() if c!=0])
    
    equip()
    buystuff()

    print("\nMy Equipment:\n", *[f"{c:6.0f} of {recap(i)}\n" for i,c in myEquipment.items() if c!=0])
    print(f"\nGold: {Bank:.2f}")
    print("\nMissed Items:\n", *[f"{c:6.0f} of {recap(i)}\n" for i,c in wishDict.items() if c!=0])

if __name__=="__main__":
    main()
       