from climber import Char
from enemy import Enemy
import random as rd
import acts
import helping_functions
from ansimarkup import parse, ansiprint
import math
import time
import save_handlery
import copy

list_of_enemies = []
relics_seen_list = []
silent = Char("Silent",66,deck = [],gold = 99,relics=[{"Name":"Ring of the Snake","Rarity":"Starter","Owner":"Silent","Type":"Relic"}])
active_character = [silent]

eventMonsterChance = 0.1
eventTreasureChance = 0.02
eventShopChance = 0.03      


def check_if_character_dead():
    global active_character
    for character in active_character:
        if character.alive == False:
            for potion in character.potionBag:
                if potion.get("Name") == "Fairy in a Bottle":
                    character.resurrect("Fairy in a Bottle")
            for relic in character.relics:
                if relic.get("Name") == "Lizard Tale":
                    if relic.get("Counter") > 0:
                        relic["Counter"] = 0
                        character.resurrect("Lizard Tale")                        
                    else:
                        pass
            
            if character.alive == False:
                active_character.pop(0)

def check_if_enemy_dead():
	global list_of_enemies
	try:
		i = 0
		for enemy in list_of_enemies:
			if enemy.alive == False:
				if enemy.stolenGold > 0:
					ansiprint(active_character[0].displayName,"killed an enemy that had stolen Gold.")
					active_character[0].set_gold(enemy.stolenGold)
				
				if len(enemy.stolenCard) > 0:
					for card in enemy.stolenCard:
						active_character[0].add_CardToHand(card)

				for relic in active_character[0].relics:
					if relic.get("Name") == "Gremlin Horn":
						active_character[0].draw(1)
						active_character[0].gainEnergy(1)
						ansiprint("You drew 1 card and received <yellow>1 Energy</yellow> because of <light-red>Gremlin Horn</light-red>!")
					elif relic.get("Name") == "The Specimen":
						if enemy.poison > 0:
							if len(list_of_enemies) > 1:
								print("Snipper.")
								snap = rd.randint(0,len(list_of_enemies)-1)
								while snap == i:
									snap = rd.randint(0,len(list_of_enemies)-1)

								list_of_enemies[snap].set_poison(enemy.poison)

				ansiprint("The",list_of_enemies[i].name,"has been defeated.")
				list_of_enemies.pop(i)
				
				if enemy.leader == True and len(list_of_enemies) >= 1:
					list_of_enemies = []
					ansiprint("All other Minions are fleeing!")

			else:
				i += 1
	except Exception as e:
		print(e,"Issue in check_if_enemy_dead entities.")

def enemy_runs_away():
	i = 0
	for enemy in list_of_enemies:
		if enemy.runaway == True:
			list_of_enemies.pop(i)
			i += 1
		else:
			i += 1

def spawn_enemies(theEnemies:list):

	for enemy in theEnemies:
		list_of_enemies.append(enemy)


def fill_enemy_list():
    if helping_functions.gameAct == 1:
        encounterList = []
        checklist = [1,2,3,4]
        i = 0
        while i < 3:
            snap = checklist.pop(rd.randint(0,len(checklist) - 1))
            #snap = 4
            miniList = []
            if snap == 1:
                enemy = "Cultist"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

            elif snap == 2:                                             
                enemy = "Jaw Worm"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

            elif snap == 3:
                lousecheck = rd.randint(0,2)
                if lousecheck == 0:
                    
                    enemy = "Green Louse"
                    miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                    miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                    
                elif lousecheck == 1:
                    
                    enemy = "Red Louse"
                    miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                    miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

                elif lousecheck == 2:
                    enemy = "Red Louse"
                    miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                    enemy = "Green Louse"
                    miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

            elif snap == 4:
                
                if rd.randint(0,1) == 0:
                    
                    enemy = "Medium Acid Slime"
                    miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                    enemy = "Small Spike Slime"
                    miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

                else:
                    enemy = "Small Acid Slime"
                    miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                    enemy = "Medium Spike Slime"
                    miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

            encounterList.append(miniList)
            i += 1

        checklist = list(helping_functions.nchoices_with_restrictions([0.0625,0.125,0.0625,0.125,0.0625,0.125,0.125,0.09375,0.09375,0.125],{0:1,1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:1},k=15))
        
        for setup in checklist:
            miniList = []

            if setup == 0:
                gremlins = ["Mad Gremlin","Mad Gremlin","Sneaky Gremlin","Sneaky Gremlin","Fat Gremlin","Fat Gremlin","Gremlin Wizard","Shield Gremlin"]
                
                gremls = 0
                while gremls < 4:
                    enemy = gremlins.pop(rd.randint(0,len(gremlins) - 1))
                    miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                    gremls += 1
            
            elif setup == 1:
                if rd.randint(0,1) == 0:
                    enemy = "Large Acid Slime"
                    miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                else:
                    enemy = "Large Spike Slime"
                    miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

            elif setup == 2:
                enemy = "Small Acid Slime"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

                enemy = "Small Spike Slime"

                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
           
            elif setup == 3:
                enemy = "Red Slaver"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

            elif setup == 4:
                enemy = "Blue Slaver"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
            
            elif setup == 5:
                i = 0
                while i < 3:
                    if rd.randint(0,1) == 0:
                        enemy = "Red Louse"
                    else:
                        enemy = "Green Louse"
                
                    miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                    i += 1

            elif setup == 6:
                
                enemy = "Fungi Beast"
                
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

            elif setup == 7:
            
                if rd.randint(0,1) == 0:
                    
                    enemy = rd.choices(["Red Louse","Green Louse"])[0]
                    
                else:
                    enemy = rd.choices(["Medium Acid Slime","Medium Spike Slime"])[0]
        

                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

                kindOfThug = rd.randint(0,2)

                if kindOfThug == 0:
                    enemy = "Looter"

                elif kindOfThug == 1:
                    enemy = "Cultist"
                   
                elif kindOfThug == 2:
                    enemy = rd.choices(["Blue Slaver","Red Slaver"])[0]
                
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
               
            elif setup == 8:
            
                enemy = rd.choices(["Fungi Beast","Jaw Worm"])[0]
                    
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

                kindOfBeast = rd.randint(0,2)

                if rd.randint(0,1) == 0:

                    enemy = rd.choices(["Red Louse","Green Louse"])[0]
                    
                else: 
                    enemy = rd.choices(["Medium Acid Slime","Medium Spike Slime"])[0]
                    
                
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
               
            elif setup == 9:
            
                enemy = "Looter"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

            encounterList.append(miniList)

        return encounterList

    elif helping_functions.gameAct == 2:
        encounterList = []
        checklist = [1,2,3,4,5]
        i = 0
        while i < 2:
            snap = checklist.pop(rd.randint(0,len(checklist)-1))
            miniList = []
            if snap == 1:
                enemy = "Spheric Guardian"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),block = enemies[enemy].get("Block"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death"),artifact = enemies[enemy].get("Artifact")))

            elif snap == 2:
                enemy = "Chosen"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

            elif snap == 3:
                enemy = "Shelled Parasite"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

            elif snap == 4:
                enemy = "Byrd"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                

            elif snap == 5:
                enemy = "Looter"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                enemy = "Mugger"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                
            
            encounterList.append(miniList)
            i += 1
        
        checklist = list(helping_functions.nchoices_with_restrictions([0.07,0.1,0.07,0.21,0.14,0.21,0.1,0.1],{0:1,1:1,2:1,3:1,4:1,5:1,6:1,7:1},k=15))        

        for setup in checklist:
            miniList = []
            if setup == 1:
                enemy = "Byrd"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                enemy = "Chosen"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
            elif setup == 2:
                enemy = "Cultist"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                enemy = "Chosen"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
            elif setup == 3:
                enemy = "Bolt Sentry"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death"), artifact = enemies[enemy].get("Artifact")))
                enemy = "Spheric Guardian"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),block = enemies[enemy].get("Block"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death"),artifact = enemies[enemy].get("Artifact")))
            elif setup == 4:
                enemy = "Snake Plant"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
            elif setup == 5:
                enemy = "Snecko"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
            elif setup == 6:
                enemy = "Centurion"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                enemy = "Mystic"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
            elif setup == 7:
                enemy = "Cultist"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
            elif setup == 8:
                enemy = "Shelled Parasite"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                enemy = "Fungi Beast"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
            encounterList.append(miniList)
        return encounterList
            #Continue Here https://slay-the-spire.fandom.com/wiki/Act_2
    elif helping_functions.gameAct == 3:
        encounterList = []
        checklist = [1,2,3]
        i = 0
        while i < 2:
            snap = checklist.pop(rd.randint(0,len(checklist)-1))
            miniList = []
            if snap == 1:
                enemy = "Darkling"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

            elif snap == 2:
                enemy = "Orb Walker"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),ritual = enemies[enemy].get("Ritual")))

            elif snap == 3:
                subchecklist = [0,0,1,1,2,2]
                forms = 0
                while forms < 3:
                    
                    former = subchecklist.pop(rd.randint(0,len(subchecklist)-1)) 
                    if former == 0:
                        enemy = "Spiker"
                        miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                    
                    elif former == 1:
                        enemy = "Exploder"
                        miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic")))

                    elif former == 2:
                        enemy = "Repulsor"
                        miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic")))
            
                    forms+=1
            i+=1
            encounterList.append(miniList)

        checklist = list(helping_functions.nchoices_with_restrictions([0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125],{0:1,1:1,2:1,3:1,4:1,5:1,6:1,7:1},k=15))

        for setup in checklist:
            miniList = []
            if setup == 0:
                subchecklist = [0,0,1,1,2,2]
                forms = 0
                while forms < 4:
                    former = subchecklist.pop(rd.randint(0,len(subchecklist)-1)) 
                    if former == 0:
                        enemy = "Spiker"
                        miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                    
                    elif former == 1:
                        enemy = "Exploder"
                        miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic")))

                    elif former == 2:
                        enemy = "Repulsor"
                        miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic")))
                    forms+=1                
            
            elif setup == 1:
                enemy = "The Maw"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intention_logic = enemies[enemy].get("Intentions_Logic")))
            
            elif setup == 2:
                forms = 0
                while forms < 2:
                    former = rd.randint(0,2)
                    
                    if former == 0:
                        enemy = "Spiker"
                        miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                    
                    elif former == 1:
                        enemy = "Exploder"
                        miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic")))

                    elif former == 2:
                        enemy = "Repulsor"
                        miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic")))
                    
                    forms += 1

                enemy = "Spheric Guardian"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),block = enemies[enemy].get("Block"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death"),artifact = enemies[enemy].get("Artifact")))

            elif setup == 3:
                enemy = "Darkling"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

            elif setup == 4:
                enemy = "Writhing Mass"                
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

            elif setup == 5:
                enemy = "Jaw Worm Hard"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),block = enemies[enemy].get("Block"),strength=enemies[enemy].get("Strength"),intentions = enemies[enemy].get("Intentions"),intention_logic = [["Random"],list(helping_functions.nchoices_with_restrictions([0.25,0.3,0.45],{0:1,1:2,2:1}))],on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),block = enemies[enemy].get("Block"),strength=enemies[enemy].get("Strength"),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),block = enemies[enemy].get("Block"),strength=enemies[enemy].get("Strength"),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
            
            elif setup == 6:
                enemy = "Spire Growth"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic")))
                
            elif setup == 7:
                enemy = "Transient"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death"),fading6=True))
            
            encounterList.append(miniList)
        return encounterList


def fill_elite_list():
    encounterList = []
    checklist = list(helping_functions.nchoices_with_restrictions([0.333334,0.333333,0.333333],{0:1,1:1,2:1},10))

    if helping_functions.gameAct == 1:

        for setup in checklist:
            miniList = []
            if setup == 0:
                enemy = "Bolt Sentry"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death"), artifact = enemies[enemy].get("Artifact")))

                enemy = "Beam Sentry"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death"), artifact = enemies[enemy].get("Artifact")))

                enemy = "Bolt Sentry"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death"), artifact = enemies[enemy].get("Artifact")))

            elif setup == 1:
                enemy = "Lagavulin"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death"), metallicize = enemies[enemy].get("Metallicize")))
            
            elif setup == 2:
                enemy = "Gremlin Nob"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))


            encounterList.append(miniList)

    elif helping_functions.gameAct == 2:

        for setup in checklist:
            miniList = []
            if setup == 0:
                enemy = "Gremlin Leader"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),leader = True))
                #need to insert random moblins here.
                
                gremlins = ["Mad Gremlin","Sneaky Gremlin","Fat Gremlin","Gremlin Wizard","Shield Gremlin"]
                
                gremls = 0
                while gremls < 2:
                    enemy = gremlins[rd.randint(0,len(gremlins) - 1)]
                    miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic")))
                    gremls +=1

            elif setup == 1:
                enemy = "Book of Stabbing"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death"),painfullStabs= True))
            
            elif setup == 2:
                enemy = "Red Slaver"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic")))
                enemy = "Taskmaster"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic")))
                enemy = "Blue Slaver"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic")))


            encounterList.append(miniList)

    elif helping_functions.gameAct == 3:

        for setup in checklist:
            miniList = []
            if setup == 0:
                enemy = "Nemesis"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),intangiblePower=True))
            elif setup == 1:
                enemy = "Giant Head"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),slow=enemies[enemy].get("Slow")))
            elif setup == 2:
                enemy = "Dagger"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic")))
                enemy = "Raptomancer"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intention_logic = enemies[enemy].get("Intentions_Logic"),leader=enemies[enemy].get("Leader")))
                enemy = "Dagger"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic")))


            encounterList.append(miniList)

    elif helping_functions.gameAct == 4:
        
        miniList = []
        enemy = "Spire Shield"
        miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),artifact=enemies[enemy].get("Artifact"),on_hit_or_death=enemies[enemy].get("On_hit_or_death"),spireBroAttacked=True))
        enemy = "Spire Spear"
        miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),artifact=enemies[enemy].get("Artifact"),on_hit_or_death=enemies[enemy].get("On_hit_or_death")))
        encounterList.append(miniList)
    
    return encounterList

def fill_boss_list(act):
    encounterList = []
    checklist = list(helping_functions.nchoices_with_restrictions([0.333334,0.333333,0.333333],{0:1,1:1,2:1},3))
    
    if act == 1:

        for setup in checklist:
            miniList = []
            if setup == 0:
                enemy = "Slime Boss"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

            elif setup == 1:
                enemy = "Hexaghost"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
            
            elif setup == 2:
                enemy = "Guardian"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death"),modeshift=40))


            encounterList.append(miniList)

    elif act == 2:
        
        for setup in checklist:
            miniList = []
            if setup == 0:
                enemy = "Bronze Automaton"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death"),artifact=enemies[enemy].get("Artifact")))

            elif setup == 1:
                enemy = "The Champ"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
            
            elif setup == 2:
                enemy = "The Collector"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death"),leader=True))


            encounterList.append(miniList)

    elif act == 3:

        for setup in checklist:
            miniList = []    
            if setup == 0:
                enemy = "Cultist"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic")))
                enemy = "Cultist"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic")))
                enemy = "Awakened One"
                miniList.append(Enemy(name= enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic=enemies[enemy].get("Intentions_Logic"),on_hit_or_death=enemies[enemy].get("On_hit_or_death"),cardTypeToLookOutFor=enemies[enemy].get("CardTypeToLookOutFor"),regen=enemies[enemy].get("Regen")))

            elif setup == 1:
                enemy = "Time Eater"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),cardTypeToLookOutFor=enemies[enemy].get("CardTypeToLookOutFor")))

            elif setup == 2:
                enemy = "Deca"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),artifact=enemies[enemy].get("Artifact")))
                enemy = "Donu"
                miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),artifact=enemies[enemy].get("Artifact")))

            encounterList.append(miniList)

    elif act == 4:
        miniList = []
        enemy = "Corrupt Heart"
        miniList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),cardTypeToLookOutFor=enemies[enemy].get("CardTypeToLookOutFor"),on_hit_or_death=enemies[enemy].get("On_hit_or_death")))
        encounterList.append(miniList)

    return encounterList


def create_superElite(superElite):
   
    buff = rd.randint(0,3)

    for elite in superElite:
        if buff == 0:
            healthBuff = int(elite.health / 4)
            elite.set_maxHealth(healthBuff)
        
        elif buff == 1:
            elite.set_strength(helping_functions.gameAct + 1)
        
        elif buff == 2:
            metallicize = helping_functions.gameAct * 2 + 1
            elite.set_metallicice(metallicize)
        
        elif buff == 3:
            regen = helping_functions.gameAct * 2 + 1
            elite.set_metallicice(regen)
    ansiprint("This happened because you are fighting a <m>Super Elite</m>")

    return superElite


cards = {
    
    "Strike": {"Name": "Strike", "Damage":6, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Silent","Info":"Deal <red>6 damage</red>."},
    "Strike +": {"Name": "Strike +","Upgraded": True, "Damage":9, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Silent","Info":"Deal <red>9 damage</red>."},

    "Defend": {"Name": "Defend", "Block":5, "Energy": 1,"Type": "Skill" ,"Rarity": "Basic","Owner":"Silent","Info":"Gain <green>6 Block</green>."},
    "Defend +": {"Name": "Defend +","Upgraded": True, "Block":8, "Energy": 1,"Type": "Skill" ,"Rarity": "Basic","Owner":"Silent","Info":"Gain <green>8 Block</green>."},

    "Shiv": {"Name": "Shiv","Energy": 0,"Damage":4,"Exhaust":True,"Type": "Attack","Rarity": "Special","Owner":"Silent","Info":"Deal <red>4 damage</red>. <BLUE>Exhaust</BLUE>."},
    "Shiv +": {"Name": "Shiv +","Energy": 0,"Damage":6,"Exhaust":True,"Upgraded": True,"Type": "Attack","Rarity": "Special","Owner":"Silent","Info":"Deal <red>4 damage</red>. <BLUE>Exhaust</BLUE>."},

    "Neutralize": {"Name": "Neutralize", "Damage":3,"Weakness": 1,"Type":"Attack", "Energy": 0, "Rarity": "Basic","Owner":"Silent","Info":"Deal <red>3 damage</red>. Apply <light-cyan>1 Weak</light-cyan>."},
    "Neutralize +": {"Name": "Neutralize +","Upgraded": True, "Damage":4,"Weakness": 2,"Type":"Attack", "Energy": 0, "Rarity": "Basic","Owner":"Silent","Info":"Deal <red>3 damage</red>. Apply <light-cyan>1 Weak</light-cyan>."},

    "Survivor": {"Name": "Survivor", "Block":8, "Energy": 1, "Type":"Skill" ,"Discard": 1, "Rarity": "Basic","Owner":"Silent","Info":"Gain <green>8 Block</green>. Discard 1 Card."},
    "Survivor +": {"Name": "Survivor +", "Block":11, "Upgraded": True, "Energy": 1, "Type":"Skill" ,"Discard": 1, "Rarity": "Basic","Owner":"Silent","Info":"Gain <green>11 Block</green>. Discard 1 Card."},   

    "Bane": {"Name": "Bane", "Damage":7, "Energy": 1,"Type": "Attack" ,"Rarity": "Common","Owner":"Silent","Info":"Deal <red>7 damage</red>. If the enemy has <green>Poison</green>, deal <red>7 damage</red> again"},
    "Bane +": {"Name": "Bane +", "Damage":10, "Upgraded": True,"Energy": 1,"Type": "Attack" ,"Rarity": "Common","Owner":"Silent","Info":"Deal <red>7 damage</red>. If the enemy has <green>Poison</green>, deal <red>7 damage</red> again"},

    "Dagger Spray": {"Name": "Dagger Spray", "Damage":4, "Energy": 1, "Type":"Attack","Rarity":"Common","Owner":"Silent","Info":"Deal <red>4 damage</red> to ALL enemies twice."},
    "Dagger Spray +": {"Name": "Dagger Spray +", "Damage":6,"Upgraded": True,"Energy": 1, "Type":"Attack","Rarity":"Common","Owner":"Silent","Info":"Deal <red>6 damage</red> to ALL enemies twice."},

    "Dagger Throw": {"Name": "Dagger Throw", "Damage":9,"Draw":1,"Discard":1,"Energy": 1,"Type": "Attack" , "Rarity": "Common", "Owner":"Silent","Info":"Deal <red>9 damage</red>. Draw 1 Card. Discard 1 Card."}, 
    "Dagger Throw +": {"Name": "Dagger Throw +","Upgraded": True, "Damage":12,"Draw":1,"Discard":1,"Energy": 1,"Type": "Attack" , "Rarity": "Common", "Owner":"Silent","Info":"Deal <red>12 damage</red>. Draw 1 Card. Discard 1 Card."}, 
    
    "Flying Knee": {"Name": "Flying Knee", "Damage":8,"Energy Gain":1,"Energy": 1,"Type": "Attack" ,"Rarity": "Common","Owner":"Silent","Info":"Deal <red>8 damage</red>. Next turn, gain <yellow>1 Energy</yellow>."},
    "Flying Knee +": {"Name": "Flying Knee +", "Upgraded": True, "Damage":11,"Energy Gain":1,"Energy": 1,"Type": "Attack" ,"Rarity": "Common","Owner":"Silent","Info":"Deal <red>11 damage</red>. Next turn, gain <yellow>1 Energy</yellow>."},

    "Poisoned Stab": {"Name": "Poisoned Stab", "Damage":6,"Poison":3,"Energy": 1,"Type": "Attack" ,"Rarity": "Common","Owner":"Silent","Info":"Deal <red>6 damage</red>. Apply <green>3 Poison</green>."},
    "Poisoned Stab +": {"Name": "Poisoned Stab +", "Damage":8,"Poison":4,"Energy": 1,"Type": "Attack" ,"Upgraded": True,"Rarity": "Common","Owner":"Silent","Info":"Deal <red>8 damage</red>. Apply <green>4 Poison</green>."},

    "Quick Slash": {"Name": "Quick Slash", "Damage":8,"Draw":1,"Energy": 1,"Type": "Attack" ,"Rarity": "Common","Owner":"Silent","Info":"Deal <red>8 damage</red>. Draw 1 Card."},
    "Quick Slash +": {"Name": "Quick Slash +", "Damage":12,"Draw":1,"Energy": 1,"Type": "Attack" ,"Upgraded": True,"Rarity": "Common","Owner":"Silent","Info":"Deal <red>12 damage</red>. Draw 1 Card."},

    "Slice": {"Name": "Slice", "Damage":6,"Energy": 0,"Type": "Attack" ,"Rarity": "Common","Owner":"Silent","Info": "Deal <red>6 damage</red>."},
    "Slice +": {"Name": "Slice +", "Damage":9,"Energy": 0,"Type": "Attack" ,"Upgraded": True,"Rarity": "Common","Owner":"Silent","Info": "Deal <red>9 damage</red>."},

    "Sneaky Strike": {"Name": "Sneaky Strike", "Damage":12,"Energy": 2,"Energy Gain": 2,"Type": "Attack" ,"Rarity": "Common","Owner":"Silent","Info":"Deal <red>12 damage</red>. If you have discarded a Card this turn gain <yellow>2 Energy</yellow>."},
    "Sneaky Strike +": {"Name": "Sneaky Strike +", "Damage":16,"Energy": 2,"Energy Gain": 2,"Type": "Attack" ,"Rarity": "Common","Upgraded": True,"Owner":"Silent","Info":"Deal <red>16 damage</red>. If you have discarded a Card this turn gain <yellow>2 Energy</yellow>."},
    
    "Sucker Punch": {"Name": "Sucker Punch", "Damage":7,"Weakness": 1,"Energy": 1,"Type": "Attack" ,"Rarity": "Common","Owner":"Silent","Info":"Deal <red>7 damage</red>. Apply <light-cyan>1 Weak</light-cyan>."},
    "Sucker Punch +": {"Name": "Sucker Punch +","Damage":9,"Weakness": 2,"Energy": 1,"Type": "Attack" ,"Upgraded": True,"Rarity": "Common","Owner":"Silent","Info":"Deal <red>9 damage</red>. Apply <light-cyan>2 Weak</light-cyan>."},
    
    "All-Out Attack": {"Name": "All-Out Attack", "Damage":10,"Energy": 1,"Discard": 1,"Type": "Attack" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Deal <red>10 damage</red> to ALL enemies. Discard 1 random Card."},
    "All-Out Attack +": {"Name": "All-Out Attack +", "Damage":14,"Energy": 1,"Discard": 1,"Type": "Attack" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Deal <red>14 damage</red> to ALL enemies. Discard 1 random Card."},

    "Backstab": {"Name": "Backstab", "Damage":11,"Energy": 0,"Innate": True,"Exhaust": True, "Type": "Attack" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Deal <red>11 damage</red>. <BLUE>Exhaust<BLUE>. <BLUE>Innate<BLUE>."},
    "Backstab +": {"Name": "Backstab +", "Damage":15,"Energy": 0,"Innate": True,"Exhaust": True, "Type": "Attack" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Deal <red>15 damage</red>. <BLUE>Exhaust<BLUE>. <BLUE>Innate<BLUE>."},

    "Choke": {"Name": "Choke", "Damage":12,"Energy": 2, "Choking": 3, "Type": "Attack" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Deal <red>12 damage</red>. Whenever you play a Card this turn, the enemy loses <red>3 HP</red>."},
    "Choke +": {"Name": "Choke +", "Damage":12,"Energy": 2, "Choking": 5, "Type": "Attack" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Deal <red>12 damage</red>. Whenever you play a Card this turn, the enemy loses <red>5 HP</red>."},

    "Dash": {"Name": "Dash", "Damage":10,"Block":10,"Energy": 2, "Type": "Attack" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Gain <green>10 Block</green. Deal <red>10 damage</red>."},
    "Dash +": {"Name": "Dash +", "Damage":13,"Block":13,"Energy": 2, "Type": "Attack" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Gain <green>12 Block</green. Deal <red>12 damage</red>."},

    "Endless Agony": {"Name": "Endless Agony", "Damage":4,"Exhaust":True,"Energy": 0, "Type": "Attack" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Whenever you draw this Card, add a copy of it into your hand. Deal <red>4 damage</red>. <BLUE>Exhaust<BLUE>"},
    "Endless Agony +": {"Name": "Endless Agony +", "Damage":6,"Exhaust":True,"Energy": 0, "Type": "Attack" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Whenever you draw this Card, add a copy of it into your hand. Deal <red>6 damage</red>. <BLUE>Exhaust<BLUE>"},

    "Eviscerate": {"Name": "Eviscerate", "Damage":7,"Energy": 3, "Type": "Attack" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Costs <yellow>1 Energy</yellow> less for each discarded Card this turn. Deal <red>7 damage</red> 3 times."},
    "Eviscerate +": {"Name": "Eviscerate +", "Damage":9,"Energy": 3, "Type": "Attack" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Costs <yellow>1 Energy</yellow> less for each discarded Card this turn. Deal <red>9 damage</red> 3 times."},

    "Finisher": {"Name": "Finisher", "Damage":6,"Energy": 1, "Type": "Attack" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Deal <red>6 damage</red> for each <red>Attack</red> this turn."},
    "Finisher +": {"Name": "Finisher +", "Damage":8,"Energy": 1, "Type": "Attack" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Deal <red>8 damage</red> for each <red>Attack</red> this turn."},

    "Flechettes": {"Name": "Flechettes", "Damage":4,"Energy": 1, "Type": "Attack" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Deal <red>4 damage</red> for each <green>Skill</green> in your hand."},
    "Flechettes +": {"Name": "Flechettes +", "Damage":6,"Energy": 1, "Type": "Attack" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Deal <red>6 damage</red> for each <green>Skill</green> in your hand."},

    "Heel Hook": {"Name": "Heel Hook", "Damage":5,"Energy": 1,"Energy Gain":1,"Draw":1, "Type": "Attack" ,"Rarity": "Uncommon","Owner":"Silent","Info": "Deal <red>5 damage</red>. If the enemy has <light-cyan>Weak</light-cyan>, gain <yellow>1 Energy</yellow> and draw 1 Card."},
    "Heel Hook +": {"Name": "Heel Hook +", "Damage":8,"Energy": 1,"Energy Gain":1,"Draw":1, "Type": "Attack" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info": "Deal <red>5 damage</red>. If the enemy has <light-cyan>Weak</light-cyan>, gain <yellow>1 Energy</yellow> and draw 1 Card."},

    "Masterful Stab": {"Name": "Masterful Stab", "Damage":12,"Energy": 0, "Type": "Attack" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Cost <yellow>1 Energy</yellow> extra for each time you <red>lose HP</red> this combat. Deal <red>12 damage</red>."},
    "Masterful Stab +": {"Name": "Masterful Stab +", "Damage":16,"Energy": 0, "Type": "Attack" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Cost <yellow>1 Energy</yellow> extra for each time you <red>lose HP</red> this combat. Deal <red>16 damage</red>."},

    "Predator": {"Name": "Predator", "Damage":15,"Energy": 2,"Drawboost":2, "Type": "Attack" ,"Rarity": "Uncommon","Owner":"Silent","Info": "Deal <red>15 damage</red>. Draw 2 additonal Cards next turn."},
    "Predator +": {"Name": "Predator +", "Damage":20,"Energy": 2,"Drawboost":2, "Type": "Attack" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info": "Deal <red>20 damage</red>. Draw 2 additonal Cards next turn."},

    "Riddle with Holes": {"Name": "Riddle with Holes","Damage":3,"Energy": 2, "Type": "Attack" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Deal <red>3 damage</red> 5 times."},
    "Riddle with Holes +": {"Name": "Riddle with Holes +","Damage":4,"Energy": 2, "Type": "Attack" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Deal <red>4 damage</red> 5 times."},

    "Skewer": {"Name": "Skewer", "Damage":7, "Energy": "X", "Type": "Attack" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Deal <red>7 damage</red> <yellow>X</yellow> times."},
    "Skewer +": {"Name": "Skewer +", "Damage":10, "Energy": "X", "Type": "Attack" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Deal <red>10 damage</red> <yellow>X</yellow> times."},

    "Die Die Die": {"Name": "Die Die Die","Damage":13,"Energy": 1,"Exhaust":True, "Type": "Attack" ,"Rarity": "Rare","Owner":"Silent","Info":"Deal <red>13 damage</red> to ALL enemies. <BLUE>Exhaust<BLUE>"},
    "Die Die Die +": {"Name": "Die Die Die +","Damage":17,"Energy": 1,"Exhaust":True, "Type": "Attack" ,"Upgraded": True,"Rarity": "Rare","Owner":"Silent","Info":"Deal <red>17 damage</red> to ALL enemies. <BLUE>Exhaust<BLUE>"},
    
    "Glass Knife": {"Name": "Glass Knife","Damage":8,"Energy": 1, "Type": "Attack" ,"Rarity": "Rare","Owner":"Silent","Info":"Deal <red>8 damage</red> twice. Decrease the damage of this card by 2 for this combat."},
    "Glass Knife +": {"Name": "Glass Knife +","Damage":12,"Energy": 1, "Type": "Attack" ,"Upgraded": True,"Rarity": "Rare","Owner":"Silent","Info":"Deal <red>8 damage</red> twice. Decrease the damage of this card by 2 for this combat."},

    "Grand Finale": {"Name": "Grand Finale","Damage":50,"Energy": 1, "Type": "Attack" ,"Rarity": "Rare","Owner":"Silent","Info":"Can only be played if there are no cards in your Drawpile. Deal <red>50 damage</red> to ALL enemies."},
    "Grand Finale +": {"Name": "Grand Finale +","Damage":60,"Energy": 1, "Type": "Attack" ,"Upgraded": True,"Rarity": "Rare","Owner":"Silent","Info":"Can only be played if there are no cards in your Drawpile. Deal <red>60 damage</red> to ALL enemies."},
    
    "Unload": {"Name": "Unload","Damage":14,"Energy": 1, "Type": "Attack","DiscardType":"Attack","Rarity": "Rare","Owner":"Silent","Info":"Deal <red>14 damage</red>. Discard all <red>non-Attack</red> Cards from your hand."},
    "Unload +": {"Name": "Unload +","Damage":18,"Energy": 1, "Type": "Attack","DiscardType":"Attack","Upgraded": True,"Rarity": "Rare","Owner":"Silent","Info":"Deal <red>18 damage</red>. Discard all <red>non-Attack</red> Cards from your hand."},

    "Acrobatics": {"Name": "Acrobatics", "Draw":3,"Discard":1, "Energy": 1,"Type": "Skill" ,"Rarity": "Common","Owner":"Silent","Info":"Draw 3 Cards. Discard 1 Card."},
    "Acrobatics +": {"Name": "Acrobatics +", "Draw":4,"Discard":1, "Energy": 1,"Type": "Skill" ,"Upgraded": True,"Rarity": "Common","Owner":"Silent","Info":"Draw 4 Cards. Discard 1 Card."},

    "Backflip": {"Name": "Backflip","Block":5, "Draw":2, "Energy": 1,"Type": "Skill" ,"Rarity": "Common","Owner":"Silent","Info":"Gain <green>5 Block</green>. Draw 2 Cards."},
    "Backflip +": {"Name": "Backflip +","Block":8, "Draw":2, "Energy": 1,"Type": "Skill" ,"Upgraded": True,"Rarity": "Common","Owner":"Silent","Info":"Gain <green>8 Block</green>. Draw 2 Cards."},

    "Blade Dance": {"Name": "Blade Dance","Shivs":3,"Energy": 1,"Type": "Skill" ,"Rarity": "Common","Owner":"Silent","Info":"Add <red>3 Shivs</red> into your hand."},
    "Blade Dance +": {"Name": "Blade Dance +","Shivs":4,"Energy": 1,"Type": "Skill" ,"Upgraded": True,"Rarity": "Common","Owner":"Silent","Info":"Add <red>4 Shivs</red> into your hand."},

    "Cloak and Dagger": {"Name": "Cloak and Dagger","Block":6,"Shivs":1,"Energy": 1,"Type": "Skill" ,"Rarity": "Common","Owner":"Silent","Info":"Gain <green>6 Block</green>. Add <red>1 Shiv<red> to your hand."},
    "Cloak and Dagger +": {"Name": "Cloak and Dagger +","Block":6,"Shivs":2,"Energy": 1,"Type": "Skill" ,"Upgraded": True,"Rarity": "Common","Owner":"Silent","Info":"Gain <green>6 Block</green>. Add <red>2 Shiv<red> to your hand."},

    "Deadly Poison": {"Name": "Deadly Poison","Poison":5,"Energy": 1,"Type": "Skill" ,"Rarity": "Common","Owner":"Silent","Info":"Apply <green>5 Poison</green>."},
    "Deadly Poison +": {"Name": "Deadly Poison +","Poison":7,"Energy": 1,"Type": "Skill" ,"Upgraded": True,"Rarity": "Common","Owner":"Silent","Info":"Apply <green>7 Poison</green>."},
    
    "Deflect": {"Name": "Deflect","Block":5,"Energy": 0,"Type": "Skill" ,"Rarity": "Common","Owner":"Silent","Info":"Gain <green>5 Block</green>"},
    "Deflect +": {"Name": "Deflect +","Block":8,"Energy": 0,"Type": "Skill" ,"Upgraded": True,"Rarity": "Common","Owner":"Silent","Info":"Gain <green>8 Block</green>"},
    
    "Dodge and Roll": {"Name": "Dodge and Roll","Block":4,"Energy": 1,"Type": "Skill" ,"Rarity": "Common","Owner":"Silent","Info":"Gain <green>4 Block</green>. Next turn, gain <green>4 Block</green>."},
    "Dodge and Roll +": {"Name": "Dodge and Roll +","Block":6,"Energy": 1,"Type": "Skill" ,"Upgraded": True,"Rarity": "Common","Owner":"Silent","Info":"Gain <green>6 Block</green>. Next turn, gain <green>6 Block</green>."},

    "Outmaneuver": {"Name": "Outmaneuver","Energy Gain":2,"Energy": 1,"Type": "Skill" ,"Rarity": "Common","Owner":"Silent","Info":"Next turn gain <yellow>2 Energy</yellow>."},
    "Outmaneuver +": {"Name": "Outmaneuver +","Energy Gain":3,"Energy": 1,"Type": "Skill" ,"Upgraded": True,"Rarity": "Common","Owner":"Silent","Info":"Next turn gain <yellow>3 Energy</yellow>."},

    "Piercing Wail": {"Name": "Piercing Wail","Strength Modifier":6,"Energy": 1,"Exhaust": True,"Type": "Skill" ,"Rarity": "Common","Owner":"Silent","Info":"ALL enemies lose <red>6 Strength</red> this turn. <BLUE>Exhaust</BLUE>."},
    "Piercing Wail +": {"Name": "Piercing Wail +","Strength Modifier":8,"Energy": 1,"Exhaust": True,"Type": "Skill" ,"Upgraded": True,"Rarity": "Common","Owner":"Silent","Info":"ALL enemies lose <red>8 Strength</red> this turn. <BLUE>Exhaust</BLUE>."},
    
    "Prepared": {"Name": "Prepared","Draw":1,"Discard":1,"Energy": 0,"Type": "Skill" ,"Rarity": "Common","Owner":"Silent","Info":"Draw 1 Card. Discard 1 Card."},
    "Prepared +": {"Name": "Prepared +","Draw":2,"Discard":2,"Energy": 0,"Type": "Skill" ,"Upgraded": True,"Rarity": "Common","Owner":"Silent","Info":"Draw 2 Cards. Discard 2 Cards."},

    "Blur": {"Name": "Blur","Block":5,"KeepBlock":1,"Energy": 1,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Gain <green>5 Block</green>. <green>Block</green> is not removed at the start of your next turn."},
    "Blur +": {"Name": "Blur +","Block":8,"KeepBlock":1,"Energy": 1,"Type": "Skill" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Gain <green>8 Block</green>. <green>Block</green> is not removed at the start of your next turn."},

    "Bouncing Flask": {"Name": "Bouncing Flask","Poison":3,"Bounces":3,"Energy": 2,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Randomly apply <green>3 Poison</green> 3 times."},
    "Bouncing Flask +": {"Name": "Bouncing Flask +","Poison":3,"Bounces":4,"Energy": 2,"Type": "Skill" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Randomly apply <green>3 Poison</green> 4 times."},
    
    "Calculated Gamble": {"Name": "Calculated Gamble","Exhaust": True,"Energy": 0,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Discard your entire hand. Draw as many cards. <BLUE>Exhaust<BLUE>."},
    "Calculated Gamble +": {"Name": "Calculated Gamble +","Energy": 0,"Type": "Skill" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Discard your entire hand. Draw as many cards."},

    "Catalyst": {"Name": "Catalyst","Multiplikator":2,"Energy": 1,"Exhaust": True,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Double the enemy's <green>Poison</green>. <BLUE>Exhaust</BLUE>."},
    "Catalyst +": {"Name": "Catalyst +","Multiplikator":3,"Energy": 1,"Exhaust": True,"Upgraded": True,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Triple the enemy's <green>Poison</green>. <BLUE>Exhaust</BLUE>."},
    
    "Concentrate" :{"Name": "Concentrate","Energy Gain":2,"Discard": 3,"Energy": 0,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Discard 3 Cards. Gain <yellow>2 Energy</yellow>."},
    "Concentrate +" :{"Name": "Concentrate +","Energy Gain":2,"Discard": 2,"Energy": 0,"Upgraded": True,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Discard 2 Cards. Gain <yellow>2 Energy</yellow>."},
    
    "Crippling Cloud" :{"Name": "Crippling Cloud","Poison":4,"Weakness": 2,"Energy": 2,"Exhaust":True ,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Apply <green>4 Poison</green> and <light-cyan>2 Weak</light-cyan> to ALL enemies. <BLUE>Exhaust</BLUE>."},
    "Crippling Cloud +" :{"Name": "Crippling Cloud +","Poison":7,"Weakness": 2,"Energy": 2,"Exhaust":True ,"Upgraded": True,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Apply <green>6 Poison</green> and <light-cyan>2 Weak</light-cyan> to ALL enemies. <BLUE>Exhaust</BLUE>."},
    
    "Distraction" :{"Name": "Distraction","Energy": 1,"Exhaust":True ,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Add a random <green>Skill</green> into your hand. It costs <yellow>0 Energy<yellow> this turn."},
    "Distraction +" :{"Name": "Distraction +","Energy": 0,"Exhaust":True ,"Type": "Skill" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Add a random <green>Skill</green> into your hand. It costs <yellow>0 Energy<yellow> this turn."},
    
    "Escape Plan" :{"Name": "Escape Plan","Block":3,"Draw": 1,"Energy": 0 ,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Draw 1 Card. If you draw a <green>Skill</green>, gain <green>3 Block</green>."},
    "Escape Plan +" :{"Name": "Escape Plan +","Block":5,"Draw": 1,"Energy": 0 ,"Type": "Skill" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Draw 1 Card. If you draw a <green>Skill</green>, gain <green>5 Block</green>."},
    
    "Expertise" :{"Name": "Expertise","Draw":6,"Energy": 1 ,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Draw until you have 6 cards in your hand."},
    "Expertise +" :{"Name": "Expertise +","Draw":7,"Energy": 1 ,"Type": "Skill" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Draw until you have 7 cards in your hand."},
    
    "Leg Sweep" :{"Name": "Leg Sweep","Block":11,"Weakness":2,"Energy": 2 ,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Apply <light-cyan>2 Weak</light-cyan>. Gain <green>11 Block</green>."},
    "Leg Sweep +" :{"Name": "Leg Sweep +","Block":14,"Weakness":3,"Energy": 2 ,"Type": "Skill" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Apply <light-cyan>3 Weak</light-cyan>. Gain <green>14 Block</green>."},
    

    "Reflex" :{"Name": "Reflex","Draw":2 ,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Silent","Info":"<RED>Unplayable</RED>. If this Card is discared, draw 2 Cards."},
    "Reflex +" :{"Name": "Reflex +","Draw":3 ,"Type": "Skill" ,"Rarity": "Uncommon","Upgraded": True,"Owner":"Silent","Info":"<RED>Unplayable</RED>. If this Card is discared, draw 3 Cards."},
    
    "Tactician" :{"Name": "Tactician","Energy Gain":1,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Silent","Info":"<RED>Unplayable</RED>. If this Card is discared, gain <yellow>1 Energy</yellow>."},
    "Tactician +" :{"Name": "Tactician","Energy Gain":2 ,"Type": "Skill" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"<RED>Unplayable</RED>. If this Card is discared, gain <yellow>2 Energy</yellow>."},
    
    "Setup" :{"Name": "Setup","Back Putter":1,"Energy Change Type":"Until Played","Energy Change":0,"Energy": 1 ,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Put a Card from your hand on top of your Drawpile. It costs <yellow>0 Energy</yellow> until played"},
    "Setup +" :{"Name": "Setup +","Back Putter":1,"Energy Change Type":"Until Played","Energy Change":0,"Energy": 0,"Type": "Skill" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Put a Card from your hand on top of your Drawpile. It costs <yellow>0 Energy</yellow> until played"},

    "Terror" :{"Name": "Terror", "Vulnerable":99, "Energy": 1 ,"Type": "Skill" ,"Exhaust":True ,"Rarity": "Uncommon","Owner":"Silent","Info":"Apply <light-cyan>99 Vulnerable</light-cyan>."},
    "Terror +" :{"Name": "Terror +", "Vulnerable":99, "Energy": 0 ,"Type": "Skill" ,"Exhaust":True ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Apply <light-cyan>99 Vulnerable</light-cyan>."},

    "Adrenaline" :{"Name": "Adrenaline","Draw":2,"Energy": 0,"Energy Gain":1,"Exhaust":True ,"Type": "Skill" ,"Rarity": "Rare","Owner":"Silent","Info":"Draw 2 Cards. Gain <yellow>1 Energy</yellow>. <BLUE>Exhaust<BLUE>."},
    "Adrenaline +" :{"Name": "Adrenaline +","Draw":2,"Energy": 0,"Energy Gain":2,"Exhaust":True ,"Upgraded": True,"Type": "Skill" ,"Rarity": "Rare","Owner":"Silent","Info":"Draw 2 Cards. Gain <yellow>2 Energy</yellow>. <BLUE>Exhaust<BLUE>."},

    "Alchemize" :{"Name": "Alchemize","Potion":1,"Energy": 1,"Exhaust":True ,"Type": "Skill" ,"Rarity": "Rare","Owner":"Silent","Info":"Obtain a random <c>Potion</c>. <BLUE>Exhaust</BLUE>."},
    "Alchemize +" :{"Name": "Alchemize +","Potion":1,"Energy": 0,"Exhaust":True ,"Type": "Skill" ,"Upgraded": True,"Rarity": "Rare","Owner":"Silent","Info":"Obtain a random <c>Potion</c>. <BLUE>Exhaust</BLUE>."},

    "Corpse Explosion" :{"Name": "Corpse Explosion","Poison":6,"Energy": 2 ,"Type": "Skill" ,"Rarity": "Rare","Owner":"Silent","Info":"Apply <green>6 Poison</green>. When the enemy dies, deal <red>damage</red> equal to its Max HP to ALL enemies."},
    "Corpse Explosion +" :{"Name": "Corpse Explosion +","Poison":9,"Energy": 2 ,"Type": "Skill" ,"Rarity": "Rare","Upgraded": True,"Owner":"Silent","Info":"Apply <green>9 Poison</green>. When the enemy dies, deal <red>damage</red> equal to its Max HP to ALL enemies."},

    "Doppelganger" :{"Name": "Doppelganger","Energy": "X","Exhaust":True ,"Type": "Skill" ,"Rarity": "Rare","Owner":"Silent","Info":"Next turn, draw X Cards and gain <yellow>X Energy</yellow>."},
    "Doppelganger +" :{"Name": "Doppelganger +","Energy": "X","Exhaust":True ,"Type": "Skill" ,"Upgraded": True,"Rarity": "Rare","Owner":"Silent","Info":"Next turn, draw X+1 Cards and gain <yellow>X+1 Energy</yellow>."},
    
    "Malaise" :{"Name": "Malaise","Energy": "X","Exhaust":True ,"Type": "Skill" ,"Rarity": "Rare","Owner":"Silent","Info":"Enemy loses <red>X Stength</red>. Apply <light-cyan>X Weak<light-cyan>. <BLUE>Exhaust</BLUE>."},
    "Malaise +" :{"Name": "Malaise +","Energy": "X","Exhaust":True ,"Type": "Skill" ,"Upgraded": True,"Rarity": "Rare","Owner":"Silent","Info":"Enemy loses <red>X+1 Stength</red>. Apply <light-cyan>X+1 Weak<light-cyan>. <BLUE>Exhaust</BLUE>."},
    
    "Phantasmal Killer" :{"Name": "Phantasmal Killer","Energy": 1,"DoubleDamage":1 ,"Type": "Skill" ,"Rarity": "Rare","Owner":"Silent","Info":"Next turn your <red>Attacks</red> deal double damage."},
    "Phantasmal Killer +" :{"Name": "Phantasmal Killer +","Energy": 0,"DoubleDamage":1 ,"Upgraded": True,"Type": "Skill" ,"Rarity": "Rare","Owner":"Silent","Info":"Next turn your <red>Attacks</red> deal double damage."},
    
    "Bullet Time" :{"Name": "Bullet Time","Energy": 3,"Bullet Time":1 ,"Type": "Skill" ,"Rarity": "Rare","Owner":"Silent","Info":"You cannot draw additonal Cards this turn. Reduce the cost of all Cards in your hand to 0 this turn."},
    "Bullet Time +" :{"Name": "Bullet Time +","Energy": 2,"Bullet Time":1 ,"Type": "Skill" ,"Upgraded": True,"Rarity": "Rare","Owner":"Silent","Info":"You cannot draw additonal Cards this turn. Reduce the cost of all Cards in your hand to 0 this turn."},

    "Storm of Steel" :{"Name": "Storm of Steel","Energy": 1 ,"Type": "Skill" ,"Rarity": "Rare","Owner":"Silent","Info":"Discard your hand. Add <red>1 Shiv</red> for each card you discarded this way."},
    "Storm of Steel +" :{"Name": "Storm of Steel +","Energy": 1 ,"Type": "Skill" ,"Upgraded": True,"Rarity": "Rare","Owner":"Silent","Info":"Discard your hand. Add <red>1 Shiv +</red> for each card you discarded this way."},

    "Burst" :{"Name": "Burst", "Burst":1, "Energy": 1,"Type": "Skill" ,"Rarity": "Rare","Owner":"Silent","Info":"This turn, your next <green>Skill</green> is played twice."},
    "Burst +" :{"Name": "Burst +", "Burst":2, "Energy": 1,"Type": "Skill" ,"Upgraded": True,"Rarity": "Rare","Owner":"Silent","Info":"This turn, your next <green>2 Skills</green> are played twice."},

    "Accuracy" :{"Name": "Accuracy", "Accuracy":4, "Energy": 1,"Type": "Power" ,"Rarity": "Uncommon","Owner":"Silent","Info":"<red>Shivs</red> deal an extra <red>4 damage</red>."},
    "Accuracy +" :{"Name": "Accuracy +", "Accuracy":6, "Energy": 1,"Type": "Power" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"<red>Shivs</red> deal an extra <red>6 damage</red>."},

    "After Image" :{"Name": "After Image", "After Image":1, "Energy": 1,"Type": "Power" ,"Rarity": "Rare","Owner":"Silent","Info":"Whenever you play a card, gain <green>1 Block</green>."},
    "After Image +" :{"Name": "After Image +", "After Image":1, "Innate": True,"Upgraded":True, "Energy": 1,"Type": "Power" ,"Rarity": "Rare","Owner":"Silent","Info":"Whenever you play a card, gain <green>2 Block</green>."},
    
    "Caltrops" :{"Name": "Caltrops", "Spikes":3, "Energy": 1,"Type": "Power" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Whenever you are attacked, deal <red>3 damage</red> back."},  
    "Caltrops +" :{"Name": "Caltrops +", "Spikes":5, "Energy": 1,"Type": "Power" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Whenever you are attacked, deal <red>5 damage</red> back."},
    
    "Footwork" :{"Name": "Footwork", "Dexterity":2, "Energy": 1,"Type": "Power" ,"Rarity": "Uncommon","Owner":"Silent","Info":"Gain <green>2 Dexterity</green>."},
    "Footwork +" :{"Name": "Footwork +", "Dexterity":3, "Energy": 1,"Type": "Power" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"Gain <green>3 Dexterity</green>."},

    "Infinite Blades" :{"Name": "Infinite Blades", "Infinite Blades":1, "Energy": 1,"Type": "Power" ,"Rarity": "Uncommon","Owner":"Silent","Info":"At the start of your turn, add <red>1 Shiv</red> to your hand."},
    "Infinite Blades +" :{"Name": "Infinite Blades +", "Infinite Blades":1,"Innate": True, "Energy": 1,"Type": "Power" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"At the start of your turn, add <red>1 Shiv</red> to your hand. <BLUE>Innate<BLUE>."},

    "NoxiousFumes" :{"Name": "Noxious Fumes", "Noxiousness":2, "Energy": 1,"Type": "Power" ,"Rarity": "Uncommon","Owner":"Silent","Info":"At the start of your turn, apply <green>2 Poison</green> to ALL enemies."},
    "NoxiousFumes +" :{"Name": "Noxious Fumes +", "Noxiousness":3, "Energy": 1,"Type": "Power" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent","Info":"At the start of your turn, apply <green>3 Poison</green> to ALL enemies."},

    "Well-Laid Plans" :{"Name": "Well-Laid Plans", "Well Planed":1, "Energy": 1,"Type": "Power" ,"Rarity": "Uncommon","Owner":"Silent","Info":"At the end of your turn, Retain up to 1 Card."},
    "Well-Laid Plans +" :{"Name": "Well-Laid Plans +", "Well Planed":2, "Energy": 1,"Upgraded": True,"Type": "Power" ,"Rarity": "Uncommon","Owner":"Silent","Info":"At the end of your turn, Retain up to 2 Card."},

    "A Thousand Cuts" :{"Name": "A Thousand Cuts", "Thousand Cuts":1, "Energy": 2,"Type": "Power" ,"Rarity": "Rare","Owner":"Silent","Info":"Whenever you play a Card, deal <red>1 damage</red> to ALL enemies."},
    "A Thousand Cuts +" :{"Name": "A Thousand Cuts +", "Thousand Cuts":2, "Energy": 2,"Upgraded": True,"Type": "Power" ,"Rarity": "Rare","Owner":"Silent","Info":"Whenever you play a Card, deal <red>2 damage</red> to ALL enemies."},

    "Envenom" :{"Name": "Envenom", "Envenom":1, "Energy": 2,"Type": "Power" ,"Rarity": "Rare","Owner":"Silent","Info":"Whenever an <red>Attack</red> deals unblocked <red>damaged</red>,apply <green>1 Poison</green>."},
    "Envenom +" :{"Name": "Envenom +", "Envenom":1, "Energy": 1,"Type": "Power" ,"Upgraded": True,"Rarity": "Rare","Owner":"Silent","Info":"Whenever an <red>Attack</red> deals unblocked <red>damaged</red>,apply <green>1 Poison</green>."},

    "Tools of the Trade" :{"Name": "Tools of the Trade", "Tools":1, "Energy": 1,"Type": "Power" ,"Rarity": "Rare","Owner":"Silent","Info":"At the start of your turn, draw 1 Card. Discard 1 Card."},
    "Tools of the Trade +" :{"Name": "Tools of the Trade +", "Tools":1, "Energy": 0,"Type": "Power" ,"Upgraded": True,"Rarity": "Rare","Owner":"Silent","Info":"At the start of your turn, draw 1 Card. Discard 1 Card."},

    "Wraith Form" :{"Name": "Wraith Form", "Wraithness":1,"Intangible":2, "Energy": 3,"Type": "Power" ,"Rarity": "Rare","Owner":"Silent","Info":"Gain <blue>2 Intangible</blue>. At the end of your turn, lose <green>1 Dexterity</green>."},
    "Wraith Form +" :{"Name": "Wraith Form +", "Wraithness":1,"Intangible":3, "Energy": 3,"Upgraded": True,"Type": "Power" ,"Rarity": "Rare","Owner":"Silent","Info":"Gain <blue>3 Intangible</blue>. At the end of your turn, lose <green>1 Dexterity</green>."},

    "Bandage Up": {"Name": "Bandage Up","Heal": 4, "Energy": 0, "Exhaust": True, "Type": "Skill", "Rarity": "Uncommon", "Owner":"Colorless","Info":"<red>Heal 4 HP</red>.<BLUE>Exhaust</BLUE>."},
    "Bandage Up +": {"Name": "Bandage Up +","Heal": 6, "Energy": 0, "Exhaust": True, "Type": "Skill","Upgraded": True, "Rarity": "Uncommon", "Owner":"Colorless","Info":"<red>Heal 6 HP</red>.<BLUE>Exhaust</BLUE>."},
    
    "Blind": {"Name": "Blind","Weakness": 2, "Energy": 0, "Type": "Skill", "Rarity": "Uncommon", "Owner":"Colorless","Info":"Apply <light-cyan>2 Weak</light-cyan>."},
    "Blind +": {"Name": "Blind +","Weakness": 2, "Energy": 0, "Type": "Skill", "Rarity": "Uncommon","Upgraded": True, "Owner":"Colorless","Info":"Apply <light-cyan>2 Weak</light-cyan> to ALL enemies."},
    
    "Trip": {"Name": "Trip","Vulnerable": 2, "Energy": 0, "Type": "Skill", "Rarity": "Uncommon", "Owner":"Colorless","Info":"Apply <light-cyan>2 Weak</light-cyan>."},
    "Trip +": {"Name": "Trip +","Vulnerable": 2, "Energy": 0, "Type": "Skill", "Rarity": "Uncommon","Upgraded": True, "Owner":"Colorless","Info":"Apply <light-cyan>2 Vulnerable</light-cyan> to ALL enemies."},

    "Dark Shackles": {"Name": "Dark Shackles","Strength Modifier":9,"Energy": 0,"Exhaust": True,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Colorless","Info":"Enemy loses <red>9 Strength</red> this turn. <BLUE>Exhaust</BLUE>."},
    "Dark Shackles +": {"Name": "Dark Shackles +","Strength Modifier":15,"Energy": 0,"Exhaust": True,"Type": "Skill","Upgraded": True,"Rarity": "Uncommon","Owner":"Colorless","Info":"Enemy loses <red>15 Strength</red> this turn. <BLUE>Exhaust</BLUE>."},

    "Deep Breath": {"Name": "Deep Breath","Draw":1,"Energy": 0,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Colorless","Info":"Shuffle your Discardpile into your Drawpile. Draw 1 card."},
    "Deep Breath +": {"Name": "Deep Breath +","Draw":2,"Energy": 0,"Type": "Skill" ,"Rarity": "Uncommon","Upgraded": True,"Owner":"Colorless","Info":"Shuffle your Discardpile into your Drawpile. Draw 2 card."},

    "Discovery" :{"Name": "Discovery","Energy": 1,"Exhaust":True ,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Colorless","Info":"Choose 1 of 3 random cards to add into your hand. It costs 0 this turn. <BLUE>Exhaust</BLUE>."},
    "Discovery +" :{"Name": "Discovery +","Energy": 0,"Exhaust":True ,"Type": "Skill" ,"Rarity": "Uncommon","Upgraded": True,"Owner":"Colorless","Info":"Choose 1 of 3 random cards to add into your hand. It costs 0 this turn. <BLUE>Exhaust</BLUE>."},

    "Dramatic Entrance": {"Name": "Dramatic Entrance","Damage":8,"Energy": 0,"Innate":True,"Type": "Attack" ,"Rarity": "Uncommon","Owner":"Colorless","Info":"Deal <red>8 damage</red> to ALL enemies. <BLUE>Innate.</BLUE>. <BLUE>Exhaust</BLUE>."},
    "Dramatic Entrance +": {"Name": "Dramatic Entrance","Damage":12,"Energy": 0,"Innate":True,"Type": "Attack" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Colorless","Info":"Deal <red>12 damage</red> to ALL enemies. <BLUE>Innate.</BLUE>. <BLUE>Exhaust</BLUE>."},
    
    "Enlightenment": {"Name": "Enlightenment","Energy": 0,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Colorless","Info":"Reduce the cost of all cards in your hand to <yellow>1 Energy</yellow> this turn."},
    "Enlightenment +": {"Name": "Enlightenment","Energy": 0,"Type": "Skill" ,"Rarity": "Uncommon","Upgraded": True,"Owner":"Colorless","Info":"Reduce the cost of all cards in your hand to <yellow>1 Energy</yellow> for the rest of the battle."},

    "Finesse": {"Name": "Finesse","Energy": 0,"Block":2,"Draw":1,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Colorless","Info":"Gain <green>2 Block</green>. Draw 1 card."},
    "Finesse +": {"Name": "Finesse +","Energy": 0,"Block":4,"Draw":1,"Type": "Skill" ,"Rarity": "Uncommon","Upgraded": True,"Owner":"Colorless","Info":"Gain <green>4 Block</green>. Draw 1 card."},
    
    "Flash of Steel": {"Name": "Flash of Steel","Energy": 0,"Damage":3,"Draw":1,"Type": "Attack" ,"Rarity": "Uncommon","Owner":"Colorless"},
    "Flash of Steel +": {"Name": "Flash of Steel +","Energy": 0,"Damage":5,"Draw":1,"Type": "Attack","Upgraded": True,"Rarity": "Uncommon","Owner":"Colorless"},

    "Forethought": {"Name": "Forethought","Back Putter":1,"Energy Change Type":"Energy changed until played","Energy Change":0,"Energy": 0 ,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Colorless","Info":"Put a Card from your hand to the bottom of your draw pile. It costs 0 until played."},
    "Forethought +": {"Name": "Forethought +","Energy Change Type":"Energy changed until played","Energy Change":0,"Energy": 0 ,"Type": "Skill" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Colorless","Info":"Put any number of Cards from your hand to the bottom of your draw pile. It costs 0 until played."},

    "Good Instincts": {"Name": "Good Instincts","Energy": 0,"Block":6,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Colorless","Info":"Gain <green>6 Block</green>."},
    "Good Instincts +": {"Name": "Good Instincts +","Energy": 0,"Block":9,"Type": "Skill" ,"Rarity": "Uncommon","Upgraded": True,"Owner":"Colorless","Info":"Gain <green>9 Block</green>."},

    "Impatience": {"Name": "Impatience","Energy": 0,"Draw":2,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Colorless","Info":"If you have no <red>Attacks</red> in your hand, draw 2 cards."},
    "Impatience +": {"Name": "Impatience +","Energy": 0,"Draw":3,"Type": "Skill" ,"Rarity": "Uncommon","Upgraded": True,"Owner":"Colorless","Info":"If you have no <red>Attacks</red> in your hand, draw 3 cards."},

    "Jack of All Trades": {"Name": "Jack of All Trades","Energy": 0,"Draw":1,"Exhaust":True,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Colorless","Info":"Add 1 random Colorless card into your hand. <BLUE>Exhaust<BLUE>."},
    "Jack of All Trades +": {"Name": "Jack of All Trades +","Energy": 0,"Draw":2,"Exhaust":True,"Upgraded": True,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Colorless","Info":"Add 2 random Colorless card into your hand. <BLUE>Exhaust<BLUE>."},

    "Madness": {"Name": "Madness","Energy": 1,"Exhaust":True,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Colorless","Info":"Reduce the cost of a random card in your hand to <yellow>0 Energy</yellow> this combat. <BLUE>Exhaust<BLUE>."},
    "Madness +": {"Name": "Madness","Energy": 0,"Exhaust":True,"Type": "Skill" ,"Rarity": "Uncommon","Upgraded": True,"Owner":"Colorless","Info":"Reduce the cost of a random card in your hand to <yellow>0 Energy</yellow> this combat. <BLUE>Exhaust<BLUE>."},

    "Mind Blast": {"Name": "Mind Blast","Energy": 2,"Innate":True,"Type": "Attack" ,"Rarity": "Uncommon","Owner":"Colorless","Info":"<BLUE>Innate</BLUE>.Deal <red>damage</red> equal to the number of cards in your draw pile."},
    "Mind Blast +": {"Name": "Mind Blast +","Energy": 1,"Innate":True,"Type": "Attack" ,"Rarity": "Uncommon","Upgraded": True,"Owner":"Colorless","Info":"<BLUE>Innate</BLUE>.Deal <red>damage</red> equal to the number of cards in your draw pile."},

    "Panacea": {"Name": "Panacea","Energy": 0,"Artifact":1, "Exhaust":True,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Colorless","Info":"Gain <light-red>1 Artifact</light-red>. <BLUE>Exhaust</BLUE>."},
    "Panacea +": {"Name": "Panacea +","Energy": 0,"Artifact":2, "Exhaust":True,"Type": "Skill" ,"Rarity": "Uncommon","Upgraded": True,"Owner":"Colorless","Info":"Gain <light-red>2 Artifact</light-red>. <BLUE>Exhaust</BLUE>."},

    "Panic Button": {"Name": "Panic Button","Energy": 0,"Block":30,"NoBlock":2, "Exhaust":True,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Colorless","Info":"Gain <green>30 Block</green>. You can't gain <green>Block</green> for 2 turns."},
    "Panic Button +": {"Name": "Panic Button +","Energy": 0,"Block":40,"NoBlock":2, "Exhaust":True,"Type": "Skill" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Colorless","Info":"Gain <green>40 Block</green>. You can't gain <green>Block</green> for 2 turns."},

    "Purify": {"Name": "Purify","Energy": 0,"Exhausting":3, "Exhaust":True,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Colorless","Info":"Exhaust up to 3 Cards. <BLUE>Exhaust</BLUE>."},
    "Purify +": {"Name": "Purify +","Energy": 0,"Exhausting":5, "Exhaust":True,"Type": "Skill" ,"Rarity": "Uncommon","Upgraded": True,"Owner":"Colorless","Info":"Exhaust up to 5 Cards. <BLUE>Exhaust</BLUE>."},

    "Swift Strike": {"Name": "Swift Strike","Damage":7,"Energy": 0,"Type": "Attack" ,"Rarity": "Uncommon","Owner":"Colorless","Info":"Deal <red>7 damage</red>."},
    "Swift Strike +": {"Name": "Swift Strike +","Damage":10,"Energy": 0,"Type": "Attack" ,"Rarity": "Uncommon","Upgraded": True,"Owner":"Colorless","Info":"Deal <red>10 damage</red>."},

    "Apotheosis": {"Name": "Apotheosis","Energy": 2,"Type": "Skill","Exhaust":True ,"Rarity": "Rare","Owner":"Colorless","Info":"Upgrade ALL Cards for this battle. <BLUE>Exhaust</BLUE>."},
    "Apotheosis +": {"Name": "Apotheosis +","Energy": 1,"Type": "Skill","Exhaust":True ,"Rarity": "Rare","Upgraded": True,"Owner":"Colorless","Info":"Upgrade ALL Cards for this battle. <BLUE>Exhaust</BLUE>."},

    "Chrysalis": {"Name": "Chrysalis","Cards":3,"Energy": 2,"Type": "Skill","Exhaust":True ,"Rarity": "Rare","Owner":"Colorless","Info":"Shuffle <green>3 random Skills</green> into your draw pile. They cost 0 this combat. <BLUE>Exhaust</BLUE>."},
    "Chrysalis +": {"Name": "Chrysalis +","Cards":5,"Energy": 2,"Type": "Skill","Exhaust":True ,"Rarity": "Rare","Upgraded": True,"Owner":"Colorless","Info":"Shuffle <green>5 random Skills</green> into your draw pile. They cost 0 this combat. <BLUE>Exhaust</BLUE>."},

    "Hand of Greed": {"Name": "Hand of Greed","Damage":20,"Gold":20,"Energy": 2,"Type": "Attack" ,"Rarity": "Rare","Owner":"Colorless","Info":"Deal <red>20 damage</red>. If this kills the enemy, gain <yellow>20 Gold</yellow>."},
    "Hand of Greed +": {"Name": "Hand of Greed +","Damage":25,"Gold":25,"Energy": 2,"Type": "Attack" ,"Upgraded": True,"Rarity": "Rare","Owner":"Colorless","Info":"Deal <red>25 damage</red>. If this kills the enemy, gain <yellow>25 Gold</yellow>."},

    "Magnetism": {"Name": "Magnetism","Energy": 2,"Type": "Power","Rarity": "Rare","Owner":"Colorless","Info":"At the start of your turn, add a random Colorless card into your hand."},
    "Magnetism +": {"Name": "Magnetism +","Energy": 1,"Type": "Power","Rarity": "Rare","Upgraded": True,"Owner":"Colorless","Info":"At the start of your turn, add a random Colorless card into your hand."},

    "Master of Strategy": {"Name": "Master of Strategy","Draw":3,"Energy": 0,"Exhaust":True,"Type": "Skill","Rarity": "Rare","Owner":"Colorless","Info":"Draw 3 Cards. <BLUE>Exhaust</BLUE>."},
    "Master of Strategy +": {"Name": "Master of Strategy +","Draw":4,"Energy": 0,"Exhaust":True,"Type": "Skill","Upgraded": True,"Rarity": "Rare","Owner":"Colorless","Info":"Draw 4 Cards. <BLUE>Exhaust</BLUE>."},

    "Mayhem": {"Name": "Mayhem","Energy": 2,"Type": "Power","Rarity": "Rare","Owner":"Colorless","Info":"At the start of your turn, play the top card of your Drawpile."},
    "Mayhem +": {"Name": "Mayhem +","Energy": 1,"Type": "Power","Rarity": "Rare","Upgraded": True,"Owner":"Colorless","Info":"At the start of your turn, play the top card of your Drawpile."},
    
    "Metamorphosis": {"Name": "Metamorphosis","Energy": 2,"Cards":3,"Exhaust":True,"Type": "Skill","Rarity": "Rare","Owner":"Colorless","Info":"Shuffle <red>3 random Attacks</red> into your draw pile. They cost 0 this combat. <BLUE>Exhaust</BLUE>."},
    "Metamorphosis +": {"Name": "Metamorphosis +","Energy": 2,"Cards":5,"Exhaust":True,"Type": "Skill","Upgraded": True,"Rarity": "Rare","Owner":"Colorless","Info":"Shuffle <red>5 random Attacks</red> into your draw pile. They cost 0 this combat. <BLUE>Exhaust</BLUE>."},
    
    "Panache": {"Name": "Panache","Energy": 0,"Damage":10,"Type": "Power","Rarity": "Rare","Owner":"Colorless","Info":"Every time you play 5 cards in a single turn, deal <red>10 damage</red> to ALL enemies."},
    "Panache +": {"Name": "Panache +","Energy": 0,"Damage":14,"Type": "Power","Rarity": "Rare","Upgraded": True,"Owner":"Colorless","Info":"Every time you play 5 cards in a single turn, deal <red>14 damage</red> to ALL enemies."},
    
    "Sadistic Nature": {"Name": "Sadistic Nature","Energy": 0,"Damage":5,"Type": "Power","Rarity": "Rare","Owner":"Colorless","Info":"Whenever you apply a <light-cyan>debuff</light-cyan> to an enemy, they take <red>5 damage</red>."},
    "Sadistic Nature +": {"Name": "Sadistic Nature +","Energy": 0,"Damage":7,"Type": "Power","Upgraded": True,"Rarity": "Rare","Owner":"Colorless","Info":"Whenever you apply a <light-cyan>debuff</light-cyan> to an enemy, they take <red>7 damage</red>."},
    
    "Secret Technique": {"Name": "Secret Technique","Draw":1,"Place":"Drawpile","Typing": "Skill","Energy": 0,"Type": "Skill","Exhaust":True,"Rarity": "Rare","Owner":"Colorless","Info":"Put a <green>Skill</green> from your Drawpile into your hand. <BLUE>Exhaust</BLUE>."},
    "Secret Technique +": {"Name": "Secret Technique +","Draw":1,"Place":"Drawpile","Typing": "Skill","Upgraded": True,"Energy": 0,"Type": "Skill","Rarity": "Rare","Owner":"Colorless","Info":"Put a <green>Skill</green> from your Drawpile into your hand."},

    "Secret Weapon": {"Name": "Secret Weapon","Draw":1,"Place":"Drawpile","Typing": "Attack","Energy": 0,"Type": "Skill","Exhaust":True,"Rarity": "Rare","Owner":"Colorless","Info":"Put a <red>Attack</red> from your Drawpile into your hand. <BLUE>Exhaust</BLUE>"},
    "Secret Weapon +": {"Name": "Secret Weapon +","Draw":1,"Place":"Drawpile","Typing": "Attack","Energy": 0,"Upgraded": True,"Type": "Skill","Rarity": "Rare","Owner":"Colorless","Info":"Put a <red>Attack</red> from your Drawpile into your hand."},

    "The Bomb": {"Name": "The Bomb","Energy": 2,"Damage":40,"Type": "Skill","Rarity": "Rare","Owner":"Colorless","Info":"At the end of 3 turns, deal <red>40 damage</red> to ALL enemies."},
    "The Bomb +": {"Name": "The Bomb +","Energy": 2,"Damage":50,"Type": "Skill","Rarity": "Rare","Upgraded": True,"Owner":"Colorless","Info":"At the end of 3 turns, deal <red>50 damage</red> to ALL enemies."},
    
    "Thinking Ahead": {"Name": "Thinking Ahead","Energy": 0,"Draw":2,"Back Putter": 1,"Exhaust":True,"Type": "Skill","Rarity": "Rare","Owner":"Colorless","Info":"Draw 2 Cards. Put a Card from your hand on top of your Drawpile. <BLUE>Exhaust</BLUE>."},
    "Thinking Ahead +": {"Name": "Thinking Ahead +","Energy": 0,"Draw":2,"Back Putter": 1,"Type": "Skill","Upgraded": True,"Rarity": "Rare","Owner":"Colorless","Info":"Draw 3 Cards. Put a Card from your hand on top of your Drawpile. <BLUE>Exhaust</BLUE>."},

    "Transmutation": {"Name": "Transmutation","Energy": "X","Exhaust":True,"Type": "Skill","Rarity": "Rare","Owner":"Colorless","Info":"Add X random Colorless Cards into your hand. They cost <yellow>0 Energy</yellow> this turn. <BLUE>Exhaust</BLUE>."},
    "Transmutation +": {"Name": "Transmutation +","Energy": "X","Exhaust":True,"Type": "Skill","Rarity": "Rare","Upgraded": True,"Owner":"Colorless","Info":"Add X random <blue>upgraded</blue> Colorless Cards into your hand. They cost <yellow>0 Energy</yellow> this turn. <BLUE>Exhaust</BLUE>."},

    "Violence": {"Name": "Violence","Energy": 0,"Draw":3,"Place":"Drawpile","Typing":"Attack","Exhaust":True,"Type": "Skill","Rarity": "Rare","Owner":"Colorless","Info":"Put <red>3 random Attacks</red> from your Drawpile into your hand. <BLUE>Exhaust</BLUE>."},
    "Violence +": {"Name": "Violence +","Energy": 0,"Draw":4,"Place":"Drawpile","Typing":"Attack","Exhaust":True,"Upgraded": True,"Type": "Skill","Rarity": "Rare","Owner":"Colorless","Info":"Put <red>4 random Attacks</red> from your Drawpile into your hand. <BLUE>Exhaust</BLUE>."},
    
    "Apparition": {"Name": "Apparition","Energy": 1,"Intangible":1,"Exhaust":True,"Ethereal":True,"Type": "Skill","Rarity": "Special","Owner":"Colorless","Info":"<BLUE>Ethereal</BLUE>. Gain <blue>1 Intangible</blue>. <BLUE>Exhaust</BLUE>."},
    "Apparition +": {"Name": "Apparition +","Energy": 1,"Intangible":1,"Exhaust":True,"Type": "Skill","Upgraded": True,"Rarity": "Special","Owner":"Colorless","Info":"Gain <blue>1 Intangible</blue>. <BLUE>Exhaust</BLUE>."},

    "Ritual Dagger": {"Name": "Ritual Dagger","Energy": 1,"Damage":15,"FatalBonus":3,"Exhaust":True,"Type": "Attack","Rarity": "Special","Owner":"Colorless","Info":"Deal <red>15 damage</red>. If this kills the enemy, permanently increase this Card's <red>damage</red> by 3. <BLUE>Exhaust</BLUE>. UPGRADING THIS CARD IS CURRENLY ILL-ADVISED AS IT'S BUGGED!"},
    "Ritual Dagger +": {"Name": "Ritual Dagger +","Energy": 1,"Damage":15,"FatalBonus":5,"Exhaust":True,"Upgraded": True,"Type": "Attack","Rarity": "Special","Owner":"Colorless","Info":"Deal <red>15 damage</red>. If this kills the enemy, permanently increase this Card\'s <red>damage</red> by 5. <BLUE>Exhaust</BLUE>."},

    "Bite": {"Name": "Bite", "Damage":7,"Heal":2, "Energy": 1,"Type": "Attack" ,"Rarity": "Special","Owner":"Colorless","Info":"Deal <red>6 damage</red>."},
    "Bite +": {"Name": "Bite +","Upgraded": True, "Damage":8,"Heal":3, "Energy": 1,"Type": "Attack" ,"Rarity": "Special","Owner":"Colorless","Info":"Deal <red>9 damage</red>."},

    "JAX": {"Name": "JAX","Energy": 0,"Strength":2,"Harm":3,"Type": "Skill","Rarity": "Special","Owner":"Colorless","Info":"Lose <red>3 HP</red>. Gain <red>2 Strength</red>."},
    "JAX +": {"Name": "JAX +","Energy": 0,"Strength":3,"Harm":3,"Upgraded": True,"Type": "Skill","Rarity": "Special","Owner":"Colorless","Info":"Lose <red>3 HP</red>. Gain <red>3 Strength</red>."},

    "Slimed": {"Name": "Slimed", "Energy": 1, "Exhaust": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire","Info":"<BLUE>Exhaust</BLUE>."},
    
    "Dazed": {"Name": "Dazed", "Ethereal": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire","Info":"<BLUE>Ethereal</BLUE>. <RED>Unplayable</RED>."},
    
    "Void": {"Name": "Void", "Ethereal": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire","Info":"<RED>Unplayable</RED> Whenever this card is drawn, lose <yellow>1 Energy</yellow>. <BLUE>Ethereal</BLUE>."},

    "Burn" : {"Name": "Burn", "DiscardDamage": 2, "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>. At the end of your turn, take <red>2 damage</red>."},
    "Burn +": {"Name": "Burn +", "DiscardDamage": 4, "Type": "Status", "Rarity": "Enemy","Upgraded": True,"Owner":"The Spire","Info":"<RED>Unplayable</RED>. At the end of your turn, take <red>4 damage</red>."},
    "Wound" : {"Name": "Wound", "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>."},


    "Clumsy": {"Name": "Clumsy","Ethereal":True,"Type": "Curse","Rarity": "Curse","Owner":"The Spire","Info":"<BLUE>Ethereal</BLUE>. <RED>Unplayable</RED>."},
    "Injury": {"Name": "Injury","Type": "Curse","Rarity": "Curse","Owner":"The Spire","Info":"<RED>Unplayable</RED>."},
    "Decay": {"Name": "Decay","Type": "Curse","Rarity": "Curse","Owner":"The Spire","Info":"<RED>Unplayable</RED>. At the end of your turn, take <red>2 damage</red>."},
    "Parasite": {"Name": "Parasite","Type": "Curse","Rarity": "Curse","Owner":"The Spire","Info":"<RED>Unplayable</RED> If transformed or removed from your deck, lose <red>3 Max HP</red>."},
    "Regret": {"Name": "Regret","Type": "Curse","Rarity": "Curse","Owner":"The Spire","Info":"<RED>Unplayable</RED>. At the end of your turn, lose <red>1 HP</red> for each Card in your hand."},
    "Shame": {"Name": "Shame","Type": "Curse","Rarity": "Curse","Owner":"The Spire","Info":"<RED>Unplayable</RED>. At the end of your turn, gain <light-cyan>1 Frail</light-cyan>."},
    "Doubt": {"Name": "Doubt","Type": "Curse","Rarity": "Curse","Owner":"The Spire","Info":"<RED>Unplayable</RED>. At the end of your turn, gain <light-cyan>1 Weak</light-cyan>."},
    "Pain": {"Name": "Pain","Type": "Curse","Rarity": "Curse","Owner":"The Spire","Info":"<RED>Unplayable</RED>. While in hand, lose <red>1 HP</red> when other cards are played."},
    "Writhe": {"Name": "Writhe","Innate": True,"Type": "Curse","Rarity": "Curse","Owner":"The Spire","Info":"<RED>Unplayable</RED>. <BLUE>Innate</BLUE>."},
    "Normality": {"Name": "Normality","Type": "Curse","Rarity": "Curse","Owner":"The Spire","Info":"<RED>Unplayable</RED>. You cannot play more than 3 Cards this turn."},
    
    "Curse of the Bell": {"Name": "Curse of the Bell","Type": "Curse","Rarity": "Special","Owner":"The Spire","Info":"<RED>Unplayable</RED>. Cannot be removed from your deck."},
    "Necronomicurse": {"Name": "Necronomicurse","Type": "Curse","Rarity": "Special","Owner":"The Spire","Info":"<RED>Unplayable</RED>. Cannot be removed from your deck."},
    "Ascender's Bane": {"Name": "Ascender's Bane","Ethereal":True,"Type": "Curse","Rarity": "Special","Owner":"The Spire","Info":"<BLUE>Ethereal</BLUE>. <RED>Unplayable</RED>."},
    }

potions = {
    
    "Ancient Potion": {"Name": "Ancient Potion", "Potion Yield":1, "Rarity": "Uncommon","Owner":"The Spire","Type": "Potion","Info":"Gain <light-red>1 Artifact</light-red>."},
    "Attack Potion": {"Name": "Attack Potion","Potion Yield": 1, "Rarity": "Common","Owner":"The Spire","Type": "Potion","Info":"Choose 1 of <red>3 random Attack</red> Cards to add into your hand. It costs <yellow>0 Energy</yellow> this turn."},
    "Blessing of the Forge": {"Name": "Blessing of the Forge","Rarity": "Common","Owner":"The Spire","Type": "Potion","Type": "Potion","Info":"<blue>Upgrade</blue> ALL cards in your hand."},
    "Block Potion": {"Name": "Block Potion","Potion Yield": 12,"Rarity": "Common","Owner":"The Spire","Type": "Potion","Info":"Gain <green>12 Block</green>."},
    "Blood Potion": {"Name": "Blood Potion","Rarity": "Common","Owner":"The Spire","Type": "Potion","Info":"<red>Heal for 20%</red> of your <red>Max HP</red>."},
    "Colorless Potion": {"Name": "Colorless Potion","Potion Yield": "Colorless", "Rarity": "Common","Owner":"The Spire","Type": "Potion","Info":"Choose 1 of <white>3 random Colorless</white> Cards to add into your hand. It costs <yellow>0 Energy</yellow> this turn."},
    "Cultist Potion": {"Name": "Cultist Potion","Potion Yield":1,"Rarity": "Rare","Owner":"The Spire","Type": "Potion","Info":"Gain <red>1 Strength</red> at the start of each turn."},
    "Cunning Potion": {"Name": "Cunning Potion","Potion Yield":3,"Rarity": "Uncommon","Owner":"Silent","Type": "Potion","Info":"Add <red>3 upgraded Shivs</red> to your hand."},
    "Dexterity Potion": {"Name": "Dexterity Potion","Potion Yield":2,"Rarity": "Common","Owner":"The Spire","Type": "Potion","Info":"Gain <green>2 Dexterity</green>."},
    "Strength Potion": {"Name": "Strength Potion","Potion Yield":2,"Rarity": "Common","Owner":"The Spire","Type": "Potion","Info":"Gain <red>2 Strength</red>."},
    "Distilled Chaos": {"Name": "Distilled Chaos","Potion Yield":3,"Rarity": "Uncommon","Owner":"The Spire","Type": "Potion","Info":"Play the top 3 Cards of your Drawpile."},
    "Duplication Potion": {"Name": "Duplication Potion","Potion Yield":1,"Rarity": "Uncommon","Owner":"The Spire","Type": "Potion","Info":"This turn, your next Card is played twice."},
    "Energy Potion": {"Name": "Energy Potion","Potion Yield":2,"Rarity": "Common","Owner":"The Spire","Type": "Potion","Info":"Gain <yellow>2 Energy</yellow>."},

    "Entropic Brew": {"Name": "Entropic Brew","Rarity": "Rare","Owner":"The Spire","Type": "Potion","Info":"Fill all your empty <c>potion slots</c> with <c>random potions</c>."},
    
    "Essence of Steel": {"Name": "Essence of Steel","Potion Yield": 4,"Rarity": "Uncommon","Owner":"The Spire","Type": "Potion","Info":"Gain <green>4 Plated Armor</green>."},
    "Explosive Potion": {"Name": "Explosive Potion","Potion Yield": 10,"Rarity": "Uncommon","Owner":"The Spire","Type": "Potion","Info":"<Deal <red>10 damage</red> to all enemies."},
    "Fairy in a Bottle": {"Name": "Fairy in a Bottle","Rarity": "Rare","Owner":"The Spire","Type": "Potion","Info":"When you would <black>die</black>, <red>heal to 30\% of your Max HP</red> instead and discard this <c>Potion</c>."},
    "Fear Potion": {"Name": "Fear Potion","Potion Yield": 3,"Rarity": "Common","Owner":"The Spire","Type": "Potion","Info":"Apply <light-cyan>3 Vulnerable</light-cyan>."},
    "Fire Potion": {"Name": "Fire Potion","Potion Yield": 20,"Rarity": "Common","Owner":"The Spire","Type": "Potion","Info":"Deal <red>20 damage</red> to target enemy."},
    "Fruit Juice": {"Name": "Fruit Juice","Potion Yield": 5,"Rarity": "Rare","Owner":"The Spire","Type": "Potion","Info":"Gain <red>5 Max HP</red>."},
    "Gamblers Brew": {"Name": "Gamblers Brew","Rarity": "Uncommon","Owner":"The Spire","Type": "Potion","Info":"Discard any number of Cards, then draw that many."},

    "Ghost in a Jar": {"Name": "Ghost in a Jar","Potion Yield": 1,"Rarity": "Uncommon","Owner":"The Spire","Type": "Potion","Info":"Gain <blue>1 Intangible</blue>."},
    "Liquid Bronze": {"Name": "Liquid Bronze","Potion Yield": 3,"Rarity": "Uncommon","Owner":"The Spire","Type": "Potion","Info":"Gain <blue>3 Thorns</blue>."},
    
    "Liquid Memories": {"Name": "Liquid Memories","Rarity": "Uncommon","Owner":"The Spire","Type": "Potion","Info":"Choose a card in your Discardpile and return it to your hand. It costs <yellow>0 Energy</yellow> this turn."},
    
    "Poison Potion": {"Name": "Poison Potion","Potion Yield":6,"Rarity": "Common","Owner":"The Spire","Type": "Potion","Info":"Apply <green>6 Poison</green> to target enemy."},
    "Power Potion": {"Name": "Power Potion","Potion Yield":1,"Rarity": "Common","Owner":"The Spire","Type": "Potion","Info":"Add 1 of 3 random <blue>Power Cards</blue> to your hand, it costs <yellow> 0 Energy</yellow> this turn."},
    "Regen Potion": {"Name": "Regen Potion","Potion Yield":5,"Rarity": "Uncommon","Owner":"The Spire","Type": "Potion","Info":"Gain <green>6 Regeneration</green>."},
    "Skill Potion": {"Name": "Skill Potion","Potion Yield":1,"Rarity": "Common","Owner":"The Spire","Type": "Potion","Info":"Choose 1 of 3 <green>random Skill</green> Cards to add into your hand. It costs <yellow>0 Energy</yellow> this turn."},
    "Smoke Bomb": {"Name": "Smoke Bomb","Rarity": "Rare","Owner":"The Spire","Type": [False,"Potion"],"Info":"Escape from a non-boss combat. Receive no rewards."},
    "Snecko Oil": {"Name": "Snecko Oil","Potion Yield":5,"Rarity": "Rare","Owner":"The Spire","Type": "Potion","Info":"Draw 5 Cards. Randomize the costs of all Cards in your hand for the rest of the combat."},
    "Speed Potion": {"Name": "Speed Potion","Potion Yield":5,"Rarity": "Common","Owner":"The Spire","Type": "Potion","Info":"Gain <green>5 Dexterity</green>. At the end of your turn lose <green>5 Dexterity</green>."},
    "Flex Potion": {"Name": "Flex Potion","Potion Yield":5,"Rarity": "Common","Owner":"The Spire","Type": "Potion","Info":"Gain <red>5 Strength</red>. At the end of your turn lose <red>5 Strength</red>."},
    "Swift Potion": {"Name": "Swift Potion","Potion Yield": 3,"Rarity": "Common","Owner":"The Spire","Type": "Potion","Info":"Draw 3 Cards."},
    "Weak Potion": {"Name": "Weak Potion","Potion Yield": 3,"Rarity": "Common","Owner":"The Spire","Type": "Potion","Info":"Apply <light-cyan>3 Weak</light-cyan>."},
        
    }

potionNames = ["Ancient Potion","Attack Potion","Blessing of the Forge","Block Potion","Blood Potion","Colorless Potion","Cultist Potion",
"Cunning Potion","Dexterity Potion","Strength Potion","Distilled Chaos","Duplication Potion","Energy Potion","Entropic Brew","Essence of Steel",
"Explosive Potion","Fairy in a Bottle","Fear Potion","Fire Potion","Fruit Juice","Gamblers Brew","Ghost in a Jar","Liquid Bronze","Liquid Memories",
"Poison Potion","Power Potion","Regen Potion","Skill Potion","Smoke Bomb","Snecko Oil","Speed Potion","Flex Potion","Swift Potion","Weak Potion"]


relics = {
	
	"Ring of the Snake": {"Name":"Ring of the Snake","Rarity":"Starter","Owner":"Silent","Type":"Relic","Info":"At the start of each combat, draw 2 additional cards."},
	"Akabeko":{"Name":"Akabeko","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Your first attack each combat deals <red>8 additional damage</red>"},
	"Anchor":{"Name":"Anchor","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Start each combat with <green>10 Block</green>."},
	"Ancient Tea Set":{"Name":"Ancient Tea Set","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Whenever you enter a <blue>Rest Site</blue>, start the next combat with <yellow>2 extra Energy</yellow>."},
	"Art of War":{"Name":"Art of War","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"If you do not play any <red>Attacks</red> during your turn, gain <yellow>1 extra Energy</yellow> next turn."},
	"Bag of Marbles":{"Name":"Bag of Marbles","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"At the start of each combat, apply <light-cyan>1 Vulnerable</light-cyan> to ALL enemies."},
	"Bag of Preparation":{"Name":"Bag of Preparation","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"At the start of each combat, draw 2 additional cards."},
	"Blood Vial":{"Name":"Blood Vial","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"At the start of each combat, <red>heal 2 HP</red>."},
	"Bronze Scales":{"Name":"Bronze Scales","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Start each combat with <blue>3 Thorns</blue>."},
	"Centennial Puzzle":{"Name":"Centennial Puzzle","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"The first time you lose HP each combat, draw 3 cards."},
	"Ceramic Fish":{"Name":"Ceramic Fish","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Whenever you add a Card to your deck, gain <yellow>9 gold</yellow>."},
	"Dream Catcher":{"Name":"Dream Catcher","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Whenever you <blue>rest</blue>, you may add a Card to your deck."},
	"Happy Flower":{"Name":"Happy Flower","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Every 3 turns, gain <yellow>1 Energy</yellow>."},
	"Juzu Bracelet":{"Name":"Juzu Bracelet","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Regular enemy combats are no longer encountered in <blue>Event rooms</blue>."},
	"Lantern":{"Name":"Lantern","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Gain <yellow>1 Energy</yellow> on the first turn of each combat."},
	"Maw Bank":{"Name":"Maw Bank","Working":True,"Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Whenever you climb a floor, gain <yellow>12 Gold</yellow>. No longer works when you spend any Gold at the <yellow>Shop$</yellow>."},
	"Meal Ticket":{"Name":"Meal Ticket","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Whenever you enter a <yellow>Shop$</yellow> room, <red>heal 15 HP</red>."},
	"Nunchaku":{"Name":"Nunchaku","Counter":0,"Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Every time you play <red>10 Attacks</red>, gain <yellow>1 Energy</yellow>."},
	"Oddly Smooth Stone":{"Name":"Oddly Smooth Stone","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"At the start of each combat, gain <green>1 Dexterity</green>."},
	"Omamori":{"Name":"Omamori","Counter":2,"Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Negate the next <m>2 Curses</m> you obtain."},
	"Orichalcum":{"Name":"Orichalcum","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"If you end your turn without <green>Block</green>, gain <green>6 Block</green>."},
	
	"Pen Nib":{"Name":"Pen Nib","Counter":0,"Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Every <red>10th Attack</red> you play deals double damage."},
	
	"Potion Belt":{"Name":"Potion Belt","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Upon pick up, gain <c>2 Potion slots</c>."},
	"Preserved Insect":{"Name":"Preserved Insect","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Enemies in Elite rooms have <red>25\% less HP</red>."},
	"Regal Pillow":{"Name":"Regal Pillow","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"<red>Heal an additional 15</red> HP when you <blue>rest</blue>."},
	"Smiling Mask":{"Name":"Smiling Mask","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"The <yellow>Merchant's</yellow> Card removal service now always costs <yellow>50 Gold</yellow>."},
	"Snecko Skull":{"Name":"Snecko Skull","Rarity":"Common","Owner":"Silent","Type":"Relic","Info":"Whenever you apply <green>Poison</green>, apply an additional <green>1 Poison</green>."},
	"Strawberry":{"Name":"Strawberry","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"If you end your turn without <green>Block</green>, gain <green>6 Block</green>."},
	"The Boot":{"Name":"The Boot","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Whenever you would deal <red>4 or less unblocked Attack damage</red>, increase it to <red>5</red>."},	
	"Tiny Chest":{"Name":"Tiny Chest","Rarity":"Common","Counter":0,"Owner":"The Spire","Type":"Relic","Info":"Every 4th <blue>Event</blue> room is a <yellow>Treasure</yellow> room."},
	"Toy Ornithopter":{"Name":"Toy Ornithopter","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Whenever you drink a <c>Potion</c>, <red>heal 5 HP</red>."},
	"Vajra":{"Name":"Vajra","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"At the start of each combat, gain <red>1 Strength</red>."},
	"War Paint":{"Name":"War Paint","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Upon pickup upgrade <green>2 random Skills</green>."},
	"Whetstone":{"Name":"Whetstone","Rarity":"Common","Owner":"The Spire","Type":"Relic","Info":"Upon pickup upgrade <red>2 random Attacks</red>."},
	
	"Blue Candle":{"Name":"Blue Candle","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"<m>Curse</m> Cards can now be played. Playing a <m>Curse</m> will make you <red>lose 1 HP</red> and Exhausts the Card."},
	"Bottled Flame":{"Name":"Bottled Flame","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"Upon pick up, choose an <red>Attack</red>. Start each combat with this Card in your hand."},
	"Bottled Lightning":{"Name":"Bottled Lightning","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"Upon pick up, choose a <green>Skill</green>. Start each combat with this Card in your hand."},
	"Bottled Tornado":{"Name":"Bottled Tornado","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"Upon pick up, choose a <blue>Power</blue>. Start each combat with this Card in your hand."},
	"Darkstone Periapt":{"Name":"Darkstone Periapt","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"Whenever you obtain a <m>Curse</m>, increase your <red>Max HP by 6</red>."},
	"Eternal Feather":{"Name":"Eternal Feather","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"For every 5 Cards in your deck, <red>heal 3</red> HP whenever you enter a <blue>Rest Site</blue>."},
	"Frozen Egg":{"Name":"Frozen Egg","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"Whenever you add a <blue>Power</blue> to your deck, it is Upgraded."},
	"Gremlin Horn":{"Name":"Gremlin Horn","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"Whenever an enemy dies, gain <yellow>1 Energy</yellow> and draw 1 Card."},
	"Horn Cleat":{"Name":"Horn Cleat","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"At the start of your 2nd turn, gain <green>14 Block</green>."},
	"Ink Bottle":{"Name":"Ink Bottle","Counter":0,"Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"Whenever you play 10 cards, draw 1 Card."},
	"Kunai":{"Name":"Kunai","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"Every time you play <red>3 Attacks</red> in a single turn, gain <green>1 Dexterity</green>."},
	"Letter Opener":{"Name":"Letter Opener","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"Every time you play <green>3 Skills</green> in a single turn, deal <red>5 damage</red> to ALL enemies."},
	"Matryoshka":{"Name":"Matryoshka","Counter":2,"Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"The next <yellow>2 Chests</yellow> you open contain <light-red>2 Relics</light-red>."},
	"Meat on the Bone":{"Name":"Meat on the Bone","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"If your <red>HP</HP> is at or below 50\% at the end of combat, <red>heal 12 HP</red>."},
	"Mercury Hourglass":{"Name":"Mercury Hourglass","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"At the start of your turn, deal <red>3 damage</red> to ALL enemies."},
	"Molten Egg":{"Name":"Molten Egg","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"Whenever you add an <red>Attack</red> to your deck, it is Upgraded."},
	"Mummified Hand":{"Name":"Mummified Hand","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"Whenever you play a <blue>Power</blue>, a random card in your hand costs <yellow>0 Energy</yellow> for the turn."},
	"Ninja Scroll":{"Name":"Ninja Scroll","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"Start each combat with <red>3 Shivs</red> in hand."},
	"Ornamental Fan":{"Name":"Ornamental Fan","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"Every time you play <red>3 Attacks</red> in a single turn, gain <green>4 Block</green>."},
	
	"Pantograph":{"Name":"Pantograph","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"At the start of <black>Boss</black> combats, <red>heal 25 HP</red>."},
	"Paper Krane":{"Name":"Paper Krane","Rarity":"Uncommon","Owner":"Silent","Type":"Relic","Info":"Enemies with <light-cyan>Weak</light-cyan> deal 50\% less damage rather than 25\%."},
	"Pear":{"Name":"Pear","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"Raise your <red>Max HP by 10</red>."},
	"Question Card":{"Name":"Question Card","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"On future Card Reward screens you have 1 additional Card to choose from."},
	"Shuriken":{"Name":"Shuriken","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"Every time you play <red>3 Attacks</red> in a single turn, gain <red>1 Strength</red>."},
	"Singing Bowl":{"Name":"Singing Bowl","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"When adding Cards to your deck, you may gain <red>+2 Max HP</red> instead."},
	"Strike Dummy":{"Name":"Strike Dummy","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"Cards containing \"Strike\" deal <red>3 additional damage</red>."},
	"Sundial":{"Name":"Sundial","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"Every 3 times you shuffle your Drawpile, gain <yellow>2 Energy</yellow>."},
	"The Courier":{"Name":"The Courier","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"The <yellow>merchant</yellow> no longer runs out of Cards, <light-red>Relics</light-red>, or <c>Potions</c> and his prices are reduced by 20%."},
	"Toxic Egg":{"Name":"Toxic Egg","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"Whenever you add a <green>Skill</green> to your deck, it is Upgraded."},

	"White Beast Statue":{"Name":"White Beast Statue","Rarity":"Uncommon","Owner":"The Spire","Type":"Relic","Info":"<c>Potions</c> always drop after combat."},
	
	"Bird-Faced Urn":{"Name":"Bird-Faced Urn","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"Whenever you play a <blue>Power</blue>, <red>heal 2 HP</red>."},
	"Calipers":{"Name":"Calipers","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"At the start of your turn, lose <green>15 Block</green> rather than all of your <green>Block</green>."},
	"Captain's Wheel":{"Name":"Captain's Wheel","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"At the start of your 3rd turn, gain <green>18 Block</green>."},
	"Dead Branch":{"Name":"Dead Branch","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"Whenever you Exhaust a Card, add a random Card to your hand."},
	"Du-Vu Doll":{"Name":"Du-Vu Doll","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"For each <m>Curse</m> in your deck, start each combat with <red>1 additional Strength</red>."},
	"Fossilized Helix":{"Name":"Fossilized Helix","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"Prevent the first time you would <red>lose HP</red> in combat."},
	
    "Ginger":{"Name":"Ginger","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"You can no longer become <light-cyan>Weakened</light-cyan>."},
	
    "Girya":{"Name":"Girya","Counter":3,"Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"You can now gain <red>Strength</red> at <blue>Rest Sites</blue>. (3 times max)"},
	"Ice Cream":{"Name":"Ice Cream","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"<yellow>Energy</yellow> is now conserved between turns."},
	"Lizard Tail":{"Name":"Lizard Tail","Counter":1,"Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"When you would <black>die</black>, <red>heal to 50\%</red> of your </red>Max HP</red> instead (works once)."},
	"Mango":{"Name":"Mango","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"Upon pickup, raise your <red>Max HP by 14</red>."},
	"Old Coin":{"Name":"Old Coin","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"Gain <yellow>300 Gold</yellow>."},
	"Peace Pipe":{"Name":"Peace Pipe","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"You can now remove Cards from your deck at <blue>Rest Sites</blue>."},
	"Pocketwatch":{"Name":"Pocketwatch","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"Whenever you play 3 or less Cards in a turn, draw 3 additional Cards at the start of your next turn."},
	"Prayer Wheel":{"Name":"Prayer Wheel","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"Normal enemies drop an additional Card reward."},
	"Shovel":{"Name":"Shovel","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"You can now Dig for <light-red>Relics</light-red> at <blue>Rest Sites</blue>."},
	"Stone Calendar":{"Name":"Stone Calendar","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"At the end of turn 7, deal <red>52 damage</red> to ALL enemies."},
	"The Specimen":{"Name":"The Specimen","Rarity":"Rare","Owner":"Silent","Type":"Relic","Info":"Whenever an enemy <black>dies</black>, transfer any <green>Poison</green> it has to a random enemy."},
	

	"Thread and Needle":{"Name":"Thread and Needle","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"At the start of each combat, gain <green>4 Plated Armor</green>."},
	"Tingsha":{"Name":"Tingsha","Rarity":"Rare","Owner":"Silent","Type":"Relic","Info":"Whenever you discard a card during your turn, deal <red>3 damage</red> to a random enemy for each card discarded."},
	"Torii":{"Name":"Torii","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"Whenever you would receive <red>5 or less unblocked Attack damage</red>, reduce it to <red>1</red>."},
	"Tough Bandages":{"Name":"Tough Bandages","Rarity":"Rare","Owner":"Silent","Type":"Relic","Info":"Whenever you discard a Card during your turn, gain <green>3 Block</green>."},
	"Tungsten Rod":{"Name":"Tungsten Rod","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"Gain <yellow>300 Gold</yellow>."},
	"Turnip":{"Name":"Turnip","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"Gain <yellow>300 Gold</yellow>."},
	"Unceasing Top":{"Name":"Unceasing Top","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"Whenever you have no Cards in hand during your turn, draw a Card."},
	"Astrolabe":{"Name":"Astrolabe","Rarity":"Rare","Owner":"The Spire","Type":"Relic","Info":"Upon pickup, choose and Transform 3 Cards, then Upgrade them."},
	
    "Black Star":{"Name":"Black Star","Rarity":"Boss","Owner":"The Spire","Type":"Relic","Info":"Elites drop an additional <light-red>Relic</light-red> when defeated."},
    "Busted Crown":{"Name":"Busted Crown","Rarity":"Boss","Owner":"The Spire","Type":"Relic","Info":"Gain <yellow>1 Energy</yellow> at the start of each turn. On Card Reward screens, you have 2 fewer Cards to choose from."},
    "Calling Bell":{"Name":"Calling Bell","Rarity":"Boss","Owner":"The Spire","Type":"Relic","Info":"Upon pickup, obtain a unique <m>Curse</m> and <light-red>3 Relics</light-red>."},
    "Coffee Dripper":{"Name":"Coffee Dripper","Rarity":"Boss","Owner":"The Spire","Type":"Relic","Info":"Gain <yellow>1 Energy</yellow> at the start of each turn. You can no longer <blue>Rest at Rest Sites</blue>."},
    "Cursed Key":{"Name":"Cursed Key","Rarity":"Boss","Owner":"The Spire","Type":"Relic","Info":"Gain <yellow>1 Energy</yellow> at the start of each turn. Whenever you open a non-boss chest, obtain a <m>Curse</m>."},
    "Ectoplasm":{"Name":"Ectoplasm","Rarity":"Boss","Owner":"The Spire","Type":"Relic","Info":"Gain <yellow>1 Energy</yellow> at the start of each turn. You can no longer gain <yellow>Gold</yellow>."},
    "Empty Cage":{"Name":"Empty Cage","Rarity":"Boss","Owner":"The Spire","Type":"Relic","Info":"Upon pickup, remove 2 Cards from your Deck."},
    "Fusion Hammer":{"Name":"Fusion Hammer","Rarity":"Boss","Owner":"The Spire","Type":"Relic","Info":"Gain <yellow>1 Energy</yellow> at the start of each turn. You can no longer Smith at <blue>Rest Sites</blue>."},
    "Hovering Kite":{"Name":"Hovering Kite","Rarity":"Boss","Owner":"Silent","Type":"Relic","Info":"The first time you discard a Card each turn, gain <yellow>1 Energy</yellow>."},
    "Pandora's Box":{"Name":"Pandora's Box","Rarity":"Boss","Owner":"The Spire","Type":"Relic","Info":"Transform all <red>Strikes</red> and <green>Defends</green>."},
    "Philosopher's Stone":{"Name":"Philosopher's Stone","Rarity":"Boss","Owner":"The Spire","Type":"Relic","Info":"Gain <yellow>1 Energy</yellow> at the start of each turn. ALL enemies start with <red>1 Strength</red>."},
    "Ring of the Serpent":{"Name":"Ring of the Serpent","Rarity":"Boss","Owner":"Silent","Type":"Relic","Info":"Replaces <light-red>Ring of the Snake</light-red>. At the start of your turn, draw 1 additional Card."},
    "Runic Dome":{"Name":"Runic Dome","Rarity":"Boss","Owner":"The Spire","Type":"Relic","Info":"Gain <yellow>1 Energy</yellow> at the start of each turn. You can no longer see enemy Intents."},
    "Runic Pyramid":{"Name":"Runic Pyramid","Rarity":"Boss","Owner":"The Spire","Type":"Relic","Info":"At the end of your turn, you no longer discard your hand."},
    "Sacred Bark":{"Name":"Sacred Bark","Rarity":"Boss","Owner":"The Spire","Type":"Relic","Info":"Double the effectiveness of most <c>Potions</c>."},
    "Slaver's Collar":{"Name":"Slaver's Collar","Rarity":"Boss","Owner":"The Spire","Type":"Relic","Info":"During <black>Boss</black> and Elite combats, gain <yellow>1 Energy</yellow> at the start of your turn."},
    "Sozu":{"Name":"Sozu","Rarity":"Boss","Owner":"The Spire","Type":"Relic","Info":"Gain <yellow>1 Energy</yellow> at the start of each turn. You can no longer obtain <c>Potions</c>."},
    "Snecko Eye":{"Name":"Snecko Eye","Rarity":"Boss","Owner":"The Spire","Type":"Relic","Info":"Draw 2 additional cards each turn. Start each combat <light-cyan>Confused</light-cyan>."},
    "Velvet Choker":{"Name":"Velvet Choker","Rarity":"Boss","Owner":"The Spire","Type":"Relic","Info":"Gain <yellow>1 Energy</yellow> at the start of each turn. You cannot play more than 6 Cards per turn."},
    "Wrist Blade":{"Name":"Wrist Blade","Rarity":"Boss","Owner":"Silent","Type":"Relic","Info":"<red>Attacks</red> that cost <yellow>0 Energy</yellow> deal <red>4 additional damage</red>."},

    "Cultist Headpiece":{"Name":"Cultist Headpiece","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"CAW CAW CAWWWW!"},
    
    "Face of Cleric":{"Name":"Face of Cleric","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"Raise your <red>Max HP by 1</red> after each combat."},
    "Golden Idol":{"Name":"Golden Idol","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"Enemies drop 25% more <yellow>Gold</yellow>."},
    "Bloody Idol":{"Name":"Bloody Idol","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"Whenever you gain <yellow>Gold</yellow>, heal <red>5 HP</red>."},

    "Gremlin Visage":{"Name":"Gremlin Visage","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"Start each combat with <light-cyan>1 Weak</light-cyan>."},
    "Mark of the Bloom":{"Name":"Mark of the Bloom","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"You can no longer <red>heal</red>."},
    "Mutagenic Strength":{"Name":"Mutagenic Strength","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"Start each combat with <red>3 Strength</red> that is lost at the end of your turn."},
    
    "Necronomicon":{"Name":"Necronomicon","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"The first <red>Attack</red> played each turn that costs 2 or more is played twice. When you take this <light-red>Relic</light-red>, become <m>Cursed</m>."},
    "Nilry's Codex":{"Name":"Nilry's Codex","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"At the end of each turn, you can choose 1 of 3 random Cards to shuffle into your Drawpile."},
    "Enchiridion":{"Name":"Enchiridion","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"At the start of each combat, add a random <blue>Power</blue> to your hand. It costs <yellow>0 Energy</yellow> until the end of turn."},

    "Neow's Lament":{"Name":"Neow's Lament","Counter":3,"Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"Enemies in your first 3 combats will have <red>1 HP</red>."},
    "N'loth's Hungry Face": {"Name":"N'loth's Hungry Face","Counter":1,"Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"The next non-boss chest you open is empty."},
    "Odd Mushroom":{"Name":"Odd Mushroom","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"When <light-cyan>Vulnerable</light-cyan>, take 25% more <red>damage</red> rather than 50%."},
    "Ssserpent Head":{"Name":"Ssserpent Head","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"Whenever you enter an <blue>Event</blue> room, gain <yellow>50 Gold</yellow>."},
    "Warped Tongs":{"Name":"Warped Tongs","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"At the start of your turn, Upgrade a random Card in your hand for the rest of combat."},
    "Red Mask":{"Name":"Red Mask","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"At the start of each combat, apply <light-cyan>1 Weakness</light-cyan> to ALL enemies."},
    "N'loth's Gift": {"Name":"N'loth's Gift","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"Triples the chance of receiving rare Cards as monster rewards."},

    "Cauldron":{"Name":"Cauldron","Rarity":"Shop","Owner":"The Spire","Type":"Relic","Info":"Upon pickup, brews 5 random <c>Potions</c>."},
    "Chemical X":{"Name":"Chemical X","Rarity":"Shop","Owner":"The Spire","Type":"Relic","Info":"Whenever you play a cost <yellow>X</yellow> Card, its effects are increased by 2."},
    "Clockwork Souvenir":{"Name":"Clockwork Souvenir","Rarity":"Shop","Owner":"The Spire","Type":"Relic","Info":"At the start of each combat, gain <light-cyan>1 Artifact</light-cyan>."},
    "Dolly's Mirror":{"Name":"Dolly's Mirror","Rarity":"Shop","Owner":"The Spire","Type":"Relic","Info":"Upon pickup, obtain an additional copy of a Card in your deck."},
    "Frozen Eye":{"Name":"Frozen Eye","Rarity":"Shop","Owner":"The Spire","Type":"Relic","Info":"When viewing your Drawpile, the Cards are now shown in order."},
    "Hand Drill":{"Name":"Hand Drill","Rarity":"Shop","Owner":"The Spire","Type":"Relic","Info":"Whenever you break an enemy's <green>Block</green>, apply <light-cyan>2 Vulnerable</light-cyan>."},
    "Lee's Waffle":{"Name":"Lee's Waffle","Rarity":"Shop","Owner":"The Spire","Type":"Relic","Info":"Raise your <red>Max HP by 7</red> and <red>heal</red> all of your <red>HP</red>."},
    "Medical Kit":{"Name":"Medical Kit","Rarity":"Shop","Owner":"The Spire","Type":"Relic","Info":"<light-cyan>Status</light-cyan> Cards can now be played. Playing a <light-cyan>Status</light-cyan> will Exhaust the Card."},
    "Membership Card":{"Name":"Membership Card","Rarity":"Shop","Owner":"The Spire","Type":"Relic","Info":"50\% discount on all products in the <yellow>Shop$</yellow>!"},
    "Orrery":{"Name":"Orrery","Rarity":"Shop","Owner":"The Spire","Type":"Relic","Info":"Choose and add 5 Cards to your deck."},
    "Sling of Courage":{"Name":"Sling of Courage","Rarity":"Shop","Owner":"The Spire","Type":"Relic","Info":"Start each Elite combat with <red>2 Strength</red>. (Does not work against <black>Bosses</black>)"},
    "Strange Spoon":{"Name":"Strange Spoon","Rarity":"Shop","Owner":"The Spire","Type":"Relic","Info":"Cards which Exhaust when played will instead discard 50\% of the time."},
    "The Abacus":{"Name":"The Abacus","Rarity":"Shop","Owner":"The Spire","Type":"Relic","Info":"Gain <green>6 Block</green> whenever you shuffle your Drawpile."},
    
    "Toolbox":{"Name":"Toolbox","Rarity":"Shop","Owner":"The Spire","Type":"Relic","Info":"At the start of each combat, choose 1 of 3 random Colorless Cards and add the chosen Card into your hand."},
    "Twisted Funnel":{"Name":"Twisted Funnel","Rarity":"Shop","Owner":"The Spire","Type":"Relic","Info":"At the start of each combat, apply <green>4 Poison</green> to ALL enemies."},

    "Red Key": {"Name":"Red Key","Rarity":"Special","Owner":"The Spire","Type":"Relic","Info":"You need to obtain the <red>Red</red>,<green>Green</green> and <blue>Blue</blue> Key. Why? Find out yourself!"},
    "Blue Key": {"Name":"Blue Key","Rarity":"Special","Owner":"The Spire","Type":"Relic","Info":"You need to obtain the <red>Red</red>,<green>Green</green> and <blue>Blue</blue> Key. Why? Find out yourself!"},
    "Green Key": {"Name":"Green Key","Rarity":"Special","Owner":"The Spire","Type":"Relic","Info":"You need to obtain the <red>Red</red>,<green>Green</green> and <blue>Blue</blue> Key. Why? Find out yourself!"}


    }

# silent_deck = [ {"Name": "Strike", "Damage":100, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Silent","Unique ID":1},
#                 {"Name": "Strike", "Damage":100, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Silent","Unique ID":2},
#                 {"Name": "Strike", "Damage":100, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Silent","Unique ID":3},
#                 {"Name": "Strike", "Damage":100, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Silent","Unique ID":4},
#                 {"Name": "Strike", "Damage":100, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Silent","Unique ID":5},
#                 {"Name": "Survivor", "Block":8, "Energy": 1, "Type":"Skill" ,"Discard": 1, "Rarity": "Basic","Owner":"Silent","Unique ID":6},
#                 {"Name": "Neutralize", "Damage":3,"Weakness": 1,"Energy": 0,"Type":"Attack", "Rarity": "Basic","Owner":"Silent","Unique ID":7},
                
#                 ]

silent_deck = [ {"Name": "Strike", "Damage":6, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Silent"},
                {"Name": "Strike", "Damage":6, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Silent"},
                {"Name": "Strike", "Damage":6, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Silent"},
                {"Name": "Strike", "Damage":6, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Silent"},
                {"Name": "Strike", "Damage":6, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Silent"},
                {"Name": "Defend", "Block":5, "Energy": 1,"Type": "Skill" ,"Rarity": "Basic","Owner":"Silent"},
                {"Name": "Defend", "Block":5, "Energy": 1,"Type": "Skill" ,"Rarity": "Basic","Owner":"Silent"},
                {"Name": "Defend", "Block":5, "Energy": 1,"Type": "Skill" ,"Rarity": "Basic","Owner":"Silent"},
                {"Name": "Defend", "Block":5, "Energy": 1,"Type": "Skill" ,"Rarity": "Basic","Owner":"Silent"},
                {"Name": "Defend", "Block":5, "Energy": 1,"Type": "Skill" ,"Rarity": "Basic","Owner":"Silent"},
                {"Name": "Survivor", "Block":8, "Energy": 1, "Type":"Skill" ,"Discard": 1, "Rarity": "Basic","Owner":"Silent"},
                {"Name": "Neutralize", "Damage":3,"Weakness": 1,"Energy": 0,"Type":"Attack", "Rarity": "Basic","Owner":"Silent"},
                
                ]


#ACT 1 Encounter

enemies = {"Gremlin": {"Name":"Fat Gremlin","Health":(14,18),"Intentions":["Smash 5/1"],"Intentions_Logic":[["Random"],[0]*100]},
            "Cultist": {"Name":"Cultist", "Health": (50,56),"Intentions":[1],"Intentions_Logic":[["First Move Set"],["Ritual 5"]]},
            "Jaw Worm": {"Name": "Jaw Worm","Health": (42,46),"Intentions":[12, "Thrash 7/5", "Bellow 5|9"],"Intentions_Logic":[["Jaw Worm"]]},
            "Jaw Worm Hard": {"Name": "Jaw Worm","Health": (42,46),"Block":9,"Strength":5,"Intentions":[12, "Thrash 7/5", "Bellow 5|9"],"Intentions_Logic":[["Jaw Worm"]]},

            "Red Louse": {"Name":"Red Louse","Health":(11,17),"Intentions": [(6,8),"Grow 2"], "Intentions_Logic":[["Red Louse"]],"On_hit_or_death":[["Curl","Hit"]]},
            "Green Louse": {"Name":"Green Louse","Health":(12,18),"Intentions": [(6,8),"Weak 2"], "Intentions_Logic":[["Green Louse"]],"On_hit_or_death":[["Curl","Hit"]]},
            
            "Looter": {"Name": "Looter","Health":(46,50),"Intentions":["Steal 11/20", "Lunge 14/20", "SmokeBomb 6"],"Intentions_Logic":[["Looter"]]},
            
            "Red Slaver": {"Name": "Red Slaver","Health":(48,52),"Intentions":[14,"Scape 9/2","Entangle"],"Intentions_Logic":[["Red Slaver"]]},
            "Blue Slaver": {"Name": "Blue Slaver","Health":(48,52),"Intentions":[13,"Rake 8/2"],"Intentions_Logic":[["Blue Slaver"]]},

            "Fungi Beast": {"Name": "Fungi Beast","Health":(24,28),"Intentions":[6,"Grow 5"],"Intentions_Logic": [["Fungi Beast"]],"On_hit_or_death":[["Vulnerable 3","Death"]]},

            "Small Acid Slime": {"Name": "Small Acid Slime","Health":(9,13),"Intentions":[4,"Weak 1"], "Intentions_Logic":[["Small Acid Slime"]]},
            "Medium Acid Slime": {"Name": "Medium Acid Slime","Health":(29,34),"Intentions":[12,"CorrosiveSpit 8/1","Weak 1"],"Intentions_Logic":[["Medium Acid Slime"]]},
            "Large Acid Slime": {"Name": "Large Acid Slime","Health":(68,72),"Intentions":[18,"CorrosiveSpit 12/2","Weak 2"],"Intentions_Logic": [["Large Acid Slime"]],"On_hit_or_death":[["Split","Hit"]]},

            "Small Spike Slime": {"Name": "Small Spike Slime","Health":(11,15),"Intentions":[6],"Intentions_Logic":[["Random"],[0]*100]},
            "Medium Spike Slime": {"Name": "Medium Spike Slime","Health":(29,34),"Intentions": ["CorrosiveSpit 10/1","Frail 1"],"Intentions_Logic":[["Medium Spike Slime"]]},
            "Large Spike Slime": {"Name": "Large Spike Slime", "Health":(67,73),"Intentions":["CorrosiveSpit 18/2","Frail 3"],"Intentions_Logic":[["Large Spike Slime"]],"On_hit_or_death":[["Split","Hit"]]},
            
            "Fat Gremlin": {"Name": "Fat Gremlin","Health":(14,18),"Intentions":["Smash 5/1"],"Intentions_Logic":[["Random"],[0]*100]},
            "Mad Gremlin": {"Name": "Mad Gremlin","Health":(21,25),"Intentions":[5],"Intentions_Logic":[["Random"],[0]*100],"On_hit_or_death": [["Anger 2","Hit"]]},
            "Shield Gremlin":{"Name": "Shield Gremlin","Health": (13,17),"Intentions":["Protect 11"],"Intentions_Logic":[["Random"],[0]*100]},
            "Sneaky Gremlin": {"Name": "Sneaky Gremlin","Health":(11,15),"Intentions":[10],"Intentions_Logic":[["Random"],[0]*100]},
            "Gremlin Wizard": {"Name": "Gremlin Wizard","Health":(22,26),"Intentions":["Charging",30],"Intentions_Logic":[["Random"],[0,0]+[1]*98]},
            
            "Gremlin Nob": {"Name":"Gemlin Nob", "Health": (85,90),"Intentions":[16,"SkullBash 8/2","Enrage 3"],"Intentions_Logic":[["Random"],[2]+[1,0,0]*33]},
            
            "Beam Sentry": {"Name":"Beam Sentry", "Health": (39,45),"Intentions":[10,"Bolt 3"],"Intentions_Logic":[["Random"],[0,1]*50],"Artifact":1}, 
            "Bolt Sentry": {"Name":"Bolt Sentry", "Health": (39,45),"Intentions":[10,"Bolt 3"],"Intentions_Logic":[["Random"],[1,0]*50],"Artifact":1},

            "Lagavulin": {"Name":"Lagavulin", "Health": (112,115),"Intentions":["Asleep 3"],"Intentions_Logic":[["Random"],[0]*100],"On_hit_or_death": [["Asleep","Hit"]], "Metallicize": 8},

            "Slime Boss": {"Name": "Slime Boss", "Health":(150,150),"Intentions":["GoopSpray 5","Preparing",38],"Intentions_Logic":[["Random"],[0,1,2]*33],"On_hit_or_death":[["Split","Hit"]]},
            "Guardian": {"Name": "Guardian", "Health":(250,250),"Intentions":["Block 9",36,"VentSteam 2","Multiattack 5*4"],"Intentions_Logic":[["Random"],[0,1,2,3]*25],"On_hit_or_death":[["Modeshift","Hit"]]},
            "Hexaghost":{"Name": "Hexaghost", "Health":(264,264),"Intentions":["Activate","Divider","Sear 6/2","Multiattack 6*2", "Bellow 3/12","Inferno 3*6"],"Intentions_Logic":[["Random"],[0,1] + [2,3,2,4,3,2,5]*30]},
            
            "Byrd": {"Name":"Byrd","Health":(26,33),"Intentions":["Multiattack 1*6","Grow 1",14],"Intentions_Logic":[["Byrd"]],"On_hit_or_death":[["Fly 4","Hit"]]},

            "Chosen": {"Name":"Chosen","Health":(98,103),"Intentions":["Multiattack 6*2",21,"Scrape 12/2","Drain 3/3","Hex"],"Intentions_Logic":[["Chosen"]]},
            "Mugger": {"Name": "Mugger","Health":(50,54),"Intentions":["Steal 11/20", "Lunge 18/20", "SmokeBomb 17"],"Intentions_Logic":[["Mugger"]]},

            "Shelled Parasite": {"Name": "Shelled Parasite","Health":(70,75),"Intentions":["Multiattack 7*2", "Suck 12", "Fell 21/2"],"Intentions_Logic":[["Shelled Parasite"]],"Plated Armor":14},
            #continue here
            "Spheric Guardian": {"Name": "Spheric Guardian","Health":(20,20),"Block":40,"Intentions":["Harden 11/15","Multiattack 11*2", "Block 35", "Fell 11/5"],"Intentions_Logic":[["Spheric Guardian"]],"Artifact":3,"Barricade":True},
            "Centurion": {"Name": "Centurion","Health":(78,83),"Intentions":[14,"CenturionDefendAlly"],"Intentions_Logic":[["Centurion"]]},
            "Mystic": {"Name": "Mystic","Health":(78,83),"Intentions":["Fell 9/2","MysticBuff","MysticHeal 20"],"Intentions_Logic":[["Mystic"]]},
            "Snecko": {"Name": "Snecko","Health":(120,125),"Intentions":["Smash 10/2",18,"Perplexing Glare"],"Intentions_Logic":[["Snecko"]]},

            "Snake Plant": {"Name": "Snake Plant","Health":(78,82),"Intentions":["Multiattack 8*3","Roar 2"],"Intentions_Logic":[["Snake Plant"]],"On_hit_or_death":[["Malleable 3","Hit"]]},

            "Book of Stabbing": {"Name": "Book of Stabbing","Health":(168,172),"Intentions":["Multiattack 7*3",24],"Intentions_Logic":[["Book of Stabbing"]],"Painfull Stabs":True},
            "Gremlin Leader": {"Name": "Gremlin Leader","Health":(145,155),"Intentions":["Encourage 3/6","Rally","Multiattack 6*3"],"Intentions_Logic":[["Gremlin Leader"]],"Leader":True},
            "Taskmaster": {"Name": "Taskmaster","Health":(57,64),"Intentions":["ScouringWhip 7/3"],"Intentions_Logic":[["Random"],[0]*100]},
        
            "Pointy": {"Name": "Pointy","Health":(34,34),"Intentions":["Multiattack 6*2"],"Intentions_Logic":[["Random"],[0]*100]},
            "Romeo": {"Name": "Romeo","Health":(37,41),"Intentions":["RomeoTaunt","Rake 12/3", 17],"Intentions_Logic":[["Random"],[0]+[1,2,2]*33]},
            "Bear": {"Name": "Bear","Health":(40,44),"Intentions":["BearHug 4","Thrash 10/9", 20],"Intentions_Logic":[["Random"],[0]+[1,2]*50]},


            "Bronze Automaton": {"Name": "Bronze Automaton","Health":(320,320),"Intentions":["Multiattack 8*2","Bellow 4|12",50,"Spawn Orbs"],"Intentions_Logic":[["Random"],[3]+[0,1,0,1,2]*30],"Artifact":3},
            "Bronze Orb": {"Name": "Bronze Orb","Health":(54,60),"Intentions":[8,"Support Automaton","Stasis"],"Intentions_Logic":[["Bronze Orb"]]},

            "The Champ" : {"Name":"The Champ","Health":(440,440),"Intentions_Logic":[["The Champ Phase 1"]]},

            "The Collector": {"Name":"The Collector","Health":(300,300),"Intentions_Logic":[["The Collector"]],"Leader": True},

            "Darkling": {"Name": "Darkling","Health":(50,59),"Intentions":[(9,13),"Bellow 2|12","Multiattack 9*2"],"Intentions_Logic":[["Darkling"]],"On_hit_or_death":[["Lifelink","Death"]]},
            "Orb Walker": {"Name": "Orb Walker", "Health":(92,102),"Intentions":[16,"Laser 11/1"],"Intentions_Logic":[["Orb Walker"]],"Ritual":5},
            "Spiker": {"Name": "Spiker", "Health":(44,60),"Intentions":[9,"SpikeUp 2"],"Intentions_Logic":[["Spiker"]],"On_hit_or_death":[[7,"Hit"]]},
            "Exploder": {"Name": "Exploder", "Health":(30,35),"Intentions":[11,"Explode 30"],"Intentions_Logic":[["Random"],[0,0,1]]},
            "Repulsor": {"Name": "Repulsor", "Health":(31,38),"Intentions":[13,"Repulse 2"],"Intentions_Logic":[["Repulsor"]]},
        
            "The Maw": {"Name": "The Maw", "Health":(300,300),"Intentions_Logic":[["The Maw"]]},
            "Spire Growth": {"Name": "Spire Growth", "Health":(190,190),"Intentions":[18,25,"Constrict 12"],"Intentions_Logic":[["Spire Growth"]]},
            "Transient": {"Name": "Transient","Health":(999,999),"Intentions":["Transientattack 40"],"Intentions_Logic":[["Random"],[0]*20],"On_hit_or_death": [["Shifting","Hit"]],"Fading":True},
            "Writhing Mass": {"Name": "Writhing Mass","Health":(175,175),"Intentions":["Thrash 15/16","Wither 10/2","Multiattack 9*3",38,"Implant"],"Intentions_Logic":[["Writhing Mass"]],"On_hit_or_death": [["Malleable 3","Hit"],["Reactive","Hit"]]},
                    
            "Nemesis": {"Name": "Nemesis","Health":(200,200),"Intentions":[45,"Multiattack 7*3","BurningDebuff 5"],"Intentions_Logic":[["Nemesis"]],"Intangible Power":True},
            "Giant Head": {"Name":"Giant Head","Health":(520,520),"Intentions":[13,"Weak 1","GiantHead 40"],"Intentions_Logic":[["Giant Head"]],"Slow":True},

            "Raptomancer": {"Name": "Raptomancer","Health":(190,200),"Intentions_Logic":[["Raptomancer"]],"Leader":True},
            "Dagger": {"Name": "Dagger","Health":(20,25),"Intentions":["ScouringWhip 9/1","Explode 25"],"Intentions_Logic":[["Random"],[0,1,1,1]]},

        	"Donu":{"Name":"Donu","Health":(265,265),"Intentions":["MysticBuff 3","Multiattack 12*2"],"Intentions_Logic":[["Random"],[0,1]*50],"Artifact":3},
        	"Deca":{"Name":"Deca","Health":(265,265),"Intentions":["SquareOfDeca 16|3","DazeBeam 12*2"],"Intentions_Logic":[["Random"],[1,0]*50],"Artifact":3},

        	"Awakened One": {"Name":"Awakened One","Health":(320,320),"Intentions":[20,"Multiattack 6*4"],"Intentions_Logic":[["Awakened One"]], "CardTypeToLookOutFor":"Power Strength 2","Regen":15,"On_hit_or_death":[["Rebirth","Death"]]},
        	
        	"Time Eater": {"Name":"Time Eater","Health":(480,480),"Intentions":["TimeSlam 32/2","Ripple 20|1","Multiattack 8*3"],"Intentions_Logic":[["Time Eater"]], "CardTypeToLookOutFor":"Everything Counter Opposites 1"},

            "Spire Shield": {"Name":"Spire Shield","Health":(125,125),"Intentions":["Bash 12/1","Fortify 30","Thrash 38/99"],"Intentions_Logic":[["Spire Shield"]],"Artifact":2,"On_hit_or_death":[["SpireBros","Hit"]]},
            "Spire Spear": {"Name":"Spire Spear","Health":(180,180),"Intentions":["Multiattack 10*4","BurnStrike 6*2","CircleOfPower 2",],"Intentions_Logic":[["Spire Spear"]], "Artifact":2,"On_hit_or_death":[["SpireBros","Hit"]]},
                                                                
            "Corrupt Heart":{"Name":"Corrupt Heart","Health":(800,800),"Intentions":["Debilitate 2","Multiattack 2*15",45,"HeartBuff"],"Intentions_Logic":[["Corrupt Heart"]],"On_hit_or_death":[["Invincible 200","Hit"]],"CardTypeToLookOutFor":"Everything BeatOfDeath Opposites 2"}
        	}    


    

enemyEncounters = fill_enemy_list()
eliteEncounters = fill_elite_list()
bossEncounters = fill_boss_list(helping_functions.gameAct)

#enemyEncounters = [[Enemy(name="Raptomancer",max_health=rd.randint(190,200),intention_logic=[["Raptomancer"]],leader=True)]]


def update_encounter():
	helping_functions.turn_counter = 0

	if active_character[0].get_floor() == "Enemy":
		list_of_enemies.extend(enemyEncounters.pop(0))
		helping_functions.encounter_counter += 1
		if active_character[0].faceOfCleric > 0:
			active_character[0].set_maxHealth(1)

	elif active_character[0].get_floor() == "Elite":
		list_of_enemies.extend(eliteEncounters.pop(0))
		if active_character[0].faceOfCleric > 0:
			active_character[0].set_maxHealth(1)

	elif active_character[0].get_floor() == "Super":
		
		superElite = create_superElite(eliteEncounters.pop(0))
				
		list_of_enemies.extend(superElite)
		if active_character[0].faceOfCleric > 0:
			active_character[0].set_maxHealth(1)

	elif active_character[0].get_floor() == "Boss":
		list_of_enemies.extend(bossEncounters.pop(0))
		if active_character[0].faceOfCleric > 0:
			active_character[0].set_maxHealth(1)

	elif active_character[0].get_floor() == "Start":
		neowBlesses()

	elif active_character[0].get_floor() == "Fires":
		visit_campfire()

	elif active_character[0].get_floor() == "Event":
		visit_event()

	elif active_character[0].get_floor() == "Shop$":
		shop = helping_functions.generateShop()
		helping_functions.displayShop(shop)

	elif active_character[0].get_floor() == "Chest":
		visit_treasureChest()
	
	else:
		list_of_enemies.extend(enemyEncounters.pop(0))


def visit_campfire():
    fusionHammer = False
    coffeeDripper = False
    dreamCatcher = False
    regalPillow = False
    key = False

    sleepOrUpgrade = ["Sleep","Upgrade"]



    for relic in active_character[0].relics:
        if relic.get("Name") == "Fusion Hammer":
            fusionHammer = True
        elif relic.get("Name") == "Coffee Dripper":
            coffeeDripper = True
        elif relic.get("Name") == "Ancient Tea Set":
            active_character[0].energyBoost(2)
        elif relic.get("Name") == "Dream Catcher":
            dreamCatcher = True
        elif relic.get("Name") == "Regal Pillow":
            regalPillow = True
        elif relic.get("Name") == "Peace Pipe":
            sleepOrUpgrade.append("Toke Card")
        
        elif relic.get("Name") == "Girya":
            sleepOrUpgrade.append("Train")
            giryaIndex = active_character[0].relics.index(relic)
        elif relic.get("Name") == "Shovel":
            sleepOrUpgrade.append("Shovel")
        elif relic.get("Name") == "Eternal Feather":
            healAmountFeather = math.floor((len(active_character[0].deck)/5)*3)
            active_character[0].heal(healAmountFeather)
            ansiprint("You healed <red>"+str(healAmountFeather)+"</red>because of <light-red>Eternal Feather</light-red>!")
        elif relic.get("Name") == "Red Key":
            key = True

    if key == False:
        sleepOrUpgrade.append("Obtain <red>Red Key</red>")

    sleepOrUpgrade.extend(["Check Deck","Check Map","Leave"])
    
 

    while True:
        
        try:
            i = 0
            for sleepspot in sleepOrUpgrade:
                i+=1
                ansiprint(str(i)+".",sleepspot)

            choice = input("What do you want to do?\n")
            choice = int(choice)-1
            if choice in range(len(sleepOrUpgrade)):
                pass
            else:
                print("Type the number of one of the choices shown.")
                continue
        except Exception as e:
            active_character[0].explainer_function(choice)
            print ("You have to type a number.\n")
            continue

        if sleepOrUpgrade[choice] == "Sleep":
            if coffeeDripper:
                ansiprint("You can't sleep because you own <light-red>Coffee Dripper</light-red>.")
                continue

            healAmount = math.floor((active_character[0].max_health / 100)*30)
            
            if regalPillow:
                healAmount += 15
                ansiprint("You healed an extra 15 becaue of <light-red>Regal Pillow</light-red>.")

            active_character[0].heal(healAmount)

            if dreamCatcher:
            	dreamRewards = helping_functions.generateCardRewards()
            	ansiprint("You dream of more cards because you own a <light-red>Dream Catcher</light-red>.")
            	helping_functions.pickCard(dreamRewards)
            
            break
                
        elif sleepOrUpgrade[choice] == "Upgrade":
            if fusionHammer:
                ansiprint("You can't upgrade Cards becaue you own <light-red>Fusion Hammer</light-red>.")
                continue
            
            active_character[0].removeCardsFromDeck(1,removeType = "Upgrade")
            break    
            
        
        elif sleepOrUpgrade[choice] == "Train":
            

            if active_character[0].relics[giryaIndex].get("Counter") == 3:
                ansiprint("Training is limited to 3. You have reached the limit!")
                continue
            
            active_character[0].relics[giryaIndex]["Counter"] += 1
            break

        elif sleepOrUpgrade[choice] == "Toke Card":
            
            active_character[0].removeCardsFromDeck(amount=1,removeType="Remove",place="Deck")
            break
        
        elif sleepOrUpgrade[choice] == "Shovel":
            
            shovelRelic = helping_functions.generateRelicRewards(place="Event")
            helping_functions.pickRelic(shovelRelic)

            break

        elif sleepOrUpgrade[choice] == "Obtain <red>Red Key</red>":
            active_character[0].add_relic({"Name":"Red Key","Rarity":"Special","Owner":"The Spire","Type":"Relic","Info":"You need to obtain the <red>Red</red>,<green>Green</green> and <blue>Blue</blue> Key. Why? Find out yourself!"})
            break

        elif sleepOrUpgrade[choice] == "Check Deck":
            active_character[0].showDeck()

        elif sleepOrUpgrade[choice] == "Check Map":
            acts.show_map(helping_functions.game_map,helping_functions.game_map_dict)

        elif sleepOrUpgrade[choice] == "Leave":
            break

        else:
            print(sleepOrUpgrade[choice],"<--- What is this?")

def visit_treasureChest():
    nlothsHungryFace = False
    cursedKey = False
    blueKey = False
    openLeave = ["Open"]

    for relic in active_character[0].relics:
        if relic.get("Name") == "N'loth's Hungry Face":
            nlothsHungryFaceIndex = active_character[0].relics.index(relic)
            if active_character[0].relics[nlothsHungryFaceIndex]["Counter"] > 0:
                nlothsHungryFace = True
        elif relic.get("Name") == "Blue Key":
            blueKey = True

        elif relic.get("Name") == "Cursed Key":
            ansiprint("If you open the chest you will be <m>cursed</m> because of <light-red>Cursed Key</light-red>")
            cursedKey = True

    openLeave.extend(["Check Deck","Check Map","Leave"])
    

    chestType = rd.randint(1,100)

    if chestType <= 50:
        chestType = "Small Chest"
    elif chestType <= 83:
        chestType = "Medium Chest"
    else:
        chestType = "Large Chest"

    ansiprint("You're standing in front of a",chestType+". <light-red>Let's wonder what's insinde!</light-red>.")
    if nlothsHungryFace == False:
        chestRelic = helping_functions.generateRelicRewards(place=chestType)
        if blueKey == False:
            chestRelic.append({"Name":"Blue Key","Rarity":"Special","Owner":"The Spire","Type":"Relic","Info":"You need to obtain the <red>Red</red>,<green>Green</green> and <blue>Blue</blue> Key. Why? Find out yourself!"})

    while True:
        
        i = 0
        for option in openLeave:
            ansiprint(str(i+1)+".",option)
            i+=1
        
        choice = input("What do you want to do?\n")
        choice = int(choice)-1
        try:
            if choice in range(len(option)):
                pass
            else:
                print("Type the number of one of the choices shown.")
                continue
        except Exception as e:
            active_character[0].explainer_function(choice)
            print ("You have to type a number.\n",e)
            pass

        if openLeave[choice] == "Open":
            if cursedKey == True:
                curses = {k:v for k,v in cards.items() if v.get("Type") == "Curse" and v.get("Rarity") != "Special"}
                card_add = rd.choices(list(curses.items()))[0][1]
                active_character[0].add_CardToDeck(card_add)

            if nlothsHungryFace:
                active_character[0].relics[nlothsHungryFaceIndex]["Counter"] = 0
                ansiprint("You did not receive a <light-red>Relic<light-red> because your <light-red>N'loth's Hungry Face<light-red> ate it! It's repleted now, though.")
                
            else:
                helping_functions.pickRelic(chestRelic)
            
            break
        
        elif openLeave[choice] == "Check Deck":
            active_character[0].showDeck()

        elif openLeave[choice] == "Check Map":
            acts.show_map(helping_functions.game_map,helping_functions.game_map_dict)

        elif openLeave[choice] == "Leave":
            break

        else:
            print(openLeave[choice],"<--- What is this?")


def neowBlesses():
    
    damageValue = math.floor((active_character[0].health / 10) * 3)

    ansiprint("A <light-blue>giant whale</light-blue> approaches you... Choose a <green>blessing</green>.")
    allBlessings = ["Max HP +6","Enemies in the next three combat will have one health","Remove a card","Transform a card",
    "Upgrade a card","Choose a card to obtain","Choose an uncommon colorless card to obtain","Obtain a random rare card",
    "Obtain a random common relic","Receive 100 Gold","Obtain 3 random Potions"]
    positives = rd.sample(allBlessings,k=2)
    

    advantages = ["Remove 2 cards","Transform 2 cards","Gain 250 Gold","Choose a rare card to obtain",
    "Choose a rare colorless card to obtain","Obtain a random rare relic","Max HP +12"]
    
    disadvantages = ["Lose 6 Max HP","Take " +str(damageValue)+" Damage","Obtain a Curse","Lose all Gold"]

    vantagePairsList = []

    for advantage in advantages:
        for disadvantage in disadvantages:
            if advantage == "Gain 250 Gold" and disadvantage == "Lose all Gold":
                pass
            elif advantage == "Max HP + 12" and disadvantage == "Lose 6 max health":
                pass
            else:
                vantagePairsList.append([advantage,disadvantage])


    vantagePairingsPick = rd.sample(vantagePairsList,k=1)[0]

    blessings = [positives[0],positives[1],vantagePairingsPick,"<green>Obtain random boss relic</green>. <red>Loose your starting relic</red>."]
    
    while True:
        i = 0
        for blessing in blessings:
            if i < 2:
                ansiprint(str(i+1)+". <green>"+blessing+"</green>")
            elif i == 3:
                ansiprint(str(i+1)+".",blessing)
            else:
                ansiprint(str(i+1)+". <green>"+blessing[0]+"</green>. <red>"+blessing[1]+"</red>.")
            i+=1          
        try:
            choice = input("Which blessing do you want to receive?")
            choice = int(choice)-1
            if choice in range(len(blessings)):
                break
            else:
                print("Type the number of one of the blessings shown.")
                pass
        except Exception as e:
            active_character[0].explainer_function(choice)
            print ("You have to type a number.\n")
            pass
    

    if type(blessings[choice]) == list:
        if blessings[choice][0] == "Remove 2 cards":
        	active_character[0].removeCardsFromDeck(2)
        
        elif blessings[choice][0] == "Gain 250 Gold":
        	active_character[0].set_gold(250)

        elif blessings[choice][0] == "Max HP + 12":
        	active_character[0].set_maxHealth(12)

        elif blessings[choice][0] == "Choose a rare card to obtain":
            
            rare_cards = {k:v for k,v in cards.items() if v.get("Owner") == active_character[0].name and v.get("Rarity") == "Rare" and v.get("Upgraded") != True}
            threeRareCards = rd.choices(list(rare_cards.items()),k=3)
            
            three_options = []
            for card in threeRareCards:
                three_options.append(card[1])

            helping_functions.pickCard(three_options)

        elif blessings[choice][0] == "Choose a rare colorless card to obtain":

            while True:
                rareColorlessCards = helping_functions.generateCardRewards(colorless=True)
                notRare = False
                for card in rareColorlessCards:
                    if card.get("Rarity") != "Rare":
                        notRare = True
                if notRare == False:
                    break

            helping_functions.pickCard(rareColorlessCards,place = "Deck")

        elif blessings[choice][0] == "Transform 2 cards":

            active_character[0].removeCardsFromDeck(2,removeType = "Transform")

        elif blessings[choice][0] == "Obtain a random rare relic":

            randomRareRelic = helping_functions.generateRelicRewards(specificType="Rare")
            active_character[0].add_relic(randomRareRelic[0])
            

        if blessings[choice][1] == "Lose 6 max health":
            active_character[0].set_maxHealth(-6)

        elif blessings[choice][1] == "Take " +str(damageValue)+" Damage":
            active_character[0].set_health(-damageValue)
        
        elif blessings[choice][1] == "Obtain a Curse":
            curses = {k:v for k,v in cards.items() if v.get("Type") == "Curse" and v.get("Rarity") != "Special"}
            
            card_add = rd.choices(list(curses.items()))[0][1]
            
            active_character[0].add_CardToDeck(card_add)

        elif blessings[choice][1] == "Lose all Gold":
            goldSwish = -active_character[0].gold
            active_character[0].set_gold(goldSwish)   
            
    elif blessings[choice] == "Max HP +6":
        active_character[0].set_maxHealth(6)

    elif blessings[choice] == "Enemies in the next three combat will have one health":
        active_character[0].add_relic({"Name":"Neow's Lament","Counter":3,"Rarity":"Event","Owner":"The Spire","Type":"Relic"})

    elif blessings[choice] == "Remove a card":
        active_character[0].removeCardsFromDeck(1)

    elif blessings[choice] == "Transform a card":
        active_character[0].removeCardsFromDeck(1,removeType = "Transform")

    elif blessings[choice] == "Upgrade a card":
        active_character[0].removeCardsFromDeck(1,removeType = "Upgrade")

    elif blessings[choice] == "Choose a card to obtain":
        
        random_cards = {k:v for k,v in cards.items() if v.get("Owner") == active_character[0].name and v.get("Rarity") != "Special" and v.get("Upgraded") != True and v.get("Rarity") != "Basic"}
        threeRareCards = rd.choices(list(random_cards.items()),k=3)
            
        three_options = []
        for card in threeRareCards:
            three_options.append(card[1])

        helping_functions.pickCard(three_options)

    elif blessings[choice] == "Choose an uncommon colorless card to obtain":
        
        while True:
            uncommonColorlessCards = helping_functions.generateCardRewards(colorless=True)
            notUncommon = False
            for card in uncommonColorlessCards:
                if card.get("Rarity") != "Uncommon":
                    notUncommon = True
            if notUncommon == False:
                break

        helping_functions.pickCard(uncommonColorlessCards,place = "Deck")

    elif blessings[choice] == "<green>Obtain random boss relic</green>. <red>Loose your starting relic</red>.":

        active_character[0].remove_Relic("Ring of the Snake")

        randomBossRelic = rd.randint(0,20)

        if randomBossRelic == 0:
            active_character[0].add_relic({"Name":"Astrolabe","Rarity":"Boss","Owner":"Silent","Type":"Relic"})  
        elif randomBossRelic == 1:
            active_character[0].add_relic({"Name":"Black Star","Rarity":"Boss","Owner":"The Spire","Type":"Relic"})
        elif randomBossRelic == 2:
            active_character[0].add_relic({"Name":"Busted Crown","Rarity":"Boss","Owner":"The Spire","Type":"Relic"})
        elif randomBossRelic == 3:
            active_character[0].add_relic({"Name":"Calling Bell","Rarity":"Boss","Owner":"Silent","Type":"Relic"})  
        elif randomBossRelic == 4:
            active_character[0].add_relic({"Name":"Cursed Key","Rarity":"Boss","Owner":"The Spire","Type":"Relic"})
        elif randomBossRelic == 5:
            active_character[0].add_relic({"Name":"Coffee Dripper","Rarity":"Boss","Owner":"The Spire","Type":"Relic"})
        elif randomBossRelic == 6:
            active_character[0].add_relic({"Name":"Ectoplasm","Rarity":"Boss","Owner":"The Spire","Type":"Relic"})
        elif randomBossRelic == 7:
            active_character[0].add_relic({"Name":"Empty Cage","Rarity":"Boss","Owner":"The Spire","Type":"Relic"})
        elif randomBossRelic == 8:
            active_character[0].add_relic({"Name":"Fusion Hammer","Rarity":"Boss","Owner":"The Spire","Type":"Relic"})
        elif randomBossRelic == 9:
            active_character[0].add_relic({"Name":"Hovering Kite","Rarity":"Boss","Owner":"Silent","Type":"Relic"})
        elif randomBossRelic == 10:
            active_character[0].add_relic({"Name":"Pandora's Box","Rarity":"Boss","Owner":"The Spire","Type":"Relic"})
        elif randomBossRelic == 11:
            active_character[0].add_relic({"Name":"Philosopher's Stone","Rarity":"Boss","Owner":"The Spire","Type":"Relic"})
        elif randomBossRelic == 12:
            active_character[0].add_relic({"Name":"Runic Dome","Rarity":"Boss","Owner":"The Spire","Type":"Relic"})
        elif randomBossRelic == 13:
            active_character[0].add_relic({"Name":"Runic Pyramid","Rarity":"Boss","Owner":"The Spire","Type":"Relic"})
        elif randomBossRelic == 14:
            active_character[0].add_relic({"Name":"Sacred Bark","Rarity":"Boss","Owner":"The Spire","Type":"Relic"})
        elif randomBossRelic == 15:
            active_character[0].add_relic({"Name":"Sacred Bark","Rarity":"Boss","Owner":"The Spire","Type":"Relic"})
        elif randomBossRelic == 16:
            active_character[0].add_relic({"Name":"Slaver's Collar","Rarity":"Boss","Owner":"The Spire","Type":"Relic"})
        elif randomBossRelic == 17:
            active_character[0].add_relic({"Name":"Sozu","Rarity":"Boss","Owner":"The Spire","Type":"Relic"})
        elif randomBossRelic == 18:
            active_character[0].add_relic({"Name":"Snecko Eye","Rarity":"Boss","Owner":"The Spire","Type":"Relic"})
        elif randomBossRelic == 19:
            active_character[0].add_relic({"Name":"Velvet Choker","Rarity":"Boss","Owner":"The Spire","Type":"Relic"})
        elif randomBossRelic == 20:
            active_character[0].add_relic({"Name":"Wrist Blade","Rarity":"Boss","Owner":"Silent","Type":"Relic"})  


    elif blessings[choice] == "Obtain a random rare card":
        
        random_cards = {k:v for k,v in cards.items() if v.get("Owner") == active_character[0].name and v.get("Rarity") == "Rare" and v.get("Upgraded") != True}
        card_add = rd.choices(list(random_cards.items()))[0][1]
            
        active_character[0].add_CardToDeck(card_add)
    
    elif blessings[choice] == "Obtain a random common relic":
        commonRelic = helping_functions.generateRelicRewards(specificType="Common")
        active_character[0].add_relic(commonRelic[0])

    elif blessings[choice] == "Receive 100 Gold":
        active_character[0].set_gold(100)

    elif blessings[choice] == "Obtain 3 random Potions":

        threePotions = helping_functions.generatePotionRewards(event = True,amount = 3)
        helping_functions.pickPotion(threePotions)
    
    else:
        print("What is written here?:",blessings[choice])


def event_PurpleFireSpirits():
    ansiprint("You happen upon a group of what looks like <m>purple</m> <red>fire spirits</red> dancing around a large bonfire.\nThe spirits toss small bones and fragments into the fire, which brilliantly erupts each time. As you approach, the spirits all turn to you, expectantly...")
    ansiprint("You have to <light-blue>remove a card</light-blue>. Choose wisely.")
    
    offeredCard = active_character[0].removeCardsFromDeck(1,removeType = "Remove",purpleFire = True)
    
    if offeredCard["Rarity"] == "Rare":
        ansiprint("The flames burst, nearly knocking you off your feet, as the fire doubles in strength.\nThe spirits dance around you excitedly before merging into your form, filling you with warmth and strength.\nYour Max HP increases by 10 and you are healed to full HP.")
        active_character[0].heal(active_character[0].max_health)
        active_character[0].set_maxHealth(10)
    
    elif offeredCard["Rarity"] == "Uncommon":
        ansiprint("The flames erupt, growing significantly stronger! The spirits dance around you excitedly, filling you with a sense of warmth.You are healed to full HP.")
        active_character[0].heal(active_character[0].max_health)

    elif offeredCard["Rarity"] == "Common" or offeredCard["Rarity"] == "Special":
        ansiprint("The flames grow slightly brighter. The spirits continue dancing. You feel slightly warmer from their presence..")
        active_character[0].heal(5)

    elif offeredCard["Rarity"] == "Basic":
        ansiprint("Nothing happens... The Spirits seem to be ignoring you now. Disappointing...")

    elif offeredCard["Rarity"] == "Curse":
        ansiprint("However, the spirits aren't happy that you offered a Curse... The card fizzles a meek black smoke. You receive a... something in return.")
        active_character[0].add_relic({"Name":"Spirit Poop","Rarity":"Event","Owner":"The Spire","Type":"Relic"})

    else:
        print(offeredCard,"<--Which rarity and other things does this card have?")


def event_theDivineFountain():
    ansiprint("You come across <blue>shimmering water</blue> flowing endlessly from a fountain on a nearby wall.")
    divineFountainOptions = ["1. <blue>[Drink the water]</blue>. Loose all curses.","2. Leave"]
    checkNumbers = ["1","2"]

    for option in divineFountainOptions:
        ansiprint (option)
    
    snap = input("What do you want to do?\n")
    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")
        

    if snap == "1":
        ansiprint("As you drink the <blue>water</blue>, you feel a <C>dark</C> grasp loosen.")
        i = 0
        while i < len(active_character[0].deck):
            if active_character[0].deck[i]["Rarity"] == "Curse":
                active_character[0].removeCardsFromDeck(1,removeType = "Remove",index = i)
            else:
                i += 1
    elif snap == "2":
        print("You leave.")
    else:
        print(snap,"<--- what is this? def theDivineFountain()")



def event_TheDuplicator():
    ansiprint("Before you lies a <G><c>decorated altar</c></G> to some ancient entity.")
    duplicatorOptions = ["1. <light-blue>[Pray]</light-blue> Duplicate a card in your deck","2. [Leave] Nothings happens."]
    checkNumbers = ["1","2"]

    for option in duplicatorOptions:
        ansiprint (option)

    snap = input("What do you want to do?\n")
    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")


    if snap == "1":
        ansiprint("You kneel respectfully. A ghastly mirror image appears from the shrine and collides into you.")
        active_character[0].removeCardsFromDeck(1,removeType = "Duplicate")
    elif snap == "2":
        print("You leave.")
    else:
        print(snap,"<--- what is this? def theDuplicator()")

def event_ThePurifier():
    ansiprint("Before you lies an elaborate shrine to a forgotten spirit..")
    purifierOptions = ["1. <light-blue>[Pray]</light-blue> Remove a card in your deck","2. [Leave] Nothings happens."]
    checkNumbers = ["1","2"]

    for option in purifierOptions:
        ansiprint (option)

    snap = input("What do you want to do?\n")
    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        ansiprint("As you kneel in reverence, you feel a weight lifted off your shoulders.")
        active_character[0].removeCardsFromDeck(1,removeType = "Remove")
    elif snap == "2":
        print("You ignore the shrine and leave.")
    else:
        print(snap,"<--- what is this? def event_ThePurifier()")


def event_TheTransmogrifier():
    ansiprint("Before you lies an elaborate shrine to a forgotten spirit.")
    transmorphOptions = ["1. <light-blue>[Pray]</light-blue> Transform a card in your deck","2. [Leave] Nothings happens."]
    checkNumbers = ["1","2"]

    for option in transmorphOptions:
        ansiprint (option)

    snap = input("What do you want to do?\n")
    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        ansiprint("As the power of the shrine flows through you, your mind feels altered.")
        active_character[0].removeCardsFromDeck(1,removeType = "Transform")
    elif snap == "2":
        print("You ignore the shrine and leave.")
    else:
        print(snap,"<--- what is this? def event_ThePurifier()")

def event_upgradeShrine():
    ansiprint("Before you lies an elaborate shrine to a forgotten spirit.")
    upgradeOptions = ["1. <light-blue>[Pray]</light-blue> Upgrade a card in your deck","2. [Leave] Nothings happens."]
    checkNumbers = ["1","2"]

    for option in upgradeOptions:
        ansiprint (option)

    snap = input("What do you want to do?\n")
    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        ansiprint("The shrine's energy flows into you, making you stronger.")
        active_character[0].removeCardsFromDeck(1,removeType = "Upgrade")
    elif snap == "2":
        print("You ignore the shrine and leave.")
    else:
        print(snap,"<--- what is this? def event_ThePurifier()")


def event_GoldenShrine():
    ansiprint("Before you lies an elaborate shrine to an <yellow>ancient spirit</yellow>.")
    shrineOptions = ["1. [Pray] <yellow>Gain 50 Gold</yellow>.","2. [Desecrate] <yellow>Gain 275 Gold</yellow>. Become <m>Cursed (Regret)</m>.","3. [Leave] Nothing happens."]
    checkNumbers = ["1","2","3"]

    for option in shrineOptions:
        ansiprint (option)

    snap = input("What do you want to do?\n")
    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        ansiprint("As your hand touches the shrine, <yellow>gold</yellow> rains from the ceiling showering you in riches.")
        active_character[0].set_gold(50)
    
    elif snap == "2":
        ansiprint("Each time you strike the shrine, <yellow>gold</yellow> pours forth again and again!")
        active_character[0].set_gold(275)
        ansiprint("As you pocket the riches, something <m>weighs heavily on you</m>.")
        active_character[0].add_CardToDeck({"Name": "Regret","Type": "Curse","Rarity": "Curse","Owner":"The Spire"})
    
    elif snap == "3":
        ansiprint("You ignore the shrine.")

    else:
        print(snap,"<--- what is this? def goldenShrine()")


def event_AncientLaboratory():
    ansiprint("You find yourself in a room filled with racks of test tubes, beakers, flasks, forceps, pinch clamps, stirring rods, tongs, goggles, funnels, pipets, cylinders, condensers, and even a rare spiral tube of glass. Why do you know the name of all these tools? It doesn't matter, you take a look around.")


    input("Type anything to search the place.")

    random_potions = {k:v for k,v in potions.items() if v.get("Owner") == active_character[0].name or v.get("Owner") == "The Spire"}
    twoPotions = rd.choices(list(random_potions.items()),k=2)
            
    two_options = []
    for potion in twoPotions:
        two_options.append(potion[1])

    helping_functions.pickPotion(two_options)


def event_MatchAndKeep():

    moltenEgg = False
    toxicEgg = False
    frozenEgg = False

    for relic in active_character[0].relics:
        if relic.get("Name") == "Molten Egg":
            moltenEgg = True
        
        elif relic.get("Name") == "Toxic Egg":
            toxicEgg = True
        
        elif relic.get("Name") == "Frozen Egg":
            frozenEgg = True

    memoryGame = []

    basics = {k:v for k,v in cards.items() if v.get("Owner") == active_character[0].name and v.get("Rarity") == "Basic" and v.get("Upgraded") != True and v.get("Type") != "Special"}
    commons = {k:v for k,v in cards.items() if v.get("Owner") == active_character[0].name and v.get("Rarity") == "Common" and v.get("Upgraded") != True and v.get("Type") != "Special"}
    uncommons = {k:v for k,v in cards.items() if v.get("Owner") == active_character[0].name and v.get("Rarity") == "Uncommon" and v.get("Upgraded") != True and v.get("Type") != "Special"}
    rares = {k:v for k,v in cards.items() if v.get("Owner") == active_character[0].name and v.get("Rarity") == "Rare" and v.get("Upgraded") != True and v.get("Type") != "Special"}
    curses = {k:v for k,v in cards.items() if v.get("Rarity") == "Curse" and v.get("Type") != "Special"}

    while True:
        memoryGame.append(rd.choices(list(curses.items()))[0][1])
        memoryGame.append(rd.choices(list(curses.items()))[0][1])
        memoryGame.append(rd.choices(list(basics.items()))[0][1])
        memoryGame.append(rd.choices(list(commons.items()))[0][1])
        memoryGame.append(rd.choices(list(uncommons.items()))[0][1])
        memoryGame.append(rd.choices(list(rares.items()))[0][1])
        
        #the curses can't be the same.
        if memoryGame[0]["Name"] == memoryGame[1]["Name"]:
            memoryGame = []
            continue 
        else:
            break

    i = 0
    while i < len(memoryGame):

        if moltenEgg == True and memoryGame[i].get("Type") == "Attack":
            newUpgradedCard = helping_functions.upgradeCard(shoplist[i].pop(i),"External Function")
            shoplist[i].insert(i,newUpgradedCard)
            

        elif toxicEgg == True and memoryGame[i].get("Type") == "Skill":
            newUpgradedCard = helping_functions.upgradeCard(memoryGame[i].pop(i),"External Function")
            memoryGame[i].insert(i,newUpgradedCard)
            

        elif frozenEgg == True and memoryGame[i].get("Type") == "Power":
            newUpgradedCard = helping_functions.upgradeCard(memoryGame[i].pop(i),"External Function")
            memoryGame[i].insert(i,newUpgradedCard)
            
       	i+=1

    memoryGame.extend(memoryGame.copy())
    rd.shuffle(memoryGame)

    tries = 5
    i = 0

    ansiprint("A <green>gremlin</green> is madly shuffling cards on a table. This monster seems to be a harmless one. You approach him out of curiosity.")
    ansiprint("<green>Gremlin</green>: \"<blue>Twelve</blue> cards. Match them to keep them! Five tries, no do-overs.\"")
    ansiprint("<green>Gremlin</green>: \"You ready? Let's start!\"")

    while i < tries:
        try:
            pickOne = input("Which card do you want to unveil? Type a number between 1 & 12.")
            pickOne = int(pickOne)-1
            if pickOne in range(len(memoryGame)):
                if memoryGame[pickOne] == "Drawn":
                    print("You've already added this card to the deck.")
                    continue
                print(memoryGame[pickOne].get("Name"))
            else:
                continue
            
            while True:
                try:
                    pickTwo = input("Which other card do you want to unveil?")
                    pickTwo = int(pickTwo)-1
                    if pickTwo in range(len(memoryGame)) and pickTwo != pickOne:
                        if memoryGame[pickTwo] == "Drawn":
                            print("You've already added this card to the deck.")
                            continue

                        print(memoryGame[pickTwo].get("Name"))
                        break
                    else:
                        print("Pick a different number.")
                except:
                    active_character[0].explainer_function(pickTwo)
                    print("You have to type a number.")
                    

            if memoryGame[pickOne]["Name"] == memoryGame[pickTwo]["Name"]:
                
                active_character[0].add_CardToDeck(memoryGame.pop(pickOne))
                memoryGame.insert(pickOne,"Drawn")
                print(memoryGame[pickTwo].get("Name"))
                memoryGame.pop(pickTwo)
                memoryGame.insert(pickTwo,"Drawn")

            pickOne = None
            pickTwo = None
            i += 1
            print("This was your",i,"try. You have 5.")
            time.sleep(3)
            
            print("\n"*100)

        except:
            active_character[0].explainer_function(pickOne)
            print("You have to type a number.")

    print("You complete the gremlin's game and look up. He disappeared?")

def event_OminousForge():
    ansiprint("You duck into a small hut. Inside, you find what appears to be a forge. The smithing tools are covered with dust, yet a fire roars inside the furnace. You feel on edge...")
    
    forgeOptions = ["1. <yellow>[Forge]</yellow> Upgrade a card.","2. <light-red>[Rummage]</light-red> Gain special <light-red>Relic</light-red>. Become <m>Cursed</m> (Pain).","3. [Leave] Nothing happens."]
    checkNumbers = ["1","2","3"]

    for option in forgeOptions:
        ansiprint (option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        ansiprint("You decide to put the forge to use and...")
        active_character[0].removeCardsFromDeck(1,removeType="Upgrade")
        ansiprint("...CLANG CLAAANG CLANG!... improve your arsenal!")

    elif snap == "2":
        active_character[0].add_relic({"Name":"Warped Tongs","Rarity":"Event","Owner":"The Spire","Type":"Relic"})
        active_character[0].add_CardToDeck({"Name": "Pain","Type": "Curse","Rarity": "Curse","Owner":"The Spire"})

    elif snap == "3":
        ansiprint("There doesn't seem to be anything of use. You exit the way you came, the flames of the furnace casting eerie shadows on the walls inside the hut..")

    else:
        ansiprint(snap,"issues with error detection in ominousForge")

def event_weMeetAgain():
    ansiprint("We meet again! A cheery disheveled fellow approaches you gleefully.You do not know this man. \n\"It's me, Ranwid! Have any goods for me today? The usual? A fella like me can't make it alone, you know?\" \nYou eye him suspiciously and consider your options...")
    
    randomPotion = None
    randomCard = None
    randomGold = None
    donationOptions = []

    i = 1
    if len(active_character[0].potionBag) > 0:
        randomPotion = rd.randint(0,len(active_character[0].potionBag)-1)
        donationOptions.append(str(i)+". [Give Potion] Lose a <c>"+active_character[0].potionBag[randomPotion]["Name"]+"</c>. Receive a Relic.")
        i+=1

    if active_character[0].gold >= 50:
        randomGold = rd.randint(50,active_character[0].gold)
        donationOptions.append(str(i)+". [Give Gold] Lose <yellow>"+str(randomGold)+"</yellow>. Receive a Relic.",)
        i+=1
    
    cardCheck = [card for card in active_character[0].deck if card.get("Rarity") != "Basic" and card.get("Type") != "Curse"]

    if len(cardCheck) > 0:
        while True:
            randomCard = rd.randint(0,len(active_character[0].deck)-1)
            if active_character[0].deck[randomCard].get("Rarity") == "Basic" or active_character[0].deck[randomCard].get("Type") == "Curse":
                continue
            else:
                donationOptions.append(str(i)+". [Give Card] Lose <blue>"+active_character[0].deck[randomCard]["Name"]+"</blue>. Receive a Relic.")
                break
        i+=1


    donationOptions.append(str(i)+". [Leave] Nothing happens.")

    for option in donationOptions:
        ansiprint (option)

    while True:
        try:
            snap = input("What do you want to do?\n")
            snap = int(snap)-1
            if snap not in range (len(donationOptions)):
                
                continue
            
            if snap == len(donationOptions)-1:
                break
            elif "Gold" in donationOptions[snap]:
                active_character[0].set_gold(-randomGold)  
            elif "Potion" in donationOptions[snap]:
                active_character[0].remove_Potion(index = randomPotion)
            elif "Card" in donationOptions[snap]:            
                active_character[0].removeCardsFromDeck(1,removeType="Remove",index=randomCard)      

            weMeetAgainRelic = helping_functions.generateRelicRewards("Event")
            helping_functions.pickRelic(weMeetAgainRelic)

            break
        
        except Exception as e:
            active_character[0].explainer_function(snap)
            print(e,"You have to type a number.")

def event_wheelOfChange():
    input("[Play] Spin the wheel and get a prize. (Type anything).")

    i = 0
    while i < 50:
        snap = rd.randint(1,6)
        if snap == 1:
            ansiprint("<yellow>Gold</yellow>")
        elif snap == 2:
            ansiprint("<light-red>Relic</light-red>")
        elif snap == 3:
            ansiprint("<red>Heal</red>")
        elif snap == 4:
            ansiprint("<m>Curse</m>")
        elif snap == 5:
            ansiprint("<M>Remove</M>")
        elif snap == 6:
            ansiprint("<RED>Damage</RED>")

        if i > 46:
            time.sleep(0.2)
        elif i > 35:
            time.sleep(0.09)
        elif i > 32:
            time.sleep(0.04)
        elif i > 12:
            time.sleep(0.026)
        elif i > 5:
            time.sleep(0.04)
        else:
            time.sleep(0.01)    
        i+=1

    if snap == 1:
        ansiprint("<yellow>GOLD</yellow>!")
        active_character[0].set_gold(100*helping_functions.gameAct)
    elif snap == 2:
        wheelOfChangeRelic = helping_functions.generateRelicRewards("Event")
        helping_functions.pickRelic(wheelOfChangeRelic)
    elif snap == 3:
        active_character[0].heal(active_character[0].max_health)
    elif snap == 4:
        active_character[0].add_CardToDeck({"Name": "Decay","Type": "Curse","Rarity": "Curse","Owner":"The Spire"})
    elif snap == 5:
        active_character[0].removeCardsFromDeck(1,removeType="Remove")
    elif snap == 6:
        damage = math.floor((active_character[0].max_health/100) *15)
        active_character[0].set_health(-damage)

def event_theWomanInBlue():
    ansiprint("From the darkness, an arm pulls you into a small shop. As your eyes adjust, you see a pale woman in sharp clothes gesturing towards a wall of potions. Pale Woman: \"Buy a potion. Now!\" she states.")
    damage = math.floor((active_character[0].max_health/100) *5)
    womanOptions = ["1. [Buy 1 Potion] 10 Gold.","2. [Buy 2 Potion] 20 Gold.","3. [Buy 3 Potion] 30 Gold.", "4. [Leave] Receive <red>"+str(damage)+"</red> damage."]
    checkNumbers = ["1","2","3","4"]

    for option in womanOptions:
        ansiprint (option)

    snap = None
    while True:
        
        snap = input("What do you want to do?\n")
        while snap not in checkNumbers:
            active_character[0].explainer_function(snap,answer=False)
            snap = input("What do you want to do? Pick the corresponding number.\n")

        if snap == "1":
            if active_character[0].gold > 10:
                active_character[0].set_gold(-10)
                break
            else:
                ansiprint("You don't have enough <yellow>gold</yellow>. You currently have <yellow>"+str(active_character[0].gold)+"Gold.")
                continue
        elif snap == "2":
            if active_character[0].gold > 20:
                active_character[0].set_gold(-20)
                break
            else:
                ansiprint("You don't have enough <yellow>gold</yellow>. You currently have <yellow>"+str(active_character[0].gold)+"Gold.")
                continue
        elif snap == "3":
            if active_character[0].gold > 30:
                active_character[0].set_gold(-30)
                break
            else:
                ansiprint("You don't have enough <yellow>gold</yellow>. You currently have <yellow>"+str(active_character[0].gold)+"Gold.")
                continue
        elif snap == "4":
            break


    if snap == "4":
        active_character[0].set_health(-damage)
        ansiprint("WHAM!\nHer gloved fist collides with your face, nearly knocking you off your feet.\nPale Woman: \"Get out before I litter the floor with your guts.\"\nYou take her word and exit with your guts still safely in your body.")
        
    else:
        options = []
        random_potions = {k:v for k,v in potions.items() if v.get("Owner") == active_character[0].name or v.get("Owner") == "The Spire"}
        choices_potion = rd.choices(list(random_potions.items()),k=int(snap))
        for potion in choices_potion:
            options.append(potion[1])

        helping_functions.pickPotion(options)
        ansiprint("Pale Woman: \"Good. Now leave.\"")

def event_faceTrade():
    ansiprint("You walk by an eerie statue holding several masks...\nSomething behind you softly whispers, \"Stop.\"\nYou swerve around to face the statue which is now facing you!\nOn closer inspection, it's not a statue but a statuesque, gaunt man. Is he even breathing?\nEerie Man: \"Face. Let me touch? Maybe trade?")
    damage = math.floor((active_character[0].max_health/100) *10)
    maskOptions = ["1. [Touch] Lose <red>"+str(damage)+" Health</red>. <yellow>Gain 50 Gold</yellow>.","2. <light-red>[Trade]</light-red> Receive Relic.","3. [Leave] Nothing happens."]
    checkNumbers = ["1","2","3"]
    
    for option in maskOptions:
        ansiprint (option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        ansiprint("Eerie Man: \"Compensation. Compensation.\"\nMechanically, he cranes out a neat stack of gold and places it into your pouch.\nEerie Man: \"What a nice face. Nice face.\" While he touches your face, you begin to feel your life drain out of it!\nDuring this, his mask falls off and shatters. Screaming, he quickly covers his face with all six arms dropping even more masks! Amidst all the screaming and shattering, you escape.\nHis face was completely blank.)")
        active_character[0].set_gold(50)
        active_character[0].set_health(-damage)

    elif snap == "2":
        ansiprint("Eerie Man: \"For me? FOR ME? Oh yes.. Yes. Yes.. mmm...\"\nYou see one of his arms flicker, and your face is in its hand!")
        faceRoll = rd.randint(0,4)

        if faceRoll == 0:
            active_character[0].add_relic({"Name":"Cultist Headpiece","Rarity":"Event","Owner":"The Spire","Type":"Relic"})
        elif faceRoll == 1:
            active_character[0].add_relic({"Name":"Face of Cleric","Rarity":"Event","Owner":"The Spire","Type":"Relic"})
        elif faceRoll == 2:
            active_character[0].add_relic({"Name":"Gremlin Visage","Rarity":"Event","Owner":"The Spire","Type":"Relic"})
        elif faceRoll == 3:
            active_character[0].add_relic({"Name":"N'loth's Hungry Face","Counter":1,"Rarity":"Event","Owner":"The Spire","Type":"Relic"})
        elif faceRoll == 4:
            active_character[0].add_relic({"Name":"Ssserpent Head","Rarity":"Event","Owner":"The Spire","Type":"Relic"})

        ansiprint("Your face has been swapped. Eerie Man: \"Nice face. Nice face.")
        

    elif snap == "3":
        ansiprint("Eerie Man: \"Stop. Stop. Stop. Stop. Stop! WAIT FOR MEEEE!\"You keep going... This was probably the right call.")
    else:
        ansiprint(snap,"event_faceTrade has an issue")

def event_bigFish():
    #exclusiveAct1Event
    ansiprint("As you make your way down a long corridor you see a banana, a donut, and a box floating about. No... upon closer inspection they are tied to strings coming from holes in the ceiling. There is a quiet cackling from above as you approach the objects. What do you do?")
    healing = math.floor(active_character[0].max_health/3)
    fishOptions = ["1. [Banana] Heal <red>"+str(healing)+" Health</red>","2. [Donut] Max HP +5","3. [Box] Receive a Relic. Become <m>Cursed (Regret)</m>"]
    checkNumbers = ["1","2","3"]

    for option in fishOptions:
        ansiprint (option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        ansiprint("You eat the <yellow>banana</yellow>. It is nutritious and slightly <blue>magical</blue>, healing you.")
        active_character[0].heal(healing)

    elif snap == "2":
        ansiprint("You eat the <fg #C89D7C>donut</fg #C89D7C>. It really hits the spot! Your <red>Max HP</red> increases.")
        active_character[0].set_maxHealth(5)
    
    elif snap == "3":
        bigFishRelic = helping_functions.generateRelicRewards(place="Event")
        ansiprint("You grab the box. Inside you find a <light-red>"+bigFishRelic[0].get("Name")+"</light-red>!\nHowever, you really craved the donut...\nYou are filled with sadness, but mostly <m>regret</m>.")
        active_character[0].add_relic(bigFishRelic[0])
        active_character[0].add_CardToDeck({"Name": "Regret","Type": "Curse","Rarity": "Curse","Owner":"The Spire"})    

def event_DeadAdventurer():
    #exclusiveAct1Event
    eliteAdversary = []
    bossRandom = rd.randint(1,3)
    ansiprint("You come across a dead adventurer on the floor. His pants have been stolen! Also, ...")
    time.sleep(0.3)
    if bossRandom == 1:
        ansiprint("...he looks to have been eviscerated and chopped by giant claws.")
        enemy = "Lagavulin"
        eliteAdversary.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = [20,"SiphonSoul 2"],intention_logic = [["Random"],[1,0,0]*33]))
                                                                                                
    elif bossRandom == 2:
        ansiprint("...the armor and face appear to be scoured by flames.")
        enemy = "Bolt Sentry"
        eliteAdversary.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death"), artifact = enemies[enemy].get("Artifact")))
        
        enemy = "Beam Sentry"
        eliteAdversary.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death"), artifact = enemies[enemy].get("Artifact")))
        
        enemy = "Bolt Sentry"
        eliteAdversary.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death"), artifact = enemies[enemy].get("Artifact")))
        

    elif bossRandom == 3:
        ansiprint("...it looks as though he's been gouged and trampled by a horned beast.")
        enemy = "Gremlin Nob"
        eliteAdversary.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))


    time.sleep(0.3)
    ansiprint("Though his possessions are still intact, you're in no mind to find out what happened here...")
    rewards = ["30 Gold","Random Relic","Nothing"]
    deadOptions = ["1. [Search] Find Loot. <red>35%</red> that an Elite will return to fight you.","2. [Leave] Nothing happens."]
    checkNumbers = ["1","2"]

    for option in deadOptions:
        ansiprint (option)

    eliteChance = 35
    deadAdventurerRelic = helping_functions.generateRelicRewards(place="Event")
    while True:
        if len(rewards) == 0:
            ansiprint("Looks like you searched all his belongings without a hitch!")
            break
        else:
            snap = input("What do you want to do?\n")
        while snap not in checkNumbers:
            active_character[0].explainer_function(snap,answer=False)
            snap = input("What do you want to do? Pick the corresponding number.\n")

        if snap == "1":
            if rd.randint(1,100) > eliteChance:
                reward = rewards.pop(rd.randint(0,len(rewards)-1))
                if reward == "30 Gold":
                    ansiprint("You found some gold!")
                    active_character[0].set_gold(30)
                elif reward == "Random Relic":
                    ansiprint("You found a <light-red>Relic</light-red>!!")
                    active_character[0].add_relic(deadAdventurerRelic.pop(0))

                elif reward == "Nothing":
                    ansiprint("Hmm couldn't find anything!!")
                eliteChance += 25
                continue
            else:
                ansiprint("While searching the adventurer you are caught off guard! Prepare for BATTLE!")
                eventFight(eliteAdversary)
                
                eventCardsRewards = helping_functions.generateCardRewards()
                goldReward = rd.randint(25,35)
                

                while len(rewards) > 0:
                    reward = rewards.pop(0)
                    if reward == "30 Gold":
                        ansiprint("You found some <yellow>Gold</yellow>!")
                        active_character[0].set_gold(30)
                    elif reward == "Random Relic":
                    	active_character[0].add_relic(deadAdventurerRelic.pop(0))
                    elif reward == "Nothing":
                        pass
                helping_functions.afterEventBattleRewardScreen(gold= goldReward,cards = eventCardsRewards)
                break

        elif snap == "2":
            ansiprint("You exit without a sound.")
            break
            
def event_GoldenIdol():
    #exclusiveAct1Event
    ansiprint("You come across an inconspicuous pedestal with a <yellow>shining gold idol</yellow> sitting peacefully atop. It looks incredibly valuable.\nYou sure don't see any traps nearby.")
    
    idolOptions = ["1. [Take] Obtain <light-red>Golden Idol</light-red>. <red>Triggers a trap</red>.","2. [Leave] Nothing happens."]
    checkNumbers = ["1","2"]
    
    damageSmash = math.floor((active_character[0].max_health/100)*35)
    damageHide = math.floor(active_character[0].max_health/10)
    boulderOptions = ["1. [Outrun] Become Cursed - Injury","2. [Smash] Take <red>"+str(damageSmash)+" damage</red>." ,"3. [Hide] Lose <red>" +str(damageHide)+ " Max HP</red>."]
    checkNumbers2 = ["1","2","3"]

    for option in idolOptions:
        ansiprint (option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        ansiprint("As you grab the Idol and stow it away, a giant boulder smashes through the ceiling into the ground next to you. You realize that the floor is slanted downwards as the boulder starts to roll towards you.")
        active_character[0].add_relic({"Name":"Golden Idol","Rarity":"Event","Owner":"The Spire","Type":"Relic"})

        for option in boulderOptions:
            ansiprint (option)

        snapTwo = input("What do you want to do?\n")

        while snapTwo not in checkNumbers2:
            active_character[0].explainer_function(snapTwo,answer=False)
            input("What do you want to do? Pick the corresponding number.\n")

        if snapTwo == "1":
            ansiprint("RUUUUUUUUUUN! You barely leap into a side passageway as the boulder rushes by. Unfortunately it feels like you sprained something!")
            active_character[0].add_CardToDeck({"Name": "Injury","Type": "Curse","Rarity": "Curse","Owner":"The Spire"})

        elif snapTwo == "2":
            ansiprint("You throw yourself at the boulder with everything you have. When the dust clears, you can make a safe way out.")
            active_character[0].set_health(-damageSmash)

        elif snapTwo == "3":
            ansiprint("SQUISH! The boulder flattens you a little as it passes by, but otherwise you can get out of here.")
            active_character[0].set_maxHealth(-damageHide)
        else:
            ansiprint("Issue in eventGoldenIdol. Boulder")

    elif snap == "2":
        ansiprint("If there was ever an obvious trap, this would be it. You decide not to interfere with objects placed upon pedestals.")

    else:
        ansiprint("Issue in eventGoldenIdol. Idol")

          
def event_HypnotizingColoredMushrooms():
    #exclusiveAct1EventOnlyFloor7

    ansiprint("You enter a corridor full of hypnotizing colored mushrooms.\nDue to your lack of specialization in mycology you are unable to identify the specimens.\nYou want to escape, but feel oddly compelled to eat a mushroom.")
    healing = math.floor(active_character[0].max_health/4)
    shroomOptions = ["1. [Stomp] Anger the Mushrooms.","2. [Eat] Heal <red>"+str(healing)+" HP</red>. Become <m>Cursed: (Parasite)</m>."]
    checkNumbers = ["1","2"]
    fungiList = []
    for option in shroomOptions:
        ansiprint (option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        ansiprint("<red>Ambushed!! Rodents infested by the mushrooms appear out of nowhere!</red>")
        enemy = "Fungi Beast"
        fungiList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
        fungiList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
        fungiList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
        eventFight(fungiList)
        goldReward = helping_functions.generateGoldReward("Creep")
        cardReward = helping_functions.generateCardRewards()
        potionReward = helping_functions.generatePotionRewards()
        relicReward = {"Name":"Odd Mushroom","Rarity":"Event","Owner":"The Spire","Type":"Relic"}
        helping_functions.afterEventBattleRewardScreen(gold= goldReward,cards = cardReward,potion = potionReward,relic=relicReward)

    elif snap == "2":
        ansiprint("You give in to the unnatural desire to eat. As you consume mushroom after mushroom, you feel yourself entering into a daze and pass out. As you awake, you feel very odd.\nYou heal <red>"+str(healing)+"</red> but you also get <m>infected</m>.")
        active_character[0].heal(healing)
        active_character[0].add_CardToDeck({"Name": "Parasite","Type": "Curse","Rarity": "Curse","Owner":"The Spire"})

    else:
        ansiprint("Mistake in hypnotizingMushrooms. Sorry.")

def event_LivingWall():
    #exclusiveAct1Event
    ansiprint("As you come to a dead-end and begin to turn around, walls slam down from the ceiling, trapping you! Three faces materialize from the walls and speak.\n\n<light-blue>Forget what you know, and I'll let you go.</light-blue>\n<green>I require change to see a new space.</green>\n<yellow>If you want to pass me, then you must grow.</yellow>")
    
    wallOptions = ["1. <light-blue>[Forget]</light-blue> Remove a card from your deck.","2. <green>[Change]</green> Transform a card in your deck.","3. <yellow>[Grow]</yellow> Upgrade a card in your deck."]
    checkNumbers = ["1","2","3"]

    for option in wallOptions:
        ansiprint (option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        active_character[0].removeCardsFromDeck(1,removeType="Remove")

    elif snap == "2":
        active_character[0].removeCardsFromDeck(1,removeType="Transform")

    elif snap == "3":
        active_character[0].removeCardsFromDeck(1,removeType="Upgrade")

    else:
        ansiprint("Issues in event_LivingWall.")
    
    ansiprint("Satisfied, the walls in front of you merge back into the ceiling, leaving a path forward.")

def event_ScrapOoze():
    #exclusiveAct1Event
    ansiprint("As you walk into the room you hear a gurgling and the grinding of metals. Before you is a slime-like creature that ate too much scrap for its own good. From the center of the creature you see glints of strange light, perhaps something magical? <yellow>It looks like you can get some treasure if you just reach inside its </yellow>... opening. <red>However, the acid and sharp objects may hurt.</red>")
    
    healthLoss = 5
    relicSuccessChance = 25
    oozeOptions = ["1. <red>[Reach Inside]</red> Lose <red>"+str(healthLoss)+" HP</red>. <yellow>"+str(relicSuccessChance)+"% to find Relic</yellow>.","2. [Leave] Nothing happens."]
    checkNumbers = ["1","2"]

    while True:
        for option in oozeOptions:
            ansiprint (option)

        snap = input("What do you want to do?\n")

        while snap not in checkNumbers:
            active_character[0].explainer_function(snap,answer=False)
            snap = input("What do you want to do? Pick the corresponding number.\n")

        if snap == "1":
            if rd.randint(1,100) > relicSuccessChance:
                relicSuccessChance +=10
                healthLoss += 1
                active_character[0].set_health(-healthLoss)
                ansiprint("<red>Ouch! All you find is corroded metal and a bit of burning pain.</red>\n<yellow>However, you're still convinced there's a relic...</yellow>")
                oozeOptions = ["1. <red>[Reach Inside]</red> Lose <red>"+str(healthLoss)+" HP</red>. <light-red>"+str(relicSuccessChance)+"% to find Relic</light-red>.","2. [Leave] Nothing happens."]
            else:
                ansiprint("<green>Success!</green> After rummaging through the metal and burning acid, you finally grab hold of a <light-red>Relic</light-red> and yank it out. You pull your way out of the ooze <red>damaged</red> but rewarded.")
                oozeRelic = helping_functions.generateRelicRewards(place = "Event")
                helping_functions.pickRelic(oozeRelic)
                break

        elif snap == "2":
            ansiprint("You decide to leave the area. The slime pays no attention, content with its meal.")
            break
        else:
            ansiprint("Issues in event_ScrapOoze.")

def event_shiningLight():
    #exclusiveAct1Event
    ansiprint("You find a <yellow>shimmering mass of light</yellow> encompassing the center of the room. Its warm glow and enchanting patterns invite you in.")

    #diesen Upgrade Test muss man eigentlich machen bevor man das Event betritt. Aka don't add this event to the pool, if 
    #upgradeTest = [card for card in entities.active_character[0].deck if card.get("Upgraded") != True and card.get("Type") != "Curse"]
    #if len(upgradeTest) >= 2:
    
    damage = math.floor((active_character[0].max_health/100) *30)
    lightOptions = ["1. <yellow>[Enter]</yellow> Upgrade 2 random cards. Take <red>" +str(damage)+" Damage</red>.","2. [Leave] Nothing happens"]
    checkNumbers = ["1","2"]

    for option in lightOptions:
        ansiprint (option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        ansiprint("<yellow>As you walk through the light, you notice that the light is absorbed into you</yellow>.\n<red>It's scorching hot!</red> However, the pain quickly recedes.\n<blue>You feel invigorated</blue>, as though you received a well deserved slap.\n")
        i = 0
        while i < 2:
            index = helping_functions.getRandomSpecifiedCardIndex(specifics="Upgrade")
            active_character[0].removeCardsFromDeck(amount = 1,removeType = "Upgrade",index = index)
            i+=1
        
    elif snap == "2":
        ansiprint("You walk around it, wondering what could have been.")

    else:
        ansiprint("SnizzlesOfMizzles. Something wrong happened in event_shinigLight")

def event_theSerpent():
    #exclusiveAct1Event
    ansiprint("You walk into a room to find a large hole in the ground. As you approach the hole, an enormous serpent creature appears from within. \n<green>Serpent</green>: \"Ho hooo! Hello hello! what have we got here? Hello adventurer, I ask a simple question.\n\"<green>Serpent</green>: \"The most fulfilling of lives is that in which you can <yellow>buy anything<yellow>!\"<green>Serpent</green>: \"<m>Do you agree</m>?\"")

    #diesen Upgrade Test muss man eigentlich machen bevor man das Event betritt. Aka don't add this event to the pool, if 
    #upgradeTest = [card for card in entities.active_character[0].deck if card.get("Upgraded") != True and card.get("Type") != "Curse"]
    #if len(upgradeTest) >= 2:
    
    serpentOptions = ["1. <yellow>[Agree]</yellow> Receive <yellow>150 Gold</yellow>. Become <m>Cursed (Doubt)</m>","2. [Disagree] Nothing happens"]
    checkNumbers = ["1","2"]

    for option in serpentOptions:
        ansiprint (option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":

        ansiprint("Serpent: \"Yeeeeeeessssssssssessss\"\n<green>Serpent</green>: \"Thisss will all be worthhh it.\"\n<green>Serpent</green>: \"..ssSSs..... ss... sssss....!\"\nThe <green>Serpent</green> rears its head and blasts a <yellow>stream of Gold</yellow> upwards!\nIt is amazing and terrifying simultaneously.\nYou gather all the <yellow>Gold</yellow>, thank the snake, and get going. <m>You've felt better before</m>.")
        active_character[0].set_gold(150)
        active_character[0].add_CardToDeck({"Name": "Doubt","Type": "Curse","Rarity": "Curse","Owner":"The Spire"})
    elif snap == "2":
        ansiprint("The serpent stares at you with a look of extreme disappointment. You wonder what could have been.")

    else:
        ansiprint("Somenthing wrong in event The Serpent.")

def event_poolOfGoop():
    #exclusiveAct1Event
    ansiprint("You fall into a puddle.\nIT'S MADE OF <green>SLIME GOOP</green>!!\nFrantically, you claw yourself out over several minutes as you feel the goop starting to <red>burn</red>.\nYou can feel goop in your ears, goop in your nose, goop everywhere.\nClimbing out, you notice that some of your <yellow>gold</yellow> is missing. Looking back to the puddle you see your missing coins combined with <yellow>gold</yellow> from unfortunate adventurers mixed together in the puddle.\n")

    goldLoss = rd.randint(35,75)

    if goldLoss > active_character[0].gold:
        goldLoss == active_character[0].gold

    poolOptions = ["1. [Gather Gold] Gain <yellow>75 Gold</yellow>. Lose <red>11 HP</red>","2. [Leave It] Lose <yellow>" + str(goldLoss)+" Gold</yellow>."]
    checkNumbers = ["1","2"]

    for option in poolOptions:
        ansiprint (option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        active_character[0].set_gold(75)
        active_character[0].set_health(-11)
        ansiprint("Feeling the <red>sting of the goop</red> as the prolonged exposure starts to melt away at your skin, you manage to fish out the <yellow>gold</yellow>.")

    elif snap == "2":
        active_character[0].set_gold(-goldLoss)
        ansiprint("You decide that mess is not worth it, so you leave your and the other <yellow>gold</yellow> lying in the goop.")
        
    else:
        ansiprint("Somenthing wrong in event The Goop.")

def event_wingStatue():
    #exclusiveAct1Event
    ansiprint("Among the stone and boulders, you notice an intricate <blue>large blue</blue> statue resembling a wing.\nYou find <yellow>gold</yellow> spilling from its cracks. Maybe there is more inside...")

    attacks = list([card for card in active_character[0].deck if card.get("Type") == "Attack"])
    tenDamageCards = list([card for card in attacks if card.get("Damage") >= 10])

    if len(tenDamageCards) > 0:

        goldGain = rd.randint(50,80)
        wingOptions = ["1. [Pray] Remove a card from your deck. Lose <red>7 HP</red>.","2. [Destroy] Gain <yellow>" + str(goldGain)+" Gold</yellow>.","3. [Leave] Nothing happens."]
        checkNumbers = ["1","2","3"]

        for option in wingOptions:
            ansiprint (option)

        snap = input("What do you want to do?\n")

        while snap not in checkNumbers:
            active_character[0].explainer_function(snap,answer=False)
            snap = input("What do you want to do? Pick the corresponding number.\n")

        if snap == "1":
            ansiprint("Someone once told you of a cult that worshipped a giant bird. As you kneel in prayer, you begin to feel ... lightheaded.\nYou wake up some time later, feeling strangely <red>fleet of foot</red>.")
            active_character[0].removeCardsFromDeck(1,removeType = "Remove")
            active_character[0].set_health(-7)

        elif snap == "2":
            ansiprint("With all your might, you hack away at the statue.\nIt soon crumbles, revealing a <yellow>pile of gold</yellow>. You grab as much as you can and continue onwards.")
            active_character[0].set_gold(goldGain)
        
        elif snap == "3":
            ansiprint("The statue makes you feel uneasy. You walk past and continue onward.")

        else:
            print(snap,"Something wrong in lenDamageCards > 0 in event event_wingStatue")
    
    elif len(tenDamageCards) == 0:

        wingOptions = ["1. [Pray] Remove a card from your deck. Lose <red>7 HP</red>.","2. [Leave] Nothing happens."]
        checkNumbers = ["1","2"]

        for option in wingOptions:
            ansiprint (option)

        snap = input("What do you want to do?\n")

        while snap not in checkNumbers:
            active_character[0].explainer_function(snap,answer=False)
            snap = input("What do you want to do? Pick the corresponding number.\n")

        if snap == "1":
            ansiprint("Someone once told you of a cult that worshipped a giant bird. As you kneel in prayer, you begin to feel ... lightheaded.\nYou wake up some time later, feeling strangely <red>fleet of foot</red>.")
            active_character[0].removeCardsFromDeck(1,removeType = "Remove")
            active_character[0].set_health(-7)
        
        elif snap == "2":
            ansiprint("The statue makes you feel uneasy. You walk past and continue onward.")

        else:
            print(snap,"Something wrong in lenDamageCards = 0 in event event_wingStatue")
    else:

        print(tenDamageCards)
        print("Something went wrong in Wing Statue Event.")

#ACT 2 Events

def event_ancientWriting():
    ansiprint("Scaling the city, you notice a wall covered in the writing of Ancients.\nAs you try to wrap your head around what the puzzling symbols and glyphs could mean, the writing begins to glow.\nSuddenly, the message becomes clear...")


    ancientOptions = ["1. [Elegance] Remove a card from your deck.","2. [Simplicity] Upgrade all <red>\"Strikes\"</red> and <green>\"Defends\"</green>."]
    checkNumbers = ["1","2"]

    for option in ancientOptions:
        ansiprint (option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        active_character[0].removeCardsFromDeck(1,"Remove")
        ansiprint("The answer was elegance. Of course.")

    elif snap =="2":
        i = 0
        while i < len(active_character[0].deck):
            if active_character[0].deck[i].get("Name") == "Strike":
                helping_functions.upgradeCard(active_character[0].deck.pop(i),place = "Deck",index = i)
            elif active_character[0].deck[i].get("Name") == "Defend":
                helping_functions.upgradeCard(active_character[0].deck.pop(i),place = "Deck",index = i)
            i+=1
        ansiprint("The truth is always simple.")
    else:
        print("Something went wrong in event_ancientWriting.")

def event_Augmenter():

    ansiprint("A man with an eyepatch and a devilish grin strides up to you.\nShady Man: \"Hey there, stranger. Interested in advancing science? I can make you stronger than any training or blessing.\nYou're gonna need it if you're one of those heroes with a death wish.\"\nShady Man: \"Whad'ya say?\"")
    
    augmenterOptions = ["1. [Test JAX] Obtain a <green>JAX</green>.", "2. [Become Test Subject] Choose and Transform 2 cards in your deck.","3. <light-red>[Ingest Mutagens]</light-red> Obtain a <light-red>Mutagenic Strength</light-red>."]
    checkNumbers = ["1","2","3"]

    for option in augmenterOptions:
        ansiprint (option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        ansiprint("Shady Man: \"Excellent.\"The man hands over a dangerous looking syringe filled with a <green>glowing liquid</green> before skulking off into a shadowy alleyway.")
        active_character[0].add_CardToDeck({"Name": "JAX","Energy": 0,"Strength":2,"Harm":3,"Type": "Skill","Rarity": "Special","Owner":"Colorless","Info":"Lose <red>3 HP</red>. Gain <red>2 Strength</red>."})

    elif snap == "2":
        ansiprint("Shady Man: \"Superb.\" The man injects you with three unknown substances and pulls out a notepad.\nAs you begin to feel light-headed, he starts to frantically write down notes.\n Losing track of time completely, by the time you regain your senses, the shady character has disappeared.")
        active_character[0].removeCardsFromDeck(2,removeType = "Transform")

    elif snap == "3":
        ansiprint("Shady Man: \"Marvelous.\" You quaff the mysterious substance. Immediately, you are invigorated and feel your muscle fibers twitch.")
        active_character[0].add_relic({"Name":"Mutagenic Strength","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"Start each combat with <red>3 Strength</red> that is lost at the end of your turn."})

    else:
        print("Issue in Augmenter Event.")

def event_theColosseum():
    ansiprint("Thwack!!! You were knocked unconscious.\nGroggy and with a throbbing head, you awaken to find yourself thrown in the center of a massive stadium with an overflowing audience of Slavers, Cultists, and other denizens of the City!\nAn armored giant with a golden crown bellows at you from atop, Armored Giant: \"WE NOW BEGIN THE COMBAT!!!!\"A gate on the opposite side opens...")

    slavers = []
    enemy = "Red Slaver"
    slavers.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
    enemy = "Blue Slaver"
    slavers.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

    ansiprint("<red>[Fight]</red> Begins a battle with <red>Blue Slaver</red> and <red>Red Slaver</red>.")
    input("Type anything to start the fight.\n")

    eventFight(slavers)

    ansiprint("Armored Giant: \"WELL DONE, WEAKLING!\"\nThe giant mock claps whilst he riles up the crowd with exaggerated gestures.\n<yellow>Gold</yellow> and confetti shower you!\nArmored Giant: \"TIME FOR THE REAL CHALLENGE!!\"\nThe last battle left a small opening in the Colosseum’s wall, you can easily escape through there while everyone is distracted.\nDo you stay and fight?")

    colosseumoptions = ["1. [COWARDICE] Escape.","2. [VICTORY] Begins a fight with a <red>Taskmaster</red> and a <red>Gremlin Nob</red>."]
    checkNumbers = ["1","2"]

    for option in colosseumoptions:
        ansiprint(option)

    snap = input("What do you want to do?")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        ansiprint("While the crowd is loosing itself in pandemoniums, you escape through the small opening in the wall. Probably smart.")

    elif snap == "2":
        ansiprint("The chants of the crowd get louder and louder. You ready yourself!")

        slavers = []
        enemy = "Gremlin Nob"
        slavers.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
        enemy = "Taskmaster"
        slavers.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

        eventFight(slavers)
        
        goldReward = 100
        cardReward = helping_functions.generateCardRewards()
        relicReward = helping_functions.generateRelicRewards(specificType = "Uncommon")
        secondrelicReward = helping_functions.generateRelicRewards(specificType = "Rare")
        helping_functions.afterEventBattleRewardScreen(gold = goldReward,cards = cardReward, relic = relicReward[0], secondRelic = secondrelicReward[0])

def event_CouncilOfGhosts():
    ansiprint("As you continue your ascent, thick <black>black smoke</black> begins to billow out of the ground and walls around you, coalescing into three masked forms that start to speak.\nShape #1: \"Another puppet of Neow I think.\"\nShape #2: \"<red>AGREED! SHE ALWAYS MAKES THE FUNNEST TOYS</red>!\"\nYou notice an over-sized grin as the third addresses you.\nShape #3: \"Ignore the others... Would you like a taste of our power?\"\n")
    

    ghostlyOptions = ["1. [Accept] Receive <green>3 Apparition</green>. Lose <red>50% Max HP</red>.","2. [Refuse] Nothing happens.."]
    checkNumbers = ["1","2"]

    for option in ghostlyOptions:
        ansiprint (option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        ansiprint("Shape #3: \"Excellent!\"\nAs the ghostly shape speaks, you notice its large mouth opening wider and wider. Thick <black>black smoke</black> spews forth and envelops the room. You cannot see or breathe...\nJust before you lose consciousness, the sensation stops.\nWhatever those things were, they are gone now. You continue on, feeling rather hollow.\n")
        i = 0
        while i < 3:
            active_character[0].add_CardToDeck({"Name": "Apparition","Energy": 1,"Intangible":1,"Exhaust":True,"Ethereal":True,"Type": "Skill","Rarity": "Special","Owner":"Colorless","Info":"<BLUE>Ethereal</BLUE>. Gain <blue>1 Intangible</blue>. <BLUE>Exhaust</BLUE>."})
            i+=1
        halfMaxHealth = math.floor(active_character[0].max_health // 2)

        active_character[0].set_maxHealth(-halfMaxHealth)

    elif snap == "2":
        ansiprint("Shape #3: \"How disappointing...\"\nShape #1: \"<red>You will join us sooner or later.</red>\"\nShape #2: \"HA HA HA HAHAHA!\"\nThe shapes fade away, leaving only the unnerving laughter ringing in your ears.")

def event_cursedBook():
	ansiprint("In an abandoned temple, you find a giant book, open, riddled with <m>cryptic writings</m>.\nAs you try to interpret the elaborate script, it begins shift and morph into writing you are familiar with.")

	bookOptions = ["1. [Read] You know it's <green>good</green>. You know it's <red>bad</red>.","2. [Leave] Nothing happens.."]
	checkNumbers = ["1","2"]

	for option in bookOptions:
		ansiprint(option)

	snap = input("What do you want to do?\n")

	while snap not in checkNumbers:
		active_character[0].explainer_function(snap,answer=False)
		snap = input("What do you want to do? Pick the corresponding number.\n")

	if snap == "1":
		ansiprint("Odd. The book seems to be about an Ancient named <light-blue>Neow</light-blue>.\nThis piques your interest, but you have a general feeling of <m>malaise</m>.")
		input("[Continue]")
		ansiprint("The Ancient of resurrection, Neow, was exiled to the bottom of the Spire.\nYou feel compelled to read more, but your <red>body begins to ache</red>.")
		active_character[0].set_health(-1)
		input("[Continue]")
		ansiprint("Seeking vengeance, Neow blesses outsiders, using them for her own purposes.\nYou are starting to feel <red>very weak and tired</red>.")
		active_character[0].set_health(-2)
		input("[Continue]")
		ansiprint("Those resurrected by Neow remember only fragments of their past selves, <m>cursed</m> to <black>fight</black> for eternity.\nAs you near the final page, your <red>old wounds begin to reopen</red>!")
		active_character[0].set_health(-3)

		moreBookOptions = ["1. [Take] Obtain the <light-red>Book</light-red>. Lose <red>15 HP</red>.","2. [Leave] Lose <red>3 HP</red>"]

		for option in moreBookOptions:
			ansiprint(option)

		snap = input("What do you want to do?\n")

		while snap not in checkNumbers:
			active_character[0].explainer_function(snap,answer=False)
			snap = input("What do you want to do? Pick the corresponding number.\n")

		if snap == "1":
			ansiprint("Upon finishing the tome, you decide to take it with you. With proof in hand, will you retain your memories?")
			active_character[0].set_health(-15)
			book = rd.randint(1,3)
			if book == 1:
				active_character[0].add_relic({"Name":"Necronomicon","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"The first <red>Attack</red> played each turn that costs 2 or more is played twice. When you take this <light-red>Relic</light-red>, become <m>Cursed</m>."})
				
			elif book == 2:
				active_character[0].add_relic({"Name":"Enchiridion","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"At the start of each combat, add a random <blue>Power</blue> to your hand. It costs <yellow>0 Energy</yellow> until the end of turn."})
			
			elif book == 3:
				active_character[0].add_relic({"Name":"Nilry's Codex","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"At the end of each turn, you can choose 1 of 3 random Cards to shuffle into your Drawpile."})
	
		elif snap == "2":
			ansiprint("With incredible strain and willpower, you resist the trance of the tome and <red>SLAM</red> it shut.\nYou turn and exit the temple, <red>feeling drained</red>...")
			active_character[0].set_health(-3)

	elif snap == "2":
		ansiprint("You exit, feeling a <m>dark energy</m> emanating from the book on the pedestal.")

def event_theForgottenAltar():
	ansiprint("In front of you sits an altar to a forgotten god.\nAtop the altar sits an <yellow>ornate</yellow> <red>female</red> <yellow>statue</yellow> with arms outstretched.\nShe calls out to you, demanding <red>sacrifice</red>.")
	healthLoss = math.floor(active_character[0].max_health / 100 * 35)

	altarOptions = ["1. [Sacrifice] Gain <red>5 Max HP</red>. Lose <red>"+str(healthLoss)+"HP</red>.","2. [Desecrate] Become <m>Cursed - Decay</m>."]
	checkNumbers = ["1","2"]
	goldenIdol = False

	for relic in active_character[0].relics:
		if relic.get("Name") == "Golden Idol":
			goldenIdol = True

	if goldenIdol == True:
		altarOptions.append("3. [Offer] Obtain a special <light-red>Relic</light-red>. Lose <light-red>Golden Relic</light-red>.")
		checkNumbers.append("3")

	for option in altarOptions:
		ansiprint(option)

	snap = input("What do you want to do?\n")

	while snap not in checkNumbers:
		active_character[0].explainer_function(snap,answer=False)
		snap = input("What do you want to do? Pick the corresponding number.\n")

	if snap == "1":
		ansiprint("You stand on the altar and <red>cut your wrists</red>.\nAs the <red>blood spills</red> out in sacrifice, the arms of the statue reach out and close around your eyes.\nEverything goes <black>dark</black>.\nYou wake up a short time later feeling a new potential surging through you.\n")
		active_character[0].set_maxHealth(5)
		active_character[0].set_health(-healthLoss)

	elif snap == "2":
		ansiprint("You lash out and smash the statue in front of you, breaking the magical hold the room had placed upon you.\nA dark wail echoes all around you, and you can feel the <m>cursed magic</m> seep into your bones.")
		active_character[0].add_CardToDeck({"Name": "Decay","Type": "Curse","Rarity": "Curse","Owner":"The Spire","Info":"<RED>Unplayable</RED>. At the end of your turn, take <red>2 damage</red>."})

	elif snap == "3":
		active_character[0].remove_Relic("Golden Idol")
		active_character[0].add_relic({"Name":"Bloody Idol","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"Whenever you gain <yellow>Gold</yellow>, heal <red>5 HP</red>."})

def event_theJoust():
	ansiprint("As you make your way through the large buildings you come across a long narrow bridge and spot knights on either side, facing one another. You approach...\nKnight: \"HALT!\"\nA knight forcefully gestures you to stop with its giant lance.\nKnight: \"Today is the day I must settle the score with the <red>murderer</red> of my beloved pet, Noodles. Until then, you may not pass.\"\nKnight: \"Fellow witness, why don't you bet on who you think will <yellow>emerge victorious</yellow>?\"\n")
	
	joustOptions = ["1. [Murderer] Bet <yellow>50 Gold</yellow> - 70%: win <yellow>100 Gold</yellow>. ","2. [Owner] Bet <yellow>50 Gold</yellow> - 30%: win <yellow>250 Gold</yellow>.."]
	checkNumbers = ["1","2"]
	knight = False

	for option in joustOptions:
		ansiprint(option)

	if rd.randint(1,10) <= 3:
		knight = True

	snap = input("What do you want to do?\n")

	while snap not in checkNumbers:
		active_character[0].explainer_function(snap,answer=False)
		snap = input("What do you want to do? Pick the corresponding number.\n")

	if snap == "1":
		ansiprint("Knight: \"I can't believe you're betting against Noodles!\"\nFurious, he clamps down his helmet and rushes towards his nemesis.")
		ansiprint("<yellow>*CRASH!!!*</yellow>\n<red>*KLAAAAANG*</red>\n<green>*POW!*</green>")

		if knight == True:
			ansiprint("The nemesis was slain.")
			ansiprint("You lost the bet, but at least you weren't gouged by a lance.")
			active_character[0].set_gold(-50)

		else:
			ansiprint("The knight died.")
			ansiprint("You win the bet. Unsure what to think, you grab your winnings and leave.")
			active_character[0].set_gold(100)
	
	elif snap == "2":

		ansiprint("Knight: \"Give me strength, Noodles!\"\nClamping down his helmet, the knight charges forward.")
		ansiprint("<yellow>*CRASH!!!*</yellow>\n<red>*KLAAAAANG*</red>\n<green>POW!</green>")

		if knight == True:
			ansiprint("The nemesis was slain.")
			ansiprint("You win the bet. Unsure what to think, you grab your winnings and leave.")
			active_character[0].set_gold(250)

		else:
			ansiprint("The knight died.")
			ansiprint("You lost the bet, but at least you weren't gouged by a lance.")
			active_character[0].set_gold(-50)

def event_knowingSkull():
	ansiprint("You find yourself in an old, decorated chamber. In the center of the room, a large skull sits atop an ornate pedestal.\n As you approach, the skull bursts <red>into flames</red> and turns to face you.\n\"WHAT IS IT YOU SEEK? WHAT IS IT YOU OFFER?\"\nIn sync with its final words, the door behind you slams shut.\n")
	healthLoss = math.floor(active_character[0].max_health / 10)
	if healthLoss < 6:
		healthLoss = 6

	skullOptions = ["1. [Riches?] Obtain <yellow>90 Gold</yellow>. Lose <red>"+str(healthLoss)+" HP</red>.","2. [Success?] Obtain a random Uncommon Colorless card. Lose <red>"+str(healthLoss)+" HP</red>.","3. [A Pick Me Up?] Obtain a <c>Potion</c>. Lose <red>"+str(healthLoss)+" HP</red>.","4. [How do I leave?] End the event. Lose <red>"+str(healthLoss)+" HP</red>."]

	checkNumbers = ["1","2","3","4"]

	while True:
		skullOptions = ["1. [Riches?] Obtain <yellow>90 Gold</yellow>. Lose <red>"+str(healthLoss)+" HP</red>.","2. [Success?] Obtain a random Uncommon Colorless card. Lose <red>"+str(healthLoss)+" HP</red>.","3. [A Pick Me Up?] Obtain a <c>Potion</c>. Lose <red>"+str(healthLoss)+" HP</red>.","4. [How do I leave?] End the event. Lose <red>"+str(healthLoss)+" HP</red>."]
		for option in skullOptions:
			ansiprint(option)

		snap = input("What do you want to do?\n")

		while snap not in checkNumbers:
			active_character[0].explainer_function(snap,answer=False)
			snap = input("What do you want to do? Pick the corresponding number.\n")

		if snap == "1":
			ansiprint("\"YOU MORTALS NEVER CHANGE. IT IS DONE.\"\n<yellow>Gold</yellow> rains down on you.")
			active_character[0].set_gold(90)
			active_character[0].set_health(-healthLoss)
		
		elif snap == "2":
			ansiprint("\"PERHAPS THIS WILL HELP?\"You obtain a card.")
			random_cards = {k:v for k,v in cards.items() if v.get("Rarity") == "Uncommon" and v.get("Owner") == "Colorless" and v.get("Upgraded") != True}
			card_add = rd.choices(list(random_cards.items()))[0][1]
			active_character[0].add_CardToDeck(card_add)
			active_character[0].set_health(-healthLoss)

		elif snap == "3":
			ansiprint("\"DRINK UP!\"\nYou obtain a <c>Potion</c>.")
			random_potions = {k:v for k,v in potions.items() if v.get("Owner") == active_character[0].name or v.get("Owner") == "The Spire"}
			onePotion = rd.choices(list(random_potions.items()),k=1)
			active_character[0].add_Potion(onePotion[0][1])

			active_character[0].set_health(-healthLoss)		

		elif snap == "4":
			ansiprint("\"BEHIND YOU, MORTAL.\"\nYou peek behind the skull. Surely enough, there is a door.")
			active_character[0].set_health(-healthLoss)
			break

		healthLoss += 1				

def event_theLibrary():
	ansiprint("You come across an ornate building which appears abandoned.\nA plaque that has been torn free from a wall is on the floor. It reads, <light-blue>\"THE LIBRARY\"</light-blue>.\nInside, you find countless rows of scrolls, manuscripts, and books.\nYou pick one and cozy yourself into a chair for some quiet time.\n")
	healthGain = math.floor(active_character[0].max_health / 5)
	libraryOptions = ["1. [Read] Choose 1 of 20 cards to add to your deck.","2. [Sleep] Heal <red>"+str(healthGain)+" HP</red>."]
	libraryCards = []
	checkNumbers = ["1","2"]
	
	for option in libraryOptions:
		ansiprint(option)

	snap = input("What do you want to do?\n")

	while snap not in checkNumbers:
		active_character[0].explainer_function(snap,answer=False)
		snap = input("What do you want to do? Pick the corresponding number.\n")

	if snap == "1":
		i = 0
		while i < 20:
			repeat = False
			commonCardChance = helping_functions.commonCardChance * 100
			uncommonCardChance = helping_functions.uncommonCardChance * 100
			rareCardChance = helping_functions.rareCardChance * 100
			
			cardChance = rd.randint(1,100)

			if cardChance <= rareCardChance:
				random_cards = {k:v for k,v in cards.items() if v.get("Rarity") == "Rare" and v.get("Owner") == active_character[0].name and v.get("Upgraded") != True}
				card_add = rd.choices(list(random_cards.items()))[0][1]
			elif cardChance <= uncommonCardChance:
				random_cards = {k:v for k,v in cards.items() if v.get("Rarity") == "Uncommon" and v.get("Owner") == active_character[0].name and v.get("Upgraded") != True}
				card_add = rd.choices(list(random_cards.items()))[0][1]
			else: 
				random_cards = {k:v for k,v in cards.items() if v.get("Rarity") == "Common" and v.get("Owner") == active_character[0].name and v.get("Upgraded") != True}
				card_add = rd.choices(list(random_cards.items()))[0][1]
			
			if len(libraryCards) > 0:
				for card in libraryCards:
					if card.get("Name") == card_add.get("Name"):
						repeat = True
			if repeat == True:
				continue

			libraryCards.append(card_add)
			
			i+=1

		checkDeck = len(active_character[0].deck)
		helping_functions.pickCard(libraryCards)
		
		while checkDeck == len(active_character[0].deck):
			ansiprint("You can't skip a card in the Library.")	
			helping_functions.pickCard(libraryCards)

	elif snap == "2":
		ansiprint("Reading is for chumps.\nYou doze off in a comfy chair instead.\nZzz... zzz... ..Zz....\n<red>You wake up feeling refreshed.</red>")
		active_character[0].heal(healthGain)

def event_maskedBandits():
    ansiprint("You encounter a group of bandits wearing large <red>red masks</red>.\nRomeo: \"Hello, pay up to pass... a reasonable fee of <yellow>ALL your Gold</yellow> will do! Heh heh!\"")
    banditOptions = ["1. [Pay] Lose <yellow>"+str(active_character[0].gold)+" Gold</yellow>.","2. <red>[Fight!]</red> Enter combat against three bandits."]
    
    checkNumbers = ["1","2"]
    
    for option in banditOptions:
        ansiprint(option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        active_character[0].set_gold(-active_character[0].gold)
        ansiprint("Romeo: \"Hehehe.. Thanks for the <yellow>gold</yellow>!\"\nRomeo: \"Oh, I love <yellow>Gold</yellow>. It's so nice. shiny shiny chits they are!\"\nRomeo: \"Hey <red>Bear</red>, hey! This guy gave us all his <yellow>Gold</yellow>! What a sucker, right?\nRomeo: Get this, I just had to ask nicely. Who knew?! I certainly didn't! What a chump!\"\nRomeo: \"Gang, let's all have a laugh for this wondrous occasion! Hahaah Ho HOH hoho! Hoh!\"\nRomeo: \"Oh? You're still here? Did you overhear something? Didn't think so.\nRomeo: <red>*snerk*</red> ...loser.... Hahaha haaah\"")

    elif snap == "2":

        bandits = []
        enemy = "Pointy"
        bandits.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
        enemy = "Romeo"
        bandits.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))
        enemy = "Bear"
        bandits.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),on_hit_or_death = enemies[enemy].get("On_hit_or_death")))

        eventFight(bandits)
    
        goldReward = rd.randint(25,35)
        cardReward = helping_functions.generateCardRewards()
        relicReward = {"Name":"Red Mask","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"At the start of each combat, apply <light-cyan>1 Weakness</light-cyan> to ALL enemies."}
        
        helping_functions.afterEventBattleRewardScreen(gold = goldReward,cards = cardReward, relic = relicReward)

def event_theMausoleum():
    ansiprint("Venturing through a series of tombs, you are faced with a <yellow>large sarcophagus</yellow> studded with gems in the center of a circular room.You cannot make out the writing on the coffin, however, you do notice <black>black</black> <m>fog</m> seeping out from the sides.")

    mausoOptions = ["1. [Open Coffin] Obtain a <light-red>Relic</light-red>. Become <m>Cursed - Writhe</m>","2. [Leave] Nothing happens."]
    
    checkNumbers = ["1","2"]
    
    for option in mausoOptions:
        ansiprint(option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        ansiprint("You push open the coffin. As you do, <m>black fog</m> spews forth and covers the entire room! Inside, you find no body, only a <light-red>Relic</light-red>. You take it and move onwards, <m>coughing violently</m>.")
        active_character[0].add_CardToDeck({"Name": "Writhe","Innate": True,"Type": "Curse","Rarity": "Curse","Owner":"The Spire","Info":"<RED>Unplayable</RED>. <BLUE>Innate</BLUE>."})
        relic = helping_functions.generateRelicRewards()
        active_character[0].add_relic(relic[0])

    elif snap == "2":
        ansiprint("You leave without touching the grave not wanting to disturb the dead.")

def event_theNest():
    ansiprint("A long line of <light-blue>hooded figures</light-blue> can be seen entering an <m>unassuming cathedral</m>.\nNaturally, you join the line and are quickly surrounded by <red>Cultists</red>!\nThey ignore you as they gleefully chant and wave their weapons around.\nCultists: \"<red>MURDER!! MURDER MURDER!!</red>\"\nCultists: \"<light-blue>CAW CAW CAAAAAWWW!</light-blue>\"\nCultists: \"<red>MURDER! MURDER MUURDER!!</red>\"\nCultists: \"<light-blue>CAAW CAW CAAAAAAWW!!</light-blue>\"\nYou eye a <yellow>Donation Box</yellow>...")

    nestOptions = ["1. [Stay in Line] Obtain <red>Ritual Dagger</red>. Lose <red>6 HP</red>","2. [Smash and Grab] Obtain <yellow>50 Gold</yellow>."]
    
    checkNumbers = ["1","2"]
    
    for option in nestOptions:
        ansiprint(option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        ansiprint("You decide to stay in line <m>(out of fear)</m> to see what will happen.\nEventually, you are face-to-face with the leader.\nA well-dressed <red>Cultist</red> hands you an <yellow>Ornate Dagger</yellow>. Like the others before you, you slash your forearm and let the <red>blood drip into a misshapen bowl</red>.\nThe cultists chant and holler for you!\nCultists: \"<light-blue>CAAW CAW CAAAAAAWW</light-blue>!!\"You chant, too. Why not?")
        active_character[0].add_CardToDeck({"Name": "Ritual Dagger","Energy": 1,"Damage":15,"FatalBonus":3,"Exhaust":True,"Type": "Attack","Rarity": "Special","Owner":"Colorless","Info":"Deal <red>15 damage</red>. If this kills the enemy, permanently increase this Card's <red>damage</red> by 3. <BLUE>Exhaust</BLUE>. UPGRADING THIS CARD IS CURRENLY ILL-ADVISED AS IT'S BUGGED!"})
        active_character[0].set_health(-6)

    elif snap =="2":
        ansiprint("They didn't even notice.")
        active_character[0].set_gold(50)

def event_nLoth():
    ansiprint("An odd creature with a hunched back sprouting several tentacles is scrounging through a pile of trash and debris in front of you.\nAs you approach, he shuffles towards you in a non-threatening manner.\n\"N'loth hungry. Feed N'loth.\"")

    if len(active_character[0].relics) > 1:
        firstRelic = rd.randint(0,len(active_character[0].relics)-1)
        secondRelic = rd.randint(0,len(active_character[0].relics)-1)
        while secondRelic == firstRelic:
            secondRelic = rd.randint(0,len(active_character[0].relics)-1)

        nlothOptions = ["1. [Offer] Offer <light-red>"+ active_character[0].relics[firstRelic].get("Name")+"</light-red>. Receive <light-red>N'loth's Gift</light-red>","2. [Offer] Offer <light-red>"+ active_character[0].relics[secondRelic].get("Name")+"</light-red>. Receive <light-red>N'loth's Gift</light-red>","3. [Leave] Nothing happens."]
    
        checkNumbers = ["1","2","3"]
    

        for option in nlothOptions:
            ansiprint(option)

        snap = input("What do you want to do?\n")

        while snap not in checkNumbers:
            active_character[0].explainer_function(snap,answer=False)
            snap = input("What do you want to do? Pick the corresponding number.\n")

        if snap == "1":
            ansiprint("Holding the <light-red>"+ active_character[0].relics[firstRelic].get("Name")+"</light-red> out towards him, N’loth snatches it out of your hand with his tentacles, dislocates his jaw, and slurps down your offer in one quick gulp.\nHe gives you a large, toothy grin as more tentacles appear from behind his cloak, these ones brandishing an <light-red>impossibly neat looking box</light-red>. He pushes it towards you until you take it.")
            active_character[0].remove_Relic(active_character[0].relics[firstRelic].get("Name"))
            active_character[0].add_relic({"Name":"N'loth's Gift","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"Triples the chance of receiving rare Cards as monster rewards."})

        elif snap == "2":
            ansiprint("Holding the <light-red>"+ active_character[0].relics[secondRelic].get("Name")+"</light-red> out towards him, N’loth snatches it out of your hand with his tentacles, dislocates his jaw, and slurps down your offer in one quick gulp.\nHe gives you a large, toothy grin as more tentacles appear from behind his cloak, these ones brandishing an <light-red>impossibly neat looking box</light-red>. He pushes it towards you until you take it.")
            active_character[0].remove_Relic(active_character[0].relics[secondRelic].get("Name"))
            active_character[0].add_relic({"Name":"N'loth's Gift","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"Triples the chance of receiving rare Cards as monster rewards."})

        elif snap == "3":
            ansiprint("You shake your head. N'loth hunches even further and sighs, then scuttles away.")


    elif len(active_character[0].relics) == 1:
        nlothOptions = ["1. [Offer] Offer <light-red>"+ active_character[0].relics[0].get("Name")+"</light-red>. Receive <light-red>N'loth's Gift</light-red>","2. [Leave] Nothing happens."]
    
        checkNumbers = ["1","2"]

        for option in nlothOptions:
            ansiprint(option)

        snap = input("What do you want to do?\n")

        while snap not in checkNumbers:
            active_character[0].explainer_function(snap,answer=False)
            snap = input("What do you want to do? Pick the corresponding number.\n")

        if snap == "1":
            ansiprint("Holding the <light-red>"+ active_character[0].relics[0].get("Name")+"</light-red> out towards him, N’loth snatches it out of your hand with his tentacles, dislocates his jaw, and slurps down your offer in one quick gulp.\nHe gives you a large, toothy grin as more tentacles appear from behind his cloak, these ones brandishing an <light-red>impossibly neat looking box</light-red>. He pushes it towards you until you take it.")
            active_character[0].remove_Relic(active_character[0].relics[0].get("Name"))
            active_character[0].add_relic({"Name":"N'loth's Gift","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"Triples the chance of receiving rare Cards as monster rewards."})

        elif snap == "2":
            ansiprint("You shake your head. N'loth hunches even further and sighs, then scuttles away.")


    else:
        ansiprint("How do you get here and have 0 Relics? N'loth pities you and gives you several relics.")

def event_oldBeggar():
    ansiprint("An old beggar cloaked in fur reaches his hands out towards you as you pass. \"Spare some <yellow>coin</yellow>, child?\"")

    oldOptions = ["1. [Offer Gold] Lose <yellow>75 Gold</yellow>. Remove a card from your deck.","2. [Leave] Nothing happens."]
    
    checkNumbers = ["1","2"]
    
    while True:
        for option in oldOptions:
            ansiprint(option)

        snap = input("What do you want to do?\n")

        while snap not in checkNumbers:
            active_character[0].explainer_function(snap,answer=False)
            snap = input("What do you want to do? Pick the corresponding number.\n")

        if snap == "1":
            if active_character[0].gold < 75:
                ansiprint("You don't have enough <yellow>Gold</yellow> to donate.")
                continue
            active_character[0].set_gold(-75)
            ansiprint("The beggar takes off its cloak to reveal that he is <light-blue>Cleric</light-blue>!\nCleric: \"You are a kind soul. RECEIVE MY PURIFICATION!\" he screams. You are unsure if he is grateful or mad.")
            active_character[0].removeCardsFromDeck(1,removeType="Remove")
            ansiprint("Cleric: \"I hope you do better this time, friend!\" he shouts. Wondering what was implied by this, you push forward.")
            break
        
        elif snap == "2":
            ansiprint("The beggar looks to the floor as you pass.\n\"You will never make a difference... You never do.\"")
            break

def event_pleadingVagrant():
    ansiprint("While sneaking past a group of shrouded figures, one of them approaches you.\n\"Got anything for me friend? Please... maybe some <yellow>Coin</yellow>?\"\n\"I just need somewhere to stay, I have <light-red>treasures</light-red> I can trade...\"\nHe seems delusional, but harmless.")

    vagrantOptions = ["1. [Give 85 Gold] Lose <yellow>85 Gold</yellow>. Obtain a random <light-red>Relic</light-red>.","2. [Rob] Obtain a random <light-red>Relic</light-red>. Become <m>Cursed - Shame</m>.","3. [Leave] Nothing happens."]

    checkNumbers = ["1","2","3"]
    relic = helping_functions.generateRelicRewards()
    while True:
        for option in vagrantOptions:
            ansiprint(option)

        snap = input("What do you want to do?\n")

        while snap not in checkNumbers:
            active_character[0].explainer_function(snap,answer=False)
            snap = input("What do you want to do? Pick the corresponding number.\n")

        if snap == "1":
            if active_character[0].gold < 85:
                ansiprint("The Vagrant needs more Gold for his <light-red>Treasure</light-red>")
                continue
            active_character[0].set_gold(-85)
            ansiprint("Oh yes, yes! Here here, a fair trade!")
            
            active_character[0].add_relic(relic[0])
            break
        
        elif snap == "2":
            active_character[0].add_relic(relic[0])
            ansiprint("You snatch the precious <light-red>Relic</light-red> from his clutches and walk away.\nFrom behind you hear,\"Have you no shame? <m>HAVE YOU NO SHAAAAAME</m>?!\"\nYou actually do.")
            active_character[0].add_CardToDeck({"Name": "Shame","Type": "Curse","Rarity": "Curse","Owner":"The Spire","Info":"<RED>Unplayable</RED>. At the end of your turn, gain <light-cyan>1 Frail</light-cyan>."})
            break

        elif snap == "3":
            ansiprint("You have nothing to give to this shrouded figures. You try to avoid eye contact as you walk past him.")

def event_Vampires():
    bloodVial = False
    for relic in active_character[0].relics:
        if relic.get("Name") == "Blood Vial":
            bloodVial = True

    ansiprint("Navigating an unlit street, you come across several hooded figures in the midst of some <black>dark ritual</black>.\nAs you approach, they turn to you in eerie unison. The tallest among them bares fanged teeth and extends a long, pale hand towards you.")
    if active_character[0].name == "Silent" or active_character[0].name == "Watcher":
        ansiprint("Fanged Stranger: \"Join us sister, and feel the warmth of the Spire.\"")

    healthLoss = math.floor(active_character[0].max_health / 100 * 30) 
    vampireOptions = ["1. [Accept] Remove all <red>Strikes</red>. Receive <red>5 Bites</red>. Lose <red>"+ str(healthLoss)+" Max HP</red>.","2. [Refuse] Nothing happens."]
    checkNumbers = ["1","2"]

    if bloodVial:
        checkNumbers.append("3")
        vampireOptions.append("3. [Offer] <light-red>Blood Vial</light-red>. Remove all <red>Strikes</red>. Receive <red>5 Bites</red>.")
    
    for option in vampireOptions:
        ansiprint (option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        ansiprint("The tall figure grabs your arm, pulls you forward, and sinks his fangs into your neck.\nYou feel a <black>dark force</black> pour into your neck and course through your body.\n...\nYou wake up some time later, alone. An intense hunger passes through your belly. <red>You must feed</red>.\n")
        active_character[0].set_health(-healthLoss)

        i = 0
        while i < 5:
            active_character[0].add_CardToDeck({"Name": "Bite", "Damage":7,"Heal":2, "Energy": 1,"Type": "Attack" ,"Rarity": "Special","Owner":"Colorless","Info":"Deal <red>6 damage</red>."})
            i+=1
        
        i = 0
        
        while i < len(active_character[0].deck):
            if active_character[0].deck[i].get("Name") == "Strike":
                active_character[0].deck.pop(i)
            elif active_character[0].deck[i].get("Name") == "Strike +":
                active_character[0].deck.pop(i)
            else:
                i+=1
        
    elif snap =="2":
        ansiprint("You step back and raise your weapon in defiance. The tall figure sighs.˜Fanged Stranger: \"Very well.\"\nThe entire group of hooded figures morph into a thick black fog that flows away from you.\nYou are alone once more.")
        
    elif snap == "3":
        ansiprint("The pale figures gasp as you take out the <light-red>Blood Vial</light-red>.\nPale Figures: \"The master's blood... the master's blood! <red>THE MASTER'S BLOOD</red>!\"They all chant fervently as the tall one bows before you.\nFanged Stranger: \"Drink from His blood, and become one with <red>Him</red>.\"\nThe chant growing louder, you consume the contents of the vial. Your vision immediately warps and fades to <black>darkness</black>.\nYou wake up some time later, alone. An intense hunger passes through your belly. <red>You must feed<red>.\n")
        i = 0
        while i < 5:
            active_character[0].add_CardToDeck({"Name": "Bite", "Damage":7,"Heal":2, "Energy": 1,"Type": "Attack" ,"Rarity": "Special","Owner":"Colorless","Info":"Deal <red>6 damage</red>."})
            i+=1
        
        i = 0
        while i < len(active_character[0].deck):
            if active_character[0].deck[i].get("Name") == "Strike":
                active_character[0].deck.pop(i)
            elif active_character[0].deck[i].get("Name") == "Strike +":
                active_character[0].deck.pop(i)
            else:
                i+=1

def event_Falling():
    ansiprint("As you head upwards hopping from one floating shape to another, you slip.\nYou begin to fall.\nWhile in free fall you consider your options:\nLand safely with your <green>greatest techniques</green>.\n<blue>Channel a Power</blue> to survive the fall.\n<red>Strike at the wall</red> to hang on to it.\n")
    attack = False
    skill = False
    power = False
    checkNumbers = []
    for card in active_character[0].deck:
        if card.get("Type") == "Attack":
            attack = True
        elif card.get("Type") == "Skill":
            skill = True
        elif card.get("Type") == "Power":
            power = True

    fallingOptions = []
    i = 0 
    if attack:
        attackIndex = helping_functions.getRandomSpecifiedCardIndex(specifics="Attack")
        fallingOptions.append(str(i+1)+". [Strike] Lose <red>"+ active_character[0].deck[attackIndex].get("Name")+"</red>.",)
        i+=1

    if skill:
        skillIndex = helping_functions.getRandomSpecifiedCardIndex(specifics="Skill")
        fallingOptions.append(str(i+1)+". [Land] Lose <green>"+ active_character[0].deck[skillIndex].get("Name")+"</green>.",)
        i+=1

    if power:
        powerIndex = helping_functions.getRandomSpecifiedCardIndex(specifics="Power")
        fallingOptions.append(str(i+1)+". [Channel] Lose <blue>"+ active_character[0].deck[powerIndex].get("Name")+"</blue>.",)
        i+=1

    if len(fallingOptions) > 0:
        i = 0
        for _ in fallingOptions:
            checkNumbers.append(str(i+1))
            i+=1

        for option in fallingOptions:
            ansiprint(option)

        snap = input("What do you want to do?\n")

        while snap not in checkNumbers:
            active_character[0].explainer_function(snap,answer=False)
            snap = input("What do you want to do? Pick the corresponding number.\n")

        
        if "[Strike]" in fallingOptions[int(snap)-1]:
            active_character[0].removeCardsFromDeck(amount=1,removeType = "Remove",index = attackIndex)
            ansiprint("You are able to latch on to the wall, and manage to make a short hop onto another stable platform.")

        elif "[Land]" in  fallingOptions[int(snap)-1]:        
            active_character[0].removeCardsFromDeck(amount=1,removeType = "Remove",index = skillIndex)
            ansiprint("You land with extreme grace before continuing on.")
        
        elif "[Channel]" in  fallingOptions[int(snap)-1]:
            ansiprint("Harnessing and expending some of your raw power, you manage to land unhurt.")
            active_character[0].removeCardsFromDeck(amount=1,removeType = "Remove",index = powerIndex)
        
    else:     
        ansiprint("You land like a feather. You are grace. Suddenly you hear clapping behind you. A hooded figure approaches with a skulled head.\n\"That was grandios. You.. remind of someone...\"\nShe hands you something and walks away.")
        active_character[0].add_CardToDeck({"Name": "Grand Finale +","Damage":60,"Energy": 1, "Type": "Attack" ,"Upgraded": True,"Rarity": "Rare","Owner":"Silent","Info":"Can only be played if there are no cards in your Drawpile. Deal <red>60 damage</red> to ALL enemies."})

def event_MindBloom():
    ansiprint("While walking and traversing through the chaos of the Spire, your thoughts suddenly begin to feel very... real...Imaginings of <red>monsters</red> and <yellow>riches</yellow> begin to manifest themselves into reality.\nThe sensation is quickly fleeting. What do you do?")
    rich = None
    bloomOptions = ["1. [I am War] <red>Fight a Boss from Act 1</red>. Obtain a rare <light-red>Relic</light-red>","2. [I am Awake] <green>Upgrade all Cards</green>. <red>You can no longer heal</red>."]
    if active_character[0].get_position()[0] < 5:
        rich = True
        bloomOptions.append("3. [I am Rich] Gain <yellow>999 gold</yellow>. Become <m>Cursed - 2 Normalities</m>.")
    else:
        rich = False
        bloomOptions.append("3. [I am Healthy] Heal to full Hp. Become <m>Cursed - Doubt</m>.")

    checkNumbers = ["1","2","3"]
    
    for option in bloomOptions:
        ansiprint(option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        act1Boss = fill_boss_list(1)[0]
        eventFight(act1Boss)
        relicReward = helping_functions.generateRelicRewards(specificType="Rare")[0]
        goldReward = 25
        helping_functions.afterEventBattleRewardScreen(gold = goldReward, relic = relicReward)

    elif snap == "2":
        ansiprint("Everything makes sense now.\nThe lack of memories, the ascent, the Ancient One.\nThis is the way it always was.\nThis is the way it always will be.\nAll will be forgotten again soon...")
        i = 0
        while i < len(active_character[0].deck):
            if active_character[0].deck[i].get("Type") != "Status" and active_character[0].deck[i].get("Type") != "Curse" and active_character[0].deck[i].get("Upgrade") == None:
                helping_functions.upgradeCard(active_character[0].deck.pop(i),"Deck",index=i)   
            i+=1
        
        active_character[0].add_relic({"Name":"Mark of the Bloom","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"You can no longer <red>heal</red>."})

    elif snap == "3" and rich == True:
        
        active_character[0].set_gold(999)
        ansiprint("\nCan it really be this easy?\n")
        active_character[0].add_CardToDeck({"Name": "Normality","Type": "Curse","Rarity": "Curse","Owner":"The Spire","Info":"<RED>Unplayable</RED>. You cannot play more than 3 Cards this turn."})
        active_character[0].add_CardToDeck({"Name": "Normality","Type": "Curse","Rarity": "Curse","Owner":"The Spire","Info":"<RED>Unplayable</RED>. You cannot play more than 3 Cards this turn."})
        
    elif snap == "3" and rich == False:
        active_character[0].heal(active_character[0].max_health)
        ansiprint("\nCan it really be this easy?\n")
        active_character[0].add_CardToDeck({"Name": "Doubt","Type": "Curse","Rarity": "Curse","Owner":"The Spire","Info":"<RED>Unplayable</RED>. At the end of your turn, gain <light-cyan>1 Weak</light-cyan>."})

def event_secretPortal():
    ansiprint("Before you is a sight that seems out of place in the alien landscape around you.\nStrangely placed into one of the living walls of the Beyond is an enclosed stone entrance filled with a <c>swirling magical portal</c>.\nYou aren't sure where it leads, but maybe it could speed your journey through the Spire.'")

    portalOptions = ["1. [Enter the Portal] Immediately travel to the boss.","[Leave] Nothing happens."]
    
    checkNumbers = ["1","2"]
    
    for option in portalOptions:
        ansiprint(option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        helping_functions.game_map[13][0] = "Portal"
        helping_functions.game_map_dict[("Portal",13,0)] = helping_functions.game_map_dict[("Fires",13,0)]
        active_character[0].set_position([13,0])
        ansiprint("Jumping through the portal, your sense of time and space is completely torn apart.\nAs you reorient yourself to the new surroundings, you realize that right before you is a fearsome battle.")

    elif snap == "2":
        ansiprint("Careful and cautious seems the better approach for reaching the top of the Spire. Ignoring the portal you continue on.")

def event_sensoryStone():
    ansiprint("Navigating through the Beyond, you discover a <light-blue>glowing tesseract</light-blue> spinning and shifting gently in the air.\nYou touch it.\nA <red>sharp pain</red> flows through you, followed by vivid flashes of a distant memory.\n...whose memories are these?\n")

    sensoryOptions = ["1. [Recall] Add 1 Colorless Card to your deck.","2. [Recall] Add 2 Colorless Cards to your deck, take <red>5 Damage</red>.","3. [Recall] Add 3 Colorless Cards to your deck, take <red>10 damage</red>."]
    
    checkNumbers = ["1","2","3"]
    
    for option in sensoryOptions:
        ansiprint(option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        
        colorlessCards = helping_functions.generateCardRewards(colorless=True)
        helping_functions.pickCard(colorlessCards)

    elif snap == "2":
       # cardOptions = ["Card Reward 1","Card Reward 2"]
        colorlessCards1 = helping_functions.generateCardRewards(colorless=True)
        colorlessCards2 = helping_functions.generateCardRewards(colorless=True)
        multipleRewards = [colorlessCards1,colorlessCards2]
        helping_functions.afterEventBattleRewardScreen(multipleCardRewards=multipleRewards)

    elif snap == "3":
        colorlessCards1 = helping_functions.generateCardRewards(colorless=True)
        colorlessCards2 = helping_functions.generateCardRewards(colorless=True)
        colorlessCards3 = helping_functions.generateCardRewards(colorless=True)

        multipleRewards = [colorlessCards1,colorlessCards2,colorlessCards3]

        helping_functions.afterEventBattleRewardScreen(multipleCardRewards=multipleRewards)

    memory = rd.randint(0,3)

    if memory == 0:
        ansiprint("<red>FEAR</red>.\nA demonic creature towers above you, wings spread wide as it howls with laughter. Dead bodies of a tribe surround you while the village is engulfed in terrible <m>dark flames</m>.\nThe demon calls out, taunting you.\n<red>\"YOU REALLY ARE THE STRONGEST NOW! Haha.. HEHE... HAHAHAAAAH!!\"</red>\nThis laughter echoes forever...")
    elif memory == 1:
        ansiprint("<green>TRIUMPH</green>.\nThe remains of a <m>ghostly creature</m> sink slowly into the mud before you, barely visible in the moonlight. You have proven yourself amongst your sisters.\nStanding victoriously, you wait in silence as the others ceremoniously place the <yellow>creature's</yellow> skull atop your head. The ritual has concluded.\nYou head towards the Spire...")
    elif memory == 2:
        ansiprint("<light-blue>CONFUSION</light-blue>.\n<yellow>[OBJECTIVE]</yellow> <green>BALANCE must be ENFORCED</green>\n<yellow>[DEFINE]</yellow> <green>BALANCE</green>\n<yellow>[ERROR]</yellow> <green>BALANCE NOT FOUND</green>\n<yellow>[DEFINE]</yellow> <green>BALANCE</green>\n<yellow>[ERROR]</yellow> <green>BALANCE NOT FOUND</green>\n<yellow>[WARNING]</yellow> <green>Large object approaching</green>\n\"I... ..am ....Neow..\"")
    elif memory == 3:
        ansiprint("<c>SERENITY</c>.\nTwo primitive creatures fight over a carcass on the side of the road. You observe, devoid of emotion.\n<yellow>Watch. Remember. Live.</yellow> This is the Watcher's mission.\nRecently, one of your peers had stopped reporting on their assignment: a Spire of unknown origin.\nAs the fight ends, you continue onward, unfazed by the bloody scene that took place.")

def event_mysteriousSphere():
    ansiprint("Jutting from the chaotic terrain around you, a bony sphere surrounds a mysterious glowing object within.\nWhile you are curious what lies inside, you notice some sentries keeping an eye on it.\n")

    sphereOptions = ["1. <red>[Open Sphere]</red> Fight two dangerous enemies!","2. [Leave] Nothing happens."]
    
    checkNumbers = ["1","2"]
    
    for option in sphereOptions:
        ansiprint(option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        ansiprint("As soon as you strike the sphere, the sentries spring to life around you!")
        orbList = []
        enemy = "Orb Walker"
        orbList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),ritual = enemies[enemy].get("Ritual")))
        orbList.append(Enemy(name = enemies[enemy].get("Name"),max_health = rd.randint(enemies[enemy].get("Health")[0],enemies[enemy].get("Health")[1]),intentions = enemies[enemy].get("Intentions"),intention_logic = enemies[enemy].get("Intentions_Logic"),ritual = enemies[enemy].get("Ritual")))
        eventFight(orbList)
        cardReward = helping_functions.generateCardRewards()
        goldReward = rd.randint(45,55)
        potionReward = helping_functions.generatePotionRewards()
        randomRareRelic = helping_functions.generateRelicRewards(specificType="Rare")[0]
        helping_functions.afterEventBattleRewardScreen(gold=goldReward,potion = potionReward,cards= cardReward,relic=randomRareRelic)

    elif snap == "2":
        ansiprint("No need to be greedy.")

def event_theMoaiHead():
    goldenIdol = False
    for relic in active_character[0].relics:
        if relic.get("Name") == "Golden Idol":
            goldenIdol = True

    maxHPLoss = math.floor(active_character[0].max_health / 100 * 18)

    ansiprint("You stumble across something that feels *very* out of place.\nBefore you, an enormous stony head emerges from a large wall segment that does not shift and change like the rest of this area.\nThe head's mouth is wide open, and it reveals large intimidating teeth stained red with blood.\nThe surface of the statue is riddled with pictographs that seem to indicate people throwing themselves into the mouth of this head and being devoured. Why would anyone do that?\n")
    checkNumbers = ["1","2"]
    moaiOptions = ["1. [Jump Inside] <red>Heal to full HP</red>. Decrease your <red>Max HP</red> by <red>"+str(maxHPLoss)+"</red>.","2. [Leave] Nothing happens."]
    
    if goldenIdol:
        moaiOptions.append("3. [Offer <light-red>Golden Idol</light-red>] Gain <yellow>333 Gold</yellow>. Lose <light-red>Golden Idol</light-red>.")
        checkNumbers.append("3")

    for option in moaiOptions:
        ansiprint(option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        ansiprint("At first when you step up into the mouth of the statue, nothing happens.\nAs you start to feel more than a little foolish, the huge molars slam down from above, crushing you whole.\n<black>Darkness</black>.\nSometime later from within the dark, you see a sliver of light, and hear what you now realize is the sound of stony teeth slowly rising upwards.\nYou leave confused.")
        active_character[0].set_maxHealth(-maxHPLoss)
        active_character[0].heal(active_character[0].max_health)

    elif snap == "2":
        ansiprint("Yeah. You're not going to walk into a gaping mouth.")

    elif snap == "3":
        
        ansiprint("You jump back a little as the gigantic molars smash down on the <light-red>idol</light-red>, smashing it into dust. As the teeth start to rise up again, <yellow>gold</yellow> pours forth in a torrent from the opening, flooding you with riches.")
        active_character[0].remove_Relic("Golden Idol")
        active_character[0].set_gold(333)
        
def event_tombOfLordRedMask():
    ansiprint("A highly ornamented tomb can be seen on the other side of a floating path.\nUpon reaching the tomb, you notice a slot for <yellow>Gold</yellow> with a scratched out inscription above it.")
    redMask = False
    for relic in active_character[0].relics:
        if relic.get("Name") == "Red Mask":
            redMask = True

    if redMask:
        lordOptions = ["1. [Wear the <light-red>Red Mask</light-red>]</red> Gain <yellow>222 Gold</yellow>.","2. [Leave] Nothing happens."]
    
    else:
        lordOptions = ["1. [Offer <yellow>"+str(active_character[0].gold)+" Gold</yellow>] Lose all <yellow>Gold</yellow>. Obtain a <light-red>Red Mask<light-red>.","2. [Leave] Nothing happens."]

    checkNumbers = ["1","2"]
    
    for option in lordOptions:
        ansiprint(option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1" and redMask == True:
        ansiprint("You don the <light-red>Red Mask</light-red> and the tomb starts to flake away... a secret passage!\nThe passage is lined with countless stolen goods and mounds of <yellow>Gold</yellow>!")
        active_character[0].set_gold(222)

    elif snap == "1":
        ansiprint("After you've put every last of your coins into the slot, an opening appears in the tomb and out slides a small <light-red>Red Mask</light-red> with a note attached.\nNote: \"Take from others as I have taken from you!\"")
        active_character[0].set_gold(-active_character[0].gold)
        active_character[0].add_relic({"Name":"Red Mask","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"At the start of each combat, apply <light-cyan>1 Weakness</light-cyan> to ALL enemies."})

    elif snap == "2":
        ansiprint("You leave and don't look back.")

def event_windingHalls():
    ansiprint("As you slowly make your way up the twisting pathways, you constantly find yourself losing your way as the walls and ground seem to inexplicably shift before your eyes.\nThe constant <m>whispering voices</m> in the back of your head aren't helping things either.\nPassing by a structure you are certain you have previously seen you start to question if you are going insane, or if the impossible geography of this place is starting to get to you.\nYou need to change something, and soon.\nThat's what the <m>voices</m> say anyway, and why would they lie?")
    maxHPLoss1 = math.floor(active_character[0].max_health / 100 * 18)
    maxHPLoss2 = math.floor(active_character[0].max_health / 100 * 5)
    healAmount = math.floor(active_character[0].max_health / 5)
    windingOptions = ["1. [Embrace Madness] Receive 2 Madness. Lose <red>"+str(maxHPLoss1)+ " HP</red>.","2. [Press On] Become <m>Cursed - Writhe</m>. <red>Heal "+str(healAmount)+"</red>.","3. [Retrace Your Steps] Lose <red>"+str(maxHPLoss2)+" HP</red>."]
    
    checkNumbers = ["1","2","3"]
    
    for option in windingOptions:
        ansiprint(option)

    snap = input("What do you want to do?\n")

    while snap not in checkNumbers:
        active_character[0].explainer_function(snap,answer=False)
        snap = input("What do you want to do? Pick the corresponding number.\n")

    if snap == "1":
        ansiprint("Something in you cracks.\nOnly the truly mad can understand a place like this, so you give into the chattering voices and continue on with a <m>\"new\"</m> perspective.\nThings do seem to make so much more sense now.")
        active_character[0].add_CardToDeck({"Name": "Madness","Energy": 1,"Exhaust":True,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Colorless","Info":"Reduce the cost of a random card in your hand to <yellow>0 Energy</yellow> this combat. <BLUE>Exhaust<BLUE>."})
        active_character[0].add_CardToDeck({"Name": "Madness","Energy": 1,"Exhaust":True,"Type": "Skill" ,"Rarity": "Uncommon","Owner":"Colorless","Info":"Reduce the cost of a random card in your hand to <yellow>0 Energy</yellow> this combat. <BLUE>Exhaust<BLUE>."})
        active_character[0].set_health(-maxHPLoss1)

    elif snap == "2":
        ansiprint("As you take a moment to stop and carefully observe the undulating landscape around you, the hint of a pattern starts to emerge from within the randomness.\nWhenever the demented noises begin to interrupt your thoughts, you struggle through the mental pain and ignore it.\nEventually you successfully map out a path forward, and continue on, now resistant to the nefarious nature of this alien place.")
        active_character[0].heal(healAmount)
        active_character[0].add_CardToDeck({"Name": "Writhe","Innate": True,"Type": "Curse","Rarity": "Curse","Owner":"The Spire","Info":"<RED>Unplayable</RED>. <BLUE>Innate</BLUE>."},)

    elif snap == "3":
        ansiprint("You spend what seems like an eternity lost in the maze.\nSlowly but surely, you are able to retrace your steps, reorient yourself, and make it out of the twisting passages.\nYou feel <red>drained</red> from the experience.")
        active_character[0].set_health(-maxHPLoss2)


def eventFight(listOfMonsters):

    active_character[0].resetChar()
    active_character[0].set_drawPile()
    helping_functions.turn_counter = 0

    for monster in listOfMonsters:
        list_of_enemies.append(monster)

    while len(list_of_enemies) > 0 and active_character[0].alive == True:
        helping_functions.turn_counter = helping_functions.count_up(helping_functions.turn_counter)
        active_character[0].turn(helping_functions.turn_counter)
                
        for enemy in list_of_enemies:
            enemy.turn(helping_functions.turn_counter)
    
    if active_character[0].faceOfCleric > 0:
            active_character[0].set_maxHealth(1)


actOneEvents = [event_bigFish,event_DeadAdventurer,event_GoldenIdol,event_HypnotizingColoredMushrooms,event_LivingWall,event_ScrapOoze,event_shiningLight,
    event_theSerpent,event_poolOfGoop,event_wingStatue]

universalEvents = [event_PurpleFireSpirits,event_theDivineFountain,event_TheDuplicator,event_ThePurifier,event_TheTransmogrifier,event_upgradeShrine,event_GoldenShrine,
    event_AncientLaboratory,event_MatchAndKeep,event_OminousForge,event_weMeetAgain,event_wheelOfChange,event_theWomanInBlue,
    event_faceTrade]

actTwoEvents = [event_Vampires,event_pleadingVagrant,event_maskedBandits,event_theMausoleum,event_theNest,
    event_oldBeggar,event_nLoth,event_theLibrary,event_knowingSkull,event_theJoust,event_theForgottenAltar,
    event_cursedBook,event_CouncilOfGhosts,event_theColosseum,event_Augmenter,event_ancientWriting]

actThreeEvents = [event_Falling,event_MindBloom,event_secretPortal,event_sensoryStone,event_mysteriousSphere,event_theMoaiHead,event_windingHalls,event_tombOfLordRedMask]



def visit_event():
    #this still needs handling for events that have a condition such as the remove all curses event.
    global eventMonsterChance
    global eventTreasureChance
    global eventShopChance
    global actOneEvents
    global actTwoEvents
    global universalEvents

    for relic in active_character[0].relics:
    	if relic.get("Name") == "Juzu Bracelet":
    		eventMonsterChance = 0
    	elif relic.get("Name") == "Tiny Chest":
    		relic["Counter"] += 1
    		if relic["Counter"] % 4 == 0:
    			eventMonsterChance = 0
    			eventTreasureChance = 1
    			eventShopChance = 0
    	elif relic.get("Name") == "Ssserpent Head":
    		active_character[0].set_gold(50)
    		ansiprint("You received <yellow>50 Gold</yellow> because of <light-blue>Ssserpent Head</light-blue>.")

    eventChance = 1 - eventMonsterChance - eventTreasureChance - eventShopChance

    unknownLocation = list(helping_functions.nchoices_with_restrictions([eventChance,eventMonsterChance,eventTreasureChance,eventShopChance],k = 1))

    if unknownLocation[0] == 0:

    	if rd.randint(0,1) == 0:
    		if helping_functions.gameAct == 1:
    			rd.shuffle(actOneEvents)
    			actOneEvents.pop(0)()
    		elif helping_functions.gameAct == 2:
    			rd.shuffle(actTwoEvents)
    			actTwoEvents.pop(0)()
    		elif helping_functions.gameAct == 3:
    			rd.shuffle(actThreeEvents)
    			actThreeEvents.pop(0)()

    	else:
    		
    		if len(universalEvents) > 0:
    			rd.shuffle(universalEvents)
    			universalEvents.pop(0)()
    		else:
    			if helping_functions.gameAct == 1:
    				rd.shuffle(actOneEvents)
    				actOneEvents.pop(0)()
    			elif helping_functions.gameAct == 2:
    				rd.shuffle(actTwoEvents)
    				actTwoEvents.pop(0)()
    			elif helping_functions.gameAct == 3:
    				rd.shuffle(actThreeEvents)
    				actThreeEvents.pop(0)()

    	eventMonsterChance += 0.1
    	eventTreasureChance += 0.02
    	eventShopChance += 0.03

    elif unknownLocation[0] == 1:
    	
    	list_of_enemies.extend(enemyEncounters.pop(0))
    	helping_functions.encounter_counter += 1

    	eventMonsterChance = 0.1
    	eventTreasureChance += 0.02
    	eventShopChance += 0.03

    	floor = active_character[0].get_floor()
    	y = active_character[0].position[0]
    	x = active_character[0].position[1]
    	helping_functions.game_map[y][x] = "Creep"        
    	helping_functions.game_map_dict[("Creep",y,x)] = helping_functions.game_map_dict[(floor,y,x)]


    elif unknownLocation[0] == 2:

    	visit_treasureChest()
    	eventMonsterChance += 0.1
    	eventTreasureChance = 0.02
    	eventShopChance += 0.03

    elif unknownLocation[0] == 3:
    	
    	ansiprint("\nThere was a <yellow>Merchant</yellow> hiding here!\n")
    	shop = helping_functions.generateShop()
    	helping_functions.displayShop(shop)

    	eventMonsterChance += 0.1
    	eventTreasureChance += 0.02
    	eventShopChance = 0.03

    else:
    	print(unknownLocation[0],"This should be either one 2 or three.")    






# 1 = normal_fight
# 2 = elite_fight
# 3 = question_mark
# 4 = bon_fire
# 5 = merchant
# 6 = treasure_room 
# 7 = boss_fight
# 8 = start


