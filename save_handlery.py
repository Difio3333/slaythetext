import pickle
import entities
import helping_functions
import acts
from pathlib import Path

saveDecision = ""

def the_question_of_safety():
	global saveDecision
	while True:
		
		try:
			prodPath = str(Path.cwd())+"/slaythetextSave.dat"
			devPath = str(Path.cwd())+"/documents/slaythetext/slaythetextSave.dat"
			f = open(prodPath)
			f.close()
		except FileNotFoundError:
			print("No savefile detected in "+prodPath+".\n\n")

			entities.choose_character()
			entities.active_character[0].set_deck()
			entities.active_character[0].add_relic({"Name":"The Courier","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"The <yellow>merchant</yellow> no longer runs out of Cards, <light-red>Relics</light-red>, or <c>Potions</c> and his prices are reduced by 20%."})			#entities.active_character[0].add_potion({"Name": "Attack Potion","Potion Yield": 1, "Rarity": "Common","Owner":"The Spire","Type": "Potion","Info":"Choose 1 of <red>3 random Attack</red> Cards to add into your hand. It costs <yellow>0 Energy</yellow> this turn."})
			#entities.active_character[0].add_CardToDeck({"Name":"Brutality","Draw":1,"Selfhurt":1,"Vulnerable":2,"Energy":0,"Type":"Power","Rarity":"Rare","Owner":"Ironclad","Info":"At the start of your turn, lose <red>1 HP</red> and draw 1 Card."})
			break

		try:
			
			loader = ["Yes","No"]
			
			saveDecision = input("Do you want to load your save game?\n1. Yes\n2. No\n")
			saveDecision = int(saveDecision)-1
			
			if loader[saveDecision] == "Yes":
				load_and_bloat()
				saveDecision = "Yes"
				break
			
			elif loader[saveDecision] == "No":
				saveDecision = "No"
				entities.choose_character()
				entities.active_character[0].set_deck()
				entities.active_character[0].add_relic({"Name":"The Courier","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"The <yellow>merchant</yellow> no longer runs out of Cards, <light-red>Relics</light-red>, or <c>Potions</c> and his prices are reduced by 20%."})
				#entities.active_character[0].add_potion({"Name": "Attack Potion","Potion Yield": 1, "Rarity": "Common","Owner":"The Spire","Type": "Potion","Info":"Choose 1 of <red>3 random Attack</red> Cards to add into your hand. It costs <yellow>0 Energy</yellow> this turn."})
				#entities.active_character[0].add_CardToDeck({"Name":"Brutality","Draw":1,"Selfhurt":1,"Vulnerable":2,"Energy":0,"Type":"Power","Rarity":"Rare","Owner":"Ironclad","Info":"At the start of your turn, lose <red>1 HP</red> and draw 1 Card."})
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
				"Test Act": acts.testAct,
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
				"Event Shop Chance":entities.eventShopChance,
				"Beat First Act 3 Boss": helping_functions.actThreeFirstBossBeaten
				}

	devPath = str(Path.cwd())+"/documents/slaythetext/slaythetextSave.dat"
	prodPath = str(Path.cwd())+"/slaythetextSave.dat" 

	pickle.dump(saveDict, open(prodPath,"wb"))

	
def load_and_bloat():

	devPath = str(Path.cwd())+"/documents/slaythetext/slaythetextSave.dat"
	prodPath = str(Path.cwd())+"/slaythetextSave.dat" 

	path = prodPath

	acts.testAct = pickle.load(open(path,"rb")).get("Test Act")
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
	helping_functions.actThreeFirstBossBeaten= pickle.load(open(path,"rb")).get("Beat First Act 3 Boss")
	
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



