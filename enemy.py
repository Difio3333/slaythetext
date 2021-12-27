import random as rd
import entities
import math
import helping_functions
from ansimarkup import parse, ansiprint

class Enemy():
	def __init__(self, name:str = None, max_health: int = 0, intentions: list = None,
		
		intention_logic:list = None, on_hit_or_death:list = None, block: int = 0,
		
		weak: int = 0, vulnerable: int = 0, poison: int = 0,

		strength: int = 0, invulnerable: int = 0,

		ritual: int = 0, artifact: int = 0, metallicize: int = 0, platedArmor: int = 0, barricade: bool=False, regen: int = 0,

		alive: bool = True, minion: bool = False, leader: bool = False, boss: bool = False, fading6 = False, painfullStabs: bool = False, slow: bool = False, intangiblePower: bool = False,

		cardTypeToLookOutFor: str = None, modeshift: int = 0, spireBroAttacked: bool = False

		):
		
		self.codeName = name
		self.name = "<red>" + name + "</red>"
		self.identifier = name + str(rd.randint(0,999999))
		self.max_health = max_health
		self.health = self.max_health

		if intentions == None:
			self.intentions = []
		else:
			self.intentions = intentions
		
		if intention_logic == None:
			self.intention_logic = []
		else:
			self.intention_logic = intention_logic
		
		if on_hit_or_death == None:
			self.on_hit_or_death = []
		else:
			self.on_hit_or_death = on_hit_or_death

		self.block = block		
		self.leader = leader
		self.weak = weak
		self.vulnerable = vulnerable
		self.poison = poison

		self.strength = strength
		self.invulnerable = invulnerable
		self.ritual = ritual

		self.alive = alive
		self.minion = "I am no minion"
		self.boss = "I am no boss"
		
		self.modeshift = modeshift
		
		self.tracker = 0
		self.runaway = False
		self.temp_strength = 0
		self.strengthChange = 0
		self.corpseExploding = False

		self.painfullStabs = painfullStabs

		self.artifact = artifact
		self.metallicize = metallicize
		self.platedArmor = platedArmor
		self.barricade = barricade

		self.intangible = 0
		self.cardTypeToLookOutFor = cardTypeToLookOutFor
		self.regen = regen

		self.turnCounter = 0
		self.choke = 0
		self.stolenGold = 0
		self.stolenCard = []

		self.sadisticNature = 0
		self.damageCounter = 0

		self.move = None
		self.turnMarker = 0

		self.lifelink = False
		self.fading6 = fading6

		self.counter = 0
		self.slow = slow
		self.intangiblePower = intangiblePower
		self.spireBroAttacked = spireBroAttacked
		self.heartVincibility = 0
		self.moveOneSpree = 0
		self.moveTwoSpree = 0
		self.moveThreeSpree = 0

	def chooseMove(self):
		if helping_functions.turn_counter == 1:
			self.set_intention_logic()
			
		
		self.move = self.determine_choice(helping_functions.turn_counter)

	def turn(self,turn_counter):
		
		self.turnCounter = turn_counter
		
		if self.poison > 0:
			self.handle_poison()
		
		self.specialBegginingOfTurnEffects()

		entities.check_if_enemy_dead()

		if self.regen > 0:
			self.heal(self.regen)
			
		if self.barricade == False:
			self.block = 0
	
		self.action(self.move)

		self.effect_counter_down()

		self.endOfTurnEffects()
	
	def specialBegginingOfTurnEffects(self):
		
		if self.fading6 == True:
			if self.counter == 6:
				self.alive = False		
			self.counter +=1

		self.heartVincibility = 0

	def determine_choice(self,turn_counter):

		if self.intention_logic[0][0] == "Random":

			choice = self.intentions[self.intention_logic[1][turn_counter-1]]

		elif self.intention_logic[0][0] == "First Move Set":
			if turn_counter == 1:
				choice = self.intention_logic[1][0]

			else:
				choice = self.intentions[turn_counter % len(self.intentions)]

		elif self.intention_logic[0][0] == "Spiker":
			if self.counter < 6:
				choice = self.intentions[self.intention_logic[1][turn_counter-1]]
				if choice == "SpikeUp 2":
					self.counter += 1
			else:
				choice = 9

		elif self.intention_logic[0][0] == "The Maw":
			if turn_counter == 1:
				choice = "Roar 5"
			else:
				if self.move == "Roar 5" or self.move == "Gloat 5":
					if rd.randint(0,1) == 0:
						choice = 30
					else:
						snack = str(math.ceil(turn_counter/2))
						choice = "Multiattack 5*"+snack

				elif self.move == 30:
					if rd.randint(0,1) == 0:
						choice = "Gloat 5"
					else:
						snack = str(math.ceil(turn_counter/2))
						choice = "Multiattack 5*"+snack
				else:
					choice = "Gloat 5"

		elif self.intention_logic[0][0] == "Mystic":
			heal = False
			for enemy in entities.list_of_enemies:
				if enemy.max_health - enemy.health >= 20:
					heal = True

			if self.moveThreeSpree < 3 and heal == True:
				
				self.moveOneSpree = 0
				self.moveTwoSpree = 0
				self.moveThreeSpree += 1
				choice = "MysticHeal 20"

			else:
				
				if rd.randint(1,10) < 5:
					if self.moveOneSpree == 0:
						self.moveOneSpree += 1
						self.moveTwoSpree = 0
						self.moveThreeSpree = 0
						choice = "Fell 9/2"
					else:
						self.moveOneSpree = 0
						self.moveTwoSpree += 1
						self.moveThreeSpree = 0
						choice = "MysticBuff"
				else:
					if self.moveTwoSpree < 2:
						self.moveOneSpree = 0
						self.moveTwoSpree += 1
						self.moveThreeSpree = 0
						choice = "MysticBuff"

					else:
						self.moveOneSpree += 1
						self.moveTwoSpree = 0
						self.moveThreeSpree = 0
						choice = "Fell 9/2"
		
		elif self.intention_logic[0][0] == "Centurion":
			if len(entities.list_of_enemies) > 1:
				if rd.randint(1,100) <= 35:
					choice = 14
				else:
					choice = "CenturionDefendAlly"

			else:

				if rd.randint(1,100) <= 35:
					choice = 14
				else:
					choice = "Multiattack 7*3" 

			if self.moveThreeSpree < 3 and heal == True:
				
				self.moveOneSpree = 0
				self.moveTwoSpree = 0
				self.moveThreeSpree += 1
				choice = "MysticHeal 20"

			else:
				
				if rd.randint(1,10) < 5:
					if self.moveOneSpree == 0:
						self.moveOneSpree += 1
						self.moveTwoSpree = 0
						self.moveThreeSpree = 0
						choice = "Fell 9/2"
					else:
						self.moveOneSpree = 0
						self.moveTwoSpree += 1
						self.moveThreeSpree = 0
						choice = "MysticBuff"
				else:
					if self.moveTwoSpree < 2:
						self.moveOneSpree = 0
						self.moveTwoSpree += 1
						self.moveThreeSpree = 0
						choice = "MysticBuff"

					else:
						self.moveOneSpree += 1
						self.moveTwoSpree = 0
						self.moveThreeSpree = 0
						choice = "Fell 9/2"
		

		elif self.intention_logic[0][0] == "Spire Growth":
			if turn_counter == 1:
				choice = "Constrict 12"
			else:
				if entities.active_character[0].constriction == 0 and self.move != "Constrict 12":
					choice = "Constrict 12"
				else:
					choice = self.intentions[self.intention_logic[1][turn_counter-1]]

		elif self.intention_logic[0][0] == "Writhing Mass":
			if turn_counter == 1:
				snap = rd.randint(0,3)
				if snap == 0:
					choice = "Thrash 15/16"
				elif snap == 1:
					choice = "Wither 10/2"
				elif snap == 2:
					choice = "Multiattack 9*3"
				elif snap == 3:
					choice = 38
			else:
				choice = self.intentions[self.intention_logic[1][turn_counter-1]]

			if self.counter > 0 and choice == "Implant":
				self.determine_choice(turn_counter+1)

			if choice == "Implant":
				self.counter += 1
			

		elif "Gremlin Leader" in self.intention_logic[0][0]:

			if len(entities.list_of_enemies) == 1:
				if self.move == "Rally":
					choice = "Multiattack 6*3"
				elif self.move == "Multiattack 6*3":
					choice = "Rally"
				else:
					if rd.randint(1,100) > 25:
						choice = "Rally"
					else:
						choice = "Multiattack 6*3"

			elif len(entities.list_of_enemies) == 2:
				if self.move == "Encourage 5/10":
					if rd.randint(1,100) >= 50:
						choice = "Rally"
					else:
						choice = "Multiattack 6*3"

				elif self.move == "Multiattack 6*3":
					if rd.randint(1,1000) <= 625:
						choice = "Rally"
					else:
						choice = "Encourage 5/10"
				else:
					choice = "Encourage 5/10"

			else:

				if rd.randint(1,100) < 66:
					choice = "Encourage 5/10"	
				else:
					choice = "Multiattack 6*3"
		
		elif "The Champ Phase 1" in self.intention_logic[0][0]:
			
			if self.health < self.max_health // 2:
				choice = "ChampAnger"

			else:
				if turn_counter % 4 == 0:
					choice = "VentSteam 2"
				
				else:
					champMove = rd.randint(1,100)

					if champMove <= 15:
						choice = "DefensiveStance 20|7"
						if self.metallicize == 14:
							choice = "Gloat 4"
					elif champMove <= 30:
						choice = "Gloat 4"
					elif champMove <= 55:
						choice = "Smash 14/2"
					else:
						choice = 18


				if choice == self.move:
					if self.move == "DefensiveStance 20|7":
						choice = "Gloat 4"
					elif self.move == "Gloat 4":
						choice = "Smash 14/2"
					elif self.move == "Smash 14/2":
						choice = 18
					elif self.move == 18:
						choice = "Smash 14/2"
					elif self.move == "VentSteam 2":
						pass
					else:
						print("Issue in The Champ Phase 1. Please report what is written here:",choice,"\nThanks!")

		elif "The Champ Phase 2" in self.intention_logic[0][0]:
			if (turn_counter - self.turnMarker) % 3 == 0:
				choice = "Multiattack 10*2"

			else:

				if turn_counter % 4 == 0:
					choice = "VentSteam 2"
				
				else:
					champMove = rd.randint(1,100)

					if champMove <= 15:
						choice = "DefensiveStance 20|7"
						if self.metallicize == 14:
							choice = "Gloat 4"
					elif champMove <= 30:
						choice = "Gloat 4"
					elif champMove <= 55:
						choice = "Smash 14/2"
					else:
						choice = 18


				if choice == self.move:
					if self.move == "DefensiveStance 20|7":
						choice = "Gloat 4"
					elif self.move == "Gloat 4":
						choice = "Smash 14/2"
					elif self.move == "Smash 14/2":
						choice = 18
					elif self.move == 18:
						choice = "Smash 14/2"
					elif self.move == "VentSteam 2":
						pass
					else:
						print("Issue in The Champ Phase 2. Please report what is written here:",choice,"\nThanks!")

		elif "The Collector" in self.intention_logic[0][0]:
			if turn_counter == 1:
				choice = "Spawn Torch Heads"

			elif turn_counter == 4:
				choice = "MegaDebuff 5"

			else:
				collectorMoves = rd.randint(1,100)
				if len(entities.list_of_enemies) < 3:
					if collectorMoves <= 25:
						choice = "Spawn Torch Heads"
					
					elif collectorMoves <= 55:
						choice = "TorchBuff 5|23"
						if self.move == "TorchBuff 5|23":
							if rd.randint(1,100)<= 40:
								choice = "Spawn Torch Heads"
							else:
								choice = 21
					else:
						choice = 21
						if self.move == 21:
							if rd.randint(1,100)<= 48:
								choice = "Spawn Torch Heads"
							else:
								choice = "TorchBuff 5|23"
				
				else:
					if collectorMoves <= 70:
						choice = 21
						if self.move == 21:
							choice = "TorchBuff 5|23"
					else:
						choice = "TorchBuff 5|23"
						if self.move == "TorchBuff 5|23":
							choice = 21

		elif "Raptomancer" in self.intention_logic[0][0]:
			if turn_counter == 1:
				choice = "SpawnDaggers"

			else:
				if len(entities.list_of_enemies) >= 3:
					mover = rd.randint(0,2)

					if mover == 0 or mover == 1:
						choice = "SnakeStrike 16*2 1"

					else:
						choice = 34
				else:
					mover = rd.randint(0,2)

					if mover == 0:
						choice = "SpawnDaggers"
					elif mover == 1:
						choice = "SnakeStrike 16*2 1"
					elif mover == 2:
						choice = 34
				


		elif self.intention_logic[0][0] == "Time Eater":
			if self.health < math.floor(self.max_health / 2):
				choice = "Haste"
			else:
				choice = self.intentions[self.intention_logic[1][turn_counter-1]]


		elif self.intention_logic[0][0] == "Spire Shield":
			if turn_counter % 3 == 0:
				choice = "Thrash 38/99"
			
			elif turn_counter % 2 == 0:
				if self.move == "Bash 12/1":
					choice = "Fortify 30"

				elif self.move == "Fortify 30":
					choice = "Bash 12/1"

				else:
					if rd.randint(0,1) == 0:
						choice = "Bash 12/1"
					else:
						choice = "Fortify 30"					
			else:
				if self.move == "Bash 12/1":
					choice = "Fortify 30"

				elif self.move == "Fortify 30":
					choice = "Bash 12/1"

				else:
					if rd.randint(0,1) == 0:
						choice = "Bash 12/1"
					else:
						choice = "Fortify 30"


		elif self.intention_logic[0][0] == "Corrupt Heart":
			if turn_counter == 1:
				choice = "Debilitate 2"
			else:
				if turn_counter >= 4:
					if turn_counter % 3 - 1 == 0:
						choice = "HeartBuff"
					else:
						if self.move == "Multiattack 2*15":
							choice = 45
						elif self.move == 45:
							choice = "Multiattack 2*15"
						else:
							if rd.randint(0,1) == 0:
								choice = 45
							else:
								choice = "Multiattack 2*15"

				else:
					if self.move == "Multiattack 2*15":
						choice = 45
					elif self.move == 45:
						choice = "Multiattack 2*15"
					else:
						if rd.randint(0,1) == 0:
							choice = 45
						else:
							choice = "Multiattack 2*15"

		else:
					
			choice = self.intentions[self.intention_logic[1][turn_counter-1]]

		return choice

	def action(self, action):

		if type(action) == int:
			stabbingCheck = entities.active_character[0].health
			entities.active_character[0].receive_damage(self.attack(action))
			if self.painfullStabs == True:
				if entities.active_character[0].health < stabbingCheck:
					entities.active_character[0].add_CardToDrawpile({"Name": "Wound", "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>."},index=rd.randint(0,len(entities.active_character[0].draw_pile)-1))

		elif type(action) == str:
			if "Block" in action:
				self.blocking(int(action.split(" ")[1]))
			
			elif "Multiattack" in action:
				
				i = 0
				if self.name == "<red>Book of Stabbing</red>":
					while i < helping_functions.turnCounter+1:
						stabbingCheck = entities.active_character[0].health
						
						entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("*")[0])))
						i += 1

						if entities.active_character[0].health < stabbingCheck:
							entities.active_character[0].add_CardToDrawpile({"Name": "Wound", "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>."},index=rd.randint(0,len(entities.active_character[0].draw_pile)-1))

				else:
					while i < int(action.split(" ")[1].split("*")[1]):
						entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("*")[0])))
						i += 1

			elif "Weak" in action:
				entities.active_character[0].set_weakness(int(action.split(" ")[1]))
			
			elif "Vulnerable" in action:
				entities.active_character[0].set_vulnerable(int(action.split(" ")[1]))
			
			elif "Frail" in action:
				entities.active_character[0].set_frail(int(action.split(" ")[1]))
			
			elif "Ritual" in action:
				self.set_ritual(int(action.split(" ")[1]))
			
			elif "Grow" in action:
				self.strength += int(action.split(" ")[1])
			
			elif "Rake" in action:
				entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("/")[0])))
				entities.active_character[0].set_weakness(int(int(action.split(" ")[1].split("/")[1])))
			
			elif "Scrape" in action:
				entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("/")[0])))
				entities.active_character[0].set_vulnerable(int(action.split(" ")[1].split("/")[1]))
			
			elif "Thrash" in action:
				entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("/")[0])))
				self.blocking(int(action.split(" ")[1].split("/")[1]))
			
			elif "Bellow" in action:
				
				self.set_strength(int(action.split(" ")[1].split("|")[0]))
				self.blocking(int(action.split(" ")[1].split("|")[1]))
			
			elif "Escape" in action:
				self.runaway = True
				ansiprint(self.name,"runs away!")
				entities.enemy_runs_away()

			elif "ScouringWhip" in action:
				entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("/")[0])))
				
				i = 0
				while i < int(action.split(" ")[1].split("/")[1]):
					entities.active_character[0].add_CardToDiscardpile({"Name": "Wound", "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>."})
					i += 1

				if self.codeName == "Taskmaster":
					self.set_strength(1)

			elif "CorrosiveSpit" in action:

				entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("/")[0])))
				i = 0
				while i < int(int(action.split(" ")[1].split("/")[1])):
					entities.active_character[0].add_CardToDiscardpile({"Name": "Slimed", "Energy": 1, "Exhaust": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire"})
					i += 1
			
			elif "GoopSpray" in action:

				i = 0
				while i < int(int(action.split(" ")[1])):
					entities.active_character[0].add_CardToDiscardpile({"Name": "Slimed", "Energy": 1, "Exhaust": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire"})
					i += 1

			elif "Spawn Orbs" in action:
				i = 0
				while i < 2:
					enemy = "Bronze Orb"
					entities.list_of_enemies.append(Enemy(name = entities.enemies[enemy].get("Name"),max_health = rd.randint(entities.enemies[enemy].get("Health")[0],entities.enemies[enemy].get("Health")[1]),intentions = entities.enemies[enemy].get("Intentions"),intention_logic = entities.enemies[enemy].get("Intentions_Logic"),on_hit_or_death = entities.enemies[enemy].get("On_hit_or_death")))
					i+=1
				ansiprint(self.name,"just spawned 2 <red>Bronze Orbs</red>.")

			elif "Support Automaton" in action:
				for enemy in entities.list_of_enemies:
					if enemy.name == "<red>Bronze Automaton</red>":
						enemy.blocking(12)

			elif "Stasis" in action:
				self.stealCard("Drawpile")
				self.intention_logic = [["Random"],list(helping_functions.nchoices_with_restrictions([0.3,0.7,0],{0:2,1:2,2:1}))]

			elif "Entangle" in action:
				entities.active_character[0].set_entangled(1)
				ansiprint(self.name,"entangles you. You may not use attacks next turn.!")
				self.intentions = [14, "Scrape 9/2"]
				self.intention_logic = [["Random"],list(helping_functions.nchoices_with_restrictions([0.45,0.55],{0:2,1:2}))]

			elif "Smash" in action:

				entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("/")[0])))
				entities.active_character[0].set_vulnerable(int(action.split(" ")[1].split("/")[1]))
				entities.active_character[0].set_frail(int(action.split(" ")[1].split("/")[1]))
			
			elif "Wither" in action:

				entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("/")[0])))
				entities.active_character[0].set_weakness(int(action.split(" ")[1].split("/")[1]))
				entities.active_character[0].set_vulnerable(int(action.split(" ")[1].split("/")[1]))

			elif "Steal" in action:
				
				entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("/")[0])))
				self.steal_gold(int(action.split(" ")[1].split("/")[1]))

			elif "Lunge" in action:

				entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("/")[0])))
				self.steal_gold(int(action.split(" ")[1].split("/")[1]))

				if "Looter" in self.name:
					self.intentions = ["SmokeBomb 6"]

				elif "Mugger" in self.name:
					self.intentions = ["SmokeBomb 17"]

				self.intention_logic = [["Random"],[0] * 100]

			elif "Fell" in action:
				entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("/")[0])))
				entities.active_character[0].set_frail(int(action.split(" ")[1].split("/")[1]))

			elif "Suck" in action:
				drainCheck = entities.active_character[0].health
				entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1])))
				if drainCheck > entities.active_character[0].health:
					healing = drainCheck - entities.active_character[0].health
					self.heal(healing)
			
			elif "CenturionDefendAlly" in action:
				
				try:
					entities.list_of_enemies[1].blocking(20)
				except Exception as e:
					self.blocking(20)

			elif "MysticBuff" in action:

				for enemy in entities.list_of_enemies:
					enemy.set_strength(4)

			elif "MysticHeal" in action:
					
				for enemy in entities.list_of_enemies:
					enemy.heal(int(action.split(" ")[1]))
				
			elif "SmokeBomb" in action:
				self.blocking(int(action.split(" ")[1]))
				
				self.intentions = ["Escape"]
				self.intention_logic = [["Random"],[0] * 100]

			elif "Perplexing Glare" in action:
				entities.active_character[0].set_confused()

			elif "Split" in action:
				
				if "Boss" in self.name:
					entities.list_of_enemies.append(Enemy("Large Spike Slime",self.health,["CorrosiveSpit 18/2","Frail 3"],[["Random"],list(helping_functions.nchoices_with_restrictions([0.3,0.7],{0:2,1:1}))],[["Split","Hit"]]))
					entities.list_of_enemies.append(Enemy("Large Acid Slime",self.health,[18,"CorrosiveSpit 12/2","Weak 2"],[["Random"],list(helping_functions.nchoices_with_restrictions([0.3,0.4,0.3],{0:1,1:2,2:1}))],[["Split","Hit"]]))
				
				elif "Spike" in self.name: 
					entities.list_of_enemies.append(Enemy("Medium Spike Slime",self.health,["CorrosiveSpit 10/1","Frail 1"],[["Random"],list(helping_functions.nchoices_with_restrictions([0.3,0.7],{0:2,1:1}))]))
					entities.list_of_enemies.append(Enemy("Medium Spike Slime",self.health,["CorrosiveSpit 10/1","Frail 1"],[["Random"],list(helping_functions.nchoices_with_restrictions([0.3,0.7],{0:2,1:1}))]))
				elif "Acid" in self.name:
					entities.list_of_enemies.append(Enemy("Medium Acid Slime",self.health,[12,"CorrosiveSpit 8/1","Weak 1"],[["Random"],list(helping_functions.nchoices_with_restrictions([0.4,0.4,0.2],{0:2,1:2,2:1}))]))
					entities.list_of_enemies.append(Enemy("Medium Acid Slime",self.health,[12,"CorrosiveSpit 8/1","Weak 1"],[["Random"],list(helping_functions.nchoices_with_restrictions([0.4,0.4,0.2],{0:2,1:2,2:1}))]))
				

				self.alive = False
				entities.check_if_enemy_dead()
				

			elif "Protect" in action:
				if len(entities.list_of_enemies) == 1:
					
					self.blocking(int(action.split(" ")[1]))
				elif len(entities.list_of_enemies) > 1:					
					while True:
						i = rd.randint(0,len(entities.list_of_enemies))
						try:
							if entities.list_of_enemies[i].identifier == self.identifier:
								continue
							else:
								entities.list_of_enemies[i].blocking(int(action.split(" ")[1]))
								break
						except:
							entities.list_of_enemies[0].blocking(int(action.split(" ")[1]))
							break

			elif "VentSteam" in action:

				entities.active_character[0].set_vulnerable(int(action.split(" ")[1]))
				entities.active_character[0].set_weakness(int(action.split(" ")[1]))

				#wrong!
			elif "DefensiveMode" in action:
				
				self.on_hit_or_death = [["Spikes " + action.split(" ")[1],"Hit"]]
				ansiprint(self.name,"now has Spikes " + action.split(" ")[1] + ".")

			elif "TwinSlam" in action:
				i = 0
				while i < int(action.split(" ")[1].split("*")[1]):
					self.attack(int(action.split(" ")[1].split("*")[0]))
					i += 1
				self.tracker += 1
				self.modeshift = 40 + self.tracker*10
				self.intentions = ["Block 9",36,"VentSteam 2","Multiattack 5*4"]
				self.intention_logic = [["Random"],[3]*(self.turnCounter - 1) + [3,0,1,2]*25] # this is a test!
				self.on_hit_or_death = [["Modeshift","Hit"]]
				self.move = "VentSteam 2"
				ansiprint(self.name,"switches back to its offensive form!")

			elif "Divider" in action:
				i = 0
				while i < int(entities.active_character[0].health // 12) + 1:
					entities.active_character[0].receive_damage(self.attack(6))
					i += 1

			elif "Sear" in action:
				entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("/")[0])))
				i = 0
				if self.tracker == 0:
					while i < int(int(action.split(" ")[1].split("/")[1])):
						entities.active_character[0].add_CardToDiscardpile({"Name": "Burn", "DiscardDamage": 2, "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>. At the end of your turn, take <red>2 damage</red>."})
						i += 1
					
				elif self.tracker > 0:
					while i < int(int(action.split(" ")[1].split("/")[1])):
						entities.active_character[0].add_CardToDiscardpile({"Name": "Burn +", "DiscardDamage": 4, "Type": "Status", "Rarity": "Enemy","Upgraded": True,"Owner":"The Spire","Info":"<RED>Unplayable</RED>. At the end of your turn, take <red>4 damage</red>."})
						i += 1
					
			elif "Laser" in action:
				entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("/")[0])))
				i = 0
				while i < int(int(action.split(" ")[1].split("/")[1])):
					entities.active_character[0].add_CardToDiscardpile({"Name": "Burn", "DiscardDamage": 2, "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>. At the end of your turn, take <red>2 damage</red>."})
					i += 1

			elif "Inferno" in action:
				i = 0
				while i < int(action.split(" ")[1].split("*")[1]):
					entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("*")[0])))
					i += 1

				i = 0
				while i < int(int(action.split(" ")[1].split("*")[0])):
						entities.active_character[0].add_CardToDiscardpile({"Name": "Burn +", "DiscardDamage": 4, "Type": "Status", "Rarity": "Enemy","Upgraded": True,"Owner":"The Spire","Info":"<RED>Unplayable</RED>. At the end of your turn, take <red>4 damage</red>."})
						i += 1
				ansiprint(entities.active_character[0].name,"now has",action.split(" ")[1].split("*")[0], entities.burnPlus["Name"], "in the discard pile.")
				self.tracker = 1
				
			elif "SkullBash" in action:
				entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("/")[0])))
				entities.active_character[0].set_vulnerable(int(action.split(" ")[1].split("/")[1]))

			elif "Drain" in action:
				self.set_strength(int(action.split(" ")[1].split("/")[0]))
				entities.active_character[0].set_weakness(int(action.split(" ")[1].split("/")[1]))

			elif "Enrage" in action:
				self.set_CardTypeToLookOutFor("Skill Strength"+" "+action.split(" ")[1])

			elif "Hex" in action:
				entities.active_character[0].set_hex()

			elif "SiphonSoul" in action:
				entities.active_character[0].set_strength(-int(action.split(" ")[1]))				
				entities.active_character[0].set_dexterity(-int(action.split(" ")[1]))

			elif "Asleep" in action:
				if int(action.split(" ")[1]) > 1:
					self.intentions = ["Asleep " + str(int(action.split(" ")[1]) - 1)]
				elif int(action.split(" ")[1]) == 1:
					self.intentions = ["Wake Up",20,"SiphonSoul 2"]
					self.intention_logic = [["Random"],[0,0,0]+[1,1,2]*32]
					self.metallicize = 0
			
			elif "Bolt" in action:
				i = 0
				while i < int(action.split(" ")[1]):
					entities.active_character[0].add_CardToDiscardpile({"Name": "Dazed","Ethereal": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire"})
					i += 1
			
			elif "Fly" in action:
				ansiprint(self.name,"is flying again!")
				self.intentions = ["Multiattack 1*6","Grow 1",14]
				self.intention_logic = [["Random"],list(helping_functions.nchoices_with_restrictions([0.5,0.3,0.2],{0:2,1:1,2:1}))]
				self.on_hit_or_death = [["Fly 4","Hit"]]


			elif "Encourage" in action:
				for enemy in entities.list_of_enemies:
					enemy.blocking(int(action.split(" ")[1].split("/")[1]))
					enemy.set_strength(int(action.split(" ")[1].split("/")[0]))
			
			elif "Rally" in action:

				i = 0
				while i < 2:
					randomGremlin = rd.randint(0,4)

					if randomGremlin == 4:
						enemy = "Gremlin Wizard"
						entities.list_of_enemies.append(Enemy(name = entities.enemies[enemy].get("Name"),max_health = rd.randint(entities.enemies[enemy].get("Health")[0],entities.enemies[enemy].get("Health")[1]),intentions = entities.enemies[enemy].get("Intentions"),intention_logic = [["Random"],[0]*(helping_functions.turn_counter+2)+[1]*98],on_hit_or_death = entities.enemies[enemy].get("On_hit_or_death")))
					else:
						if randomGremlin == 0:
							enemy = "Fat Gremlin"   			
						elif randomGremlin == 1:
							enemy = "Mad Gremlin"
						elif randomGremlin == 2:
							enemy = "Shield Gremlin"
						elif randomGremlin == 3:
							enemy = "Sneaky Gremlin"
						
						entities.list_of_enemies.append(Enemy(name = entities.enemies[enemy].get("Name"),max_health = rd.randint(entities.enemies[enemy].get("Health")[0],entities.enemies[enemy].get("Health")[1]),intentions = entities.enemies[enemy].get("Intentions"),intention_logic = entities.enemies[enemy].get("Intentions_Logic"),on_hit_or_death = entities.enemies[enemy].get("On_hit_or_death")))
					
					i+=1
				ansiprint(self.name,"just spawned",entities.list_of_enemies[-1].name,"and",entities.list_of_enemies[-2].name+".")

			elif "SpawnDaggers" in action:

				i = 0
				while i < 2:
					enemy = "Dagger"
					entities.list_of_enemies.append(Enemy(name = entities.enemies[enemy].get("Name"),max_health = rd.randint(entities.enemies[enemy].get("Health")[0],entities.enemies[enemy].get("Health")[1]),intentions = entities.enemies[enemy].get("Intentions"),intention_logic = [["Random"],[0]*(helping_functions.turn_counter +1)+[1,1,1,1,1,1,1,1]]))
					i += 1

			elif "SnakeStrike" in action:
				i = 0
				while i < int(action.split(" ")[1].split("*")[1]):
					entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("*")[0])))
					i+=1
				entities.active_character[0].set_weakness(int(action.split(" ")[2]))

			elif "Gloat" in action:
				self.set_strength(int(action.split(" ")[1]))

			elif "ChampAnger" in action:
				self.intention_logic = [["The Champ Phase 2"]]
				self.remove_AllDebuffs()
				self.set_strength(12)
				self.set_turnMarker()

			elif "DefensiveStance" in action:
				self.blocking(int(action.split(" ")[1].split("|")[0]))
				self.set_metallicice(int(action.split(" ")[1].split("|")[1]))

			elif "Roar" in action:
				entities.active_character[0].set_frail(int(action.split(" ")[1]))
				entities.active_character[0].set_weakness(int(action.split(" ")[1]))
				
				if self.codeName == "Snake Plant":
					self.intention_logic = [0]*helping_functions.turn_counter+[1,1,0]*33
					print("Snake Plant Intentionchange")
			
			elif "MegaDebuff" in action:
				entities.active_character[0].set_weakness(int(action.split(" ")[1]))
				entities.active_character[0].set_vulnerable(int(action.split(" ")[1]))
				entities.active_character[0].set_frail(int(action.split(" ")[1]))

			elif "Spawn Torch Heads" in action:

				while len(entities.list_of_enemies) < 3:
					entities.list_of_enemies.append(Enemy(name="Torch Head",max_health=rd.randint(40,45),intentions=[7],intention_logic=[["Random"],[0]*100]))

			elif "TorchBuff" in action:

				for enemy in entities.list_of_enemies:
					enemy.set_strength(int(action.split(" ")[1].split("|")[0]))

				self.blocking(int(action.split(" ")[1].split("|")[1]))

			elif "BearHug" in action:

				entities.active_character[0].set_dexterity(-int(action.split(" ")[1]))

			elif "RomeoTaunt" in action:
				ansiprint(self.name+": Get him, Bear!")

			elif "Reincarnate" in action:
				self.health = 0
				self.heal(math.floor(self.max_health / 2))
				
				self.intentions = [rd.randint(7,11)+2,"Bellow 2|12","Multiattack 9*2"]
				self.intention_logic = [["Random"],[rd.randint(0,1)]+list(helping_functions.nchoices_with_restrictions([0.3,0.3,0.4],{0:2,1:1,2:1}))]

				self.lifelink = False
			
			elif "SpikeUp" in action:

				if self.counter < 6:
					self.on_hit_or_death[0][0] += 2
					self.counter += 1
				else:
					entities.active_character[0].receive_damage(self.attack(9))

			elif "Explode" in action:
				entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1])))
				self.alive = False
				
			elif "Repulse" in action:
				
				i = 0
				while i < int(action.split(" ")[1]):
					entities.active_character[0].add_CardToDrawpile({"Name": "Dazed","Ethereal": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire"},index=rd.randint(0,len(entities.active_character[0].draw_pile)))
					i+=1

			elif "Constrict" in action:
				entities.active_character[0].set_constriction(int(action.split(" ")[1]))

			elif "Transientattack" in action:
				entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1])+(self.turnCounter-1)*10))
			
			elif "DazeBeam" in action:
				i = 0
				while i < int(action.split(" ")[1].split("*")[1]):
					entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("*")[0])))
					entities.active_character[0].add_CardToDiscardpile({"Name": "Dazed","Ethereal": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire"})
					i += 1

			elif "SquareOfDeca" in action:
				for enemy in entities.list_of_enemies:
					enemy.blocking(int(action.split(" ")[1].split("|")[0]))
					enemy.set_platedArmor(int(action.split(" ")[1].split("|")[1]))
			
			elif "Rebirth" in action:
				self.health = 0
				self.remove_AllDebuffs()
				self.heal(self.max_health)
				self.leader = True
				self.intention_logic = [["Random"],[2]*(self.turnCounter+1)+list(helping_functions.nchoices_with_restrictions([0.5,0.5],{0:2,1:2}))]
				self.intentions = ["Multiattack 10*3","Voidattack 18/1",40]
				self.move = 40

			elif "Voidattack" in action:

				entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("/")[0])))
				i = 0
				while i < int(action.split(" ")[1].split("/")[1]):
					entities.active_character[0].add_CardToDrawpile({"Name": "Void", "Ethereal": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire","Info":"<RED>Unplayable</RED> Whenever this card is drawn, lose <yellow>1 Energy</yellow>. <BLUE>Ethereal</BLUE>."},index=rd.randint(0,len(entities.active_character[0].draw_pile)-1))
					i+=1

			elif "Haste" in action:
				self.set_health(math.floor(self.max_health / 2))
				self.blocking(32)
				self.remove_AllDebuffs()
				self.intention_logic = [["Random"],[0]+list(helping_functions.nchoices_with_restrictions([0.35,0.2,0.45],{0:1,1:1,2:2}))]

			elif "TimeSlam" in action:

				entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("/")[0])))
				entities.active_character[0].set_reducedDrawByTurns(int(action.split(" ")[1].split("/")[1]))
				i = 0
				while i < int(action.split(" ")[1].split("/")[1]):
					entities.active_character[0].add_CardToDiscardpile({"Name": "Slimed", "Energy": 1, "Exhaust": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire"})
					i += 1

			elif "Ripple" in action:
				self.blocking(int(action.split(" ")[1].split("|")[0]))
				entities.active_character[0].set_weakness(int(action.split(" ")[1].split("|")[1]))
				entities.active_character[0].set_vulnerable(int(action.split(" ")[1].split("|")[1]))
				entities.active_character[0].set_frail(int(action.split(" ")[1].split("|")[1]))

			elif "BurningDebuff" in action:
				i = 0
				while i < int(action.split(" ")[1]):
					entities.active_character[0].add_CardToDiscardpile({"Name": "Burn", "DiscardDamage": 2, "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>. At the end of your turn, take <red>2 damage</red>."})
					i += 1

			elif "Implant" in action:

				entities.active_character[0].add_CardToDeck({"Name": "Parasite","Type": "Curse","Rarity": "Curse","Owner":"The Spire","Info":"<RED>Unplayable</RED> If transformed or removed from your deck, lose <red>3 Max HP</red>."})

			elif "GiantHead" in action:
				additionalDamage = self.counter * 5
				if additionalDamage < 30:
					self.counter+=1

				attackDamage = int(action.split(" ")[1]) + additionalDamage
				entities.active_character[0].receive_damage(self.attack(attackDamage))

			elif "Fortify" in action:
				for enemy in entities.list_of_enemies:
					enemy.blocking(int(action.split(" ")[1]))

			elif "BurnStrike" in action:
				i = 0
				while i < int(action.split(" ")[1].split("*")[1]):
					entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("*")[0])))
					entities.active_character[0].add_CardToDiscardpile({"Name": "Burn", "DiscardDamage": 2, "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>. At the end of your turn, take <red>2 damage</red>."})
					i+=1
			
			elif "Bash" in action:
				entities.active_character[0].receive_damage(self.attack(int(action.split(" ")[1].split("/")[0])))
				entities.active_character[0].set_strength(-int(action.split(" ")[1].split("/")[1]))

			elif "Debilitate" in action:
				entities.active_character[0].set_vulnerable(int(action.split(" ")[1]))
				entities.active_character[0].set_weakness(int(action.split(" ")[1]))
				entities.active_character[0].set_frail(int(action.split(" ")[1]))
				entities.active_character[0].add_CardToDrawpile({"Name": "Void", "Ethereal": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire","Info":"<RED>Unplayable</RED> Whenever this card is drawn, lose <yellow>1 Energy</yellow>. <BLUE>Ethereal</BLUE>."})
				entities.active_character[0].add_CardToDrawpile({"Name": "Wound", "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>."})
				entities.active_character[0].add_CardToDrawpile({"Name": "Dazed", "Ethereal": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire","Info":"<BLUE>Ethereal</BLUE>. <RED>Unplayable</RED>."})
				entities.active_character[0].add_CardToDrawpile({"Name": "Slimed", "Energy": 1, "Exhaust": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire","Info":"<BLUE>Exhaust</BLUE>."})
				entities.active_character[0].add_CardToDrawpile({"Name": "Burn", "DiscardDamage": 2, "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>. At the end of your turn, take <red>2 damage</red>."})

			elif "HeartBuff" in action:
				self.counter += 1
				self.remove_AllDebuffs()
				self.set_strength(2)
				
				if self.counter == 1:
					self.set_artifact(2)
				elif self.counter == 2:
					self.cardTypeToLookOutFor = "Everything BeatOfDeath Opposites 3"
					ansiprint("You will now receive <red>3 Damage</red> everytime you play a card.")
				elif self.counter == 3:
					self.painfullStabs = True
				elif self.counter == 4:
					self.set_strength(10)
				else:
					self.set_strength(50)

	def set_turnMarker(self):

		self.turnMarker = helping_functions.turn_counter + 1
		#this is set +1 for theChamp phase 2 but I can't explain it. Figure it out yourself. This may need editing later.

	def remove_AllDebuffs(self):

		self.weak = 0
		self.vulnerable = 0
		self.poison = 0

		self.temp_strength = 0
		self.strengthChange = 0

		if self.strength < 0:
			self.strength = 0

		self.choke = 0
		self.sadisticNature = 0
		
		ansiprint(self.name,"removed all Debuffs!")
		

	def set_CardTypeToLookOutFor (self,value):
		
		self.cardTypeToLookOutFor = value

		if value.split(" ")[1] == "Strength":
			ansiprint("Now",self.name,"will receive",value.split(" ")[2],"strength everytime you play a",value.split(" ")[0],"card.")
		elif value.split(" ")[1] == "Daze":
			ansiprint(entities.active_character[0].displayName,"will receive",value.split(" ")[2],"<light-cyan>Dazed</light-cyan> everytime you play a <red>non-attack Card</red>")
		else:
			ansiprint(entities.active_character[0].displayName,"will now be punished for playing",value.split(" ")[0],"cards!")
		

	def cardTypeCheck(self,cardType):
		try:
			if self.cardTypeToLookOutFor:
				if len(self.cardTypeToLookOutFor.split(" ")) == 4:
					
					if self.cardTypeToLookOutFor.split(" ")[2] == "Opposites":

						if cardType != self.cardTypeToLookOutFor.split(" ")[0]:
							if self.cardTypeToLookOutFor.split(" ")[1] == "Strength":
								self.set_strength (int(self.cardTypeToLookOutFor.split(" ")[2]))
							elif self.cardTypeToLookOutFor.split(" ")[1] == "Daze":
								i = 0
								while i < int(self.cardTypeToLookOutFor.split(" ")[2]):
									entities.active_character[0].add_CardToDrawpile({"Name": "Dazed","Ethereal": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire"},index=rd.randint(0,len(entities.active_character[0].draw_pile)-1))
									i+=1
							elif self.cardTypeToLookOutFor.split(" ")[1] == "Counter":
									self.counter += 1
									if self.counter % 12 == 0:
										entities.active_character[0].timeWarp = True
										ansiprint("You can't do anything this turn anymore because of",self.name)
									else:
										ansiprint("You can play",12-self.counter%12,"more cards until your turn will automatically end.")
							elif self.cardTypeToLookOutFor.split(" ")[1] == "BeatOfDeath":
								entities.active_character[0].receive_recoil_damage(int(self.cardTypeToLookOutFor.split(" ")[3]))
				else:
					if cardType == self.cardTypeToLookOutFor.split(" ")[0]:
						if self.cardTypeToLookOutFor.split(" ")[1] == "Strength":
							self.set_strength (int(self.cardTypeToLookOutFor.split(" ")[2]))
						elif self.cardTypeToLookOutFor.split(" ")[1] == "Daze":
								i = 0
								while i < int(self.cardTypeToLookOutFor.split(" ")[2]):
									entities.active_character[0].add_CardToDrawpile({"Name": "Dazed","Ethereal": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire"},index=rd.randint(0,len(entities.active_character[0].draw_pile)-1))
									i+=1

		except Exception as e:
			print(e,"<-- This happened in enemy.py cardTypeCheck()")
			pass

	def attack(self,attack):
		
		if self.spireBroAttacked == True:
			attack += int(attack * 0.5)

		damage = attack + self.strength + self.strengthChange
		
		if self.weak > 0:
			if entities.active_character[0].paperKrane > 0:
				damage -= (attack + self.strength + self.strengthChange) * 0.4
			else:
				damage -= (attack + self.strength + self.strengthChange) * 0.25


		damage = math.floor(damage)

		if damage < 0:
			damage = 0

		ansiprint(self.name,"attacks for",damage)
		
		if entities.active_character[0].spikes > 0:
			self.receive_recoil_damage(entities.active_character[0].spikes)

		if entities.active_character[0].tempSpikes > 0:
			self.receive_recoil_damage(entities.active_character[0].tempSpikes)

		return damage

	def blocking(self,blocking):
		self.block += blocking
		ansiprint(self.name,"blocks for " + str(blocking) + ".")

	def receive_damage(self,attack_damage):
		
		if self.heartVincibility >= 200:
			attack_damage = 0

		damageToHp = False
		
		if self.vulnerable > 0:
			attack_damage += attack_damage * 0.50
			attack_damage = math.floor(attack_damage)
		
		try:
			if len(self.on_hit_or_death) > 0:
			
				if "Fly" in self.on_hit_or_death[0][0]:
					attack_damage /= 2
					attack_damage = math.floor(attack_damage)

		except Exception as e:
			#print (e)
			pass

		try:
			if self.slow == True:
				
				attack_damage += math.floor(attack_damage / 100 * entities.active_character[0].card_counter*10)
				
		except Exception as e:
			print(e)
		
		if self.intangible > 0:
			attack_damage = 1
			ansiprint("Intangible reduces the damage to 1.")

		damage = attack_damage - self.block
		
		if damage > 0:
			
			damageToHp = True
			
			if self.block > 0 and entities.active_character[0].handDrill > 0:
				self.set_vulnerable(2)
				ansiprint("This happened because you own <<light-red>>Hand Drill</<light-red>>")

			self.block = 0

			for relic in entities.active_character[0].relics:
				if relic.get("Name") == "The Boot":
					if damage < 5:
						damage = 5
						ansiprint("The damage was increased to 5 because of <light-red>The Boot</light-red>!")

			self.health -= damage
			
			if self.health < 1:
				self.alive = False
			else:
				ansiprint("The " + self.name + " ("+str(self.health)+"/"+str(self.max_health)+") has taken", damage,"damage.")
				
				if entities.active_character[0].envenom > 0:
					self.set_poison(entities.active_character[0].envenom)
					ansiprint("This happened because",entities.active_character[0].name,"has <blue>Envenom</blue> in play.")

			if self.platedArmor > 0:
				self.platedArmor -= 1
				ansiprint(self.name,"has",self.platedArmor,"Plated Armor left.")

			self.damageCounter += 1

		else:
			self.block -= attack_damage
			ansiprint("The", self.name, "has", self.block,"block left.")

		try:
			if len(self.on_hit_or_death) > 0:
				self.react_on_hit_and_death(damage,damageToHp)
		except Exception as e:
			#print(e,"Issue in ")
			pass
		
		entities.check_if_enemy_dead()

	def receive_recoil_damage(self,attack_damage):
		
		if self.intangible > 0:
			attack_damage = 1
			ansiprint("Intangible reduces the damage to 1.")
		
		if self.heartVincibility >= 200:
			attack_damage = 0

		damage = attack_damage - self.block

		if int(damage) > 0:
			self.block = 0
			self.health -= int(damage)
			if self.health < 1:
				ansiprint("The",self.name,"has been defeated")
				self.alive = False
			else:
				ansiprint("The " + self.name + " ("+str(self.health)+"/"+str(self.max_health)+ ") has taken",int(damage),"damage.")
		else:
			self.block -= attack_damage
			ansiprint("The", self.name, "has", self.block,"block left and",self.health,"health left.")
		entities.check_if_enemy_dead()	
	
	def stealCard(self,place):

		if place == "Drawpile":
			rare = False
			uncommon = False
			common = False
			basic = False
			if len(entities.active_character[0].draw_pile) > 0:
				i = 0
				for card in entities.active_character[0].draw_pile:
					if card.get("Rarity") == "Rare":
						rare = True
						self.stolenCard.append(entities.active_character[0].draw_pile.pop(i))
						break	
					i+=1	
				if rare == True:
					ansiprint(self.name,"stole <blue>"+self.stolenCard[0].get("Name")+"</blue> from you!")
				else:
					i = 0
					for card in entities.active_character[0].draw_pile:
						if card.get("Rarity") == "Uncommon":
							uncommon = True
							self.stolenCard.append(entities.active_character[0].draw_pile.pop(i))
							break
						i+=1	
					
					if uncommon == True:
						ansiprint(self.name,"stole <blue>"+self.stolenCard[0].get("Name")+"</blue> from you!")
					else:
						i = 0
						for card in entities.active_character[0].draw_pile:
							if card.get("Rarity") == "Common":
								common = True
								self.stolenCard.append(entities.active_character[0].draw_pile.pop(i))
								break
							i+=1	
						
						if common == True:
							ansiprint(self.name,"stole <blue>"+self.stolenCard[0].get("Name")+"</blue> from you!")							
						else:
							i = 0
							for card in entities.active_character[0].draw_pile:
								if card.get("Rarity") == "Basic":
									basic = True
									self.stolenCard.append(entities.active_character[0].draw_pile.pop(i))
									break
								i+=1	
							
							if basic == True:
								ansiprint(self.name,"stole <blue>"+self.stolenCard[0].get("Name")+"</blue> from you!")		
							else:
								self.stealCard("Discardpile")
			else:
				self.stealCard("Discardpile")

		elif place == "Discardpile":
			rare = False
			uncommon = False
			common = False
			basic = False
			if len(entities.active_character[0].discard_pile) > 0:
				i = 0
				for card in entities.active_character[0].discard_pile:
					if card.get("Rarity") == "Rare":
						rare = True
						self.stolenCard.append(entities.active_character[0].discard_pile.pop(i))
						break	
					i+=1	
				if rare == True:
					ansiprint(self.name,"stole <blue>"+self.stolenCard[0].get("Name")+"</blue> from you!")
				else:
					i = 0
					for card in entities.active_character[0].discard_pile:
						if card.get("Rarity") == "Uncommon":
							uncommon = True
							self.stolenCard.append(entities.active_character[0].discard_pile.pop(i))
							break
						i+=1	
					
					if uncommon == True:
						ansiprint(self.name,"stole <blue>"+self.stolenCard[0].get("Name")+"</blue> from you!")
					else:
						i = 0
						for card in entities.active_character[0].discard_pile:
							if card.get("Rarity") == "Common":
								common = True
								self.stolenCard.append(entities.active_character[0].discard_pile.pop(i))
								break
							i+=1	
						
						if common == True:
							ansiprint(self.name,"stole <blue>"+self.stolenCard[0].get("Name")+"</blue> from you!")							
						else:
							i = 0
							for card in entities.active_character[0].discard_pile:
								if card.get("Rarity") == "Basic":
									basic = True
									self.stolenCard.append(entities.active_character[0].discard_pile.pop(i))
									break
								i+=1	
							
							if basic == True:
								ansiprint(self.name,"stole <blue>"+self.stolenCard[0].get("Name")+"</blue> from you!")		
							else:
								ansiprint("Insanely, there is no card this Automaton can steal.")
			else:
				ansiprint("Insanely, there is no card this Automaton can steal.")

	def handle_poison(self):
		poison_damage = self.poison
		
		if self.intangible > 0 and poison_damage > 1:
			poison_damage = 1
			ansiprint("Intangible reduces the <green>poison</green> <red>damage</red> to 1.")
		
		if self.heartVincibility >= 200:
			poison_damage = 0
		
		self.health -= poison_damage
		
		if self.health < 1:
			ansiprint("The",self.name,"has been defeated")
			self.alive = False
		else:
			self.poison -= 1
			ansiprint("The " + self.name + " ("+str(self.health)+"/"+str(self.max_health)+ ") has taken",poison_damage,"damage and has",self.poison,"poison left.")
		
		entities.check_if_enemy_dead()

	def react_on_hit_and_death(self,damage,damageToHp):
		try:
			for effect in self.on_hit_or_death:
				
				if effect[1] == "Hit":
					
					if type(effect[0]) == int:

						ansiprint(entities.active_character[0].name, "is hit by spiky recoil damage!")
						entities.active_character[0].receive_recoil_damage(effect[0])

					elif "Curl" in effect[0]:
						if self.health > 0:		
							self.blocking(int(effect[0].split(" ")[1]))
							self.on_hit_or_death = []
							ansiprint(self.name, "is curling up for",effect[0].split(" ")[1],"block.")
					
					elif "Shifting" in effect[0]:
						
						self.set_strengthChange(-damage)
						
					elif "Split" in effect[0]:
			
						if self.health <= self.max_health // 2 and self.health > 0:
							
							ansiprint(self.name, "is splitting!")
							
							self.move = "Split"
							self.intentions = ["Split"]
							self.intention_logic = [["Random"],[0]*100]

					elif "Asleep" in effect[0]:
			
						if damageToHp:
							
							ansiprint(self.name, "is waking up!")
							
							self.intentions = ["Wake Up",20,"SiphonSoul 2"]						
							self.intention_logic = [["Random"],[0]*(self.turnCounter+1)+[1,1,2]*33]
							self.on_hit_or_death = []
							self.metallicize = 0
							self.move = "Wake Up"

					elif "Anger" in effect[0]:
						if self.block == 0:
							self.strength += int(effect[0][-1])
							ansiprint("The",self.name,"got angry and increased its strength by",effect[0][-1])
					
					elif "Malleable" in effect[0]:
						if damageToHp:
							blockAmount = int(self.on_hit_or_death[0][0].split(" ")[1])+self.damageCounter-1
							self.blocking(blockAmount)
						

					elif "Modeshift" in effect[0]:
						self.modeshift -= damage
					
						if self.modeshift < 1:
							ansiprint(self.name,"switches to its defensive form!")
							self.blocking(20)
							self.intentions = ["DefensiveMode 4",10,"TwinSlam 8*2"]
							self.intention_logic = [["Random"],[0]*(self.turnCounter+1)+[0,1,2]]
							self.on_hit_or_death = []
							self.move = "DefensiveMode 4"
							
						else:
							ansiprint(self.name,"can take",self.modeshift,"more damage until it switches modes.")

					elif "Fly" in effect[0]:
						self.tracker += 1
						if self.health > 0:
							if self.tracker % int(effect[0][-1]) == 0:
								self.intentions = ["Wake Up",3,"Fly 4"]
								self.intention_logic = [["Random"],[0]*(self.turnCounter+1)+[1,2]]
								self.on_hit_or_death = []
								ansiprint(self.name,"has fallen down! It takes normal <red>damage</red> as long as it's down!")
							else:
								ansiprint("You have to hit",self.name,int(effect[0][-1])-self.tracker,"times more until it will fall down.")

					elif "Reactive" in effect[0]:
						if self.health > 0:
							ansiprint(self.name,"changed what it's going to do.")
							self.move = self.determine_choice(rd.randint(0,10))

					elif "Invincible 200" in effect[0]:
						self.heartVincibility += damage
												
						if self.heartVincibility >= 200:
							ansiprint("You can't deal more than 200 <red>Damage</red> to the",self.name,"per turn.")
							self.heal(self.heartVincibility-200)
							self.heartVincibility = 200	
						else:
							ansiprint("The",self.name,"can take",200-self.heartVincibility,"<red>Damage</red> more this turn!")

				elif effect[1] == "Death":

					if self.health < 1:
						if "Vulnerable" in effect[0]:
							
							ansiprint("The",self.name,"exploaded on death and sprays vulnerable gases all around!")
							entities.active_character[0].set_vulnerable(int(effect[0][-1]))

						elif "Lifelink" in effect[0]:
							if self.lifelink == False:
								self.alive = True
								self.lifelink = True

								

								self.intention_logic = [["Random"],[0]*(self.turnCounter-1)+[1]*20]
								self.intentions = ["Wake Up","Reincarnate"]	
								self.move = "Wake Up"

								i = 0
								for enemy in entities.list_of_enemies:
									if enemy.lifelink == True:
										i+=1
									else:
										pass
									
								if i == len(entities.list_of_enemies):
									for enemy in entities.list_of_enemies:
										enemy.alive = False
									
									entities.check_if_enemy_dead()

								else:
									ansiprint("All <red>Darklings</red> have to be below <red>1 HP</red> at the same time in order for them to die.")
							else:
								self.alive = True
								ansiprint("All <red>Darklings</red> have to be below <red>1 HP</red> at the same time in order for them to die.")

						elif "Rebirth" in effect[0]:

							self.alive = True

							ansiprint("The Awakened One is eyeing you curiously.")

							self.intention_logic = [["Random"],[0]*100]
							self.intentions = ["Rebirth"]
							self.move = "Rebirth"
							self.cardTypeToLookOutFor = None
							self.on_hit_or_death = []
							self.regen = 0

		except Exception as e:
			print(e)

	def endOfTurnEffects(self):
		
		if self.platedArmor > 0:
			self.blocking(self.platedArmor)

		if self.metallicize > 0:
			self.set_block_by_metallicice()

		if self.intangiblePower and self.turnCounter % 2 == 0:
			self.set_intangible(1)
	

	def effect_counter_down(self):
		if self.weak > 0:
			self.weak -= 1

		if self.vulnerable > 0:
			self.vulnerable -= 1

		if self.invulnerable > 0:
			self.invulnerable -= 1
		
		if self.damageCounter > 0:
			self.damageCounter = 0

		if self.intangible > 0:
			self.intangible -= 1

		self.strength += self.ritual

		self.strength += self.temp_strength

		self.temp_strength = 0
		self.strengthChange = 0

		if self.codeName == "Byrd":
			self.tracker = 0

	def heal(self,value):

		self.health += value
		if self.health > self.max_health:
			displayValue = self.health - self.max_health
			self.health = self.max_health

			ansiprint(self.name,"heals for", value - displayValue, "and now has",self.health,"Health.")
		else:
			ansiprint(self.name,"heals for", value, "and now has",self.health,"Health.")

	def set_weakness(self,value):
		if self.artifact > 0:
			self.set_artifact(-1)
		else:
			if self.sadisticNature > 0:
				self.receive_sadistic_damage()
			self.weak += value
			ansiprint(self.name, "now has",self.weak,"Weakness.")

	def set_vulnerable(self,value):
		if self.artifact > 0:
			self.set_artifact(-1)
		else:

			if self.sadisticNature > 0:
				self.receive_sadistic_damage()

			self.vulnerable += value
			ansiprint(self.name, "now has",self.vulnerable,"Vulnerable.")

	def set_tempStrength(self,value):
		if self.artifact > 0:
			self.set_artifact(-1)
		else:
			if self.sadisticNature > 0:
				self.receive_sadistic_damage()	
			self.temp_strength += value
			ansiprint(self.name, "now has lost",self.temp_strength,"Strength. It will regain it at the end of its turn!")

	def set_strengthChange(self,value):
		self.strengthChange += value
		ansiprint(self.name,"will deal",abs(self.strengthChange),"less damage next turn.")

	def set_poison(self,value):
		if self.artifact > 0:
			self.set_artifact(-1)
		else:
			if self.sadisticNature > 0:
				self.receive_sadistic_damage()	
			if entities.active_character[0].sneckoSkull > 0:
				value+=1

			self.poison += value
			ansiprint(self.name, "now has",self.poison,"poison.")
		
	def multiply_poison(self,value):
		if self.artifact > 0:
			self.set_artifact(-1)
		else:
			if self.sadisticNature > 0:
				self.receive_sadistic_damage()
			self.poison *= value
			ansiprint(self.name, "now has",self.poison,"poison.")

	def set_corpseExplosion(self,value):
		if self.artifact > 0:
			self.set_artifact(-1)
		else:
			if self.sadisticNature > 0:
				self.receive_sadistic_damage()	
			
			self.corpseExploding += value
			ansiprint(self.name, "will deal its Max HP as damage to all other enemies on death.")

	def set_choke (self,value):
		if self.artifact > 0:
			self.set_artifact(-1)
		else:
			if self.sadisticNature > 0:
				self.receive_sadistic_damage()
			
			self.choke += value
			ansiprint(self.name, "receives",self.choke,"damage everytime you play a card this turn.")

	def set_sadisticNature(self,value):
		self.sadisticNature += value
		ansiprint(self.name, "receives",self.sadisticNature,"damage everytime you they receive a debuff.")

	def set_ritual(self,value):

		self.ritual += value
		ansiprint(self.name, "now has",self.ritual,"ritual.")

	def set_strength(self,value):

		self.strength += value
		ansiprint(self.name, "now has",self.strength,"strength.")

	def set_artifact (self,value):

		self.artifact += value
		
		if value > 0:
			ansiprint(self.name, "gains", self.artifact, "artifact and now has",self.artifact,"artifact.")
		else: 	
			ansiprint(self.name, "loses one artifact and now has",self.artifact,"artifact left.")

	def set_platedArmor(self,value):

		self.platedArmor += value
		ansiprint(self.name, "now has",self.platedArmor,"plated Armor and will receive as much <green>Block</green> per turn.")

	def set_maxHealth (self,value):
		
		self.max_health += value
		self.health += value
		ansiprint(self.name,"now has <red>"+str(self.max_health)+" Max HP</red>.")
	
	def set_health (self,value):

		self.health = value

		ansiprint(self.name,"now has <red>"+str(self.health)+"</red> Health left.")

	def set_intangible(self,value):

		self.intangible += value
		ansiprint("For",self.intangible,"turn",self.name,"will only receive 1 damage per time they take damage.")

	def set_block_by_metallicice (self,value):
		self.block += self.metallicize

		ansiprint(self.name, "received",self.metallicize,"block through metallicize.")

	def set_metallicice(self,value):
		self.metallicize += value

		ansiprint(self.name, "receives",self.metallicize,"block at the start of each turn.")

	def set_regen(self,value):
		self.regen += value
		ansiprint(self.name,"regenerates",self.regen,"HP per turn.")

	def steal_gold(self,value):
	    
	    self.stolenGold += entities.active_character[0].set_gold(value,thievery = True)

	def get_strengthModifier(self):
		return self.strength + self.strengthChange + self.temp_strength

	def receive_sadistic_damage(self):

		self.receive_recoil_damage(self.sadisticNature)

	def set_intention_logic(self):
		if self.intention_logic[0][0] != "Random":
			self.dumb_check_because_this_part_of_python_sucks()

		if self.intention_logic[0][0] == "Green Louse":
			self.intention_logic[1] = list(helping_functions.nchoices_with_restrictions([0.75,0.25],{0:2,1:1}))
			
		elif self.intention_logic[0][0] == "Red Louse":
			self.intention_logic[1] = list(helping_functions.nchoices_with_restrictions([0.75,0.25],{0:2,1:1}))
		
		elif self.intention_logic[0][0] == "Jaw Worm":
			self.intention_logic[1] = list(helping_functions.nchoices_with_restrictions([0.25,0.3,0.45],{0:1,1:2,2:1}))

		elif self.intention_logic[0][0] == "Looter":
			self.intention_logic[1] = [0,0,rd.randint(1,2)]

		elif self.intention_logic[0][0] == "Red Slaver":
			self.intention_logic[1] = list(helping_functions.nchoices_with_restrictions([0.375,0.375,0.25],{0:2,1:2,2:1}))
		
		elif self.intention_logic[0][0] == "Blue Slaver":
			self.intention_logic[1] = list(helping_functions.nchoices_with_restrictions([0.4,0.6],{0:2,1:1}))
		
		elif self.intention_logic[0][0] == "Fungi Beast":
			self.intention_logic[1] = list(helping_functions.nchoices_with_restrictions([0.6,0.4],{0:2,1:1}))

		elif self.intention_logic[0][0] == "Small Acid Slime":
			self.intention_logic[1] = list(helping_functions.nchoices_with_restrictions([0.5,0.5]))

		elif self.intention_logic[0][0] == "Medium Acid Slime":
			self.intention_logic[1] = list(helping_functions.nchoices_with_restrictions([0.4,0.4,0.2],{0:2,1:2,2:1}))

		elif self.intention_logic[0][0] == "Large Acid Slime":
			self.intention_logic[1] = list(helping_functions.nchoices_with_restrictions([0.3,0.4,0.3],{0:1,1:2,2:1}))

		elif self.intention_logic[0][0] == "Byrd":
			self.intention_logic[1] = list(helping_functions.nchoices_with_restrictions([0.625,0.375],k=1)) + list(helping_functions.nchoices_with_restrictions([0.5,0.3,0.2],{0:2,1:1,2:1}))

		elif self.intention_logic[0][0] == "Chosen":
			self.intention_logic[1] = [4]+helping_functions.alternating_choices(optionsOne=[0,1],optionsTwo=[2,3],weightsOne = None,weightsTwo = [0.6,0.4])

		elif self.intention_logic[0][0] == "Shelled Parasite":
			self.intention_logic[1] = [2,rd.randint(0,1)] + list(helping_functions.nchoices_with_restrictions([0.4,0.4,0.2],{0:2,1:2,2:1}))

		elif self.intention_logic[0][0] == "Mugger":
			self.intention_logic[1] = [0,0,rd.randint(1,2)]

		elif self.intention_logic[0][0] == "Snecko":
			self.intention_logic[1] = [2]+list(helping_functions.nchoices_with_restrictions([0.60,0.40],{0:2,1:5}))

		elif self.intention_logic[0][0] == "Spheric Guardian":
			self.intention_logic[1] = [2,3] + list(helping_functions.nchoices_with_restrictions([0.5,0.5],{0:1,1:1}))
		
		elif self.intention_logic[0][0] == "Snake Plant":
			self.intention_logic[1] = list(helping_functions.nchoices_with_restrictions([0.65,0.35],{0:2,1:1}))

		elif self.intention_logic[0][0] == "Book of Stabbing":
			self.intention_logic[1] = list(helping_functions.nchoices_with_restrictions([0.85,0.15],{0:2,1:1}))

		elif self.intention_logic[0][0] == "Bronze Orb":
			self.intention_logic[1] = list(helping_functions.nchoices_with_restrictions([0.175,0.075,0.75],{0:2,1:2,2:2}))

		elif self.intention_logic[0][0] == "Darkling":
			self.intention_logic[1] = [rd.randint(0,1)]+list(helping_functions.nchoices_with_restrictions([0.3,0.3,0.4],{0:2,1:1,2:1}))

		elif self.intention_logic[0][0] == "Orb Walker":
			self.intention_logic[1] = list(helping_functions.nchoices_with_restrictions([0.4,0.6],{0:2,1:2}))

		elif self.intention_logic[0][0] == "Spiker":
			self.intention_logic[1] = list(helping_functions.nchoices_with_restrictions([0.5,0.5],{0:1,1:1}))

		elif self.intention_logic[0][0] == "Repulsor":
			self.intention_logic[1] = list(helping_functions.nchoices_with_restrictions([0.2,0.8],{0:1,1:10}))

		elif self.intention_logic[0][0] == "Spire Growth":
			self.intention_logic[1] = list(helping_functions.nchoices_with_restrictions([0.5,0.5],{0:2,1:2}))

		elif self.intention_logic[0][0] == "Writhing Mass":
			self.intention_logic[1] = list(helping_functions.nchoices_with_restrictions([0.3,0.2,0.3,0.1,0.1],{0:1,1:1,2:1,3:1,4:1}))


		elif self.intention_logic[0][0] == "Nemesis":
			self.intention_logic[1] = [rd.randint(0,1)]+list(helping_functions.nchoices_with_restrictions([0.3,0.35,0.35],{0:2,1:1,2:1}))
			
		elif self.intention_logic[0][0] == "Giant Head":
			self.intention_logic[1] = list(helping_functions.nchoices_with_restrictions([0.5,0.5],{0:2,1:2},k=4))+[2]*40
		
		elif self.intention_logic[0][0] == "Awakened One":
			self.intention_logic[1] = [0]+list(helping_functions.nchoices_with_restrictions([0.25,0.75],{0:2,1:1}))
		
		elif self.intention_logic[0][0] == "Time Eater":
			self.intention_logic[1] = [0]+list(helping_functions.nchoices_with_restrictions([0.35,0.2,0.45],{0:1,1:1,2:2}))
		
		elif self.intention_logic[0][0] == "Spire Spear":
			self.intention_logic[1] = [1]+helping_functions.spireSpearAttacks()

		

	def dumb_check_because_this_part_of_python_sucks(self):
		if len(self.intention_logic) == 1:
			self.intention_logic.append(None)
		#look you'll come back here in the future and wonder why you've done this
		#while even at the point you've created this you're not entirely sure.
		#try reading this sometimes in the future.
		#https://stackoverflow.com/questions/1132941/least-astonishment-and-the-mutable-default-argument/11416002#11416002

	