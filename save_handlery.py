import pickle
import entities
import helping_functions
import acts
from pathlib import Path

snap = ""

def the_question_of_safety():
	global snap
	while True:
		
		try:
			
			loader = ["Yes","No"]
			
			snap = input("Do you want to load a save game?\n1. Yes\n2. No\n")
			snap = int(snap)-1
			
			if loader[snap] == "Yes":
				load_and_bloat()
				snap = "Yes"
				break
			
			elif loader[snap] == "No":
				snap = "No"
				entities.active_character[0].set_deck(entities.silent_deck)
				#entities.active_character[0].add_relic({"Name":"Snecko Eye","Rarity":"Boss","Owner":"The Spire","Type":"Relic","Info":"Draw 2 additional cards each turn. Start each combat <light-cyan>Confused</light-cyan>."})
				#entities.active_character[0].add_potion({"Name": "Smoke Bomb","Rarity": "Rare","Owner":"The Spire","Type": "Potion","Info":"Escape from a non-boss combat. Receive no rewards."})
				#entities.active_character[0].add_CardToDeck({"Name": "Dagger Spray +", "Damage":6,"Upgraded": True,"Energy": 1, "Type":"Attack","Rarity":"Common","Owner":"Silent","Info":"Deal <red>6 damage</red> to ALL enemies twice."})
				break
				
		except TypeError:
			print("Type \"1\" or \"2\".")
		except Exception as e:
			print("Type \"1\" or \"2\".")
			print(e)

def save_and_rave():
	
	saveDict = {"Encounter Counter":helping_functions.encounter_counter,
				"Floor Counter":helping_functions.floor_counter,
				"Game Act":helping_functions.gameAct,
				"Game Map":helping_functions.game_map,
				"Game Map Dict":helping_functions.game_map_dict,
				"Common Card Chance":helping_functions.commonCardChance,
				"Uncommon Card Chance":helping_functions.uncommonCardChance,
				"Rare Card Chance":helping_functions.rareCardChance,
				"Potion Chance":helping_functions.generalPotionChance,
				"Remove Card Cost":helping_functions.removeCardCost,
				"List Of Enemies":entities.list_of_enemies,
				"Relics Seen":entities.relics_seen_list,
				"Active Character": entities.active_character,
				"Enemy Encounters":entities.enemyEncounters,
				"Elite Encounters":entities.eliteEncounters,
				"Boss Encounters":entities.bossEncounters,
				"Act One Events":entities.actOneEvents,
				"Universal Events":entities.universalEvents,
				"Event Monster Chance":entities.eventMonsterChance,
				"Event Treasure Chance":entities.eventTreasureChance,
				"Event Shop Chance":entities.eventShopChance
				}

	devPath = str(Path.cwd())+"/documents/slaythetext/slaythetextSave.dat"
	prodPath = str(Path.cwd())+"/slaythetextSave.dat" 

	pickle.dump(saveDict, open(prodPath,"wb"))

	
def load_and_bloat():

	devPath = str(Path.cwd())+"/documents/slaythetext/slaythetextSave.dat"
	prodPath = str(Path.cwd())+"/slaythetextSave.dat" 

	path = prodPath

	helping_functions.encounter_counter = pickle.load(open(path,"rb")).get("Encounter Counter")
	helping_functions.floor_counter = pickle.load(open(path,"rb")).get("Floor Counter")
	helping_functions.gameAct = pickle.load(open(path,"rb")).get("Game Act")
	helping_functions.game_map = pickle.load(open(path,"rb")).get("Game Map")
	helping_functions.game_map_dict = pickle.load(open(path,"rb")).get("Game Map Dict")
	helping_functions.commonCardChance = pickle.load(open(path,"rb")).get("Common Card Chance")
	helping_functions.uncommonCardChance = pickle.load(open(path,"rb")).get("Uncommon Card Chance")
	helping_functions.rareCardChance = pickle.load(open(path,"rb")).get("Rare Card Chance")
	helping_functions.generalPotionChance = pickle.load(open(path,"rb")).get("Potion Chance")
	helping_functions.removeCardCost = pickle.load(open(path,"rb")).get("Remove Card Cost")
	entities.list_of_enemies = pickle.load(open(path,"rb")).get("List Of Enemies")
	entities.relics_seen_list = pickle.load(open(path,"rb")).get("Relics Seen")
	entities.active_character = pickle.load(open(path,"rb")).get("Active Character")
	entities.enemyEncounters = pickle.load(open(path,"rb")).get("Enemy Encounters")
	entities.eliteEncounters = pickle.load(open(path,"rb")).get("Elite Encounters")
	entities.bossEncounters = pickle.load(open(path,"rb")).get("Boss Encounters")

	entities.actOneEvents = pickle.load(open(path,"rb")).get("Act One Events")
	entities.universalEvents = pickle.load(open(path,"rb")).get("Universal Events")
	entities.eventMonsterChance = pickle.load(open(path,"rb")).get("Event Monster Chance")
	entities.eventTreasureChance = pickle.load(open(path,"rb")).get("Event Treasure Chance")
	entities.eventShopChance = pickle.load(open(path,"rb")).get("Event Shop Chance")



