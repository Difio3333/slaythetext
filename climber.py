import entities
import random as rd
import time
import math
import acts
import copy
import helping_functions
import save_handlery
from ansimarkup import parse, ansiprint
import spelling_correction
from pathlib import Path
import copy

class Char():
	def __init__(self, name: str, max_health: int, energy: int = 0, energy_gain: int = 3,
		
		deck: list = [], hand: list = [], discard_pile: list = [], exhaust_pile: list = [], 

		draw_strength: int = 5, block: int = 0, gold: int = 0,

		relics: list = [], position: list = [0,0],

		alive: bool = True

		):
		
		self.name = name
		self.displayName = "<green>" + self.name + "</green>"
		self.max_health = max_health
		self.health = self.max_health - math.floor(self.max_health / 10)
		self.energy = energy
		self.energy_gain = energy_gain

		self.deck = deck
		self.draw_pile = []
		self.draw_strength = draw_strength
		self.hand = hand
		self.discard_pile = discard_pile
		self.exhaust_pile = exhaust_pile
		self.power_pile = []
		
		self.block = block
				
		self.relics = relics
		self.gold = gold
		
		self.potionBag = []
		self.potionBagSize = 3
		#negative statuses
		self.weak = 0
		self.frail = 0
		self.vulnerable = 0
		self.entangled = 0

		#positiv statuses
		
		self.smokeBomb = False
		self.position = position
		self.alive = alive
		
		#inFigtThings
		self.target = 0
		self.temp_energy = 0
		self.tempDraw = 0
		self.blockNextTurn = 0
		self.dontLoseBlock = 0

		self.strength = 0
		self.dexterity = 0

		self.ritual = 0

		self.invulnerable = 0
		
		self.discard_counter = 0
		self.exhaust_counter = 0

		self.cardsNextTurn = []
		self.doubleDamage = []
		self.theBomb = []

		self.cantDraw = 0
		self.cardsCostNothing = 0
		self.tempSpikes = 0

		self.intangible = 0
		self.constriction = 0
		#powers
		self.accuracy = 0
		self.spikes = 0
		self.infiniteBlades = 0
		self.noxiousFumes = 0
		self.wellLaidPlans = 0
		self.thousandCuts = 0
		self.afterImage = 0
		self.envenom = 0
		self.toolsOfTheTrade = 0
		self.metallicize = 0
		self.platedArmor = 0

		self.buffer = 0
		self.wraithForm = 0
		self.burst = 0

		self.attack_counter = 0
		self.skill_counter = 0
		self.card_counter = 0
		self.damage_counter = 0

		self.artifact = 0

		self.noBlock = 0
		self.magnetism = 0
		self.mayhem = 0
		self.panache = 0

		self.strengthDecrease = []
		self.dexterityDecrease = []

		self.duplication = 0
		self.regen = 0

		self.runicDome = 0
		self.velvetChoker = 0
		self.runicPyramide = 0
		self.confused = 0

		self.artOfWar = 0
		self.penNip = 0
		self.happyFlower = 0
		self.akabeko = 0
		self.sneckoSkull = 0
		self.meatOnTheBone = 0
		self.mercuryHourglass = 0
		self.mummifiedHand = 0
		self.sunDial = 0
		self.shuffle_counter = 0
		self.strikeDummy = 0
		self.birdFacedUrn = 0
		self.deadBranch = 0
		self.ginger = 0
		self.paperKrane = 0
		self.calipers = 0
		self.iceCream = 0
		self.incenseBurner = 0
		self.prayerWheel = 0
		self.torii = 0
		self.tungstenRod = 0
		self.turnip = 0
		self.unceasingTop = 0
		self.tingsha = 0
		self.toughBandages = 0
		self.medicalKit = 0
		self.blueCandle = 0
		self.chemicalX = 0
		self.strangeSpoon = 0
		self.frozenEye = 0
		self.hoveringKite = 0
		self.bloodyIdol = 0
		self.faceOfCleric = 0
		self.markOfTheBloom = 0
		self.oddMushroom = 0
		self.theAbacus = 0
		self.pocketWatch = 0
		self.stoneCalender = 0
		self.wristBlade = 0
		self.handDrill = 0
		self.necronomicon = 0
		self.warpedTongs = 0
		self.centennialPuzzle = 0
		self.nilrysCodex = 0
		self.boot = False

		self.randomTarget = 0
		self.hex = 0
		self.card_in_play = []

		self.turnMoment = 0
		self.timeWarp = False
		self.reducedDrawByTurns = []

		self.redKey = False
		self.blueKey = False
		self.greenKey = False
		self.allKeys = False

	def turn(self,turn_counter):
		
		if self.turnMoment == 0:
			self.enemyMoves()
			
			if self.dontLoseBlock > 0:
				pass
			
			elif self.calipers > 0:
				self.block -= 15
				if self.block < 0:
					self.block = 0
			else:
				self.block = 0

			if self.blockNextTurn > 0:
				self.blocking(self.blockNextTurn,unaffectedBlock = True)

			for enemy in entities.list_of_enemies:
				if enemy.metallicize > 0:
					enemy.set_block_by_metallicice(enemy.metallicize)
				if enemy.platedArmor > 0:
					enemy.blocking(enemy.platedArmor)
				
			
			if helping_functions.turn_counter == 1:
				self.relicFirstTurnEffects()
			
			self.negativeEffectsAtTheStartOfTheTurn()
			self.powersAtTheStartOfTheTurn()
			
			if self.iceCream:
				self.energy += self.energy_gain + self.temp_energy
			else:
				self.energy = self.energy_gain + self.temp_energy
			
			if len(self.reducedDrawByTurns) > 0:
				for turn in self.reducedDrawByTurns:
					if turn == helping_functions.turn_counter:
						self.tempDraw = -1

			if helping_functions.turn_counter == 1:
				self.draw_innates()
			
			else:
				while len(self.cardsNextTurn) > 0:
					self.hand.append(self.cardsNextTurn.pop(0))
				self.draw(self.draw_strength + self.tempDraw)
			
			if helping_functions.turn_counter == 1:
				self.relicFirstTurnEffects_afterDrawing()

			self.powerAfterAllCardsHaveBeenDrawn(turn_counter)
			self.reset()
			self.relicsEveryTurn(turn_counter)
			self.showHand()
			
			
			
			self.turnMoment = 1
		else:
			ansiprint("You saved during a fight!")
			
			
		while True:
			
			optionOne = "Play a <blue>Card</blue>"
			optionTwo = "Use a <c>Potion</c>"
			optionThree = "Show <light-red>Relics</light-red>"
			optionFour = "End Turn"
			optionFive = "Show All Cards"

			self.show_status()
			actionlist = [optionOne,optionTwo,optionThree,optionFour,optionFive]
			
			if self.runicDome == 0:
				self.showEnemies(skip=False)

			i = 0
			for action in actionlist:
				ansiprint(str(i+1)+".",action)
				i+=1
			try:
				plan = input("What do you want to do?\n")
				plan = int(plan)-1

				if plan not in range(len(actionlist)):
					continue
						
				if actionlist[plan] == optionOne:
					if self.velvetChoker > 0 and self.card_counter >= 6:
						ansiprint("You can't play anymore cards because you own a <light-red>Velvet Choker</light-red>.")
					elif self.timeWarp == True:
						ansiprint("You can't play anmore cards this turn because of <red>Time Eater</red>.")
					else:
						self.play_card(turn_counter)
				
				elif actionlist[plan] == optionTwo:
					if self.timeWarp == True:
						ansiprint("You can't drink anmore <c>Potions</c> this turn because of <red>Time Eater</red>.")
					else:
						self.play_potion(turn_counter)

				elif actionlist[plan] == optionThree:
					self.showRelics()
				
				elif actionlist[plan] == optionFive:
					self.print_all_cards()
				
				elif actionlist[plan] == optionFour:
					print("\n\n")
					if len(entities.list_of_enemies) > 0:
						self.powersAtTheEndOfTheTurn()
						self.cursesEndOfTurn()
						self.exhaust_ethereals()
						self.relicsAtTheEndOfTurn()
						self.discard_hand()
						self.changeEnergyCostAfterTurn()
						self.effect_counter_down()
						self.turnMoment = 0
						break
					
					else:
						self.end_of_battle_effects()
						self.turnMoment = 0
						break

				if self.unceasingTop > 0 and len(self.hand) == 0:
					self.draw(1)
					ansiprint("You have drawn another card because of <light-red>Unceasing Top</light-red>")
					self.showHand()
				time.sleep(0.03)
			
			except Exception as e:
				#print(e)
				self.explainer_function(plan)
				
	def enemyMoves(self):
		for enemy in entities.list_of_enemies:
			enemy.chooseMove()

	def gainEnergy(self,value):
		self.energy += value
		ansiprint(self.displayName, "has now <yellow>"+str(self.energy)+" Energy</yellow>.\n")	
	
	def powersAtTheStartOfTheTurn(self):
		
		if self.infiniteBlades > 0:
			iShiv = 0
			while iShiv < self.infiniteBlades:
				self.add_CardToHand({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
				iShiv += 1  
			
		if self.noxiousFumes > 0:
			for enemy in entities.list_of_enemies:
				enemy.set_poison(self.noxiousFumes)
		
		if self.ritual > 0:
			self.strength += self.ritual
			ansiprint(self.displayName,"just received",self.ritual,"Strength and now has",self.strength,"Strength.")

	def powerAfterAllCardsHaveBeenDrawn(self,turn_counter):

		if self.toolsOfTheTrade > 0:
			i = 0
			while i < self.toolsOfTheTrade:
				self.draw(1)
				self.discard(1)
				i += 1

		if self.magnetism > 0:
			i = 0
			while i < self.magnetism:
				neutral_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == "Colorless"}

				card = rd.choices(list(neutral_cards.items()))[0][1]
				
				self.add_CardToHand(card)
				
				i += 1

		if self.mayhem > 0:
			i = 0
			while i < self.mayhem:
				if len(self.draw_pile) == 0:
					self.discardBackInDrawpile()
				if len(self.draw_pile) == 0:
					anisprint("Your Discardpile and your Drawpile are empty.")
					break
				else:
					self.draw_pile[0]["Energy changed until played"] = True
					self.draw_pile[0]["Energy"] = 0

					self.card_is_played(self.draw_pile.pop(0),turn_counter)
					i += 1
				
	def negativeEffectsAtTheStartOfTheTurn(self):

		if self.constriction > 0:
			self.receive_recoil_damage(self.constriction)

	def end_of_battle_effects(self):
		
		if self.meatOnTheBone > 0 and self.health <= self.max_health/2:
			self.heal(12)
			ansiprint("<light-red>Meat on the Bone</light-red> just healed you!")
	
	def relicFirstTurnEffects(self):

		for relic in self.relics:
			
			if relic.get("Name") == "Anchor":
				self.blocking(10)
			elif relic.get("Name") == "Ring of the Snake":
				self.set_tempDraw(2)
			elif relic.get("Name") == "Bag of Marbles":
				for enemy in entities.list_of_enemies:
					enemy.set_vulnerable(1)

			elif relic.get("Name") == "Red Mask":
				for enemy in entities.list_of_enemies:
					enemy.set_weakness(1)

			elif relic.get("Name") == "Bag of Preparation":
				self.set_tempDraw(2)
			
			elif relic.get("Name") == "Blood Vial":
				self.heal(2)

			elif relic.get("Name") == "Bronze Scales":
				self.set_spikes(3)

			elif relic.get("Name") == "Lantern":
				self.energyBoost(1)
			
			elif relic.get("Name") == "Oddly Smooth Stone":
				self.set_dexterity(1)
			
			elif relic.get("Name") == "Vajra":
				self.set_strength(1)

			elif relic.get("Name") == "Girya":
				self.set_strength(relic.get("Counter"))

			elif relic.get("Name") == "Wrist Blade":
				self.wristBlade = 1

			elif relic.get("Name") == "Tungsten Rod":
				self.tungstenRod = 1

			elif relic.get("Name") == "Centennial Puzzle":
				self.centennialPuzzle = 1

			elif relic.get("Name") == "Nilry's Codex":
				self.nilrysCodex = 1

			elif relic.get("Name") == "Warped Tongs":

				self.warpedTongs = 1

			elif relic.get("Name") == "Cultis Headpeace":
				ansiprint(self.displayName+": <blue>CAW! CAAAW!</blue>")

			elif relic.get("Name") == "Hand Drill":
				self.handDrill = 1				

			elif relic.get("Name") == "The Abacus":
				self.theAbacus = 1

			elif relic.get("Name") == "Odd Mushroom":
				self.oddMushroom = 1
			
			elif relic.get("Name") == "Bloody Idol":
				self.bloodyIdol = 1
			
			elif relic.get("Name") == "Frozen Eye":
				self.frozenEye = 1

			elif relic.get("Name") == "Strange Spoon":
				self.strangeSpoon = 1

			elif relic.get("Name") == "Chemical X":
				self.chemicalX = 1
			
			elif relic.get("Name") == "Tough Bandages":
				self.toughBandages = 1

			elif relic.get("Name") == "Tingsha":
				self.tingsha = 1

			elif relic.get("Name") == "Unceasing Top":
				self.unceasingTop = 1

			elif relic.get("Name") == "Turnip":
				self.turnip = 1

			elif relic.get("Name") == "Sling of Courage" and self.get_floor() == "Elite":
				self.set_strength(2)

			elif relic.get("Name") == "Ice Cream":
				self.iceCream = 1

			elif relic.get("Name") == "Ginger":
				self.ginger = 1

			elif relic.get("Name") == "Paper Krane":
				self.paperKrane = 1

			elif relic.get("Name") == "Bird-Faced Urn":
				self.birdFacedUrn = 1

			elif relic.get("Name") == "Strike Dummy":
				self.strikeDummy = 1

			elif relic.get("Name") == "Dead Branch":
				self.deadBranch = 1

			elif relic.get("Name") == "Torii":
				self.torii = 1

			elif relic.get("Name") == "Blue Candle":
				self.blueCandle = 1

			elif relic.get("Name") == "Medical Kit":
				self.medicalKit = 1

			elif relic.get("Name") == "Sundial":
				self.sunDial =1
			
			elif relic.get("Name") == "Meat on the Bone":
				self.meatOnTheBone = 1

			elif relic.get("Name") == "Snecko Skull":
				self.sneckoSkull = 1

			elif relic.get("Name") == "Fossilized Helix":
				self.set_buffer(1)

			elif relic.get("Name") == "Preserved Insect":
				if self.get_floor() == "Elite":
					for enemy in entities.list_of_enemies():
						damage = math.floor(enemy.health/4)
						enemy.receive_recoil_damage(damage)
				ansiprint("Preserved Insect did this damage.")

			elif relic.get("Name") == "Pantograph":
				if self.get_floor() == "Boss":
					self.heal(25)
				ansiprint("Pantograph Relic heals you for 25 whenever you meet a Boss.")

			elif relic.get("Name") == "Ninja Scroll":
				self.add_CardToHand({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
				self.add_CardToHand({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
				self.add_CardToHand({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})

			elif relic.get("Name") == "Du-Vu Doll":
				i = 0
				for card in self.deck:
					if card.get("Type") == "Curse":
						i +=1
				if i > 0: 					
					self.set_strength(i)

			elif relic.get("Name") == "Thread and Needle":
				self.set_platedArmor(4)
			
			elif relic.get("Name") == "Clockwork Souvenir":
				self.set_artifact(1)

			elif relic.get("Name") == "Twisted Funnel":
				for enemy in entities.list_of_enemies:
					enemy.set_poison(4)
			
			elif relic.get("Name") == "Snecko Eye":
				self.set_drawStrength(2)
				self.set_confused()

			elif relic.get("Name") == "The Boot":
				self.theBoot = True

			elif relic.get("Name") == "Ring of the Serpent":
				self.set_drawStrength(1)

			elif relic.get("Name") == "Mutagenic Strength":
				self.set_strengthDecrease(3)
				self.set_strength(3)
			
			elif relic.get("Name") == "Neow's Lament":
				if relic.get("Counter") > 0:
					for enemy in entities.list_of_enemies:
						enemy.set_health(1)
					relic["Counter"] = relic.get("Counter") -1
					ansiprint("<light-red>Neow's Lament</light-red> works",relic.get("Counter"),"more times.")

			elif relic.get("Name") == "Gremlin Visage":
				self.set_weakness(1)

			elif relic.get("Name") == "Gremlin Visage":
				self.set_weakness(1)

			elif relic.get("Name") == "Busted Crown":
				self.set_energyGain(1)

			elif relic.get("Name") == "Ectoplasm":
				self.set_energyGain(1)
			
			elif relic.get("Name") == "Cursed Key":
				self.set_energyGain(1)

			elif relic.get("Name") == "Fusion Hammer":
				self.set_energyGain(1)
			
			elif relic.get("Name") == "Philosopher's Stone":
				self.set_energyGain(1)
				for enemy in entities.list_of_enemies:
					enemy.set_strength(1)
			
			elif relic.get("Name") == "Velvet Choker":
				self.set_energyGain(1)			
				self.velvetChoker = 1
			elif relic.get("Name") == "Runic Dome":
				self.set_energyGain(1)
				self.runicDome = 1

			elif relic.get("Name") == "Coffee Dripper":
				self.set_energyGain(1)

			elif relic.get("Name") == "Sozu":
				self.set_energyGain(1)

			elif relic.get("Name") == "Slaver's Collar":
				if self.get_floor == "Boss" or self.get_floor == "Elite" or self.get_floor == "Super":
					self.set_energyGain(1)

			elif relic.get("Name") == "Runic Pyramide":
				self.runicPyramide = 1

			elif relic.get("Name") == "Art of War":
				self.artOfWar = 1

			elif relic.get("Name") == "Akabeko":
				self.akabeko = 1

			elif relic.get("Name") == "Mercury Hourglass":
				self.mercuryHourglass = 1

			elif relic.get("Name") == "Mummified Hand":
				self.mummifiedHand = 1

			elif relic.get("Name") == "Calipers":
				self.calipers = 1

			elif relic.get("Name") == "Incense Burner":
				self.incenseBurner = 1

			elif relic.get("Name") == "Stone Calender":
				self.stoneCalender = 1

			elif relic.get("Name") == "Pocketwatch":
				self.pocketWatch = 1


	def relicsEveryTurn(self,turn_counter):

		if turn_counter == 2:
			for relic in self.relics:
				if relic.get("Name") == "Horn Cleat":
					self.blocking(14,unaffectedBlock=True)
		elif turn_counter == 3:
			for relic in self.relics:
				if relic.get("Name") == "Captain's Wheel":
					self.blocking(18,unaffectedBlock=True)

		if self.happyFlower > 0:
			if turn_counter%3 == 0:
				self.gainEnergy(1)

		if self.mercuryHourglass > 0:
			ansiprint("All Enemies receive <red>3 Damage</red> because of <light-red>Mercury Hourglass</light-red>")
			i = 0
			while i < len(entities.list_of_enemies):
				enemy_check = len(entities.list_of_enemies)
				entities.list_of_enemies[i].receive_recoil_damage(3)
				if enemy_check != len(entities.list_of_enemies):
					continue
				else:
					i+=1

		if self.incenseBurner > 0:
			incenseIndex = next((i for i, item in enumerate(self.relics) if item["Name"] == "Incense Burner"), None)
			self.relics[incenseIndex]["Counter"] += 1
			if self.relics[incenseIndex]["Counter"] % 6 == 0:
				self.set_intangible(1)
				ansiprint("Your <light-red>Incense Burner</light-red> did this!")

		if next((i for i, item in enumerate(self.relics) if item["Name"] == "Hovering Kite"), None):
			self.hoveringKite = 1
		
		if next((i for i, item in enumerate(self.relics) if item["Name"] == "Necronomicon"), None):
			self.necronomicon = 1

		if self.warpedTongs == 1:
			test = [card for card in self.hand if card.get("Upgraded") != True and card.get("Type") != "Curse" and card.get("Type") != "Status"]

			if len(list(test)) > 0:
				
				upgradeCard = rd.choices(list(test),k=1)[0]
				
				cardIndex = self.hand.index(upgradeCard)

				helping_functions.upgradeCard(self.hand.pop(self.hand.index(upgradeCard)),"Hand",index = cardIndex)


	def relicFirstTurnEffects_afterDrawing(self):
		
		for relic in self.relics:
			
			if relic.get("Name") == "Toolbox":
				colorless_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == "Colorless" and v.get("Rarity") != "Special" and "+" not in v.get("Name")}
				cards = rd.choices(list(colorless_cards.items()),k=3)
				
				three_options = []
				for card in cards:
					three_options.append(card[1])
				
				helping_functions.pickCard(three_options,place="Hand")

			if relic.get("Name") == "Enchiridion":
				random_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == self.name and v.get("Rarity") == "Rare" and v.get("Upgraded") != True and v.get("Type") == "Power"}
					
				card_add = rd.choices(list(random_cards.items()))[0][1]
				card_add["This turn Energycost changed"] = True
				card_add["Energy"] = 0	

				self.add_CardToHand(card_add)

			if relic.get("Name") == "Gambling Chip":
				print("This needs to be implemented after cards have been drawn.")
				i = 0
				yesNo = ["Yes","No"]
				handLength = len(self.hand)
				while i < handLength:
					check = input("Do you want to discard cards?(Yes/No) You draw as many as you discard.")
					
					while check not in yesNo:
						check = input("Do you want to discard another card.(Yes/No)")
						self.explainer_function(check,answer=False)
					
					if check == "Yes":
						self.discard(1)
						i+=1
					elif check == "No":
						break
					else:
						print(check,"<--- How's that not Yes or No?")
				
				self.draw(i)

	def relicsAtTheEndOfTurn(self):
		if len(entities.list_of_enemies) > 0:
			if self.pocketWatch > 0:
				if self.card_counter <= 3:
					self.set_tempDraw(3)
					ansiprint("This happened because you played 3 or less cards with <light-red>Pocket Watch</light-red>.")
			if self.stoneCalender > 0:
				if helping_functions.turn_counter == 7:
					ansiprint("All Enemies receive <red>52 Damage</red> because of <light-red>Stone Calender</light-red>.")
					i = 0
					while i < len(entities.list_of_enemies):
						enemy_check = len(entities.list_of_enemies)
						entities.list_of_enemies[i].receive_recoil_damage(52)
						if enemy_check != len(entities.list_of_enemies):
							continue
						else:
							i+=1
			if self.nilrysCodex == 1:
				try:
					
					random_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == self.name and v.get("Rarity") == "Rare" and v.get("Upgraded") != True}
					threeRandomCards = rd.choices(list(random_cards.items()),k=3)	
						
					three_options = []
					
					for card in threeRandomCards:
						three_options.append(card[1])

					helping_functions.pickCard(three_options,place="Drawpile")
				except Exception as e:
					print("Relics at the end",e)
		

	def powersAtTheEndOfTheTurn(self):
		
		if self.wellLaidPlans > 0:
			i = 0
			while i < self.wellLaidPlans and len(self.hand) > 0:
				self.showHand()
				card_index = 0
				
				try:
					card_index = input("Pick the number of the card you want to copy for next turn\n")
					card_index = int(card_index)-1
					if card_index in range(len(self.hand)):
						self.cardsNextTurn.append(self.hand.pop(card_index))
						i += 1
						

				except Exception as e:
					self.explainer_function(card_index)
					ansiprint ("You have to type on of the corresponding numbers. Well Laid Plans powersAtTheEndOfTheTurn")					
					pass
		
		if self.wraithForm > 0:
			self.set_dexterity(-self.wraithForm)

		if len(self.theBomb) > 0:
			for bomb in self.theBomb:
				if bomb[0] == helping_functions.turn_counter:
					enemy_check = len(entities.list_of_enemies)
					i = 0
					while i < len(entities.list_of_enemies):
						entities.list_of_enemies[i].receive_recoil_damage(bomb[1])
						
						if enemy_check > len(entities.list_of_enemies):
							pass
						else:
							i+=1

		if len(self.strengthDecrease) > 0:
			for decrease in self.strengthDecrease:
				if decrease[0] == helping_functions.turn_counter:
					self.set_strength(decrease[1])

		if len(self.dexterityDecrease) > 0:
			for decrease in self.dexterityDecrease:
				if decrease[0] == helping_functions.turn_counter:
					self.set_strength(decrease[1])

		for relic in self.relics:
			if relic.get("Name") == "Oricalcum":
				if self.block == 0:
					self.blocking(6,unaffectedBlock = True)

		if self.metallicize > 0:
			self.set_block_by_metallicice(self.metallicize)

		if self.platedArmor > 0:
			self.set_block_by_platedArmor(self.platedArmor)

		if self.regen > 0:
			self.regenerate()

		if self.artOfWar > 0:
			if self.attack_counter == 0:
				self.energyBoost(1)

	def play_card(self,turn_counter):
		
		if self.check_CardPlayRestricions() == True:
			return
		
		if len(self.hand) == 0:
			ansiprint("You don't have any cards in your hand to play.")
			return
		if len(entities.list_of_enemies) == 0:
			ansiprint("There are no opponents left.")
			return
		
		while True:

			try:

				self.showHand()
				print(str(len(self.hand)+1)+".  Skip")
				ansiprint("You have <yellow>"+str(self.energy)+" Energy</yellow> available.")
				
				card_index = 0

				card_index = input("Pick the number of the card you want to play\n")
				card_index = int(card_index)-1
				if card_index == len(self.hand):
					return

				if card_index in range(len(self.hand)):
					try:
						if type(self.hand[card_index]["Energy"]) == str:
							
							if self.chemicalX > 0:
								self.energy += 2
							break
							
						elif self.hand[card_index]["Energy"] <= self.energy:
							break
						
						elif self.cardsCostNothing > 0:
							break
						
						elif self.hand[card_index].get("Type") == "Status" and self.medicalKit > 0:
							break
						
						elif self.hand[card_index].get("Type") == "Curse" and self.blueCandle > 0:
							break

						else:
							ansiprint("You can't play this card.")
							return
				
					except Exception as e:	
						if e == "Energy":
							ansiprint("You don't have enough <yellow>Energy</yellow> to play this card.")
						else:
							#ansiprint("There is an issue playing this card. Play card.",type(e))
							pass
						return
					
				else:
					ansiprint ("You don't have this card!")
					
			except Exception as e:
				#print("play card",e)
				self.explainer_function(card_index)
				ansiprint ("Type a corresponding number and choose playable cards!")
				
		
		if "Grand Finale" in self.hand[card_index].get("Name"):
			if len(self.draw_pile) == 0:
				pass
			else:
				print("You need an empty Drawpile to play this card.")
				return
				
		if self.entangled > 0 and self.hand[card_index]["Type"] == "Attack":
			ansiprint("You can't play Attacks this turn because your are entangled")
			return

		
		self.card_is_played(self.hand.pop(card_index),turn_counter)

	def card_is_played (self,card,turn_counter,repeat: bool = False):
		
		self.card_in_play = [card]
		enemy_check = len(entities.list_of_enemies)
		
		if repeat:

			ansiprint(self.card_in_play[0].get("Name"),"was replayed!")

		if self.card_in_play[0]["Owner"] == "Silent":
			
			if self.card_in_play[0].get("Name") == "Strike":				
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				
			elif self.card_in_play[0].get("Name") == "Strike +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
			
			elif self.card_in_play[0].get("Name") == "Defend":
				self.blocking(self.card_in_play[0]["Block"])
			
			elif self.card_in_play[0].get("Name") == "Defend +":
				self.blocking(self.card_in_play[0]["Block"])

			elif self.card_in_play[0].get("Name") == "Neutralize":				
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				
				if enemy_check == len(entities.list_of_enemies):
					entities.list_of_enemies[self.target].set_weakness(self.card_in_play[0]["Weakness"])
				
			elif self.card_in_play[0].get("Name") == "Neutralize +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				
				if enemy_check == len(entities.list_of_enemies):
					entities.list_of_enemies[self.target].set_weakness(self.card_in_play[0]["Weakness"])

			elif self.card_in_play[0].get("Name") == "Survivor":
				self.blocking(self.card_in_play[0]["Block"])
				self.discard(self.card_in_play[0]["Discard"])
			
			elif self.card_in_play[0].get("Name") == "Survivor +":
				self.blocking(self.card_in_play[0]["Block"])
				self.discard(self.card_in_play[0]["Discard"])

			elif self.card_in_play[0].get("Name") == "Bane":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				
				if enemy_check == len(entities.list_of_enemies):
					if entities.list_of_enemies[self.target].poison > 0:						
						self.attack(self.card_in_play[0]["Damage"])

			elif self.card_in_play[0].get("Name") == "Bane +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				
				if enemy_check == len(entities.list_of_enemies):
					if entities.list_of_enemies[self.target].poison > 0:						
						self.attack(self.card_in_play[0]["Damage"])

			elif self.card_in_play[0].get("Name") == "Dagger Spray":
				i = 0

				while i < len(entities.list_of_enemies):
					enemy_check = len(entities.list_of_enemies)
					self.target = i
					self.attack(self.card_in_play[0]["Damage"])
					if enemy_check == len(entities.list_of_enemies):
						i += 1
				
				i = 0
				while i < len(entities.list_of_enemies):
					enemy_check = len(entities.list_of_enemies)
					self.target = i					
					self.attack(self.card_in_play[0]["Damage"])
					if enemy_check == len(entities.list_of_enemies):
						i += 1

			elif self.card_in_play[0].get("Name") == "Dagger Spray +":
				i = 0
				while i < len(entities.list_of_enemies):
					enemy_check = len(entities.list_of_enemies)
					self.target = i
					self.attack(self.card_in_play[0]["Damage"])
					if enemy_check == len(entities.list_of_enemies):
						i += 1
				
				i = 0
				while i < len(entities.list_of_enemies):
					enemy_check = len(entities.list_of_enemies)
					self.target = i					
					self.attack(self.card_in_play[0]["Damage"])
					if enemy_check == len(entities.list_of_enemies):
						i += 1

			elif self.card_in_play[0].get("Name") == "Dagger Throw":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				self.draw(self.card_in_play[0]["Draw"])
				self.discard(self.card_in_play[0]["Discard"])

			elif self.card_in_play[0].get("Name") == "Dagger Throw +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				self.draw(self.card_in_play[0]["Draw"])
				self.discard(self.card_in_play[0]["Discard"])
			
				
			elif self.card_in_play[0].get("Name") == "Flying Knee":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				self.energyBoost(self.card_in_play[0]["Energy Gain"])

			elif self.card_in_play[0].get("Name") == "Flying Knee +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				self.energyBoost(self.card_in_play[0]["Energy Gain"])

			elif self.card_in_play[0].get("Name") == "Poisoned Stab":
				enemy_check = len(entities.list_of_enemies)
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				
				if enemy_check == len(entities.list_of_enemies):
					entities.list_of_enemies[self.target].set_poison(self.card_in_play[0]["Poison"])
			
			elif self.card_in_play[0].get("Name") == "Poisoned Stab +":
				enemy_check = len(entities.list_of_enemies)
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				
				if enemy_check == len(entities.list_of_enemies):
					entities.list_of_enemies[self.target].set_poison(self.card_in_play[0]["Poison"])

			elif self.card_in_play[0].get("Name") == "Quick Slash":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				self.draw(self.card_in_play[0]["Draw"])

			elif self.card_in_play[0].get("Name") == "Quick Slash +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				self.draw(self.card_in_play[0]["Draw"])

			elif self.card_in_play[0].get("Name") == "Slice":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])

			elif self.card_in_play[0].get("Name") == "Slice +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])

			elif self.card_in_play[0].get("Name") == "Sneaky Strike":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				
				if self.discard_counter > 0:
					self.gainEnergy(self.card_in_play[0]["Energy Gain"])

			elif self.card_in_play[0].get("Name") == "Sneaky Strike +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				
				if self.discard_counter > 0:
					self.gainEnergy(self.card_in_play[0]["Energy Gain"])

			elif self.card_in_play[0].get("Name") == "Sucker Punch":
				
				self.choose_enemy()		
				self.attack(self.card_in_play[0]["Damage"])
				
				if enemy_check == len(entities.list_of_enemies):
					entities.list_of_enemies[self.target].set_weakness(self.card_in_play[0]["Weakness"])

			elif self.card_in_play[0].get("Name") == "Sucker Punch +":
				self.choose_enemy()		
				self.attack(self.card_in_play[0]["Damage"])
				
				if enemy_check == len(entities.list_of_enemies):
					entities.list_of_enemies[self.target].set_weakness(self.card_in_play[0]["Weakness"])


			elif self.card_in_play[0].get("Name") == "All-Out Attack":
				i = 0
				while i < len(entities.list_of_enemies):
					self.target = i
					self.attack(self.card_in_play[0]["Damage"])
					
					if enemy_check == len(entities.list_of_enemies):
						i += 1
		
				self.discard(self.card_in_play[0]["Discard"],True)
			
			elif self.card_in_play[0].get("Name") == "All-Out Attack +":
				i = 0
				while i < len(entities.list_of_enemies):
					self.target = i
					self.attack(self.card_in_play[0]["Damage"])
					
					if enemy_check == len(entities.list_of_enemies):
						i += 1
		
				self.discard(self.card_in_play[0]["Discard"],True)


			elif self.card_in_play[0].get("Name") == "Backstab":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])

			elif self.card_in_play[0].get("Name") == "Backstab +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])

		
			elif self.card_in_play[0].get("Name") == "Choke":
				self.choose_enemy()			
				self.attack(self.card_in_play[0]["Damage"])
				
				if enemy_check == len(entities.list_of_enemies):
					entities.list_of_enemies[self.target].set_choke(self.card_in_play[0]["Choking"])

			elif self.card_in_play[0].get("Name") == "Choke +":
				self.choose_enemy()			
				self.attack(self.card_in_play[0]["Damage"])
				
				if enemy_check == len(entities.list_of_enemies):
					entities.list_of_enemies[self.target].set_choke(self.card_in_play[0]["Choking"])

			
			elif self.card_in_play[0].get("Name") == "Dash":
				self.choose_enemy()
				self.blocking(self.card_in_play[0]["Block"])
				self.attack(self.card_in_play[0]["Damage"])

			elif self.card_in_play[0].get("Name") == "Dash +":
				self.choose_enemy()
				self.blocking(self.card_in_play[0]["Block"])
				self.attack(self.card_in_play[0]["Damage"])
			

			elif self.card_in_play[0].get("Name") == "Endless Agony":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				#needs to create copy on draw and exhauste on play.
			
			elif self.card_in_play[0].get("Name") == "Endless Agony +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])


			elif self.card_in_play[0].get("Name") == "Eviscerate":
				self.choose_enemy()				
				i = 0
				while i < 3:
					self.attack(self.card_in_play[0]["Damage"])					
					if enemy_check != len(entities.list_of_enemies):
						break
					i+=1

			elif self.card_in_play[0].get("Name") == "Eviscerate +":
				self.choose_enemy()				
				i = 0
				while i < 3:
					self.attack(self.card_in_play[0]["Damage"])					
					if enemy_check != len(entities.list_of_enemies):
						break
					i+=1
		

			elif self.card_in_play[0].get("Name") == "Finisher":
				self.choose_enemy()				
				i = 0
				while i < self.attack_counter:
					self.attack(self.card_in_play[0]["Damage"])
			
					if enemy_check != len(entities.list_of_enemies):
						break
					i+=1

			elif self.card_in_play[0].get("Name") == "Finisher +":
				self.choose_enemy()				
				i = 0
				while i < self.attack_counter:
					self.attack(self.card_in_play[0]["Damage"])
			
					if enemy_check != len(entities.list_of_enemies):
						break
					i+=1
			
			elif self.card_in_play[0].get("Name") == "Flechettes":
				self.choose_enemy()
				k = 0
				for card in self.hand:
					if card["Type"] == "Skill":
						k += 1
				i = 0
				while i < k:
					self.attack(self.card_in_play[0]["Damage"])
					if enemy_check != len(entities.list_of_enemies):
						break
					i+=1

			elif self.card_in_play[0].get("Name") == "Flechettes +":
				self.choose_enemy()
				k = 0
				for card in self.hand:
					if card["Type"] == "Skill":
						k += 1
				i = 0
				while i < k:
					self.attack(self.card_in_play[0]["Damage"])
					if enemy_check != len(entities.list_of_enemies):
						break
					i+=1

			elif self.card_in_play[0].get("Name") == "Heel Hook":
				self.choose_enemy()
				if entities.list_of_enemies[self.target].weak > 0:
						self.gainEnergy(self.card_in_play[0]["Energy Gain"])
						self.draw(self.card_in_play[0]["Draw"])
				self.attack(self.card_in_play[0]["Damage"])
				
			elif self.card_in_play[0].get("Name") == "Heel Hook +":
				self.choose_enemy()
				if entities.list_of_enemies[self.target].weak > 0:
						self.gainEnergy(self.card_in_play[0]["Energy Gain"])
						self.draw(self.card_in_play[0]["Draw"])
				self.attack(self.card_in_play[0]["Damage"])

			elif self.card_in_play[0].get("Name") == "Masterful Stab":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])

			elif self.card_in_play[0].get("Name") == "Masterful Stab +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
			
			
			elif self.card_in_play[0].get("Name") == "Predator":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				self.set_tempDraw(self.card_in_play[0]["Drawboost"])

			elif self.card_in_play[0].get("Name") == "Predator +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				self.set_tempDraw(self.card_in_play[0]["Drawboost"])


			elif self.card_in_play[0].get("Name") == "Riddle with Holes":
				self.choose_enemy()
				i = 0
				while i < 5:
					self.attack(self.card_in_play[0]["Damage"])
					if enemy_check != len(entities.list_of_enemies):
						break
					i+=1

			elif self.card_in_play[0].get("Name") == "Riddle with Holes +":
				self.choose_enemy()
				i = 0
				while i < 5:
					self.attack(self.card_in_play[0]["Damage"])
					if enemy_check != len(entities.list_of_enemies):
						break
					i+=1
				

			elif self.card_in_play[0].get("Name") == "Skewer":
				self.choose_enemy()
				i = 0
				while i < self.energy:
					self.attack(self.card_in_play[0]["Damage"])			
					if enemy_check != len(entities.list_of_enemies):
						break
					i+=1

			elif self.card_in_play[0].get("Name") == "Skewer +":
				self.choose_enemy()
				i = 0
				while i < self.energy:
					self.attack(self.card_in_play[0]["Damage"])			
					if enemy_check != len(entities.list_of_enemies):
						break
					i+=1
			

			elif self.card_in_play[0].get("Name") == "Die Die Die":
				i = 0
				while i < len(entities.list_of_enemies):
					enemy_check =len(entities.list_of_enemies)
					self.target = i
					self.attack(self.card_in_play[0]["Damage"])
					if enemy_check != len(entities.list_of_enemies):
						pass
					else:
						i+=1
			
			elif self.card_in_play[0].get("Name") == "Die Die Die +":
				i = 0
				while i < len(entities.list_of_enemies):					
					enemy_check =len(entities.list_of_enemies)
					self.target = i
					self.attack(self.card_in_play[0]["Damage"])
					if enemy_check != len(entities.list_of_enemies):
						pass
					else:
						i+=1


			elif self.card_in_play[0].get("Name") == "Glass Knife":
				self.choose_enemy()				
				i = 0
				while i < 2:
					self.attack(self.card_in_play[0]["Damage"])				
					if enemy_check != len(entities.list_of_enemies):
						break
					i+=1
				self.card_in_play[0]["Damage"] -= 2

			elif self.card_in_play[0].get("Name") == "Glass Knife +":
				self.choose_enemy()				
				i = 0
				while i < 2:
					self.attack(self.card_in_play[0]["Damage"])				
					if enemy_check != len(entities.list_of_enemies):
						break
					i+=1
				self.card_in_play[0]["Damage"] -= 2
			

			elif self.card_in_play[0].get("Name") == "Grand Finale":
				i = 0
				while i < len(entities.list_of_enemies):
					enemy_check =len(entities.list_of_enemies)
					self.target = i
					self.attack(self.card_in_play[0]["Damage"])
					if enemy_check != len(entities.list_of_enemies):
						pass
					else:
						i+=1

			elif self.card_in_play[0].get("Name") == "Grand Finale +":
				i = 0
				while i < len(entities.list_of_enemies):
					enemy_check =len(entities.list_of_enemies)
					self.target = i
					self.attack(self.card_in_play[0]["Damage"])
					if enemy_check != len(entities.list_of_enemies):
						pass
					else:
						i+=1
				
			elif self.card_in_play[0].get("Name") == "Unload":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				self.discard_cards_by_type_opposite(self.card_in_play[0]["DiscardType"])

			elif self.card_in_play[0].get("Name") == "Unload +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				self.discard_cards_by_type_opposite(self.card_in_play[0]["DiscardType"])


			elif self.card_in_play[0].get("Name") == "Acrobatics":
				self.draw(self.card_in_play[0]["Draw"])
				self.discard(self.card_in_play[0]["Discard"])

			elif self.card_in_play[0].get("Name") == "Acrobatics +":
				self.draw(self.card_in_play[0]["Draw"])
				self.discard(self.card_in_play[0]["Discard"])


			elif self.card_in_play[0].get("Name") == "Backflip":
				self.blocking(self.card_in_play[0]["Block"])
				self.draw(self.card_in_play[0]["Draw"])

			elif self.card_in_play[0].get("Name") == "Backflip +":
				self.blocking(self.card_in_play[0]["Block"])
				self.draw(self.card_in_play[0]["Draw"])


			elif self.card_in_play[0].get("Name") == "Blade Dance":
				i = 0
				while i < self.card_in_play[0]["Shivs"]:
					if len(self.hand) < 10:
						self.add_CardToHand({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
					else:
						self.add_CardToDiscardpile({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
					i += 1

			elif self.card_in_play[0].get("Name") == "Blade Dance +":
				i = 0
				while i < self.card_in_play[0]["Shivs"]:
					if len(self.hand) < 10:
						self.add_CardToHand({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
					else:
						self.add_CardToDiscardpile({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
					i += 1		


			elif self.card_in_play[0].get("Name") == "Cloak and Dagger":
				self.blocking(self.card_in_play[0]["Block"])
				i = 0
				while i < self.card_in_play[0]["Shivs"]:
					if len(self.hand) < 10:
						self.hand.append({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
					else:
						self.discard_pile.append({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
					i += 1

			elif self.card_in_play[0].get("Name") == "Cloak and Dagger +":
				self.blocking(self.card_in_play[0]["Block"])
				i = 0
				while i < self.card_in_play[0]["Shivs"]:
					if len(self.hand) < 10:
						self.hand.append({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
					else:
						self.discard_pile.append({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
					i += 1

			elif self.card_in_play[0].get("Name") == "Deadly Poison":
				self.choose_enemy()
				entities.list_of_enemies[self.target].set_poison(self.card_in_play[0]["Poison"])
			
			elif self.card_in_play[0].get("Name") == "Deadly Poison +":
				self.choose_enemy()
				entities.list_of_enemies[self.target].set_poison(self.card_in_play[0]["Poison"])

			elif self.card_in_play[0].get("Name") == "Deflect":
				self.blocking(self.card_in_play[0]["Block"])
			
			elif self.card_in_play[0].get("Name") == "Deflect +":
				self.blocking(self.card_in_play[0]["Block"])


			elif self.card_in_play[0].get("Name") == "Dodge and Roll":
				self.blocking(self.card_in_play[0]["Block"])
				self.blockingNextTurn(self.card_in_play[0]["Block"])

			elif self.card_in_play[0].get("Name") == "Dodge and Roll +":
				self.blocking(self.card_in_play[0]["Block"])
				self.blockingNextTurn(self.card_in_play[0]["Block"])


			elif self.card_in_play[0].get("Name") == "Outmaneuver":
				self.energyBoost(self.card_in_play[0]["Energy Gain"])

			elif self.card_in_play[0].get("Name") == "Outmaneuver +":
				self.energyBoost(self.card_in_play[0]["Energy Gain"])


			elif self.card_in_play[0].get("Name") == "Piercing Wail":
				for enemy in entities.list_of_enemies:
					enemy.set_tempStrength(self.card_in_play[0]["Strength Modifier"])
					enemy.set_strength(-self.card_in_play[0]["Strength Modifier"])

			elif self.card_in_play[0].get("Name") == "Piercing Wail +":
				for enemy in entities.list_of_enemies:
					enemy.set_tempStrength(self.card_in_play[0]["Strength Modifier"])
					enemy.set_strength(-self.card_in_play[0]["Strength Modifier"])


			elif self.card_in_play[0].get("Name") == "Prepared":
				self.draw(self.card_in_play[0]["Draw"])
				self.discard(self.card_in_play[0]["Discard"])

			elif self.card_in_play[0].get("Name") == "Prepared +":
				self.draw(self.card_in_play[0]["Draw"])
				self.discard(self.card_in_play[0]["Discard"])


			elif self.card_in_play[0].get("Name") == "Blur":
				self.blocking(self.card_in_play[0]["Block"])
				self.set_dontLoseBlock(self.card_in_play[0]["KeepBlock"])

			elif self.card_in_play[0].get("Name") == "Blur +":
				self.blocking(self.card_in_play[0]["Block"])
				self.set_dontLoseBlock(self.card_in_play[0]["KeepBlock"])


			elif self.card_in_play[0].get("Name") == "Bouncing Flask":
				i = 0
				while i < self.card_in_play[0]["Bounces"]:
					entities.list_of_enemies[rd.randint(0,len(entities.list_of_enemies)-1)].set_poison(self.card_in_play[0]["Poison"])
					i += 1

			elif self.card_in_play[0].get("Name") == "Bouncing Flask +":
				i = 0
				while i < self.card_in_play[0]["Bounces"]:
					entities.list_of_enemies[rd.randint(0,len(entities.list_of_enemies)-1)].set_poison(self.card_in_play[0]["Poison"])
					i += 1

			elif self.card_in_play[0].get("Name") == "Calculated Gamble":
				draw_power = len(self.hand)
				self.discard(len(self.hand), True)
				self.draw(draw_power)

			elif self.card_in_play[0].get("Name") == "Calculated Gamble +":
				draw_power = len(self.hand)
				self.discard(len(self.hand), True)
				self.draw(draw_power)

			elif self.card_in_play[0].get("Name") == "Catalyst":
				self.choose_enemy()
				entities.list_of_enemies[self.target].multiply_poison(self.card_in_play[0]["Multiplikator"])

			elif self.card_in_play[0].get("Name") == "Catalyst +":
				self.choose_enemy()
				entities.list_of_enemies[self.target].multiply_poison(self.card_in_play[0]["Multiplikator"])

			elif self.card_in_play[0].get("Name") == "Concentrate":				
				self.discard(self.card_in_play[0]["Discard"])
				self.gainEnergy(self.card_in_play[0]["Energy Gain"])

			elif self.card_in_play[0].get("Name") == "Concentrate +":
				self.discard(self.card_in_play[0]["Discard"])
				self.gainEnergy(self.card_in_play[0]["Energy Gain"])

			elif self.card_in_play[0].get("Name") == "Crippling Cloud":
				for enemy in entities.list_of_enemies:
					try:
						enemy.set_poison(self.card_in_play[0]["Poison"])
						enemy.set_weakness(self.card_in_play[0]["Weakness"])
					except Exception as e:
						print("Did the last enemy really just die because of sadistic nature? Nice.")

			elif self.card_in_play[0].get("Name") == "Crippling Cloud +":
				for enemy in entities.list_of_enemies:
					try:
						enemy.set_poison(self.card_in_play[0]["Poison"])
						enemy.set_weakness(self.card_in_play[0]["Weakness"])
					except Exception as e:
						print("Did the last enemy really just die because of sadistic nature? Nice.")

			elif self.card_in_play[0].get("Name") == "Distraction":
				skill_cards = {k:v for k,v in entities.cards.items() if v.get("Type") == "Skill" and v.get("Owner") == self.name and v.get("Rarity") != "Basic"}
				card = rd.choices(list(skill_cards.items()))[0][1]				
				card["This turn Energycost changed"] = True
				card["Energy"] = 0				
				self.add_CardToHand(card)

			elif self.card_in_play[0].get("Name") == "Distraction +":
				skill_cards = {k:v for k,v in entities.cards.items() if v.get("Type") == "Skill" and v.get("Owner") == self.name and v.get("Rarity") != "Basic"}
				card = rd.choices(list(skill_cards.items()))[0][1]				
				card["This turn Energycost changed"] = True
				card["Energy"] = 0				
				self.add_CardToHand(card)

			elif self.card_in_play[0].get("Name") == "Escape Plan":
				self.draw(self.card_in_play[0]["Draw"])
				if self.hand[-1]["Type"] == "Skill":
					self.blocking(self.card_in_play[0]["Block"])

			elif self.card_in_play[0].get("Name") == "Escape Plan +":
				self.draw(self.card_in_play[0]["Draw"])
				if self.hand[-1]["Type"] == "Skill":
					self.blocking(self.card_in_play[0]["Block"])

			elif self.card_in_play[0].get("Name") == "Expertise":
				while len(self.hand) < self.card_in_play[0]["Draw"]:
					self.draw(1)

			elif self.card_in_play[0].get("Name") == "Expertise +":
				while len(self.hand) < self.card_in_play[0]["Draw"]:
					self.draw(1)

			elif self.card_in_play[0].get("Name") == "Leg Sweep":
				self.choose_enemy()
				self.blocking(self.card_in_play[0]["Block"])
				entities.list_of_enemies[self.target].set_weakness(self.card_in_play[0]["Weakness"])

			elif self.card_in_play[0].get("Name") == "Leg Sweep +":
				self.choose_enemy()
				self.blocking(self.card_in_play[0]["Block"])
				entities.list_of_enemies[self.target].set_weakness(self.card_in_play[0]["Weakness"])

			elif self.card_in_play[0].get("Name") == "Reflex":
				print("This card is unplayable.")

			elif self.card_in_play[0].get("Name") == "Reflex +":
				print("This card is unplayable.")

			elif self.card_in_play[0].get("Name") == "Tactician":
				print("This card is unplayable.")

			elif self.card_in_play[0].get("Name") == "Tactician +":
				print("This card is unplayable.")

			elif self.card_in_play[0].get("Name") == "Setup":
				self.putBackOnDeck(self.card_in_play[0]["Back Putter"],0,"Energy changed until played")

			elif self.card_in_play[0].get("Name") == "Setup +":				
				self.putBackOnDeck(self.card_in_play[0]["Back Putter"],0,"Energy changed until played")

			elif self.card_in_play[0].get("Name") == "Terror":
				self.choose_enemy()
				entities.list_of_enemies[self.target].set_vulnerable(self.card_in_play[0]["Vulnerable"])

			elif self.card_in_play[0].get("Name") == "Terror +":
				self.choose_enemy()
				entities.list_of_enemies[self.target].set_vulnerable(self.card_in_play[0]["Vulnerable"])

			elif self.card_in_play[0].get("Name") == "Adrenaline":
				self.gainEnergy(self.card_in_play[0]["Energy Gain"])
				self.draw(self.card_in_play[0]["Draw"])

			elif self.card_in_play[0].get("Name") == "Adrenaline +":
				self.gainEnergy(self.card_in_play[0]["Energy Gain"])
				self.draw(self.card_in_play[0]["Draw"])

			elif self.card_in_play[0].get("Name") == "Alchemize":
				
				onePotionAlchemize = helping_functions.generatePotionRewards(event = True,amount = 1)[0]
				self.add_potion(onePotionAlchemize)
				
			elif self.card_in_play[0].get("Name") == "Alchemize +":
				onePotionAlchemize = helping_functions.generatePotionRewards(event = True,amount = 1)[0]
				self.add_potion(onePotionAlchemize)
				
			elif self.card_in_play[0].get("Name") == "Corpse Explosion":
				self.choose_enemy()
				entities.list_of_enemies[self.target].set_poison(self.card_in_play[0]["Poison"])
				entities.list_of_enemies[self.target].set_corpseExplosion(True)

			elif self.card_in_play[0].get("Name") == "Corpse Explosion +":
				self.choose_enemy()
				entities.list_of_enemies[self.target].set_poison(self.card_in_play[0]["Poison"])
				entities.list_of_enemies[self.target].set_corpseExplosion(True)
				
			elif self.card_in_play[0].get("Name") == "Doppelganger":
				self.energyBoost(self.energy)
				self.set_tempDraw(self.energy)

			elif self.card_in_play[0].get("Name") == "Doppelganger +":
				self.energyBoost(self.energy + 1)
				self.set_tempDraw(self.energy + 1)

			elif self.card_in_play[0].get("Name") == "Malaise":
				self.choose_enemy()
				entities.list_of_enemies[self.target].set_weakness(self.energy)
				entities.list_of_enemies[self.target].set_strength(-self.energy)

			elif self.card_in_play[0].get("Name") == "Malaise +":
				self.choose_enemy()
				entities.list_of_enemies[self.target].set_weakness(self.energy + 1)
				entities.list_of_enemies[self.target].set_strength(-(self.energy +1))

			elif self.card_in_play[0].get("Name") == "Nightmare":
				self.copyCardsForNextTurn(self.card_in_play[0]["Nightmare"])

			elif self.card_in_play[0].get("Name") == "Nightmare":
				self.copyCardsForNextTurn(self.card_in_play[0]["Nightmare"])

			elif self.card_in_play[0].get("Name") == "Phantasmal Killer":
				i = 0
				while i < self.card_in_play[0]["DoubleDamage"]:
					self.doubleDamage.append(turn_counter+1+len(self.doubleDamage))
					i += 1

			elif self.card_in_play[0].get("Name") == "Phantasmal Killer +":
				i = 0
				while i < self.card_in_play[0]["DoubleDamage"]:
					self.doubleDamage.append(turn_counter+1+len(self.doubleDamage))
					i += 1

			elif self.card_in_play[0].get("Name") == "Bullet Time":
				self.set_cantDraw(self.card_in_play[0]["Bullet Time"])				
				for card in self.hand:
					card["This turn Energycost changed"] = True 
					card["Energy"] = 0

			elif self.card_in_play[0].get("Name") == "Bullet Time +":
				self.set_cantDraw(self.card_in_play[0]["Bullet Time"])				
				for card in self.hand:
					card["This turn Energycost changed"] = True 
					card["Energy"] = 0

			elif self.card_in_play[0].get("Name") == "Storm of Steel":
				shiv_draw_power = len(self.hand)
				self.discard(len(self.hand), True)
				i = 0
				while i < shiv_draw_power:
					self.add_CardToHand({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
					i += 1
			
			elif self.card_in_play[0].get("Name") == "Storm of Steel +":
				shiv_draw_power = len(self.hand)
				self.discard(len(self.hand), True)
				i = 0
				while i < shiv_draw_power:
					self.add_CardToHand({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
					i += 1

			elif self.card_in_play[0].get("Name") == "Shiv":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])

			elif self.card_in_play[0].get("Name") == "Shiv +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])

			elif self.card_in_play[0].get("Name") == "Accuracy":
				self.set_accuracy(self.card_in_play[0]["Accuracy"])

			elif self.card_in_play[0].get("Name") == "Accuracy +":
				self.set_accuracy(self.card_in_play[0]["Accuracy"])

			elif self.card_in_play[0].get("Name") == "Caltrops":
				self.set_spikes(self.card_in_play[0]["Spikes"])
			
			elif self.card_in_play[0].get("Name") == "Caltrops +":
				self.set_spikes(self.card_in_play[0]["Spikes"])			

			elif self.card_in_play[0].get("Name") == "Footwork":
				self.set_dexterity(self.card_in_play[0]["Dexterity"])

			elif self.card_in_play[0].get("Name") == "Footwork +":
				self.set_dexterity(self.card_in_play[0]["Dexterity"])

			elif self.card_in_play[0].get("Name") == "Infinite Blades":
				self.set_infiniteBlades(self.card_in_play[0]["Infinite Blades"])

			elif self.card_in_play[0].get("Name") == "Infinite Blades +":
				self.set_infiniteBlades(self.card_in_play[0]["Infinite Blades"])

			elif self.card_in_play[0].get("Name") == "Noxious Fumes":
				self.set_noxiousFumes(self.card_in_play[0]["Noxiousness"])

			elif self.card_in_play[0].get("Name") == "Noxious Fumes +":
				self.set_noxiousFumes(self.card_in_play[0]["Noxiousness"])

			elif self.card_in_play[0].get("Name") == "Well-Laid Plans":
				self.set_wellLaidPlans(self.card_in_play[0]["Well Planed"])
			
			elif self.card_in_play[0].get("Name") == "Well-Laid Plans +":
				self.set_wellLaidPlans(self.card_in_play[0]["Well Planed"])
			
			elif self.card_in_play[0].get("Name") == "A Thousand Cuts":
				self.set_thousandCuts(self.card_in_play[0]["Thousand Cuts"])

			elif self.card_in_play[0].get("Name") == "A Thousand Cuts +":
				self.set_thousandCuts(self.card_in_play[0]["Thousand Cuts"])

			elif self.card_in_play[0].get("Name") == "After Image":
				self.set_afterImage(self.card_in_play[0]["After Image"])

			elif self.card_in_play[0].get("Name") == "After Image +":
				self.set_afterImage(self.card_in_play[0]["After Image"])

			elif self.card_in_play[0].get("Name") == "Envenom":
				self.set_envenom(self.card_in_play[0]["Envenom"])

			elif self.card_in_play[0].get("Name") == "Envenom +":
				self.set_envenom(self.card_in_play[0]["Envenom"])

			elif self.card_in_play[0].get("Name") == "Tools of the Trade":
				self.set_toolsOfTheTrade(self.card_in_play[0]["Tools"])
			
			elif self.card_in_play[0].get("Name") == "Tools of the Trade +":
				self.set_toolsOfTheTrade(self.card_in_play[0]["Tools"])

			elif self.card_in_play[0].get("Name") == "Wraith Form":
				self.set_intangible(self.card_in_play[0]["Intangible"])
				self.set_wraithForm(self.card_in_play[0]["Wraithness"])
			
			elif self.card_in_play[0].get("Name") == "Wraith Form +":
				self.set_intangible(self.card_in_play[0]["Intangible"])
				self.set_wraithForm(self.card_in_play[0]["Wraithness"])

			elif self.card_in_play[0].get("Name") == "Burst":
				preBurst = self.card_in_play[0]["Burst"]

			elif self.card_in_play[0].get("Name") == "Burst +":
				preBurst = self.card_in_play[0]["Burst"]


		elif self.card_in_play[0]["Owner"] == "Colorless":
						
			if self.card_in_play[0].get("Name") == "Bandage Up":
				self.heal(self.card_in_play[0]["Heal"])

			elif self.card_in_play[0].get("Name") == "Bandage Up +":
				self.heal(self.card_in_play[0]["Heal"])

			elif self.card_in_play[0].get("Name") == "Blind":
				self.choose_enemy()
				entities.list_of_enemies[self.target].set_weakness(self.card_in_play[0]["Weakness"])

			elif self.card_in_play[0].get("Name") == "Blind +":
				i = 0
				while i < len(entities.list_of_enemies):
					entities.list_of_enemies[i].set_weakness(self.card_in_play[0]["Weakness"])
					if enemy_check != len(entities.list_of_enemies):
						pass
					else:
						i+=1

			elif self.card_in_play[0].get("Name") == "Dark Shackles":
				self.choose_enemy()
				entities.list_of_enemies[self.target].set_tempStrength(self.card_in_play[0]["Strength Modifier"])
				entities.list_of_enemies[self.target].set_strength(-self.card_in_play[0]["Strength Modifier"])

			elif self.card_in_play[0].get("Name") == "Dark Shackles +":
				self.choose_enemy()
				entities.list_of_enemies[self.target].set_tempStrength(self.card_in_play[0]["Strength Modifier"])
				entities.list_of_enemies[self.target].set_strength(-self.card_in_play[0]["Strength Modifier"])

			
			elif self.card_in_play[0].get("Name") == "Deep Breath":
				self.discardBackInDrawpile()
				self.draw(self.card_in_play[0]["Draw"])

			elif self.card_in_play[0].get("Name") == "Deep Breath +":
				self.discardBackInDrawpile()
				self.draw(self.card_in_play[0]["Draw"])

			elif self.card_in_play[0].get("Name") == "Discovery":
				
				neutral_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == "Colorless"}
				cards = rd.choices(list(neutral_cards.items()),k=3)
				
				three_options = []
				for card in cards:
					card[1]["This turn Energycost changed"] = True
					card[1]["Energy"] = 0
					three_options.append(card[1])

				helping_functions.pickCard(three_options,"Hand")

			elif self.card_in_play[0].get("Name") == "Discovery +":
				
				neutral_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == "Colorless"}
				cards = rd.choices(list(neutral_cards.items()),k=3)
				
				three_options = []
				for card in cards:
					card[1]["This turn Energycost changed"] = True
					card[1]["Energy"] = 0
					three_options.append(card[1])

				helping_functions.pickCard(three_options,"Hand")

			elif self.card_in_play[0].get("Name") == "Dramatic Entrance":
				i = 0
				while i < len(entities.list_of_enemies):					
					enemy_check = len(entities.list_of_enemies)
					self.target = i
					self.attack(self.card_in_play[0]["Damage"])					
					if enemy_check != len(entities.list_of_enemies):
						pass
					else:
						i+=1

			elif self.card_in_play[0].get("Name") == "Dramatic Entrance +":
				i = 0
				while i < len(entities.list_of_enemies):
					enemy_check = len(entities.list_of_enemies)
					self.target = i
					self.attack(self.card_in_play[0]["Damage"])
					if enemy_check != len(entities.list_of_enemies):
						pass
					else:
						i+=1

			elif self.card_in_play[0].get("Name") == "Enlightenment":
				for card in self.hand:
					if card["Energy"] > 0:
						card["This turn Energycost changed"] = True
						card["Energy"] = 1

			
			elif self.card_in_play[0].get("Name") == "Enlightenment +":
				for card in self.hand:
					if card["Energy"] > 0:
						card["Energy changed for the battle"] = True
						card["Energy"] = 1	

			elif self.card_in_play[0].get("Name") == "Finesse":
				self.blocking(self.card_in_play[0]["Block"])
				self.draw(self.card_in_play[0]["Draw"])

			elif self.card_in_play[0].get("Name") == "Finesse +":
				self.blocking(self.card_in_play[0]["Block"])
				self.draw(self.card_in_play[0]["Draw"])

			elif self.card_in_play[0].get("Name") == "Flash of Steel":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				self.draw(self.card_in_play[0]["Draw"])

			elif self.card_in_play[0].get("Name") == "Flash of Steel +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				self.draw(self.card_in_play[0]["Draw"])
			
			elif self.card_in_play[0].get("Name") == "Forethought":

				self.putBackOnDeck(self.card_in_play[0]["Back Putter"],self.card_in_play[0]["Energy Change"],self.card_in_play[0]["Energy Change Type"],bottom = True)
			
			elif self.card_in_play[0].get("Name") == "Forethought +":

				self.putBackOnDeck(len(self.hand),self.card_in_play[0]["Energy Change"],self.card_in_play[0]["Energy Change Type"],bottom = True)

			elif self.card_in_play[0].get("Name") == "Good Instincts":
				self.blocking(self.card_in_play[0]["Block"])

			elif self.card_in_play[0].get("Name") == "Good Instincts +":
				self.blocking(self.card_in_play[0]["Block"])	

			elif self.card_in_play[0].get("Name") == "Impatience":
				attackCheck = [card for card in self.hand if card["Type"] == "Attack"]
				if len(attackCheck) == 0:
					self.draw(self.card_in_play[0]["Draw"])				
				else:
					print("This card is only playable if you have no attack cards in hand.")
					self.hand.append(self.card_in_play.pop(0))
					return

			elif self.card_in_play[0].get("Name") == "Impatience +":
				attackCheck = [card for card in self.hand if card["Type"] == "Attack"]
				if len(attackCheck) == 0:
					self.draw(self.card_in_play[0]["Draw"])				
				else:
					print("This card is only playable if you have no attack cards in hand.")
					self.hand.append(self.card_in_play.pop(0))
					return
			
			elif self.card_in_play[0].get("Name") == "Jack of All Trades":
				neutral_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == "Colorless"}
				card = rd.choices(list(neutral_cards.items()))[0][1]
				card["This turn Energycost changed"] = True
				card["Energy"] = 0
				self.add_CardToHand(card)

			elif self.card_in_play[0].get("Name") == "Jack of All Trades +":
				i = 0
				while i < 2:
					neutral_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == "Colorless"}
					card = rd.choices(list(neutral_cards.items()))[0][1]					
					card["This turn Energycost changed"] = True
					card["Energy"] = 0
					self.add_CardToHand(card)
					i+=1

			elif self.card_in_play[0].get("Name") == "Madness":
				if len(self.hand) > 0:
					indexOfRandomCardInHand = rd.randint(0,len(self.hand)-1)
					self.hand[indexOfRandomCardInHand]["Energy changed for the battle"] = True
					self.hand[indexOfRandomCardInHand]["Energy"] = 0
					ansiprint("<blue>"+self.hand[indexOfRandomCardInHand]["Name"]+"</blue>","now costs 0 <yellow>Energy</yellow> for the rest of the battle.")
				else:
					print("You have no cards left in your hand.")		

			elif self.card_in_play[0].get("Name") == "Madness +":
				if len(self.hand) > 0:
					indexOfRandomCardInHand = rd.randint(0,len(self.hand)-1)
					self.hand[indexOfRandomCardInHand]["Energy changed for the battle"] = True
					self.hand[indexOfRandomCardInHand]["Energy"] = 0
					ansiprint("<blue>"+self.hand[indexOfRandomCardInHand]["Name"]+"</blue>","now costs 0 <yellow>Energy</yellow> for the rest of the battle.")
				else:
					print("You have no cards left in your hand.")

			elif self.card_in_play[0].get("Name") == "Mind Blast":
				self.choose_enemy()
				self.attack(len(self.draw_pile))

			elif self.card_in_play[0].get("Name") == "Mind Blast +":
				self.choose_enemy()
				self.attack(len(self.draw_pile))

			elif self.card_in_play[0].get("Name") == "Panacea":
				self.set_artifact(self.card_in_play[0]["Artifact"])

			elif self.card_in_play[0].get("Name") == "Panacea +":
				self.set_artifact(self.card_in_play[0]["Artifact"])

			elif self.card_in_play[0].get("Name") == "Panic Button":
				self.blocking(self.card_in_play[0]["Block"])
				self.set_noBlock(2)

			elif self.card_in_play[0].get("Name") == "Panic Button +":
				self.blocking(self.card_in_play[0]["Block"])
				self.set_noBlock(2)

			elif self.card_in_play[0].get("Name") == "Purify":				
				i = 0
				self.showHand()
				while i < self.card_in_play[0]["Exhausting"]:
					snap = input("Do you want to exhaust another card? (Yes/No)")
					if snap == "Yes":

						self.exhaust(1)
						i += 1
					elif snap == "No":
						break
					else:
						print("Please type Yes or No.")
						self.explainer_function(snap,answer=False)

			elif self.card_in_play[0].get("Name") == "Purify +":				
				i = 0
				self.showHand()
				while i < self.card_in_play[0]["Exhausting"]:
					snap = input("Do you want to exhaust another card? (Yes/No)")
					if snap == "Yes":
						self.exhaust(1)
						i += 1
					elif snap == "No":
						break
					else:
						self.explainer_function(snap,answer=False)
						print("Please type Yes or No.")

			elif self.card_in_play[0].get("Name") == "Swift Strike":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])

			elif self.card_in_play[0].get("Name") == "Swift Strike +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])

			elif self.card_in_play[0].get("Name") == "Trip":
				self.choose_enemy()
				entities.list_of_enemies[self.target].set_vulnerable(self.card_in_play[0]["Vulnerable"])

			elif self.card_in_play[0].get("Name") == "Trip +":
				i = 0
				while i < len(entities.list_of_enemies):
					entities.list_of_enemies[i].set_weakness(self.card_in_play[0]["Weakness"])
					if enemy_check != len(entities.list_of_enemies):
						pass
					else:
						i+=1

			elif self.card_in_play[0].get("Name") == "Apotheosis":
				i = 0
				while i < len(self.hand):
					if self.hand[i].get("Type") != "Status" and self.hand[i].get("Type") != "Curse" and self.hand[i].get("Upgrade") == None:
						helping_functions.upgradeCard(self.hand.pop(i),"Hand",index = i)
					
					i+=1
				
				i = 0
				while i < len(self.draw_pile):
					if self.draw_pile[i].get("Type") != "Status" and self.draw_pile[i].get("Type") != "Curse" and self.draw_pile[i].get("Upgrade") == None:
						helping_functions.upgradeCard(self.draw_pile.pop(i),"Drawpile",index = i)
					
					i+=1	

				i = 0
				while i < len(self.discard_pile):
					if self.discard_pile[i].get("Type") != "Status" and self.discard_pile[i].get("Type") != "Curse" and self.discard_pile[i].get("Upgrade") == None:
						helping_functions.upgradeCard(self.discard_pile.pop(i),"Discardpile",index = i)
					
					i+=1

				i = 0
				while i < len(self.exhaust_pile):
					if self.exhaust_pile[i].get("Type") != "Status" and self.exhaust_pile[i].get("Type") != "Curse" and self.exhaust_pile[i].get("Upgrade") == None:
						helping_functions.upgradeCard(self.exhaust_pile.pop(i),"Exhaustpile",index = i)
					
					i+=1
			
			elif self.card_in_play[0].get("Name") == "Apotheosis +":
				i = 0
				while i < len(self.hand):
					if self.hand[i].get("Type") != "Status" and self.hand[i].get("Type") != "Curse" and self.hand[i].get("Upgrade") == None:
						helping_functions.upgradeCard(self.hand.pop(i),"Hand",index = i)
					
					i+=1
				
				i = 0
				while i < len(self.draw_pile):
					if self.draw_pile[i].get("Type") != "Status" and self.draw_pile[i].get("Type") != "Curse" and self.draw_pile[i].get("Upgrade") == None:
						helping_functions.upgradeCard(self.draw_pile.pop(i),"Drawpile",index = i)
					
					i+=1	

				i = 0
				while i < len(self.discard_pile):
					if self.discard_pile[i].get("Type") != "Status" and self.discard_pile[i].get("Type") != "Curse" and self.discard_pile[i].get("Upgrade") == None:
						helping_functions.upgradeCard(self.discard_pile.pop(i),"Discardpile",index = i)
					
					i+=1

				i = 0
				while i < len(self.exhaust_pile):
					if self.exhaust_pile[i].get("Type") != "Status" and self.exhaust_pile[i].get("Type") != "Curse" and self.exhaust_pile[i].get("Upgrade") == None:
						helping_functions.upgradeCard(self.exhaust_pile.pop(i),"Exhaustpile",index = i)
					
					i+=1

			elif self.card_in_play[0].get("Name") == "Chrysalis":
				while i < self.card_in_play[0]["Cards"]:
					skill_cards = {k:v for k,v in entities.cards.items() if v.get("Type") == "Skill" and v.get("Owner") == self.name and v.get("Rarity") != "Basic"}
					#create a list of banned cards and exclude them from this pool via "not in list"
					card = rd.choices(list(skill_cards.items()))[0][1]
					card["Energy changed for the battle"] = True
					card["Energy"] = 0
					self.add_CardToDrawpile(card)
					i += 1
			
			elif self.card_in_play[0].get("Name") == "Chrysalis +":
				while i < self.card_in_play[0]["Cards"]:
					skill_cards = {k:v for k,v in entities.cards.items() if v.get("Type") == "Skill" and v.get("Owner") == self.name and v.get("Rarity") != "Basic"}
					#create a list of banned cards and exclude them from this pool via "not in list"
					card = rd.choices(list(skill_cards.items()))[0][1]
					card["Energy changed for the battle"] = True
					card["Energy"] = 0
					self.add_CardToDrawpile(card)
					i += 1

			elif self.card_in_play[0].get("Name") == "Metamorphosis":
				while i < self.card_in_play[0]["Cards"]:
					attack_cards = {k:v for k,v in entities.cards.items() if v.get("Type") == "Attack" and v.get("Owner") == self.name and v.get("Rarity") != "Basic"}
					card = rd.choices(list(skill_cards.items()))[0][1]					
					card["Energy changed for the battle"] = True
					card["Energy"] = 0
					self.add_CardToDrawpile(card)
					i += 1

			elif self.card_in_play[0].get("Name") == "Metamorphosis +":
				while i < self.card_in_play[0]["Cards"]:
					attack_cards = {k:v for k,v in entities.cards.items() if v.get("Type") == "Attack" and v.get("Owner") == self.name and v.get("Rarity") != "Basic"}
					card = rd.choices(list(skill_cards.items()))[0][1]					
					card["Energy changed for the battle"] = True
					card["Energy"] = 0
					self.add_CardToDrawpile(card)
					i += 1

			elif self.card_in_play[0].get("Name") == "Swift Strike":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
			
			elif self.card_in_play[0].get("Name") == "Swift Strike +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])

			elif self.card_in_play[0].get("Name") == "Hand of Greed":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				if len(entities.list_of_enemies) < enemy_check:
					self.set_gold(self.card_in_play[0]["Gold"])
			
			elif self.card_in_play[0].get("Name") == "Hand of Greed +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				if len(entities.list_of_enemies) < enemy_check:
					self.set_gold(self.card_in_play[0]["Gold"])

			elif self.card_in_play[0].get("Name") == "Magnetism":
				self.set_magnetism(1)
			
			elif self.card_in_play[0].get("Name") == "Magnetism +":
				self.set_magnetism(1)

			elif self.card_in_play[0].get("Name") == "Master of Strategy":				
				self.draw(self.card_in_play[0]["Draw"])
			
			elif self.card_in_play[0].get("Name") == "Master of Strategy +":				
				self.draw(self.card_in_play[0]["Draw"])
			
			elif self.card_in_play[0].get("Name") == "Mayhem":				
				self.set_mayhem(1)
			
			elif self.card_in_play[0].get("Name") == "Mayhem +":
				self.set_mayhem(1)

			elif self.card_in_play[0].get("Name") == "Panache":
				self.set_panache(self.card_in_play[0]["Damage"])
			
			elif self.card_in_play[0].get("Name") == "Panache +":
				self.set_panache(self.card_in_play[0]["Damage"])

			elif self.card_in_play[0].get("Name") == "Secret Technique":
				self.draw_specific_cards_from_place(self.card_in_play[0]["Draw"],self.card_in_play[0]["Place"],self.card_in_play[0]["Typing"])
			
			elif self.card_in_play[0].get("Name") == "Secret Technique +":
				self.draw_specific_cards_from_place(self.card_in_play[0]["Draw"],self.card_in_play[0]["Place"],self.card_in_play[0]["Typing"])			

			elif self.card_in_play[0].get("Name") == "Secret Weapon":
				self.draw_specific_cards_from_place(self.card_in_play[0]["Draw"],self.card_in_play[0]["Place"],self.card_in_play[0]["Typing"])

			elif self.card_in_play[0].get("Name") == "Secret Weapon +":
				self.draw_specific_cards_from_place(self.card_in_play[0]["Draw"],self.card_in_play[0]["Place"],self.card_in_play[0]["Typing"])		
			

			elif self.card_in_play[0].get("Name") == "The Bomb":
				self.set_theBomb(self.card_in_play[0]["Damage"],turn_counter)
			
			elif self.card_in_play[0].get("Name") == "The Bomb +":
				self.set_theBomb(self.card_in_play[0]["Damage"],turn_counter)

			elif self.card_in_play[0].get("Name") == "Transmutation":
				neutral_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == "Colorless"}
				while i < self.energy:
					card = rd.choices(list(neutral_cards.items()))[0][1]
					card["This turn Energycost changed"] = True
					card["Energy"] = 0
					self.add_CardToHand(card)
					i += 1

			elif self.card_in_play[0].get("Name") == "Transmutation +":
				neutral_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == "Colorless" and v.get("Upgraded") == True}
				while i < self.energy:
					card = rd.choices(list(neutral_cards.items()))[0][1]
					card["This turn Energycost changed"] = True
					card["Energy"] = 0
					self.add_CardToHand(card)
					i += 1

			elif self.card_in_play[0].get("Name") == "Violence":				
				self.draw_specific_cards_from_place(self.card_in_play[0]["Draw"],self.card_in_play[0]["Place"],self.card_in_play[0]["Typing"],random = True)
			
			elif self.card_in_play[0].get("Name") == "Violence +":	
				self.draw_specific_cards_from_place(self.card_in_play[0]["Draw"],self.card_in_play[0]["Place"],self.card_in_play[0]["Typing"],random = True)
			
			elif self.card_in_play[0].get("Name") == "Thinking Ahead":
				self.draw(self.card_in_play[0]["Draw"])
				self.putBackOnDeck(self.card_in_play[0]["Back Putter"],bottom = True)
			
			elif self.card_in_play[0].get("Name") == "Thinking Ahead +":
				self.draw(self.card_in_play[0]["Draw"])
				self.putBackOnDeck(self.card_in_play[0]["Back Putter"],bottom = True)

			elif self.card_in_play[0].get("Name") == "Apparition":
				self.set_intangible(self.card_in_play[0]["Intangible"])
			
			elif self.card_in_play[0].get("Name") == "Apparition +":
				self.set_intangible(self.card_in_play[0]["Intangible"])

			elif self.card_in_play[0].get("Name") == "Ritual Dagger":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				if enemy_check != len(entities.list_of_enemies):
					for card in self.deck:
						if card.get("Unique ID") == self.card_in_play[0].get("Unique ID"):
							card["Damage"] += self.card_in_play[0]["FatalBonus"]
							self.card_in_play[0]["Damage"] += self.card_in_play[0]["FatalBonus"]
											
			elif self.card_in_play[0].get("Name") == "Ritual Dagger +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				if enemy_check != len(entities.list_of_enemies):
					for card in self.deck:
						if card.get("Unique ID") == self.card_in_play[0].get("Unique ID"):
							card["Damage"] += self.card_in_play[0]["FatalBonus"]
							self.card_in_play[0]["Damage"] += self.card_in_play[0]["FatalBonus"]

			elif self.card_in_play[0].get("Name") == "JAX":
				self.receive_recoil_damage(-self.card_in_play[0].get("Harm"),directDamage=True)
				self.set_strength(self.card_in_play[0].get("Strength"))
				
			elif self.card_in_play[0].get("Name") == "JAX +":
				self.receive_recoil_damage(-self.card_in_play[0].get("Harm"),directDamage=True)
				self.set_strength(self.card_in_play[0].get("Strength"))

			elif self.card_in_play[0].get("Name") == "Bite":				

				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				self.heal(self.card_in_play[0]["Heal"])

			elif self.card_in_play[0].get("Name") == "Bite +":
				self.choose_enemy()
				self.attack(self.card_in_play[0]["Damage"])
				self.heal(self.card_in_play[0]["Heal"])

			else:
				print(self.card_in_play[0].get("Name"),"<--- this card is not implemented. Snap Snap Snap.")
		

		elif self.card_in_play[0].get("Type") == "Curse":
			ansiprint("<m>"+self.card_in_play[0].get("Name")+"</m> is exhausted and is removed from play because of Blue Candle!")
			self.add_CardToExhaustpile(self.card_in_play.pop(0))
			self.receive_recoil_damage(-1,directDamage=True)

		elif self.card_in_play[0].get("Type") == "Status" and self.card_in_play[0].get("Name") != "Slimed":
			ansiprint("<black>"+self.card_in_play[0].get("Name")+"</black> is exhausted and is removed from play because of <light-red>Medical Kit</light-red>!")
			self.add_CardToExhaustpile(self.card_in_play.pop(0))
		
		elif self.card_in_play[0].get("Name") == "Slimed":
			ansiprint("You are no longer slimed.")

		else:
			print("This is a weird card",self.card_in_play[0])


		if len(self.card_in_play) > 0:

			self.check_CardPlayPenalties()

			if self.card_in_play[0].get("Type") == "Attack":
				self.set_attackCounter()

			elif self.card_in_play[0].get("Type") == "Skill":
				self.set_skillCounter()
			
			elif self.card_in_play[0].get("Type") == "Power":
				self.set_powerCounter()

			self.set_cardCounter()

			if not repeat and self.card_in_play[0].get("Type") != "Curse" and self.card_in_play[0].get("Type") != "Status":
				self.reduce_energy()

			if self.afterImage > 0:
				self.blocking(self.afterImage,unaffectedBlock= True)

			if self.thousandCuts > 0:
				i = 0
				while i < len(entities.list_of_enemies):
					
					self.target = i
					entities.list_of_enemies[i].receive_recoil_damage(self.thousandCuts)
					if enemy_check > len(entities.list_of_enemies):
						pass
					else:
						i+=1
					
				ansiprint("A Thousand Cuts did this!")

			for enemy in entities.list_of_enemies:
				enemy.cardTypeCheck(self.card_in_play[0]["Type"])
				if enemy.choke > 0:
					enemy.receive_recoil_damage(enemy.choke)

			if not repeat:
				
				if self.burst > 0 and self.card_in_play[0].get("Type") == "Skill":
					self.burst -= 1
					self.randomTarget = 1
					self.card_is_played(self.card_in_play[0],turn_counter,repeat=True)
				
				elif self.necronomicon > 0 and self.card_in_play[0].get("Energy") >= 2:
					self.necronomicon = 0
					self.randomTarget = 1
					self.card_is_played(self.card_in_play[0],turn_counter,repeat=True)

				elif self.duplication > 0 and self.card_in_play[0].get("Type") != "Curse" and self.card_in_play[0].get("Type") != "Status":
					self.duplication -= 1
					self.randomTarget = 1
					self.card_is_played(self.card_in_play[0],turn_counter,repeat=True)

				else:

					if self.card_in_play[0].get("Exhaust") == True:
						
						self.add_CardToExhaustpile(self.card_in_play.pop(0))
					
					elif self.card_in_play[0].get("Type") == "Power":
						self.power_pile.append(self.card_in_play.pop(0))
						

					else:
	
						self.add_CardToDiscardpile(self.card_in_play.pop(0),noMessage=True)
			


			enemy_check = len(entities.list_of_enemies)

			if self.panache > 0 and self.card_counter % 5 == 0:
				i = 0
				while i < len(entities.list_of_enemies):
					
					self.target = i
					entities.list_of_enemies[i].receive_recoil_damage(self.panache)
					
					if enemy_check > len(entities.list_of_enemies):
						pass
					else:
						i+=1


			#this happens after the card has been exhausted so the first burst doesn't duplicate itself.
			try:
				if preBurst > 0:
					self.set_burst(preBurst)
					preBurst = 0
			except Exception as e:

				pass

			if repeat:
				self.randomTarget = 0

	def play_potion(self,turn_counter):
		
		self.showPotions(skip=True)
		potion_index = 0
		potion_in_play = []

		if len(self.potionBag) == 0:
			ansiprint("You don't have any <c>Potions</c> in your <c>Potion Bag</c>.")
			return
		
		while True:
			try:
				ansiprint("Pick the number of the <c>Potion</c> you want to play\n")
				potion_index = input("")
				potion_index = int(potion_index)-1
				if potion_index == len(self.potionBag):
					return
				
				if potion_index in range(len(self.potionBag)):
					
					if self.potionBag[potion_index]["Name"] == "Fairy in a Bottle":
						ansiprint("<c>Fairy in a Bottle</c> can't be played. It will revive you automatically if you died. I hope.")
						return
					elif self.potionBag[potion_index]["Name"] == "Smoke Bomb" and self.get_floor() == "Boss":
						ansiprint("<c>Smoke Bomb</c> can't be played during <black>Bossfigts</black>!")
						return
					else:
						break

				else:
					ansiprint ("You don't have this <c>Potion</c>!")
					pass

			except Exception as e:
				self.explainer_function(potion_index)
				ansiprint ("Try again! Type one of the corresponding numbers! play_potion")
				pass
		
		if len(entities.list_of_enemies) == 0 and self.potionBag[potion_index]["Name"] != "Blood Potion" and self.potionBag[potion_index]["Name"] != "Fruit Juice" and self.potionBag[potion_index]["Name"] != "Entropic Brew":
			ansiprint("You don't have any <c>Potions</c> that you can play right now.")
			return


		for relic in self.relics:
			if relic.get("Name") == "Toy Ornithopter":
				self.heal(5)

		self.potion_is_played(self.potionBag.pop(potion_index),turn_counter)
	
	def potion_is_played(self,potion,turn_counter):
		sacredBark = False
		for relic in self.relics:
			if relic.get("Name") == "Sacred Bark":
				sacredBark = True

		potion_in_play = []
		potion_in_play.append(potion)

		if potion_in_play[0]["Name"] == "Ancient Potion":
			self.set_artifact(potion_in_play[0]["Potion Yield"])
			if sacredBark:
				self.set_artifact(potion_in_play[0]["Potion Yield"])


		elif potion_in_play[0]["Name"] == "Attack Potion":
				attack_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == self.name and v.get("Type") == "Attack" and "+" not in v.get("Name")}
				cards = rd.choices(list(attack_cards.items()),k=3)
				
				three_options = []
				for card in cards:
					three_options.append(card[1])

				i = 0
				print("") #just for readability
				for card in three_options:
					i += 1
					card["This turn Energycost changed"] = True
					card["Energy"] = 0
					
				
				helping_functions.pickCard(three_options,"Hand")


		elif potion_in_play[0]["Name"] == "Blessing of the Forge":
			i = 0
			while i < len(self.hand):
				if self.hand[i].get("Type") != "Status" and self.hand[i].get("Type") != "Curse" and self.hand[i].get("Upgraded") != True:
					helping_functions.upgradeCard(self.hand.pop(i),"Hand",i)
				else:
					i+=1
				
		elif potion_in_play[0]["Name"] == "Block Potion":
			self.blocking(potion_in_play[0]["Potion Yield"])
			if sacredBark:
				self.blocking(potion_in_play[0]["Potion Yield"])

		elif potion_in_play[0]["Name"] == "Blood Potion":
			if sacredBark:
				twentyPercent = math.floor((self.max_health/100)*40)
			else:
				twentyPercent = math.floor((self.max_health/100)*20)
			
			self.heal(twentyPercent)

		elif potion_in_play[0]["Name"] == "Colorless Potion":
			colorless_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == "Colorless" and v.get("Rarity") != "Special" and "+" not in v.get("Name")}
			cards = rd.choices(list(colorless_cards.items()),k=3)
			
			three_options = []
			for card in cards:
				three_options.append(card[1])

			i = 0
			print("") #just for readability
			for card in three_options:
				i += 1
				card["This turn Energycost changed"] = True
				card["Energy"] = 0
				
			
			helping_functions.pickCard(three_options,"Hand")


		elif potion_in_play[0]["Name"] == "Cultist Potion": 
			self.set_ritual(potion_in_play[0]["Potion Yield"])
			if sacredBark:
				self.set_ritual(potion_in_play[0]["Potion Yield"])

		elif potion_in_play[0]["Name"] == "Cunning Potion": 
			if sacredBark:
				shivs = potion_in_play[0]["Potion Yield"]*2
			else:
				shivs = potion_in_play[0]["Potion Yield"]

			i = 0
			while i < shivs:
				self.add_CardToHand({"Name":"Shiv +","Energy":0,"Damage":6,"Exhaust":True,"Type":"Attack","Upgraded": True,"Rarity": "Common","Owner":"Silent"})
				i+=1
	
		elif potion_in_play[0]["Name"] == "Dexterity Potion":
			self.set_dexterity(potion_in_play[0]["Potion Yield"])
			if sacredBark:
				self.set_dexterity(potion_in_play[0]["Potion Yield"])
		
		elif potion_in_play[0]["Name"] == "Strength Potion": 
			self.set_strength(potion_in_play[0]["Potion Yield"])
			if sacredBark:
				self.set_strength(potion_in_play[0]["Potion Yield"])

		elif potion_in_play[0]["Name"] == "Distilled Chaos": 
			if sacredBark:
				cardsFromTheTop = potion_in_play[0]["Potion Yield"]*2
			else:
				cardsFromTheTop = potion_in_play[0]["Potion Yield"]

			i = 0
			while i < cardsFromTheTop:
				if len(self.draw_pile) == 0:
					self.discardBackInDrawpile()
				if len(self.draw_pile) == 0:
					anisprint("Your Discardpile and your Drawpile are empty.")
					break
				else:
					self.draw_pile[0]["Energy changed until played"] = True
					self.draw_pile[0]["Energy"] = 0

					self.card_is_played(self.draw_pile.pop(0),turn_counter)
					i += 1


		elif potion_in_play[0]["Name"] == "Duplication Potion":
			self.set_duplication(potion_in_play[0]["Potion Yield"])
			if sacredBark:
				self.set_duplication(potion_in_play[0]["Potion Yield"])

		elif potion_in_play[0]["Name"] == "Energy Potion": 
			self.gainEnergy(potion_in_play[0]["Potion Yield"])
			if sacredBark:
				self.gainEnergy(potion_in_play[0]["Potion Yield"])
    	
		elif potion_in_play[0]["Name"] == "Entropic Brew": 
			snapPotions = helping_functions.generatePotionRewards(event=True, amount= self.potionBagSize - len(self.potionBag))
			i = 0
			while i < self.potionBagSize:
				self.add_potion(snapPotions.pop(0))
				i += 1
		
		elif potion_in_play[0]["Name"] == "Essence of Steel":
			self.set_platedArmor(potion_in_play[0]["Potion Yield"])
			if sacredBark:
				self.set_platedArmor(potion_in_play[0]["Potion Yield"])
		
		elif potion_in_play[0]["Name"] == "Explosive Potion":
			i = 0
			if sacredBark:
				damage = potion_in_play[0]["Potion Yield"]*2
			else:
				damage = potion_in_play[0]["Potion Yield"]


			enemy_check = len(entities.list_of_enemies)
			while i < len(entities.list_of_enemies):
				entities.list_of_enemies[i].receive_recoil_damage(damage)
				if enemy_check != len(entities.list_of_enemies):
					pass
				else:
					i+=1
    		
		elif potion_in_play[0]["Name"] == "Fear Potion": 
			self.choose_enemy()
			if sacredBark:
				fear = potion_in_play[0]["Potion Yield"]*2
			else:
				fear = potion_in_play[0]["Potion Yield"]


			entities.list_of_enemies[self.target].set_vulnerable(fear)
			
		elif potion_in_play[0]["Name"] == "Fire Potion": 
			self.choose_enemy()
			if sacredBark:
				damage = potion_in_play[0]["Potion Yield"]*2
			else:
				damage = potion_in_play[0]["Potion Yield"]
			entities.list_of_enemies[self.target].receive_recoil_damage(damage)
		
		elif potion_in_play[0]["Name"] == "Fruit Juice": 
			self.set_maxHealth(potion_in_play[0]["Potion Yield"])
			if sacredBark:
				self.set_maxHealth(potion_in_play[0]["Potion Yield"])
		
		elif potion_in_play[0]["Name"] == "Gamblers Brew":
			i = 0
			yesNo = ["Yes","No"]
			handLength = len(self.hand)
			while i < handLength:
				check = input("Do you want to discard cards?(Yes/No) You draw as many as you discard.")
				
				while check not in yesNo:
					self.explainer_function(check,answer=False)
					check = input("Do you want to discard another card.(Yes/No)")	
				
				if check == "Yes":
					self.discard(1)
					i+=1
				elif check == "No":
					break
				else:
					print(check,"<--- How's that not Yes or No?")
			
			self.draw(i)

		elif potion_in_play[0]["Name"] == "Ghost in a Jar":
			self.set_intangible(potion_in_play[0]["Potion Yield"])
			if sacredBark:
				self.set_intangible(potion_in_play[0]["Potion Yield"])
		
		elif potion_in_play[0]["Name"] == "Liquid Bronze": 
			self.set_spikes(potion_in_play[0]["Potion Yield"])
			if sacredBark:
				self.set_spikes(potion_in_play[0]["Potion Yield"])
		
		elif potion_in_play[0]["Name"] == "Liquid Memories":
			handCheck = len(self.hand)
			self.draw_specific_cards_from_place(amount = 1,place = "Discardpile")
			if handCheck < len(self.hand):
				self.hand[-1]["This turn Energycost changed"] = True
				self.hand[-1]["Energy"] = 0

			if sacredBark:
				handCheck = len(self.hand)
				self.draw_specific_cards_from_place(amount = 1,place = "Discardpile")
				if handCheck > len(self.hand):
					self.hand[-1]["This turn Energycost changed"] = True
					self.hand[-1]["Energy"] = 0

		elif potion_in_play[0]["Name"] == "Poison Potion": 
			self.choose_enemy()
			if sacredBark:
				poison = potion_in_play[0]["Potion Yield"]*2
			else:
				poison = potion_in_play[0]["Potion Yield"]

			entities.list_of_enemies[self.target].set_poison(poison)
		
		elif potion_in_play[0]["Name"] == "Power Potion": 

			power_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == self.name and v.get("Type") == "Power" and "+" not in v.get("Name")}
			cards = rd.choices(list(power_cards.items()),k=3)
			
			three_options = []
			for card in cards:
				three_options.append(card[1])

			i = 0
			print("") #just for readability
			for card in three_options:
				i += 1
				card["This turn Energycost changed"] = True
				card["Energy"] = 0
			
			helping_functions.pickCard(three_options,"Hand")


		elif potion_in_play[0]["Name"] == "Regen Potion": 
			self.set_regen(potion_in_play[0]["Potion Yield"])
			if sacredBark:
				self.set_regen(potion_in_play[0]["Potion Yield"])

		elif potion_in_play[0]["Name"] == "Skill Potion": 
			skill_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == self.name and v.get("Type") == "Skill" and "+" not in v.get("Name")}
			cards = rd.choices(list(skill_cards.items()),k=3)
			
			three_options = []
			for card in cards:
				three_options.append(card[1])

			i = 0
			print("") #just for readability
			for card in three_options:
				i += 1
				card["This turn Energycost changed"] = True
				card["Energy"] = 0
				
			
			helping_functions.pickCard(three_options,"Hand")
		
		elif potion_in_play[0]["Name"] == "Smoke Bomb":
			if self.get_floor() != "Boss":
				self.smokeBomb = True
				entities.list_of_enemies = []
				ansiprint("You threw the <c>Smoke Bomb</c> on the floor and ran away!")
			else:
				ansiprint("You can't run away from <black>Boss</black> Fights!")
				self.potionBag.append(self.potion_in_play.pop(0))

		elif potion_in_play[0]["Name"] == "Snecko Oil": 
			self.draw(potion_in_play[0]["Potion Yield"])
			if sacredBark:
				self.draw(potion_in_play[0]["Potion Yield"])
			for card in self.hand:
				card["Energy changed for the battle"] = True
				card["Energy"] = rd.randint(0,3)

		elif potion_in_play[0]["Name"] == "Speed Potion":
			if sacredBark:
				dexterity = potion_in_play[0]["Potion Yield"]*2
			else:
				dexterity = potion_in_play[0]["Potion Yield"]

			self.set_dexterityDecrease(dexterity)
			self.set_dexterity(dexterity)
			


		elif potion_in_play[0]["Name"] == "Flex Potion": 
			if sacredBark:
				strength = potion_in_play[0]["Potion Yield"]*2
			else:
				strength = potion_in_play[0]["Potion Yield"]

			self.set_strengthDecrease(strength)
			self.set_strength(strength)

		elif potion_in_play[0]["Name"] == "Swift Potion":
			self.draw(potion_in_play[0]["Potion Yield"])
			if sacredBark:
				self.draw(potion_in_play[0]["Potion Yield"])
		
		elif potion_in_play[0]["Name"] == "Weak Potion": 
			self.choose_enemy()
			if sacredBark:
				weak = potion_in_play[0]["Potion Yield"]*2
			else:
				weak = potion_in_play[0]["Potion Yield"]
			entities.list_of_enemies[self.target].set_weakness(weak)

		else:
			print(potion_in_play[0]["Name"],"forgot to implement this potion... You may have 1 Gold for it.")
			self.set_gold(1)
	
	def reset(self):
		self.block = 0
		self.discard_counter = 0
		self.temp_energy = 0
		self.tempDraw = 0
		self.blockNextTurn = 0
		
		self.burst = 0
		
		self.attack_counter = 0
		self.skill_counter = 0
		self.power_counter = 0

		self.card_counter = 0

		if self.dontLoseBlock > 0:
			self.dontLoseBlock -= 1
		self.tempSpikes = 0

		if self.intangible > 0:
			self.intangible -= 1

	def draw_specific_cards_from_place(self,amount,place,typeOfCard = None,random = False):
		
		if place == "Drawpile":
			if len(self.draw_pile) == 0:
				print("The drawpile is currently empty.")
				return
			i = 0
			while i < amount:	
				try:
					if random:
						card_index = rd.randint(0,len(self.draw_pile)-1)
					else:
						self.show_drawpile()
						card_index = input("Which card do you want to draw?\n")
						card_index = int(card_index)-1
					if card_index in range(len(self.draw_pile)):
						if typeOfCard == None:

							if len(self.hand) > 9:
								ansiprint(self.displayName,"has 10 or more cards in hand. <blue>"+ self.draw_pile[card_index]["Name"]+"<blue/>","is now in the discardpile.")
								self.discard_pile.append(self.draw_pile.pop(card_index))

							else:
								self.hand.append(self.draw_pile.pop(card_index))

							i += 1
						
						else:
							
							typeCheck = [card for card in self.draw_pile if card["Type"] == typeOfCard]
							
							if len(typeCheck) == 0:
								print("You don't have any",typeOfCard,"cards in your drawpile.")
								break
							
							if self.draw_pile[card_index]["Type"] != typeOfCard:
								if not random:
									ansiprint("You need to choose a",typeOfCard,"card!")
								continue
							
							else:
								if len(self.hand) > 9:
									ansiprint(self.displayName,"has 10 or more cards in hand. <blue>"+ self.draw_pile[card_index]["Name"]+"<blue/>","is now in the discardpile.")
									self.add_CardToDiscardpile(self.draw_pile.pop(card_index))

								else:
									self.add_CardToHand(self.draw_pile.pop(card_index))
								i += 1
					
				except Exception as e:
					self.explainer_function(card_index)
					print("You need to type a corresponding number. This is one of the more... fragile functions so just in case here is the error: draw_specific_cards_from_place",e)
		
		elif place == "Discardpile":
			i = 0
			if len(self.discard_pile) == 0:
				print("The Discardpile is currently empty.")
				return
			while i < amount:
				
				try:
					if random:
						card_index = rd.randint(0,len(self.discard_pile)-1)
					else:
						self.show_discardpile()
						card_index = input("Which card do you want to draw?\n")
						card_index = int(card_index)-1
					if card_index in range(len(self.discard_pile)):
						if typeOfCard == None:

							if len(self.hand) > 9:
								ansiprint(self.displayName,"has 10 or more cards in hand. <blue>"+ self.exhaust_pile[card_index]["Name"]+"<blue/>","is now in the discardpile.")
								self.discard_pile.append(self.draw_pile.pop(card_index))

							else:
								self.hand.append(self.discard_pile.pop(card_index))

							i += 1
						
						else:
							typeCheck = [card for card in self.discard_pile if card["Type"] == typeOfCard]
							
							if len(typeCheck) == 0:
								print("You don't have any",typeOfCard,"cards in your drawpile.")
								break
							
							if self.discard_pile[card_index]["Type"] != typeOfCard:
								if not random:
									ansiprint("You need to choose a",typeOfCard,"card!")
								continue
							
							else:
								if len(self.hand) > 9:
									ansiprint(self.displayName,"has 10 or more cards in hand. <blue>"+ self.discard_pile[card_index]["Name"]+"<blue/>","is now in the discardpile.")
									self.add_CardToDiscardpile(self.draw_pile.pop(card_index))

								else:
									self.add_CardToHand(self.discard_pile.pop(card_index))

								i += 1
					
				except Exception as e:
					self.explainer_function(card_index)
					print("You need to type a corresponding number. This is one of the more... fragile functions so just in case here is the error: draw_specific_cards_from_place",e)

		elif place == "Exhaustpile":
			i = 0
			while i < amount:
				if len(self.exhaust_pile) == 0:
					print("The Exhaustpile is currently empty.")
					return
				
				try:
					if random:
						card_index = rd.randint(0,len(self.exhaust_pile)-1)
					else:
						self.show_exhaustpile()
						card_index = input("Which card do you want to draw?\n")
						card_index = int(card_index)-1
					if card_index in range(len(self.exhaust_pile)):
						if typeOfCard == None:

							if len(self.hand) > 9:
								ansiprint(self.displayName,"has 10 or more cards in hand. <blue>"+ self.exhaust_pile[card_index]["Name"]+"<blue/>","is now in the discardpile.")
								self.discard_pile.append(self.exhaust_pile.pop(card_index))

							else:
								self.hand.append(self.exhaust_pile.pop(card_index))

							i += 1
						
						else:
							typeCheck = [card for card in self.exhaust_pile if card["Type"] == typeOfCard]
							
							if len(typeCheck) == 0:
								print("You don't have any",typeOfCard,"cards in your drawpile.")
								break
							
							if self.exhaust_pile[card_index]["Type"] != typeOfCard:
								if not random:
									ansiprint("You need to choose a",typeOfCard,"card!")
								continue
							
							else:
								if len(self.hand) > 9:
									ansiprint(self.displayName,"has 10 or more cards in hand. <blue>"+ self.exhaust_pile[card_index]["Name"]+"<blue/>","is now in the discardpile.")
									self.add_CardToDiscardpile(self.draw_pile.pop(card_index))

								else:
									self.add_CardToHand(self.exhaust_pile.pop(card_index))

								i += 1
					
				except Exception as e:
					self.explainer_function(card_index)
					print("You need to type a corresponding number. This is one of the more... fragile functions so just in case here is the error:draw_specific_cards_from_place",e)


	def draw_innates(self):
		i = 0
		otherCards = len(self.hand) #these are cards you get from relics Ninja scroll
		while i < len(self.draw_pile):
			try:
				if self.draw_pile[i].get("Innate") == True:
					self.add_CardToHand(self.draw_pile.pop(i))

				else:
					i += 1

			except Exception as e:
				print("Draw Innates",e)
				i += 1
		
		self.cardsDrawnEffectCheck(len(self.hand))

		while len(self.hand) > self.draw_strength:
			
			self.draw_pile.append(self.hand.pop(-1))
			
		draw_power = self.draw_strength + self.tempDraw - len(self.hand) + otherCards
		
		if draw_power > 0:
			self.draw(draw_power)
		else:
			return
			
	def draw(self,draw_power):
		
		if self.cantDraw > 0:
			ansiprint(self.displayName,"can't draw anything this turn.")
			return

		i = 0
		while i < draw_power:
				
			if len(self.draw_pile) == 0:
				
				self.draw_pile.extend(self.discard_pile)
				self.discard_pile = []
				self.shuffleDrawPile()

			try:
				
				if self.frozenEye > 0:
					self.add_CardToHand(self.draw_pile.pop(0))
				else:
					self.add_CardToHand(self.draw_pile.pop(rd.randint(0,len(self.draw_pile)-1)))
				
			except Exception as e:
				print("You don't have any cards left to draw.",e)
			
			i += 1
		
		self.cardsDrawnEffectCheck(i)

	def cardsDrawnEffectCheck (self,cardsDrawn):
		i = 0
		agonyCount = 0
		agonyPlusCount = 0
		try:
			while i < cardsDrawn:
				if self.hand[-(i+1)].get("Name") == "Void":
					self.gainEnergy(-1)
				elif self.hand[-(i+1)].get("Name") == "Endless Agony":
					agonyCount += 1
					
				elif self.hand[-(i+1)].get("Name") == "Endless Agony":
					agonyPlusCount += 1
				
				i+=1
		except Exception as e:
			print("cardsDrawnEffectCheck",e)
		while agonyCount > 0:
			self.add_CardToHand({"Name": "Endless Agony", "Damage":4,"Exhaust":True,"Energy": 0, "Type": "Attack" ,"Rarity": "Uncommon","Owner":"Silent"}) 
			agonyCount -= 1

		while agonyPlusCount > 0:
			self.add_CardToHand({"Name": "Endless Agony +","Damage":6,"Exhaust":True,"Energy": 0, "Type": "Attack" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent"})

	def discardBackInDrawpile(self):
		
		self.draw_pile.extend(self.discard_pile)
		self.discard_pile = []
		self.shuffleDrawPile()

	def blockingNextTurn(self,value):
		self.blockNextTurn += value + self.dexterity

		ansiprint(self.displayName,"blocks for",self.blockNextTurn,"next turn!")

	def reduce_energy(self):
		
		try:
			if self.card_in_play[0].get("Energy") == "X":
				self.energy = 0
			else:
				if self.energy - self.card_in_play[0].get("Energy") < 0:
					ansiprint("Irgendwie gibt es jetzt doch negative Energie:",self.energy)
				else:
										
					if self.cardsCostNothing > 0:
						pass
					else:
						self.energy -= self.card_in_play[0].get("Energy")
					
					ansiprint(self.displayName, "has <yellow>"+str(self.energy)+ " Energy</yellow> left.")
		
		except Exception as e:
			print(e,"issue in reduce_energy")
	

		self.changeEnergyCostAfterPlayed()

	def changeEnergyCostAfterPlayed(self):
		try:
			if self.card_in_play[0].get("Energy changed until played") == True:
				self.card_in_play[0].pop("Energy changed until played",None)
				self.card_in_play[0]["Energy"] = entities.cards[self.card_in_play[0].get("Name")].get("Energy")
	
		except Exception as e:
			print(e,"changeEnergyCostAfterPlayed")

	def changeEnergyCostAfterTurn(self):
		for card in self.hand:
			if card.get("This turn Energycost changed") == True:
				card.pop("This turn Energycost changed",None)
				card["Energy"] = entities.cards[card.get("Name")].get("Energy")

		for card in self.draw_pile:
			if card.get("This turn Energycost changed") == True:
				card.pop("This turn Energycost changed",None)
				card["Energy"] = entities.cards[card.get("Name")].get("Energy")

		for card in self.discard_pile:
			if card.get("This turn Energycost changed") == True:
				card.pop("This turn Energycost changed",None)
				card["Energy"] = entities.cards[card.get("Name")].get("Energy")

		for card in self.exhaust_pile:
			if card.get("This turn Energycost changed") == True:
				card.pop("This turn Energycost changed",None)
				card["Energy"] = entities.cards[card.get("Name")].get("Energy")

	def set_attackCounter(self):
		self.attack_counter += 1

		for relic in self.relics:
			if relic.get("Name") == "Shuriken":
				if self.attack_counter % 3 == 0:
					self.set_strength(1)
			elif relic.get("Name") == "Kunai":
				if self.attack_counter % 3 == 0:
					self.set_dexterity(1)
			elif relic.get("Name") == "Ornamental Fan":
				if self.attack_counter % 3 == 0:
					self.blocking(block_value = 4,unaffectedBlock = True)
			elif relic.get("Name") == "Nunchaku":
				relic["Counter"] += 1
				if relic.get("Counter") % 10 == 0:
					self.gainEnergy(1)
			elif relic.get("Name") == "Pen Nip":
				relic["Counter"] += 1
				if relic.get("Counter") % 10 == 0:
					self.penNip = 1
				else:
					self.penNip = 0

			elif relic.get("Name") == "Orange Pellets":
				if self.attack_counter > 0 and self.skill_counter > 0 and self.power_counter > 0:
					print("This is not implemented yet but you should be cleared of all your negative effects.")

	def set_skillCounter(self):
		self.skill_counter += 1

		for relic in self.relics:
			if relic.get("Name") == "Letter Opener":
				if self.skill_counter % 3 == 0:
					ansiprint("All Enemies receive <red>5 Damage</red> because of <light-red>Letter Opener</light-red>")
					i = 0
					while i < len(entities.list_of_enemies):
						enemy_check = len(entities.list_of_enemies)
						entities.list_of_enemies[i].receive_recoil_damage(5)
						if enemy_check != len(entities.list_of_enemies):
							continue
						else:
							i+=1

	def set_powerCounter(self):
		self.power_counter += 1
		storedCardIndexes = []
		if self.mummifiedHand > 0:
			#this needs to be implemented smarter. Just too lazy now.
			while i < len(self.hand):
				if self.hand[i].get("Energy") > 0 and self.hand[i].get("Type") == "Power":
					storedCardIndexes.append(i)
				
				i+= 1

		if len(storedCardIndexes) > 0:
			changedCardIndex = storedCardIndexes[rd.randint(0,len(storedCardIndexes)-1)]

			self.hand[changedCardIndex]["This turn Energycost changed"] = True
			self.hand[changedCardIndex]["Energy"] = 0
			
			ansiprint(self.hand[changedCardIndex].get("Name"),"costs <yellow>0 Energy</yellow> this turn because of <light-red>Mummified Hands</light-red>!")

		if self.birdFacedUrn > 0:
			self.heal(2)
			ansiprint("You <red>heal 2</red> because of <light-red>Bird-Faced Urn</light-red>!")

	def set_cardCounter (self):
		self.card_counter += 1

		
		for relic in self.relics:
			if relic.get("Name") == "Ink Bottle":
				relic["Counter"] += 1
				if relic.get("Counter") % 10 == 0:
					self.draw(1)
					ansiprint("You draw a card because you played 10 cards while owning an <light-red>Ink Bottle</light-red>.")



	def choose_enemy(self):
		
		if len (entities.list_of_enemies) > 0:
			if self.randomTarget == 0:
				self.showEnemies()
			while True:
				try:
					if self.randomTarget == 0:
						target = input("\nPick the opponent you want to target\n")
						target = int(target)-1
					else:
						target = rd.randint(0,len(entities.list_of_enemies)-1)

					if target == len(entities.list_of_enemies):
						self.hand.append(self.card_in_play.pop(0))
						break

					if target in range(len(entities.list_of_enemies)):
						break

					else:
						ansiprint("There is no opponent at that place.")
						continue
				except Exception as e:
					self.explainer_function(target)
					print("choose_enemy",e)
					ansiprint("You have to type a corresponding number! choose_enemy")
					pass
			
			self.target = target

			helping_functions.checkSpireBros(target)


		else:
			self.target = "No Enemies"
	
	def shuffleDrawPile (self):

		for cardPos in range(len(self.draw_pile)):
			randomPos = rd.randint(0,len(self.draw_pile)-1)
			self.draw_pile[cardPos], self.draw_pile[randomPos] = self.draw_pile[randomPos], self.draw_pile[cardPos]    

		self.shuffle_counter +=1

		if self.sunDial > 0:
			if self.shuffle_counter % 3 == 0:
				self.gainEnergy(2)
				ansiprint("You gained <yellow>2 Energy</yellow> because of <light-red>Sundial</light-red>!")

		if self.theAbacus > 0:
			self.blocking(6,unaffectedBlock=True)

	def shuffleDeck (self):

		for cardPos in range(len(self.deck)):
			randomPos = rd.randint(0,len(self.deck)-1)
			self.deck[cardPos], self.deck[randomPos] = self.deck[randomPos], self.deck[cardPos]

	def attack(self,attack):

		if len(entities.list_of_enemies) > 0:
			
			if self.card_in_play[0].get("Name") == "Shiv" or self.card_in_play[0].get("Name") == "Shiv+":
				attack += self.accuracy

			if self.strikeDummy > 0 and "Strike" in self.card_in_play[0].get("Name"):
				attack += 3

			if self.wristBlade == 1 and self.card_in_play[0].get("Energy") == 0:
				attack += 4
			
			if self.akabeko > 0 and self.attack_counter == 0:
				attack *= 2

			if len(self.doubleDamage) > 0:
				if self.doubleDamage[0] == helping_functions.turn_counter:
					attack *= 2

			if self.penNip > 0:
				attack*=2

			if self.weak > 0:
				damage = (attack + self.strength) - int((attack + self.strength) * 0.25)
			else:
				damage = (attack + self.strength)


			if damage < 0:
				damage = 0
			
			entities.list_of_enemies[self.target].receive_damage(damage)
			
		else:
			print("shits")
			pass

	def blocking(self,block_value,unaffectedBlock: bool = False):
		
		if self.noBlock > 0:
			ansiprint(self.displayName,"can't receive block for",self.noBlock,"turns.")
		else:
			if unaffectedBlock:
				self.block += block_value

			else:

				if self.frail > 0:
					block_value = (block_value + self.dexterity) - int((block_value + self.dexterity) * 0.25)
					self.block += block_value
				
				else:
					block_value = block_value + self.dexterity
					self.block += block_value

				if self.block < 0:
					self.block = 0
				
			ansiprint(self.displayName,"just blocked for <green>"+str(block_value)+"</green> and now has <green>" +str(self.block)+" Block</green>!")

	def energyBoost(self,value):
		self.temp_energy += value
		ansiprint(self.displayName,"will receive",self.temp_energy,"extra Energy next turn.")

	def discard(self, amount, random: bool = False):

		i = 0
		k = 0
		while i < amount:
			if len(self.hand) == 0:
				print("You don't have any Cards in your hand")
				break
			else:
				self.showHand()
				try:
					if random:
						card_index = rd.randint(0,len(self.hand) - 1)
				
					else:
						card_index = input("Pick the number of the Card you want to discard\n")
						card_index = int(card_index)-1

					if card_index < len(self.hand) and card_index >= 0:
						self.discard_pile.append(self.hand.pop(card_index))
					
					i += 1
					k -= 1
					
					self.discardCounter()


				except Exception as e:
					self.explainer_function(card_index)
					ansiprint("You have to type the number of the Card you want to discard. discard function")
					

		
		while k < 0:
			
			if self.discard_pile[k]["Name"] == "Reflex":
				self.draw(discard_pile[k]["Draw"])
					
			elif self.discard_pile[k]["Name"] == "Tactician":
				self.gainEnergy(discard_pile[k]["Energy Gain"])

			k += 1

	def discard_cards_by_type(self,typing):
		
		i = 0
		k = 0
		while i < len(self.hand):
			if self.hand[i]["Type"] == typing:
				self.discard_pile.append(self.hand.pop(i))
				if discard_pile[-1]["Name"] == "Reflex":
					self.draw(discard_pile[-1]["Draw"])
					
				elif discard_pile[-1]["Name"] == "Tactician":
					self.gainEnergy(discard_pile[-1]["Energy Gain"])
				k -= 1
				self.discardCounter()
			else:
				i += 1

		while k < 0:
			
			if self.discard_pile[k]["Name"] == "Reflex":
				self.draw(discard_pile[k]["Draw"])
					
			elif self.discard_pile[k]["Name"] == "Tactician":
				self.gainEnergy(discard_pile[k]["Energy Gain"])

			k += 1

	def discard_cards_by_type_opposite(self,typing):
		
		i = 0
		k = 0
		while i < len(self.hand):
			if self.hand[i]["Type"] != typing:
				self.discard_pile.append(self.hand.pop(i))
				k -= 1
				self.discardCounter()
			else:
				i += 1		

		while k < 0:
			
			if self.discard_pile[k]["Name"] == "Reflex":
				self.draw(discard_pile[k]["Draw"])
					
			elif self.discard_pile[k]["Name"] == "Tactician":
				self.gainEnergy(discard_pile[k]["Energy Gain"])

			k += 1

	def discard_hand(self):
		

		i=0
		while i < len(self.hand):
			try:
				self.receive_recoil_damage(self.hand[i]["DiscardDamage"]) #this uses the recoil damage function as its not affected by vulnerable etc such as recoil damage itself.
				ansiprint("You had a",self.hand[i]["Name"],"in your hand and took",self.hand[i]["DiscardDamage"],"damage because of it.")
				self.discard_pile.append(self.hand.pop(i))

			except Exception as e:
				i+=1
		
		if self.runicPyramide > 0:
			ansiprint("You keep your hand because of <light-red>Runic Pyramide</light-red>.")

		else:
			i = 0
			snap = len(self.hand)
			while i < snap:
				self.discard_pile.append(self.hand.pop(0))
				i += 1

	def exhaust(self, amount, random: bool = False):

		i = 0
		while i < amount:
			if len(self.hand) == 0:
				print("You don't have any cards in your hand left")
				break
			else:
				self.showHand()
				try:
					if random:
						card_index = rd.randint(0,len(self.hand) - 1)
					else:
						card_index = input("Pick the number of the card you want to exhaust\n")
						card_index = int(card_index)-1
					if card_index < len(self.hand):
						self.exhaust_pile.append(self.hand.pop(card_index))
						i += 1
						ansiprint("Exhausted.")
						self.exhaust_counter += 1
				
				except Exception as e:
					self.explainer_function(card_index)
					ansiprint("You have to type the number of the Card you want to exhaust. exhaust function")
					pass

				self.exhaust_pile.append(self.hand.pop(card_index))

	def exhaust_ethereals(self):
		i = 0
		while i < len(self.hand):
			if self.hand[i].get("Ethereal") == True:
				self.add_CardToExhaustpile(self.hand.pop(i))
				ansiprint("because it was <light-cyan>Ethereal</light-cyan>!")
			else:
				i += 1

	def putBackOnDeck(self, amount, energyChange = None, energyChangeType = None, bottom: bool = False):

		i = 0
		while i < amount:
			if len(self.hand) == 0:
				print("You don't have any cards in your hand")
				break
			else:
				self.showHand()
				print(str(len(self.hand)+1)+". Skip")
				try:
					
					card_index = input("Pick the number of the card you want to put back on your Deck.\n")
					card_index = int(card_index) - 1
					if card_index in range(len(self.hand)):
						if bottom:
							self.draw_pile.insert(len(self.draw_pile),self.hand.pop(card_index))
							ansiprint("<blue>"+self.draw_pile[-1]["Name"]+"</blue> is now at the bottom of your deck.")
						else:
							self.draw_pile.insert(0,self.hand.pop(card_index))
							ansiprint("<blue>"+self.draw_pile[0]["Name"]+"</blue> is now on top of your deck.")

						i += 1
						
						if energyChangeType == "For Battle":
							self.draw_pile[0]["Energy changed for the battle"] = True
							self.draw_pile[0]["Energy"] = energyChange
							ansiprint("The cost of <blue>"+self.draw_pile[0]["Name"]+ "</blue> changed to",energyChange,"for the rest of the battle.")

						elif energyChangeType == "Until Played":
							self.draw_pile[0]["Energy changed until played"] = True
							self.draw_pile[0]["Energy"] = energyChange
							ansiprint("The cost of",self.draw_pile[0]["Name"],"changed to",energyChange,"until played.")

					elif card_index == len(self.hand):
						print("You decided to skip.")
						break
					else:
						pass	
				
				except Exception as e:
					self.explainer_function(card_index)
					ansiprint("You have to type the number of the Card you want to put back on your deck. putBackOnDeck")
					pass

	def effect_counter_down(self):
		
		if self.weak > 0:
			self.weak -= 1

		if self.frail > 0:
			self.frail -= 1

		if self.vulnerable > 0:
			self.vulnerable -= 1

		if self.invulnerable > 0:
			self.invulnerable -= 1
		
		if self.entangled > 0:
			self.entangled -= 1

		if self.noBlock > 0:
			self.noBlock -= 1

		if len(self.doubleDamage) > 0:
			if helping_functions.turn_counter == self.doubleDamage[0]:
				self.doubleDamage.pop(0)

		if self.cardsCostNothing > 0:
			self.cardsCostNothing -= 1
		
		self.cantDraw = 0

		self.damage_counter = 0
		
		if self.akabeko > 0 and self.attack_counter > 0:
			self.akabeko = 0

		self.timeWarp = False

	def showRelics(self):
		for relic in self.relics:
			if "Counter" in relic:
				ansiprint("<light-red>"+relic.get("Name")+"</light-red> | Counter:",relic.get("Counter"),"| Effect:",relic.get("Info"))
			else:
				ansiprint("<light-red>"+relic.get("Name")+"</light-red>","| Effect:",relic.get("Info"))

	def showHand(self):
		ansiprint("This is your Hand:\n")

		i = 0
		for card in self.hand:
			if i+1 < 10:
				numberSpacing = "  "
			else:
				numberSpacing = " "
			
			lineSpacing = " " * (20-len(card.get("Name")))
			
			try:
				if card.get("Type") == "Attack":
					ansiprint(str(i+1)+"."+numberSpacing+"<red>"+card.get("Name")+"</red>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
				elif card.get("Type") == "Skill":
					ansiprint(str(i+1)+"."+numberSpacing+"<green>"+card.get("Name")+"</green>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
				elif card.get("Type") == "Power":
					ansiprint(str(i+1)+"."+numberSpacing+"<blue>"+card.get("Name")+"</blue>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
				elif card.get("Type") == "Curse":
					ansiprint(str(i+1)+"."+numberSpacing+"<m>"+card.get("Name")+"</m>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
				elif card.get("Type") == "Status":
					ansiprint(str(i+1)+"."+numberSpacing+"<light-cyan>"+card.get("Name")+"</light-cyan>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
			
			except Exception as e:
				print(e,"Show Hand")

			i = i + 1
	def showDeck(self,noUpgrades:bool = False,remove:bool = False):
		
		i = 0
		for card in self.deck:
			if i+1 < 10:
				numberSpacing = "  "
			else:
				numberSpacing = " "
			
			lineSpacing = " " * (20-len(card.get("Name")))
			if noUpgrades == True and (card.get("Upgraded") == True or card.get("Type") == "Curse"):
				pass
			elif card.get("Type") == "Attack":
				ansiprint(str(i+1)+"."+numberSpacing+"<red>"+card.get("Name")+"</red>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
			elif card.get("Type") == "Skill":
				ansiprint(str(i+1)+"."+numberSpacing+"<green>"+card.get("Name")+"</green>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
			elif card.get("Type") == "Power":
				ansiprint(str(i+1)+"."+numberSpacing+"<blue>"+card.get("Name")+"</blue>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
			elif card.get("Type") == "Curse":
				ansiprint(str(i+1)+"."+numberSpacing+"<m>"+card.get("Name")+"</m>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
			elif card.get("Type") == "Status":
				ansiprint(str(i+1)+"."+numberSpacing+"<light-cyan>"+card.get("Name")+"</light-cyan>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
			i = i + 1
	
	def showPotions(self,skip=False):
		try:
			
			potions = ""
			i = 0
			for potion in self.potionBag:
				potions += "{}.) <c>{}</c>\n".format(i+1,potion.get("Name"))
				i = i + 1
			if skip and len(self.potionBag)>0:
				potions += str(i+1)+".) Skip"
			elif skip == False and len(self.potionBag) == 0:
				ansiprint("You don't have any <c>Potions</c>.")
			ansiprint(potions)
		except Exception as e:
			print(e)



	def showEnemies(self,skip=True):
		#try:
		gegner = ""
		i = 0
		for opponent in entities.list_of_enemies:
			gegner += "\n{}.) {} (<red>{}</red>/<red>{}</red>)".format(i+1,opponent.name,opponent.health,opponent.max_health)
			if opponent.block > 0:
				gegner += " |<green> Block: "+str(opponent.block)+"</green>"
			if opponent.poison > 0:
				gegner += " |<green> Poison: "+str(opponent.poison)+"</green>"
			if opponent.weak > 0:
				gegner += " |<light-cyan> Weakness: "+str(opponent.weak)+"</light-cyan>"
			if opponent.vulnerable > 0:
				gegner += " |<light-cyan> Vulnerable: "+str(opponent.vulnerable)+"</light-cyan>"
			if opponent.strength != 0:
				gegner += " |<red> Strength: "+str(opponent.strength)+"</red>"
			if opponent.ritual > 0:
				gegner += " |<light-blue> Ritual: "+str(opponent.ritual)+"</light-blue>"
			if opponent.modeshift > 0:
				gegner += " |<light-blue> Modeshift: "+str(opponent.modeshift)+"</light-blue>"
			if opponent.invulnerable > 0:
				gegner += " |<light-blue> Invulnerable: "+str(opponent.invulnerable)+"</light-blue>"
			if opponent.intangible > 0:
				gegner += " |<light-blue> Invincible: "+str(opponent.intangible)+"</light-blue>"
			if opponent.artifact > 0:
				gegner += " |<light-blue> Artifact: "+str(opponent.artifact)+"</light-blue>"
			if opponent.metallicize > 0:
				gegner += " |<light-blue> Metallicize: "+str(opponent.metallicize)+"</light-blue>"
			if opponent.barricade == True:
				gegner += " |<light-blue> Barricade</light-blue>"
			if opponent.sadisticNature > 0:
				gegner += " |<light-blue> Sadistic Nature: "+str(opponent.sadisticNature)+"</light-blue>"
			if opponent.heartVincibility > 0:
				gegner += " |<light-blue> Heart Vincibility: "+str(opponent.heartVincibility)+"</light-blue>"
			if opponent.slow > 0:
				gegner += " |<light-blue> Slow: "+str(opponent.slow)+"</light-blue>"
			for effect in opponent.on_hit_or_death:
				if "Curl" in effect[0]:
					gegner += " |<light-blue> Curl: "+effect[0].split(" ")[1]+"</light-blue>"

			if opponent.move:
				gegner += " | "+ self.enemy_preview(i)
			if len(self.card_in_play) > 0 and self.card_in_play[0].get("Damage"):
				gegner += " | "+ self.determine_damage_to_enemy(self.card_in_play[0].get("Damage"),i)
			
			i = i + 1
		if skip:
			gegner += "\n" +str(i+1) + ".) Skip" 
		ansiprint(gegner,"\n")

	def enemy_preview(self,index):
		previewString = ""
		
		#removeNames from Intention
		if type(entities.list_of_enemies[index].move) == int:
			
			attackDamage = self.determine_damage_to_character(entities.list_of_enemies[index].move,index)

			previewString = "Attacks for <red>" + str(attackDamage)+"</red>"
			
		elif "Multiattack" in entities.list_of_enemies[index].move:
			
			amount = entities.list_of_enemies[index].move.split(" ")[1].split("*")[1]
			damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1].split("*")[0]),index)

			previewString = "Attacks "+amount+" times for <red>"+damage+"</red>"

		elif "Thrash" in entities.list_of_enemies[index].move:

			damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1].split("/")[0]),index)
			previewString = "Attacks for <red>"+str(damage)+"</red>. Blocks"

		elif "Blocking" in entities.list_of_enemies[index].move:

			previewString = "Will <green>Block</green>"

		elif "Weak" in entities.list_of_enemies[index].move:
			
			previewString = "Applies Debuff"

		elif "Vulnerable" in entities.list_of_enemies[index].move:
			
			previewString = "Applies Debuff"

		elif "Frail" in entities.list_of_enemies[index].move:
			
			previewString = "Applies Debuff"

		elif "Ritual" in entities.list_of_enemies[index].move:

			previewString = "Buff"

		elif "Grow" in entities.list_of_enemies[index].move:
		
			previewString = "Buff"

		elif "Bellow" in entities.list_of_enemies[index].move:
			
			previewString = "Will <green>Block</green> and Buff itself"

		elif "GoopSpray" in entities.list_of_enemies[index].move:

			previewString = "Applies strong Debuff"

		elif "Support Automaton" in entities.list_of_enemies[index].move:

			previewString = "Buff"

		elif "Entangle" in entities.list_of_enemies[index].move:

			previewString = "Applies Debuff"

		elif "Suck" in entities.list_of_enemies[index].move:

			damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1]),index)
			previewString = "Attacks for "+str(damage)+" damage. Buffs itself"
 		
		elif "CenturionDefendAlly" in entities.list_of_enemies[index].move:

			previewString = "Buff"

		elif "MysticBuff" in entities.list_of_enemies[index].move:

			previewString = "Buff"

		elif "MysticHeal" in entities.list_of_enemies[index].move:

			previewString = "Buff"

		elif "SmokeBomb" in entities.list_of_enemies[index].move:

			previewString = "Will <green>Block</green>"

		elif "CenturionDefendAlly" in entities.list_of_enemies[index].move:
			
			previewString = "Will <green>Block</green>"			

		elif "Protect" in entities.list_of_enemies[index].move:

			previewString = "Will <green>Block</green>"

		elif "VentSteam" in entities.list_of_enemies[index].move:

			previewString = "Applies Debuff"

		elif "DefensiveMode" in entities.list_of_enemies[index].move:

			previewString = "Buff"

		elif "TwinSlam" in entities.list_of_enemies[index].move:
			
			amount = entities.list_of_enemies[index].move.split(" ")[1].split("*")[1]
			damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1].split("*")[0]),index)

			previewString = "Attacks "+amount+" times for "+damage+" damage. Buffs itself"

		elif "Haste" in entities.list_of_enemies[index].move:

			previewString = "Buff"

		elif "TimeSlam" in entities.list_of_enemies[index].move:

			amount = entities.list_of_enemies[index].move.split(" ")[1].split("/")[1]
			damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1].split("/")[0]),index)

			previewString = "Attacks "+amount+" times for "+damage+" damage. Applies a negative effect"

		elif "Divider" in entities.list_of_enemies[index].move:
			damage = self.determine_damage_to_character(6,index)
			previewString = "Attacks"+ int(self.health // 12 + 1) *"times for <red>"+ str(damage)+"</red>"

		elif "Inferno" in entities.list_of_enemies[index].move:
			
			amount = entities.list_of_enemies[index].move.split(" ")[1].split("*")[1]
			damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1].split("*")[0]),index)

			previewString = "Attacks "+amount+" times for "+damage+" damage. Applies Debuff"

		elif "Enrage" in entities.list_of_enemies[index].move:

			previewString = "Buff"

		elif "Hex" in entities.list_of_enemies[index].move:
			
			previewString = "Applies strong Debuff"

		elif "SiphonSoul" in entities.list_of_enemies[index].move:
			
			previewString = "Applies strong Debuff"

		elif "Bolt" in entities.list_of_enemies[index].move:

			previewString = "Applies Debuff"

		elif "Encourage" in entities.list_of_enemies[index].move:

			previewString = "Buff"

		elif "Ripple" in entities.list_of_enemies[index].move:

			previewString = "Will <green>Block</green> and apply a Debuff"

		elif "BurningDebuff" in entities.list_of_enemies[index].move:

			previewString = "Applies Debuff"

		elif "SnakeStrike" in entities.list_of_enemies[index].move:

			amount = entities.list_of_enemies[index].move.split(" ")[1].split("*")[1]
			damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1].split("*")[0]),index)

			previewString = "Attacks "+amount+" times for <red>"+damage+"</red>. Applies Debuff"

		elif "Gloat" in entities.list_of_enemies[index].move:

			previewString = "Buff"

		elif "ChampAnger" in entities.list_of_enemies[index].move:

			previewString = "Buff"

		elif "DefensiveStance" in entities.list_of_enemies[index].move:
			
			previewString = "Buff"

		elif "Roar" in entities.list_of_enemies[index].move:

			previewString = "Applies strong Debuff"

		elif "MegaDebuff" in entities.list_of_enemies[index].move:

			previewString = "Applies strong Debuff"
			
		elif "TorchBuff" in entities.list_of_enemies[index].move:
			
			previewString = "Will <green>Block</green> and Buff"

		elif "BearHug" in entities.list_of_enemies[index].move:

			previewString = "Applies Debuff"

		elif "SpikeUp" in entities.list_of_enemies[index].move:

			previewString = "Buff"

		elif "Repulse" in entities.list_of_enemies[index].move:

			previewString = "Applies Debuff"

		elif "Constrict" in entities.list_of_enemies[index].move:

			previewString = "Applies strong Debuff"

		elif "Implant" in entities.list_of_enemies[index].move:

			previewString = "Applies strong Debuff"

		elif "GiantHead" in entities.list_of_enemies[index].move:

			additionalDamage = entities.list_of_enemies[index].counter * 5

			attackDamage = self.determine_damage_to_character(int(entities.split(" ")[1]) + additionalDamage)
			previewString = "Attacks for "+str(attackDamage)+" damage"

		elif "Fortify" in entities.list_of_enemies[index].move:

			previewString = "Buff"

		elif "BurnStrike" in entities.list_of_enemies[index].move:

			amount = entities.list_of_enemies[index].move.split(" ")[1].split("*")[1]
			damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1].split("*")[0]),index)

			previewString = "Attacks "+amount+" times for "+damage+" damage. Applies Debuff"

		elif "DazeBeam" in entities.list_of_enemies[index].move:

			amount = entities.list_of_enemies[index].move.split(" ")[1].split("*")[1]
			damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1].split("*")[0]),index)

			previewString = "Attacks "+amount+" times for "+damage+" damage. Applies Debuff"

		elif "SquareOfDeca" in entities.list_of_enemies[index].move:
			
			previewString = "Buff"

		elif "Debilitate" in entities.list_of_enemies[index].move:

			previewString = "Applies strong Debuff"			

		elif "HeartBuff" in entities.list_of_enemies[index].move:

			previewString = "Buff"

		elif "Transientattack" in entities.list_of_enemies[index].move:

			damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1])+(helping_functions.turnCounter-1)*10,index)
			previewString = "Attacks for <red>"+str(damage)+"</red>"

		elif "/" in entities.list_of_enemies[index].move:
			
			damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1].split("/")[0]),index)
			previewString = "Attacks for <red>"+str(damage)+"</red>. Applies Debuff"

		elif "|" in entities.list_of_enemies[index].move:
			
			previewString = "Buff"

		else:

			previewString = "???"
		
		return previewString

	def determine_damage_to_character(self,damage,index):

		if entities.list_of_enemies[index].spireBroAttacked == True:
			damage += int(damage * 0.5)

		plan_value = damage + entities.list_of_enemies[index].get_strengthModifier()
		
		if entities.list_of_enemies[index].weak > 0:
			if self.paperKrane > 0:		
				plan_value -= plan_value * 0.4
			else:
				plan_value -= plan_value * 0.25

		if self.vulnerable > 0:
			
			if self.oddMushroom > 0:
				plan_value += plan_value * 0.25
			else:
				plan_value += plan_value * 0.50

		plan_value = math.floor(plan_value)

		if plan_value < 0:
			plan_value = 0

		return plan_value

	def determine_damage_to_enemy(self,attack,index):

		if self.card_in_play[0].get("Name") == "Shiv" or self.card_in_play[0].get("Name") == "Shiv+":
			attack += self.accuracy

		if self.strikeDummy > 0 and "Strike" in self.card_in_play[0].get("Name"):
			attack += 3

		if self.wristBlade == 1 and self.card_in_play[0].get("Energy") == 0:
			attack += 4
		
		if self.akabeko > 0 and self.attack_counter == 0:
			attack *= 2

		if len(self.doubleDamage) > 0:
			if self.doubleDamage[0] == helping_functions.turn_counter:
				attack *= 2

		if self.weak > 0:
			attack = (attack + self.strength) - int((attack + self.strength) * 0.25)
		else:
			attack = (attack + self.strength)


		if attack < 0:
			attack = 0
			
		if entities.list_of_enemies[index].heartVincibility >= 200:
			attack = 0

		if self.penNip > 0:
			attack*=2
			self.penNip = 0
		

		if entities.list_of_enemies[index].vulnerable > 0:
			attack += attack * 0.50
			attack = math.floor(attack)
		
		try:
			if len(entities.list_of_enemies[index].on_hit_or_death) > 0:
			
				if "Fly" in entities.list_of_enemies[index].on_hit_or_death[0][0]:
					attack /= 2
					attack = math.floor(attack)

		except Exception as e:
			#print(e)
			pass

		return "Receives <red>"+str(attack) +" damage</red>"


	def receive_damage(self,attack_damage):
		if attack_damage > 0:

			if self.check_buffer():

				if self.vulnerable > 0:
					
					if self.oddMushroom > 0:
						attack_damage += attack_damage * 0.25
					else:
						attack_damage += attack_damage * 0.50
					
				attack_damage = math.floor(attack_damage)
				
				if self.intangible > 0:
					attack_damage = 1
					ansiprint("Intangible reduces the damage to 1.")

				damage = attack_damage - self.block
					
				if int(damage) > 0:
					self.block = 0
					self.damageCounter()
					
					if self.torii > 0 and damage <= 5:
						damage = 1 

					if self.tungstenRod > 0:
						damage -= 1

					self.health -= int(damage)

					if self.health < 1:
						self.alive = False
					else:
						ansiprint("The",self.displayName,"has taken <red>"+str(damage)+" damage</red> and now has <red>"+str(self.health)+" Health</red> left.")

				else:
					self.block -= attack_damage

					ansiprint(self.displayName, "has <green>"+str(self.block)+" Block</green> and <red>"+str(self.health)+" Health</red> left.")
				
				if self.alive == False:
					entities.check_if_character_dead()

	def receive_recoil_damage(self,attack_damage,directDamage: bool = False):
		#there are some differences between recoil and normal damage. Therefore there are separate functions for that.
		
		if attack_damage > 0:

			if self.check_buffer():

				if self.intangible > 0:
					attack_damage = 1
				
				if directDamage:
					damage = attack_damage
				else:
					damage = attack_damage - self.block

				if int(damage) > 0:
					if directDamage == False:
						self.block = 0
					
					self.damageCounter()
					self.health -= int(damage)
					if self.health < 1:
						ansiprint("The",self.displayName,"has been defeated")
						self.alive = False
					else:
						ansiprint("The",self.displayName,"has taken <red>"+str(damage)+" Damage</red> and now has <red>"+str(self.health)+" Health</red> left.")
				
				else:
					self.block -= attack_damage
					ansiprint(self.displayName, "has", self.block,"block left and",self.health,"health left.")

				if self.alive == False:
						entities.check_if_character_dead()

	def set_position(self,new_pos):

		self.position = new_pos

		for relic in self.relics:
			if relic.get("Name") == "Maw Bank":
				if relic.get("Counter") == 1:
					self.set_gold(12)

	def get_position(self):
		position = self.position[0],self.position[1]
		return position

	def set_dontLoseBlock(self,value):
		self.dontLoseBlock += value
		ansiprint(self.displayName, "will keep remaining block for",self.dontLoseBlock,"turns.")

	def copyCardsForNextTurn (self,value):
		self.showHand()
		card_index = 0

		while i < value:
			try:
				card_index = input("Pick the number of the card you want to keep for next turn\n")
				card_index = int(card_index) - 1
				if card_index in range(len(self.hand)):
					break

			except Exception as e:
				self.explainer_function(card_index)
				ansiprint ("Type the number of the card you want to keep for next turn. copyCardsForNextTurn")
				

		while i < value:
			self.cardsNextTurn.append(self.hand[card_index])
			i += 1

		ansiprint("Next turn",self.displayName,"will receive",i,"copies of",self.hand[card_index]["Name"])

	def set_deck(self,deck):
		
		for card in deck:

			self.add_CardToDeck(card,silence=True)
		
	def heal(self,value):

		if self.markOfTheBloom > 0:
			ansiprint("You can't heal because of <light-red>Mark of the Bloom</light-red>.")

		else:
			self.health += value
			if self.health > self.max_health:
				displayValue = self.health - self.max_health
				self.health = self.max_health

				ansiprint(self.displayName,"heals for", value - displayValue, "and now has",self.health,"Health.")
			else:
				ansiprint(self.displayName,"heals for", value, "and now has",self.health,"Health.")

	def regenerate(self):

		self.heal(self.regen)
		self.regen -= 1
		ansiprint(self.displayName,"now has",self.regen,"Regen left.")

	def set_regen(self, value):

		self.regen += value
		
		ansiprint(self.displayName,"now has",self.regen,"Regen.")

	def set_maxHealth(self,value):

		self.max_health += value
		
		if value >= 0:
			self.health += value
		if value < 0:
			if self.max_health < self.health:
				self.health = self.max_health

		ansiprint(self.displayName,"changed maximum health by",value,"and now has <red>"+str(self.max_health)+" maximum health</red> and <red>"+str(self.health)+" health</red>.")
	
	def set_health(self,value):
		tungstenRod = False
		for relic in self.relics:
			if relic.get("Name") == "Tungsten Rod":
				tungstenRod = True

		if tungstenRod and value < 0:
			value += 1

		self.health += value
		ansiprint(self.displayName,"changed health for",value,"and has <red>"+str(self.health)+" health</red> left.\n")


		if self.health < 1:
			entities.check_if_character_dead()

	def resurrect(self,source):

		if source == "Fairy in a Bottle":
			sacredBark = False
			for relic in self.relics:
				if relic.get("Name") == "Sacred Bark":
					sacredBark = True

			if sacredBark:
				self.health = math.floor((self.max_health/100)*60)
			else:
				self.health = math.floor((self.max_health/100)*30)
			

		elif source == "Lizard Tale":
			self.health = math.floor((self.max_health/100)*50)

		ansiprint(self.displayName,"resurrected and now has",self.health,"health.")

		self.alive = True

	def set_cardsCostZero(self,value):

		self.cardsCostNothing += value
		
		ansiprint(self.displayName,"cards cost nothing for",self.cardsCostNothing,"turn.")

	def set_accuracy(self,value):

		self.accuracy += value
		ansiprint(self.displayName,"has",self.accuracy,"Accuracy.")

	def set_spikes (self,value):
		
		self.spikes += value
		ansiprint(self.displayName,"has",self.spikes,"Spikes.")

	def set_tempDraw(self,value):

		self.tempDraw += value
		if value >= 0:
			
			ansiprint(self.displayName,"draws",self.tempDraw,"more cards next turn.")

		else:
			ansiprint(self.displayName,"draws",abs(self.tempDraw),"less cards next turn.")

	def set_reducedDrawByTurns(self,value):

		i = 0
		while i < value:
			self.reducedDrawByTurns.append(helping_functions.turn_counter+i+1)
			i+=1


	def set_tempSpikes (self,value):
		
		self.tempSpikes += value
		ansiprint(self.displayName,"now has",self.tempSpikes,"Spikes.")

	def set_strengthDecrease(self,value):

		if self.check_artifact():
			decrease = [helping_functions.turn_counter+1,-value]			
			self.strengthDecrease.append(decrease)			
			ansiprint(self.displayName,"will lose",value,"<red>Strength</red> next turn.")
			#this system needs to be added to enemies as well.
	
	def set_ritual(self,value):

		self.ritual += value
		ansiprint(self.displayName,"has",self.ritual,"Ritual.",self.displayName,"will receive",self.ritual,"Strength per turn.")

	def set_strength(self,value):

		self.strength += value
		ansiprint(self.displayName,"has",self.strength,"Strength.")

	def set_dexterityDecrease(self, value):

		if self.check_artifact():
			decrease = [turn_counter+1,-value]			
			self.dexterityDecrease.append(decrease)			
			ansiprint(self.displayName,"will lose",value,"Dexterity next turn.")
	
	def set_dexterity (self,value):

		self.dexterity += value
		ansiprint(self.displayName,"now has",self.dexterity,"Dexterity.")

	def set_infiniteBlades(self,value):

		self.infiniteBlades += value
		ansiprint(self.displayName,"will now receive",self.infiniteBlades,"at the beginning of each turn.")

	def set_noxiousFumes(self,value):

		self.noxiousFumes += value
		ansiprint("Enemies of",self.displayName,"will now receive",self.noxiousFumes,"poison at the beginning of each of your turns!")

	def set_wellLaidPlans (self,value):

		self.wellLaidPlans += value
		ansiprint("At the end of your turn you can keep",self.wellLaidPlans,"cards in your hand for next turn.")

	def set_thousandCuts(self,value):

		self.thousandCuts += value
		ansiprint("Whenever you play a card all enemies will receive",self.thousandCuts,"damage.")

	def set_afterImage(self,value):

		self.afterImage += value
		ansiprint("Whenever you play a card you will receive",self.afterImage,"block.")

	def set_envenom(self,value):
		self.envenom += value
		
		ansiprint("Whenever you deal damage to an enemies health they will be poisoned for",self.envenom,".")

	def set_toolsOfTheTrade(self,value):
		
		self.toolsOfTheTrade += value

		ansiprint("At the beginning of each turn you draw and discard",self.toolsOfTheTrade,"extra card(s).")

	def set_buffer(self,value):

		self.buffer += value

		if self.buffer == 1:
			ansiprint("The next time",self.displayName,"takes <red>damage</red> it will be negated.")
		elif self.buffer > 1:
			ansiprint("The next", self.buffer,"times",self.displayName,"takes <red>damage</red> it will be negated.")
		else:
			pass

	def set_intangible(self,value):
				
		self.intangible += value
		ansiprint("For",self.intangible,"turns",self.displayName,"will only receive 1 damage per time they take damage.")

	def set_magnetism (self,value):
		
		self.magnetism += value
		ansiprint(self.displayName,"will receive",self.magnetism,"Colorless Cards per turn.")

	def set_mayhem(self,value):

		self.mayhem += value
		ansiprint(self.displayName,"will automatically play the",self.mayhem,"top cards of the deck.")

	def set_theBomb(self,value,turn_counter):

		bomb = [turn_counter+3,value]
		
		self.theBomb.append(bomb)
		
		ansiprint(self.displayName,"will deal",value,"damage to all in enemies in 3 turns")
	
	def set_confused(self):
		if self.check_artifact():
			self.confused = 1
			ansiprint(self.displayName,"is confused. All cards have random cost.")

	def set_weakness(self,value):
		if self.ginger > 0:
			ansiprint("You are immune to <black>Weakness</black> thanks to <light-red>Ginger</light-red>!")
		else:
			if self.check_artifact():
				self.weak += value
				ansiprint(self.displayName, "has now",self.weak,"Weakness.\n")
			

	def set_vulnerable(self,value):
		if self.check_artifact():
			self.vulnerable += value
			ansiprint(self.displayName, "has now",self.vulnerable,"Vulnerable.\n")

	def set_frail(self,value):
		if self.turnip > 0:
			ansiprint("You are immune to being <black>Frail</black> thanks to <light-red>Turnip</light-red>!\n")
		else:
			if self.check_artifact():
				self.frail += value
				ansiprint(self.displayName, "has now",self.frail,"Frail.\n")

	def set_constriction (self,value):
		if self.check_artifact():
			self.constriction += value
			ansiprint(self.displayName,"is constricted by the <red>Spire Growth</red> and you take <red>"+str(self.constriction)+"</red> damage at the start of each turn.\n")

	def set_hex(self):
		if self.check_artifact():
			self.hex = 1
			ansiprint(self.displayName,"will receive 1 <light-cyan>Dazed</light-cyan> everytime you play a <red>non-attack</red> Card\n")

	def set_entangled(self,value):
		if self.check_artifact():
			self.entangled += value
			ansiprint(self.displayName, "is now entangled for",self.entangled,"turn.\n")

	def set_cantDraw(self,value):
		if self.check_artifact():
			self.cantDraw += value

			if self.cantDraw == 1:
				ansiprint(self.displayName, "can't draw for",self.cantDraw,"turn.\n")
			else:
				ansiprint(self.displayName, "can't draw for",self.cantDraw,"turns.\n")	

	def set_wraithForm(self,value):
		if self.check_artifact():

			self.wraithForm += value
			ansiprint("You lose",self.wraithForm,"Dexterity at the end of each of your turns.")

	def set_noBlock (self,value):

		if self.check_artifact():

			self.noBlock += value
			ansiprint(self.displayName,"can't receive block for",self.noBlock,"turns.")

	def check_artifact(self):
		
		if self.artifact > 0:
			self.artifact -= 1
			ansiprint("You lose one artifact instead of suffering from a negative effect.")
			return False
		elif self.artifact == 0:
			return True

	def check_buffer(self):
		
		if self.buffer > 0:
			self.buffer -= 1
			ansiprint("You lose one buffer instead of suffering <red>damager</red>.")
			return False
		elif self.artifact == 0:
			return True

	def set_burst (self,value):
		
		self.burst += value
		ansiprint("The next",self.burst,"skill card(s) are going to be played twice.")	

	def set_duplication (self, value):

		self.duplication += value
		ansiprint("The next",self.duplication,"card(s) are going to be played twice.")	

	def set_artifact(self,value):

		self.artifact += value

		ansiprint("You know have",self.artifact,"charge.")


	def set_drawPile(self):

		self.draw_pile = copy.deepcopy(self.deck)
		self.shuffleDrawPile()

	def print_all_cards(self):
		i = 0
		for card in self.hand:
			print(i+1,card.get("Name"))
			i+=1
		for card in self.discard_pile:
			print(i+1,card.get("Name"))
			i+=1
		for card in self.draw_pile:
			print(i+1,card.get("Name"))
			i+=1
		for card in self.exhaust_pile:
			print(i+1,card.get("Name"))
			i+=1
	def add_CardToDeck(self,card,index=None,silence=False):
		card = card.copy()
		omamori = False
		darkstonePeriapt = False
		for relic in self.relics:
			if relic.get("Name") == "Ceramic Fish":
				self.set_gold(9)
			elif relic.get("Name") == "Omamori":
				omamoriIndex = self.relics.index(relic)
				omamori = True
			elif relic.get("Name") == "Darkstone Periapt":
				darkstonePeriapt = True
		
		if card.get("Unique ID") == None:

			while True:
				card["Unique ID"] = rd.randint(0,9999999)
				i = 0
				while i < len(self.deck):
					if card.get("Unique ID") != self.deck[i].get("Unique ID"):
						i+=1
			
				if i < len(self.deck):
					print("A generated Unique ID was identical to one in your deck. That's not bad as long as this prompt is not spammed to you endlessly.")
					continue
				else:
					break

		if index == None:
			index = len(self.deck)
		
		if card.get("Type") == "Curse":
			if omamori:
				if self.relics[omamoriIndex]["Counter"] > 0:
					self.relics[omamoriIndex]["Counter"] -= 1
					ansiprint("You did not add <m>"+card.get("Name")+"</m> to the Deck because you have an <light-red>Omamori</light-red>. This works",self.relics[omamoriIndex]["Counter"],"more time(s).")
			else:
				if silence == False:
					ansiprint(self.displayName, "added", "<m>"+card.get("Name")+"</m>", "to the deck.\n")
				if darkstonePeriapt:
					self.set_maxHealth(6)
					ansiprint("You increased your <red>Max HP by 6<red> because of adding a Curse to the deck while owning <light-red>Darkstone Periapt</light-red>.")

				self.deck.insert(index,card)

		else:
			
			self.deck.insert(index,card)
			if silence == False:
				ansiprint(self.displayName, "added", "<blue>"+card.get("Name")+"</blue>", "to the deck.\n")
			if card.get("Upgraded") != True:
				for relic in self.relics:
					if relic.get("Name") == "Molten Egg" and card.get("Type") == "Attack":
						helping_functions.upgradeCard(self.deck.pop(index),place = "Deck")
					elif relic.get("Name") == "Toxic Egg" and card.get("Type") == "Skill":
						helping_functions.upgradeCard(self.deck.pop(index),place = "Deck")
					elif relic.get("Name") == "Frozen Egg" and card.get("Type") == "Power":
						helping_functions.upgradeCard(self.deck.pop(index),place = "Deck")

	def add_CardToHand(self,card,index:int=None,repeat:bool=False,silent:bool=False):
		try:
			card = card.copy()
			if index == None:
				index = len(self.hand)

			if len(self.hand) == 10:
				self.add_CardToDiscardpile(card)
				if card.get("Type") == "Curse" or card.get("Type") == "Status":
					ansiprint(self.displayName, "added", "<m>"+card.get("Name")+"</m> to the Discardpile because the Hand was full.\n")
				else:
					ansiprint(self.displayName, "added", "<blue>"+card.get("Name")+"</blue> to the Discardpile because the Hand was full.\n")
			else:
				if self.confused > 0 and type(card.get("Energy")) == int:
					
					card["Energy changed for the battle"] = True
					card["Energy"] = rd.randint(0,3)

				self.hand.insert(index,card)
				if silent == True:
					ansiprint(self.displayName, "added", "<blue>"+card.get("Name")+"</blue>", "to the hand.\n")

				if repeat == False:
					if "Agony" in card.get("Name"):
						self.add_CardToHand(card,repeat= True)
		except Exception as e:
			print(e,"Card To Hand")


	def add_CardToDrawpile(self,card,index:int=None):
		try:
			card = card.copy()
			if index == None:
				index = rd.randint(0,len(self.draw_pile))

			self.draw_pile.insert(index,card)

			if card["Type"] == "Curse" or card["Type"] == "Status":
				ansiprint(self.displayName, "added", "<m>"+card.get("Name")+"</m>", "to the Drawpile.\n")
			else:
				ansiprint(self.displayName, "added", "<blue>"+card.get("Name")+"</blue>", "to the Drawpile.\n")
		except Exception as e:
			print(e,"Card To Drawpile")


	def add_CardToDiscardpile(self,card,index=None,noMessage=False):
		try:
			card = card.copy()
			if index == None:
				index = len(self.discard_pile)
			
			self.discard_pile.insert(index,card)

			if noMessage == True:
				pass
			else:
				if card["Type"] == "Curse" or card["Type"] == "Status":
					ansiprint(self.displayName, "added", "<m>"+card.get("Name")+"</m>", "to the Discardpile.\n")
				else:
					ansiprint(self.displayName, "added", "<blue>"+card.get("Name")+"</blue>", "to the Discardpile.\n")
		except Exception as e:
			print(e,"Card To Discardpile")

	def add_CardToExhaustpile(self,card,index=None):
		try:
			card = card.copy()
			if index == None:
				index = len(self.exhaust_pile)

			if card.get("Name") == "Necronomicurse":
				ansiprint("<c>"+card.get("Name")+ "</c> can't be removed!")
				self.add_CardToHand(card)
			else:
				if self.strangeSpoon > 0 and rd.randint(0,1) == 0:
					add_CardToDiscardpile(card,index)
					ansiprint("<blue>"+card.get("Name")+"</blue> was discarded instead of exhausted because of <light-red>Strange Spoon</light-red>.")
				else:
					self.exhaust_pile.insert(index,card)

					ansiprint("<blue>"+card.get("Name")+"</blue> is now exhausted and removed from play.\n")
					if self.deadBranch > 0:
						randomCard = {k:v for k,v in entities.cards.items() if v.get("Owner") == self.name and v.get("Upgraded") == None}
						self.add_CardToHand(rd.choices(list(randomCard.items()))[0][1])
		except Exception as e:
			print(e,"Card to ExhaustPile")
	def add_potion(self,potion):
		
		sozu = False

		for relic in self.relics:
			if relic.get("Name") == "Sozu":
				sozu = True

		if sozu == True:
			ansiprint("You can't obtain any more <c>Potions</c> due to <light-red>Sozu</light-red>.")
		else:
			discardOptions = ["Yes","No"]
			
			if len(self.potionBag) == self.potionBagSize:
				ansiprint("You can't have more than",self.potionBagSize,"<c>Potions</c> in your <c>Potion Bag</c>.\n")
				
				self.showPotions()

				choice = input("Do you want to discard one of your current potions?(Yes/No)\n")
				while choice not in discardOptions:
					self.explainer_function(choice,answer=False)
					choice = input("Do you want to discard one of your current potions?(Yes/No)\n")

				if choice == "Yes":
					self.remove_Potion()
					self.add_potion(potion)
				elif choice == "No":
					print("You have chosen to not take any further potion.")
			else:
				self.potionBag.append(potion)
				ansiprint("<c>"+potion.get("Name")+"</c> is now in your <c>Potion Bag</c>.")
	
	def remove_Potion(self,index = None):
		
		while True:
			
			if index:
				choice = index
			else:
				self.showPotions()
				ansiprint("Which <c>Potion</c> do you want to remove from your <c>Potion Bag</c>?")
				choice = input ("Type the number:")
				choice = int(choice)-1
			try:
				
				if choice in range(len(self.potionBag)):
					
					ansiprint("<c>"+self.potionBag[choice]["Name"]+"</c> is removed from the <c>Potion Bag</c>.")
					self.potionBag.pop(choice)
					break

				else:
					print("Type the number of one of the potions shown.")
					pass
			except Exception as e:
				self.explainer_function(choice)
				print ("You have to type a number. remove_Potion\n")
				pass
	
	def add_relic(self,relic):

		self.relics.append(relic)

		ansiprint(self.displayName,"obtained <light-red>"+relic.get("Name")+"</light-red>.")

		if relic.get("Name") == "Strawberry":
			self.set_maxHealth(7)

		elif relic.get("Name") == "Pear":
			self.set_maxHealth(10)
	
		elif relic.get("Name") == "Mango":
			self.set_maxHealth(14)

		elif relic.get("Name") == "Lee's Waffle":
			self.set_maxHealth(7)
			self.heal(self.max_health)
			
		elif relic.get("Name") == "Potion Belt":
			self.potionBagSize += 2
			ansiprint(self.displayName,"can now hold",self.potionBagSize,"Potions.")

		elif relic.get("Name") == "War Paint":

			i = 0
			while i < 2:
				index = helping_functions.getRandomSpecifiedCardIndex(specifics = "Skill Upgrade",place ="Deck")
				if index or index == 0:
					self.removeCardsFromDeck(amount=1,removeType = "Upgrade",index = index)		
					i+=1
				else:
					break	

		elif relic.get("Name") == "Whetstone":
			
			i = 0
			while i < 2:
				index = helping_functions.getRandomSpecifiedCardIndex(specifics = "Attack Upgrade",place ="Deck")

				if index or index == 0:
					self.removeCardsFromDeck(amount=1,removeType = "Upgrade",index = index)	
					i+=1
				else:
					break	
		

		elif relic.get("Name") == "Old Coin":
			self.set_gold(300)
		
		elif relic.get("Name") == "Cauldron":
			
			random_potions = {k:v for k,v in potions.items() if v.get("Owner") == self.name or v.get("Owner") == "The Spire"}
			fivePotions = rd.choices(list(random_potions.items()),k=5)

			five_options = []
			for potion in fivePotions:
				three_options.append(potion[1])

			helping_functions.pickPotion(five_options)
	
		elif relic.get("Name") == "Ring of the Serpent":
			self.remove_Relic("Ring of the Snake")

		elif relic.get("Name") == "Empty Cage":
			
			self.removeCardsFromDeck(amount = 2,removeType = "Remove")

		elif relic.get("Name") == "Necronomicon":
			
			self.add_CardToDeck({"Name": "Necronomicurse","Type": "Curse","Rarity": "Special","Owner":"The Spire"})

		elif relic.get("Name") == "Face of Cleric":
			
			self.faceOfCleric = 1

		elif relic.get("Name") == "Mark of the Bloom":
			self.markOfTheBloom = 1

		elif relic.get("Name") == "Prayer Wheel":
			self.prayerWheel = 1


		elif relic.get("Name") == "Pandora's Box":
			i = 0
			while i < len(self.deck):
				if self.deck[i].get("Name") == "Strike" or self.deck[i].get("Name") == "Strike +" or self.deck[i].get("Name") == "Defend" or self.deck[i].get("Name") == "Defend +":
					self.removeCardsFromDeck(amount = 1,removeType = "Transform",index = i)
				else:
					i+=1

		elif relic.get("Name") == "Tiny House":
			random_potions = {k:v for k,v in potions.items() if v.get("Owner") == self.name or v.get("Owner") == "The Spire"}
			onePotion = rd.choices(list(random_potions.items()),k=5)

			one_option = []
			for potion in onePotion:
				one_option.append(potion[1])

			helping_functions.pickPotion(one_option)

			self.set_gold(50)
			self.set_maxHealth(5)

			tinyHouseCards = helping_functions.generateCardRewards()

			helping_functions.pickCard(tinyHouseCards,place= "Deck")

			index = helping_functions.getRandomSpecifiedCardIndex(specifics = "Upgrade",place ="Deck")
			if index or index == 0:
				self.removeCardsFromDeck(amount=1,removeType = "Upgrade",index = index)	
	
		elif relic.get("Name") == "Astrolabe":
			transformList = []
			i = 0
			while i < 3:
				self.showDeck()
				try:
					snap = input("Pick a card you want to transform.")
					snap = int(snap) -1
					if snap in range(len(self.deck)):
						if snap not in transformList:
							transformList.append(snap)
							i+=1
							
							#needs error handling in case there are less than 3 cards in the deck.
						else:
							ansiprint("You can't pick the same card twice.")
							
					else:
						ansiprint("Choose a number from a card within your deck.")
						

				except Exception as e:
					self.explainer_function(snap)
					print("You have to type a number. Astrolabe get")
					

			for index in transformList:
				self.removeCardsFromDeck(amount=1,removeType = "Transform",index = index)
				self.removeCardsFromDeck(amount=1,removeType = "Upgrade",index = index)


		elif relic.get("Name") == "Dolly's Mirror":

			while i < 1:
				self.showDeck()
				try:
					snap = input("Pick a card you want to duplicate.")-1
					snap = int(snap)-1
					if snap in range(len(self.deck)):
						self.add_CardToDeck(self.deck[snap])
						i+=1
						
					else:
						ansiprint("Choose a number from a card within your deck.")

				except Exception as e:
					self.explainer_function(snap)
					print("You have to type a number. Dolly's Mirror")
					

		elif relic.get("Name") == "Orrery":

			orreries = [[helping_functions.generateCardRewards(),"<blue>Card Reward 1</blue>"],[helping_functions.generateCardRewards(),"<blue>Card Reward 2</blue>"],[helping_functions.generateCardRewards(),"<blue>Card Reward 3</blue>"],[helping_functions.generateCardRewards(),"<blue>Card Reward 4</blue>"],[helping_functions.generateCardRewards(),"<blue>Card Reward 5</blue>"]] 

			while len(orreries)>0:
				i = 0
				for reward in orreries:
					ansiprint(str(i+1)+".",reward[1])
					i+=1
				print(str(i+1)+". Skip")

				try:
					snap = input("Pick up the card rewards")
					snap = int(snap)-1
					if snap in range(len(orreries)):
						deckCheck = len(self.deck)
						healthCheck = self.max_health
						helping_functions.pickCard(orreries[snap][0])
						if deckCheck < len(self.deck):
							orreries.pop(snap)
						elif healthCheck < self.max_health:
							orreries.pop(snap)

					elif snap == len(orreries):
						ansiprint("You decided to forgo any further rewards.")
						break

					else:
						print("You have to type one of the corresponding numbers.")

				except Exception as e:
					#print(e)
					self.explainer_function(snap)
					print("Type a number.")
			
		elif relic.get("Name") == "Calling Bell":
			
			self.add_CardToDeck({"Name": "Curse of the Bell","Type": "Curse","Rarity": "Special","Owner":"The Spire","Info":"<RED>Unplayable</RED>. Cannot be removed from your deck."})
			
			relic_commons = {k:v for k,v in entities.relics.items() if v.get("Rarity") == "Common"}
			relic_uncommons = {k:v for k,v in entities.relics.items() if v.get("Rarity") == "Uncommon"}
			relic_rares = {k:v for k,v in entities.relics.items() if v.get("Rarity") == "Rare"}

			callingBellRelics = []

			while True:
				callingBellRelics.append(rd.choices(list(relic_commons.items()))[0][1])
				callingBellRelics.append(rd.choices(list(relic_uncommons.items()))[0][1])
				callingBellRelics.append(rd.choices(list(relic_rares.items()))[0][1])

				for relic in callingBellRelics:
					if relic.get("Name") in entities.relics_seen_list:
						callingBellRelics = []
						continue
				break

			for relic in callingBellRelics:
				entities.relics_seen_list.append(relic.get("Name"))
				self.add_relic(relic)

		elif relic.get("Name") == "Bottled Flame":
			checkAttacks = [card for card in self.deck if card.get("Type") == "Attack"]
			
			if len(list(checkAttacks)) > 0:
				while True:
					self.showDeck()
					
					try:
						snap = input("Which Attack Card do you want to bottle?")
						snap = int(snap) -1
						if self.deck[snap].get("Type")== "Attack":
							self.deck[snap]["Innate"] = "True"
							break
						else:
							print("You have to choose one of your <red>Attacks</red> to bottle.")
						
					except Exception as e:
						self.explainer_function(snap)
						print("You have to type one of the corresponding numbers. Bottled Flame relic get")


			else:
				ansiprint("You just reveiced <light-red>Bottled Flame</light-red> but have no attacks that can be bottled.")
		
		elif relic.get("Name") == "Bottled Lightning":
			checkAttacks = [card for card in self.deck if card.get("Type") == "Skill"]
			if len(list(checkAttacks)) > 0:
				while True:
					self.showDeck()
					
					try:
						snap = input("Which Skill Card do you want to bottle?")
						snap = int(snap)-1
						if self.deck[snap].get("Type") == "Skill":
							self.deck[snap]["Innate"] = "True"
							break
						else:
							
							ansiprint("You have to choose one of your <green>Skills</green> to bottle.")
						
					except Exception as e:
						self.explainer_function(snap)
						#print(e,"You have to type one of the corresponding numbers of the cards in your deck. Bottled Lightning relic get")
						print("You have to type one of the corresponding numbers of the cards in your deck.")

			else:
				ansiprint("You just reveiced <light-red>Bottled Lightning</light-red> but have no <green>Skills</green> that can be bottled.")

		elif relic.get("Name") == "Bottled Tornado":
			checkAttacks = [card for card in self.deck if card.get("Type") == "Power"]
			if len(list(checkAttacks)) > 0:
				while True:
					self.showDeck()
					
					try:
						snap = input("Which Power do you want to bottle?")
						snap = int(snap)-1

						if self.deck[snap].get("Type")=="Power":
							self.deck[snap]["Innate"] = "True"
							break
						else:
							ansiprint("You have to choose one of your <blue>Powers</blue> to bottle.")
						
					except Exception as e:
						self.explainer_function(snap)
						#print(e,"You have to type one of the corresponding numbers of the cards in your deck. Bottled Tornado relic get")
						print("You have to type one of the corresponding numbers of the cards in your deck.")

			else:
				ansiprint("You just reveiced <light-red>Bottled Tornado</light-red> but have no power that can be bottled.")

		elif relic.get("Name") == "Red Key":
			self.redKey = True
			ansiprint("You just obtained the <red>Red Key</red>")
			if self.greenKey == True and self.blueKey == True:
				self.allKeys = True


		elif relic.get("Name") == "Green Key":
			self.greenKey = True
			ansiprint("You just obtained the <green>Green Key</green>")
			if self.redKey == True and self.blueKey == True:
				self.allKeys = True


		elif relic.get("Name") == "Blue Key":
			self.blueKey = True
			ansiprint("You just obtained the <blue>Blue Key</blue>")
			if self.redKey == True and self.greenKey == True:
				self.allKeys = True

	def remove_Relic(self,lostRelic):
		for relic in self.relics:
			if relic.get("Name") == lostRelic:
				ansiprint("<light-red>"+relic.get("Name")+"</light-red> was removed.")
				self.relics.pop(self.relics.index(relic))

	def set_metallicice(self,value):
		self.metallicize += value

		ansiprint(self.displayName, "receives",self.metallicize,"Block at the start of each turn.")

	def set_block_by_metallicice (self,value):
		
		self.block += self.metallicize
		ansiprint(self.displayName, "received",self.metallicize,"Block through Metallicize.")

	def set_platedArmor(self,value):
		self.platedArmor += value

		ansiprint(self.displayName, "receives",self.platedArmor,"block at the start of each turn.")

	def set_block_by_platedArmor(self,value):

		self.block += self.platedArmor
		ansiprint(self.displayName,"received",self.platedArmor,"Block through Plated Armor.")

	def damageCounter(self):
		self.damage_counter += 1
		
		for card in self.hand:
			
			if card["Name"] == "Masterful Stab":

				card["Energy changed for the battle"] = True
				card["Energy"] = card["Energy"]+self.damage_counter
				print(card["Name"],card["Energy"])

		for card in self.discard_pile:
			if card.get("Name") == "Masterful Stab":
				card["Energy changed for the battle"] = True
				card["Energy"] = card["Energy"]+self.damage_counter
				print(card["Name"],card["Energy"])
	

		for card in self.draw_pile:
			if card["Name"] == "Masterful Stab":
				card["Energy changed for the battle"] = True
				card["Energy"] = card["Energy"]+self.damage_counter
				print(card["Name"],card["Energy"])


		if self.platedArmor > 0:
			self.platedArmor -= 1
			ansiprint(self.displayName,"has been hit and has",self.platedArmor,"Plated Armor left.") 

		if self.centennialPuzzle > 0:			
			self.centennialPuzzle = 0
			self.draw(3)
			ansiprint("You've drawn three cards because of <light-red>Centennial Puzzle</light-red>")


	def discardCounter(self):
		self.discard_counter += 1
		
		for card in self.hand:
			if card["Name"] == "Eviscerate":
				card["This turn Energycost changed"] = True
				card["Energy"] = card["Energy"]-self.discard_counter
				if card["Energy"] < 0:
					card["Energy"] = 0

		for card in self.discard_pile:
			if card["Name"] == "Eviscerate":
				card["This turn Energycost changed"] = True
				card["Energy"] = card["Energy"]-self.discard_counter
				if card["Energy"] < 0:
					card["Energy"] = 0

		for card in self.draw_pile:
			if card["Name"] == "Eviscerate":
				card["This turn Energycost changed"] = True
				card["Energy"] = card["Energy"]-self.discard_counter
				if card["Energy"] < 0:
					card["Energy"] = 0

		if self.tingsha > 0:
			ansiprint("A random Enemy receive <red>3 Damage</red> because of <light-red>Tingsha</light-red>.")
			randomEnemy = rd.randint(0,len(entities.list_of_enemies)-1)
			entities.list_of_enemies[randomEnemy].receive_recoil_damage(3)
		
		if self.toughBandages > 0:

			self.blocking(3,unaffectedBlock=True)
			ansiprint("This happened because of <light-red>Tough Bandages</light-red>.")

		if self.hoveringKite > 0:
			self.gainEnergy(1)
			self.hoveringKite = 0

	def get_floor(self):
		try:
			floor = helping_functions.game_map[self.position[0]][self.position[1]]
		except Exception as e:
			print(e)
			print("Self Position[0]:", self.position[0],"Self Position[1]:",self.position[1])
		
		return floor

	def get_floorAndCoordinates(self):

		coordinates = (helping_functions.game_map[self.position[0]][self.position[1]],self.position[0],self.position[1])
		
		return coordinates

	def get_position(self):

		return self.position

	def show_drawpile(self):
		
		i = 0
		for card in self.draw_pile:
			if i+1 < 10:
				numberSpacing = "  "
			else:
				numberSpacing = " "
			
			lineSpacing = " " * (20-len(card.get("Name")))
			
			try:
				if card.get("Type") == "Attack":
					ansiprint(str(i+1)+"."+numberSpacing+"<red>"+card.get("Name")+"</red>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
				elif card.get("Type") == "Skill":
					ansiprint(str(i+1)+"."+numberSpacing+"<green>"+card.get("Name")+"</green>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
				elif card.get("Type") == "Power":
					ansiprint(str(i+1)+"."+numberSpacing+"<blue>"+card.get("Name")+"</blue>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
				elif card.get("Type") == "Curse":
					ansiprint(str(i+1)+"."+numberSpacing+"<m>"+card.get("Name")+"</m>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
				elif card.get("Type") == "Status":
					ansiprint(str(i+1)+"."+numberSpacing+"<light-cyan>"+card.get("Name")+"</light-cyan>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
			except Exception as e:
				print(e)
			
			i = i + 1


	def show_discardpile(self):

		i = 0
		for card in self.discard_pile:
			if i+1 < 10:
				numberSpacing = "  "
			else:
				numberSpacing = " "
			
			lineSpacing = " " * (20-len(card.get("Name")))
			
			try:
				if card.get("Type") == "Attack":
					ansiprint(str(i+1)+"."+numberSpacing+"<red>"+card.get("Name")+"</red>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
				elif card.get("Type") == "Skill":
					ansiprint(str(i+1)+"."+numberSpacing+"<green>"+card.get("Name")+"</green>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
				elif card.get("Type") == "Power":
					ansiprint(str(i+1)+"."+numberSpacing+"<blue>"+card.get("Name")+"</blue>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
				elif card.get("Type") == "Curse":
					ansiprint(str(i+1)+"."+numberSpacing+"<m>"+card.get("Name")+"</m>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
				elif card.get("Type") == "Status":
					ansiprint(str(i+1)+"."+numberSpacing+"<light-cyan>"+card.get("Name")+"</light-cyan>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
			except Exception as e:
				print(e)
			
			i = i + 1

	def show_exhaustpile(self):

		i = 0
		for card in self.discard_pile:
			if i+1 < 10:
				numberSpacing = "  "
			else:
				numberSpacing = " "
			
			lineSpacing = " " * (20-len(card.get("Name")))
			
			try:
				if card.get("Type") == "Attack":
					ansiprint(str(i+1)+"."+numberSpacing+"<red>"+card.get("Name")+"</red>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
				elif card.get("Type") == "Skill":
					ansiprint(str(i+1)+"."+numberSpacing+"<green>"+card.get("Name")+"</green>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
				elif card.get("Type") == "Power":
					ansiprint(str(i+1)+"."+numberSpacing+"<blue>"+card.get("Name")+"</blue>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
				elif card.get("Type") == "Curse":
					ansiprint(str(i+1)+"."+numberSpacing+"<m>"+card.get("Name")+"</m>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
				elif card.get("Type") == "Status":
					ansiprint(str(i+1)+"."+numberSpacing+"<light-cyan>"+card.get("Name")+"</light-cyan>"+lineSpacing+"<yellow>"+str(card.get("Energy"))+"</yellow>")
			except Exception as e:
				print(e)
			
			i = i + 1

	def set_gold(self,value,thievery = False):
		ectoplasm = False
		for relic in self.relics:
			if relic.get("Name") == "Ectoplasm":
				ectoplasm = True

		if ectoplasm and value > 0 and thievery == False:
			ansiprint("You can't earn gold because of <light-red>Ectoplasm</light-red>!")
		else:
			stolenGold = 0

			if thievery:

				self.gold -= value
				stolenGold += value
			    
				if self.gold <= 0:
					stolenGold += self.gold
					self.gold = 0

				ansiprint("")
				ansiprint(self.displayName,"lost",stolenGold,"Gold and has now only <yellow>"+str(self.gold)+" Gold</yellow> left!")
				return stolenGold
			else:
				self.gold += value
				ansiprint("")
				if self.gold < 0:
					self.gold = 0
				ansiprint(self.displayName,"received <yellow>"+str(value)+" Gold</yellow> and now has <yellow>"+str(self.gold)+" Gold</yellow>.")
				if value > 0 and self.bloodyIdol > 0:
					self.heal(5)
					ansiprint("You healed because you own a <red>Bloody</red> <light-red>Idol</light-red>.")


	def removeCardsFromDeck(self,amount:int =1,removeType: str = "Remove",purpleFire: bool = False,index = None):
		
		i = 0
		while i < amount:
			
			if index or index == 0:
				choice = index
			else:
				if removeType == "Upgrade":
					self.showDeck(noUpgrades = True)
				elif removeType == "Remove":
					self.showDeck(remove = True)
				else:
					self.showDeck()
				try:
					if removeType == "Transform":
						choice = input("Which card do you want to transform?\n")

					elif removeType == "Upgrade":
						choice = input("Which card do you want to upgrade?\n")
					
					elif removeType == "Remove":
						choice = input("Which card do you want to remove from your deck?\n")

					elif removeType == "Duplicate":
						choice = input("Which card do you want to duplicate?\n")

					else:
						print(removeType,"<-- What is this?\n")

					choice = int(choice)-1
				except:
					self.explainer_function(choice)
					print("You have to type a number. removeCardsFromDeck")
					continue
			try:
				if choice in range(len(self.deck)):
					if removeType == "Transform":
						ansiprint("<blue>"+self.deck[choice]["Name"]+"</blue> is transformed to...")
						helping_functions.transformCard(self.deck.pop(choice),"Deck",index)
					
					elif removeType == "Upgrade":
						if self.deck[choice].get("Upgraded") == True:
							ansiprint("You can only upgrade unupgraded cards. Try again!")
							continue
						elif self.deck[choice].get("Type") == "Curse":
							ansiprint("<m>Curses</m> can't be upgraded.")
							continue
						else:
							ansiprint("<blue>"+self.deck[choice]["Name"]+"</blue> is upgraded.")
							helping_functions.upgradeCard(self.deck.pop(choice),"Deck",index)

					elif removeType == "Remove":

						if self.deck[choice].get("Irremovable") == True:
							ansiprint("<m>"+self.deck[choice].get("Name")+"</m> can't be removed.")
							continue

						if self.deck[choice]["Name"] == "Parasite":
							ansiprint("<m>The Parasite</m> reeks and wretches as you attempt to <light-blue>remove it from your body</light-blue>. At the end you manage... but at what <red>price</red>?\n")
							self.set_maxHealth(-3)

						if purpleFire:
							ansiprint("<blue>"+self.deck[choice]["Name"]+"</blue> is removed from the deck.")
							offerCard = self.deck.pop(choice)
							return offerCard
						
						else:
							ansiprint("<blue>"+self.deck[choice]["Name"]+"</blue> is removed from the deck.")
							self.deck.pop(choice)

					elif removeType == "Duplicate":
						ansiprint("<blue>"+self.deck[choice]["Name"]+"</blue> is duplicated!")
						self.add_CardToDeck(self.deck[choice])
					i+=1

				else:
					print("Type the number of one of the cards in your deck shown.")
					pass
			except Exception as e:

				print ("You have to type a number.\n",e)
				pass
	

	def check_CardPlayPenalties(self):

		for card in self.hand:
			if card["Name"] == "Pain":
				self.receive_recoil_damage(1,directDamage = True)
				ansiprint("<m>"+card["Name"]+"</m> did this.")

		if self.hex > 0:
			if self.card_in_play[0].get("Type") != "Attack":
				self.add_CardToDrawpile({"Name": "Dazed","Ethereal": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire"})
	
	def check_CardPlayRestricions(self):

		for card in self.hand:
			if card["Name"] == "Normality" and self.card_counter > 3:
				ansiprint("While <m>"+card["Name"]+"</m> is in your hand, you can't play more than 3 cards per turn!")

	def cursesEndOfTurn(self):

		for card in self.hand:
			if card["Name"] == "Shame":
				self.set_frail(1)
				ansiprint("<m>"+card["Name"]+"</m> did this.")
			elif card["Name"] == "Regret":
				self.receive_recoil_damage(len(self.hand),directDamage = True)
				ansiprint("<m>"+card["Name"]+"</m> did this.")
			elif card["Name"] == "Doubt":
				self.set_weakness(1)
				ansiprint("<m>"+card["Name"]+"</m> did this.")
			elif card["Name"] == "Decay":
				self.receive_recoil_damage(2)
				ansiprint("<m>"+card["Name"]+"</m> did this.")
	
	def set_drawStrength(self,value):

		self.draw_strength += value

		ansiprint("You draw <light-green>"+str(self.draw_strength)+"</light-green> cards per turn.")

	def set_energyGain(self,value):

		self.energy_gain += value
		ansiprint("You have <yellow>"+str(self.energy_gain)+" Energy</yellow> available per turn!")

	def explainer_function(self,searchName,answer=True):
		if searchName == "San Antonio Spurs":
			self.set_gold(3000)
		elif searchName == "":
			pass
		else:
			try:
				if searchName in entities.cards:
					info = {k:v for k,v in entities.cards.items() if v.get("Name") == searchName}
					info = list(info.items())[0][1]
				
					ansiprint("\nCard | "+info.get("Name")+":",info.get("Info"),"<yellow>Energy</yellow>:",str(info.get("Energy"))+"\n")

				elif searchName in entities.potions:
					info = {k:v for k,v in entities.potions.items() if v.get("Name") == searchName}
					info = list(info.items())[0][1]
				
					ansiprint("\n<c>Potion</c> | "+"<c>"+info.get("Name")+"</c>:",info.get("Info")+"\n")

				elif searchName in entities.relics:
					info = {k:v for k,v in entities.relics.items() if v.get("Name") == searchName}
					info = list(info.items())[0][1]

					ansiprint("\n<light-red>Relic</light-red> | "+info.get("Name")+":",info.get("Info")+"\n")				
				
				elif searchName == "Save":
					if self.get_floor() == "Event":
						ansiprint("<light-blue>You can't save during Events because I can't figure out how to stop you from redoing them. Saving during fights works best!</light-blue>")
					elif self.get_floor() == "Fires":
						ansiprint("<light-blue>You can't save during Rest Sites because I can't figure out how to stop you from redoing them. Saving during fights works best!</light-blue>")
					elif self.get_floor() == "Shop$":
						ansiprint("<light-blue>You can't save during Shops because they somehow break. Saving during fights works best!</light-blue>")
					elif self.get_floor() == "Start":
						ansiprint("<light-blue>You can't save here just because. Saving during fights works best!</light-blue>")
					else:
						save_handlery.save_and_rave()
						print("The game has been saved to",str(Path.cwd())+"/slaythetextSave.dat")
						print("I know this message comes a little late but saving will always override your last save file.")
				else:
					
					while True:
						try:
							optionList = []
							
							for candidate in list(spelling_correction.candidates(searchName)):
								optionList.append(candidate)
							
							if len(optionList) == 0:
								ansiprint("This is neither a Card, a <light-red>Relic</light-red> or a <c>Potion</c>.")
								break

							elif len(optionList) == 1:
								self.explainer_function(optionList[0])
								break

							i = 0
							for thing in optionList:
								ansiprint(str(i+1)+".",thing)
								i+=1

							print(str(i+1)+". Skip")

							ansiprint("\nIs one of these the Card, <light-red>Relic</light-red> or <c>Potion</c> you were looking for?\n")
							snap = int(input("If yes type the corresponding number."))-1

							if snap in range(len(optionList)):
								self.explainer_function(optionList[snap])
								break
							elif snap == len(optionList):
								break
							else:
								pass
						except TypeError:
							break

						except Exception as e:
							if e == "object of type 'int' has no len()":
								break
							else:
								pass
								#print(e,"explainer_function issue")
								break
			
			except Exception as e:
				print(e,"This is neither a Card, a <light-red>Relic</light-red> or a <c>Potion</c>.")
				pass

	def show_status(self,event = False):
		status = "\n{} (<red>{}</red>/<red>{}</red>)".format(self.displayName,self.health,self.max_health)
		if event == False:
			status += " |<yellow> Energy: "+ str(self.energy)+"</yellow>"
			if self.block > 0:
				status += " |<green> Block: "+str(self.block)+"</green>"
			if self.weak > 0:
				status += " |<light-cyan> Weakness: "+str(self.weak)+"</light-cyan>"
			if self.vulnerable > 0:
				status += " |<light-cyan> Vulnerable: "+str(self.vulnerable)+"</light-cyan>"
			if self.frail > 0:
				status += " |<light-cyan> Frail: "+str(self.frail)+"</light-cyan>"
			if self.strength != 0:
				status += " |<red> Strength: "+str(self.strength)+"</red>"
			if self.dexterity != 0:
				status += " |<green> Dexterity: "+str(self.dexterity)+"</green>"
			if self.ritual > 0:
				status += " |<red> Ritual: "+str(self.ritual)+"</red>"
			if self.invulnerable > 0:
				status += " |<light-blue> Invulnerable: "+str(self.invulnerable)+"</light-blue>"
			if self.intangible > 0:
				status += " |<light-blue> Invincible: "+str(self.intangible)+"</light-blue>"
			if self.artifact > 0:
				status += " |<light-blue> Artifact: "+str(self.artifact)+"</light-blue>"
			if len(self.doubleDamage) > 0:
				status += " | Attacks deal Double Damage."
		# if self.metallicize > 0:
		# 	status += " |<light-blue> Metallicize: "+str(self.metallicize)+"</light-blue>"
		# if self.barricade == True:
		# 	status += " |<light-blue> Barricade</light-blue>"
		
		ansiprint(status)

	def get_smokebomb(self):
		
		if self.smokeBomb == True:
			self.smokeBomb = False
			return False
		else:
			return True

	def resetChar(self):
		self.target = None
		self.temp_energy = 0
		self.tempDraw = 0
		self.blockNextTurn = 0
		self.dontLoseBlock = 0

		self.invulnerable = 0
		self.buffer = 0
		self.discard_counter = 0
		self.exhaust_counter = 0

		self.cardsNextTurn = []
		self.doubleDamage = []

		self.cantDraw = 0
		self.cardsCostNothing = 0
		self.tempSpikes = 0

		self.intangible = 0

		self.discard_counter = 0
		self.temp_energy = 0
		self.tempDraw = 0
		
		self.burst = 0

		self.attack_counter = 0
		self.skill_counter = 0
		self.power_counter = 0

		self.card_counter = 0
		self.reducedDrawByTurns = []
		#powers
		self.accuracy = 0
		self.spikes = 0
		self.infiniteBlades = 0
		self.noxiousFumes = 0
		self.wellLaidPlans = 0
		self.thousandCuts = 0
		self.afterImage = 0
		self.envenom = 0
		self.toolsOfTheTrade = 0
		self.theBoot = False
		self.buffer = 0
		self.wraithForm = 0
		self.burst = 0
		self.weak = 0
		self.frail = 0
		self.vulnerable = 0
		self.entangled = 0
		self.block = 0
		self.artifact = 0
		
		self.magnetism = 0

		self.runicDome = 0
		self.velvetChoker = 0
		self.runicPyramide = 0
		self.confused = 0
		
		self.artOfWar = 0
		self.happyFlower = 0
		self.akabeko = 0

		self.energy_gain = 3
		self.draw_strength = 5
		self.sneckoSkull = 0
		self.meatOnTheBone = 0
		self.mercuryHourglass = 0
		self.mummifiedHand = 0

		self.strength = 0
		self.dexterity = 0

		self.sunDial = 0
		self.shuffle_counter = 0
		self.strikeDummy = 0
		self.birdFacedUrn = 0
		self.deadBranch = 0
		self.ginger = 0
		self.paperKrane = 0
		self.calipers = 0
		self.iceCream = 0
		self.incenseBurner = 0
		self.torii = 0
		self.turnip = 0
		self.unceasingTop = 0
		self.tingsha = 0
		self.toughBandages = 0
		self.medicalKit = 0
		self.blueCandle = 0
		self.chemicalX = 0
		self.strangeSpoon = 0
		self.frozenEye = 0
		self.hoveringKite = 0
		self.bloodyIdol = 0
		self.oddMushroom = 0
		self.theAbacus = 0
		self.pocketWatch = 0
		self.stoneCalender = 0
		self.handDrill = 0
		self.necronomicon = 0
		self.randomTarget = 0
		self.warpedTongs = 0
		self.nilrysCodex = 0
		self.centennialPuzzle = 0
		self.tungstenRod = 0
		self.wristBlade = 0
		self.strengthDecrease = []
		self.hex = 0
		self.constriction = 0

		self.hand = []
		self.discard_pile = []
		self.exhaust_pile = []
		self.draw_pile = []