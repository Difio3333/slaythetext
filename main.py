#import random as rd
import logging
logging.basicConfig(level = logging.DEBUG, filename = "slaythetext.log",filemode="w",format = "%(asctime)s - %(levelname)s - %(message)s")

import random as rd
import entities
import helping_functions
import colorama
import sys
import time
import save_handlery
from ansimarkup import parse, ansiprint

colorama.init()


#KNOWN ISSUES:

#events are not following any rules besides acts.
#no tutorial
#no proper error logging yet.
#Skipping Black Star second artifact makes it inaccessible.
#you can also skip green key forever I think 
#just saw 4 shops in a row.
# Need to improve visuals of watch discard and watch exhaust pile
#probably the shopitems that are replenished by courier need to be upgraded based on the act and affected by the eggs too.
#fixed some stuff with eventshops not properly being handled as shops in some regards.
#fix 4748def showHand Make attack and block numbers respect dexterity and strenght and weakness and frail and remove block cards from the deck. also handle that cards that attack and block like dash

def main():
	try:
		ansiprint("Slay the Spire is a registered trademark by Mega Crit, LLC")
		ansiprint("Please consider supporting the Developers by purchasing Slay the Spire on Steam/Gog/Epic etc.\n\n")
		ansiprint("This game requires a base understanding of Slay the Spire.")
		ansiprint("If you don't know what a <blue>Card</blue>, <light-red>Relic</light-red> or <c>Potion</c> does just type out its name wherever you are and you should get a short explanation of it.")
		ansiprint("In 99 out of 100 cases you can navigate the game by typing in the corresponding numbers of the options presented to you.")
		ansiprint("You can Save only during battles by typing \"Save\" and hitting \"Enter\" afterwards.\n\n")
		
		save_handlery.the_question_of_safety()
		rd.seed(helping_functions.seed)
		
		running = True
		while running == True and helping_functions.gameAct < 5:
			if save_handlery.saveDecision == "Yes":
				save_handlery.saveDecision = "No"
				
			else:
				entities.active_character[0].resetChar()
				entities.active_character[0].set_drawPile()
				entities.update_encounter()
			
			while len(entities.list_of_enemies) > 0:

				helping_functions.turn_counter = helping_functions.count_up(helping_functions.turn_counter)
				entities.active_character[0].turn(helping_functions.turn_counter)
				
				i = 0
				while i < len(entities.list_of_enemies):
					enemyDeadCheck = len(entities.list_of_enemies)
					entities.list_of_enemies[i].turn()
					if enemyDeadCheck <= len(entities.list_of_enemies):
						i+=1
				
				if entities.active_character[0].alive == False:
					break

				entities.check_if_enemy_dead()
			
			if entities.active_character[0].alive == True:
				helping_functions.afterBattleScreen()
			else:
				running = False

		if helping_functions.gameAct == 5:
			print("You won and beat the Heart!!")
		elif helping_functions.gameAct == 4:
			print("You won!")
		else:
			print("You have lost!")

		input("Thanks so much for playing!")

	except Exception as e:
		logging.error(f"Sorry the game crashed. You can find the crashlog in the same location where your game is located. It would be really nice if you could copy paste your game text to a txt. file and send it to slaythetext@gmail.com. Thanks and sorry for the inconveniences. Additonally there should be a slaythetext.log file in the same directory where you launched this game from. Please send that as well. \n Here is the actual Error:\n{e}",exc_info=True)
		import acts
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
		for key in saveDict:
			if key == "List Of Enemies":
				logging.debug(f"\n\n Active Enemies:\n")
				for enemy in saveDict[key]:
					for item in enemy:		
						logging.debug(f"{item}")
					logging.debug(f"\n\n Active Enemy End:\n")
			
			elif key == "Active Character":
				logging.debug("\n\nPlayer Character\n")
				for item in entities.active_character[0]:
					logging.debug(item)
				logging.debug("\n\nPlayer Character End\n")
			else:
				logging.debug(f"{key}:{saveDict[key]}")
			
		
		
		input("Sorry the game crashed. You can find the crashlog in the same location where your game is located.\nIt would be really nice if you could copy paste your game text to a txt. file and send it to slaythetext@gmail.com. Thanks and sorry for the inconveniences. Additonally there should be a slaythetext.log file in the same directory where you launched this game from. Please send that as well.")




if __name__ == "__main__":
	main()


