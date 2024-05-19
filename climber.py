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
        
        deck: list = None, hand: list = [], discard_pile: list = [], exhaust_pile: list = [], 

        draw_strength: int = 5, block: int = 0, gold: int = 0,

        relics: list = [],

        alive: bool = True

        ):
        
        self.name = name
        if self.name == "Silent":
            self.displayName = "<green>" + self.name + "</green>"
        elif self.name == "Ironclad":
            self.displayName = "<red>" + self.name + "</red>"
        elif self.name == "Defect":
            self.displayName = "<blue>" + self.name + "</blue>"
        
        self.max_health = max_health
        self.health = self.max_health - math.ceil(self.max_health / 10)
        self.energy = energy
        self.energy_gain = energy_gain
        if deck == None:
            self.deck = []
        else:
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
        self.potionBagSize = 2
        #negative statuses
        self.weak = 0
        self.frail = 0
        self.vulnerable = 0
        self.entangled = False

        #positiv statuses
        
        self.smokeBomb = False
        self.position = [0,0]
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

        self.cantDraw = False
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
        self.demonForm = 0
        self.burst = 0
        self.doubleTap = 0
        self.amplify = 0

        #defectEffects
        if self.name == "Defect":
            self.maxOrbs = 3
        else:
            self.maxOrbs = 0
        self.orbs = []
        self.focus = 0
        self.claw = 0
        self.rebound = 0
        self.preRebound = 0
        self.lightningCounter = 0
        self.frostCounter = 0
        self.equilibrium = 0
        self.heatsinks = 0
        self.hello_world = 0
        self.loop = 0
        self.selfRepair = 0
        self.staticDischarge = 0
        self.storm = 0
        self.biasedCognition = 0
        self.creativeAI = 0
        self.echoForm = 0
        self.electrodynamics = False
        self.attack_counter = 0
        self.skill_counter = 0
        self.card_counter = 0
        self.damage_counter = 0
        self.goldPlatedCables = False
        self.emotionChipTriggered = False
        self.emotionChip = False
        self.lightningCounter = 0
        self.frostCounter = 0
        self.frozenCore = False

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
        self.runicPyramid = 0
        self.confused = False

        self.artOfWar = 0
        self.penNip = 0
        
        self.akabeko = 0
        self.sneckoSkull = 0
        self.meatOnTheBone = False
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
        self.frozenEye = False
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
        self.paperPhrog = False
        self.selfFormingClay = False
        self.charonsAshes = False
        self.magicFlower = False
        self.championBelt = False
        self.brimStone = False
        self.burningBlood = False
        self.blackBlood = False
        self.runicCube = False
        self.redSkull = False
        self.redSkullStrength = False
        self.orangePellets = False
                            
        #new powers needed to add in status screen
        self.rage = 0
        self.combustDamage = 0
        self.combustSelfharm = 0
        self.darkEmbrace = 0
        self.evolve = 0
        self.feelNoPain = 0
        self.fireBreathing = 0
        self.barricade = False
        self.corruption = False
        self.juggernaut = 0
        self.rupture = 0

        self.randomTarget = False
        self.hex = False
        self.card_in_play = None
        self.double_play_card = None
        self.turnMoment = 0
        self.timeWarp = False
        self.reducedDrawByTurns = []
        self.exhaustQueue = []

        self.redKey = False
        self.blueKey = False
        self.greenKey = False
        self.allKeys = False
        self.cardIndex = None


    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value


    def turn(self,turn_counter):
        
        if self.turnMoment == 0:
            self.enemyMoves()
            self.effect_counter_down()
            if self.barricade == True:
                pass
            
            elif self.dontLoseBlock > 0:
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
                    enemy.set_block_by_metallicice()
                if enemy.platedArmor > 0:
                    enemy.blocking(enemy.platedArmor)
                
            
            if helping_functions.turn_counter == 1:
                self.relicFirstTurnEffects()
            if self.emotionChipTriggered == True:
                self.passiveOrbsTurnStart()
                self.passiveOrbsTurnEnd()
                self.emotionChipTriggered = False
            
            self.passiveOrbsTurnStart()
            self.negativeEffectsAtTheStartOfTheTurn()
            self.powersAtTheStartOfTheTurn()
            
            if self.iceCream:
                self.energy += self.energy_gain + self.temp_energy
            else:
                self.energy = self.energy_gain + self.temp_energy
            
            if len(self.reducedDrawByTurns) > 0:

                while i < len(self.reducedDrawByTurns):
                    
                    if self.reducedDrawByTurns[i] == helping_functions.turn_counter:
                        self.tempDraw = -1
                        self.reducedDrawByTurns.pop(i)
                    else:
                        i+=1

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
            self.showHand(battlemode=True)
            
            self.turnMoment = 1
        else:
            ansiprint("You saved during a fight!")
            
        while True:
            
            optionOne = "Play a <blue>Card</blue>"
            optionTwo = "Use a <c>Potion</c>"
            optionThree = "Show <light-red>Relics</light-red>"
            optionFour = "End Turn"
            optionFive = "Show Drawpile"
            optionSix = "Show Discardpile"
            optionSeven = "Show Exhaustpile"

            self.show_status()
            actionlist = [optionOne,optionTwo,optionThree,optionFour,optionFive,optionSix,optionSeven]
            #actionlist = [optionOne,optionTwo,optionThree,optionFour]

            self.showEnemies(skip=False,numbers=False)
            
            i = 0
            try:
                
                self.print_hand_and_potions()
                plan = input("\nWhat do you want to do?\n")
                plan = int(plan)-1
                
                
                #if plan not in range(len(actionlist)):
                 #   continue
                
                if plan in range(len(self.hand)):
                    if self.velvetChoker > 0 and self.card_counter >= 6:
                        ansiprint("You can't play anymore cards because you own a <light-red>Velvet Choker</light-red>.")
                    elif self.timeWarp == True:
                        ansiprint("You can't play anmore cards this turn because of <red>Time Eater</red>.")
                    else:
                        self.play_card(plan,turn_counter)

                elif plan == len(self.hand) + len(self.potionBag):
                
                    print("\n\n")
                    if len(entities.list_of_enemies) > 0:
                        self.powersAtTheEndOfTheTurn()
                        self.cursesEndOfTurn()
                        self.exhaust_ethereals()
                        self.relicsAtTheEndOfTurn()
                        self.passiveOrbsTurnEnd()
                        if self.goldPlatedCables == True:
                            self.passiveOrbsTurnEnd(loopTrigger=True)
                        self.discard_hand()
                        self.changeEnergyCostAfterTurn()
                        self.effect_counter_down()
                        self.turnMoment = 0
                        break
                    
                    else:
                        self.end_of_battle_effects()

                        #this has to trigger somewhere else!
                        self.turnMoment = 0
                        break

                elif plan == len(self.hand) + len(self.potionBag) + 1:
                    self.showRelics()
                
                elif plan == len(self.hand) + len(self.potionBag) + 2:
                    #self.print_all_cards()
                    self.show_drawpile()
                
                elif plan == len(self.hand) + len(self.potionBag) + 3:
                    #self.print_all_cards()
                    self.show_discardpile()
                elif plan == len(self.hand) + len(self.potionBag) + 4:
                    #self.print_all_cards()
                    self.show_exhaustpile()

                elif len(self.potionBag) > 0:
                
                    if plan < len(self.hand) + len(self.potionBag):
                        potion_index = plan - len(self.hand)
                        if self.timeWarp == True:
                            ansiprint(f"You can't drink anmore <light-cyan>Potions</light-cyan> this turn because of <red>Time Eater</red>.")
                        else:
                            self.play_potion(turn_counter,potion_index)
                

                if self.unceasingTop > 0 and len(self.hand) == 0:
                    self.draw(1)
                    ansiprint("You have drawn another card because of <light-red>Unceasing Top</light-red>")
                    self.showHand(battlemode=True)
                time.sleep(0.03)
            
            except Exception as e:
                print(e)
                self.explainer_function(plan)
    

    def print_hand_and_potions(self):
        hand_and_potion_length = len(self.hand)+len(self.potionBag)
        self.showHand(battlemode=True,skip=False)
        self.showPotions(skip=False)
        
        ansiprint(f"{hand_and_potion_length+1}. End Turn")
        ansiprint(f"{hand_and_potion_length+2}. Show <light-red>Relics</light-red>")
        ansiprint(f"{hand_and_potion_length+3}. Show Drawpile")
        ansiprint(f"{hand_and_potion_length+4}. Show Discardpile")
        ansiprint(f"{hand_and_potion_length+5}. Show Exhaustpile")
        
    def enemyMoves(self):
        for enemy in entities.list_of_enemies:
            enemy.chooseMove()

    def gainEnergy(self,value):
        self.energy += value
        #ansiprint(self.displayName, "has now <yellow>"+str(self.energy)+" Energy</yellow>.\n") 
    
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
            self.set_strength(self.ritual)
            ansiprint(f"<light-blue>Ritual</light-blue> did this.")

        if self.demonForm > 0:
            self.set_strength(self.demonForm)
            ansiprint(f"<light-blue>Demon Form</light-blue> did this.")

        if self.brimStone == True:
            self.set_strength(2)
            for enemy in entities.list_of_enemies:
                enemy.set_strength(1)

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
                self.playCardFromTopOfDeck(exhaust = False)
                i += 1
                
    def negativeEffectsAtTheStartOfTheTurn(self):

        if self.constriction > 0:
            self.receive_recoil_damage(self.constriction)

    def end_of_battle_effects(self):
        
        if self.meatOnTheBone == True and self.health <= self.max_health//2:
            self.heal(12)
            ansiprint("<light-red>Meat on the Bone</light-red> just <red>healed</red> you!")
            self.meatOnTheBone = False
        
        if self.burningBlood == True:
            self.heal(6)
            ansiprint("<light-red>Burning Blood</light-red> just <red>healed</red> you!")
            self.burningBlood = False

        elif self.blackBlood == True:
            self.heal(12)
            ansiprint("<light-red>Black Blood</light-red> just <red>healed</red> you!")
            self.blackBlood = False

        for relic in self.relics:
            if relic.get("name") == "Orange Pellets":
                relic["Power Counter"] = 0
                relic["Attack Counter"] = 0
                relic["Skill Counter"] = 0
                self.remove_allDebuffs()
                
    def relicFirstTurnEffects(self):

        for relic in self.relics:
            
            if relic.get("Name") == "Anchor":
                self.blocking(10)
            
            elif relic.get("Name") == "Ring of the Snake":
                self.set_tempDraw(2)

            elif relic.get("Name") == "Cracked Core":
                self.channelOrb("Lightning")

            elif relic.get("Name") == "Nuclear Battery":
                self.channelOrb("Plasma")

            elif relic.get("Name") == "Runic Capacitor":
                self.set_orbslots(3)

            elif relic.get("Name") == "Symbiotic Virus":
                self.channelOrb("Dark")

            elif relic.get("Name") == "Emotion Chip":
                self.emotionChip = True

            elif relic.get("Name") == "Gold-Plated Cables":
                self.goldPlatedCables = True


            elif relic.get("Name") == "Data Disk":
                self.set_focus(1)
            
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
                self.frozenEye = True

            elif relic.get("Name") == "Frozen Core":
                self.frozenCore = True


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
                self.meatOnTheBone = True

            elif relic.get("Name") == "Snecko Skull":
                self.sneckoSkull = 1

            elif relic.get("Name") == "Fossilized Helix":
                self.set_buffer(1)

            elif relic.get("Name") == "Preserved Insect":
                if self.get_floor() == "Elite":
                    for enemy in entities.list_of_enemies:
                        damage = math.floor(enemy.health/4)
                        enemy.receive_recoil_damage(damage)
                    ansiprint("<light-red>Preserved Insect</light-red> did this <red>damage</red>.")

            elif relic.get("Name") == "Pantograph":
                if self.get_floor() == "Boss":
                    self.heal(25)
                    ansiprint("<light-red>Pantograph Relic</light-red> <red>heals</red> you for <red>25</red> whenever you meet a <black>Boss</black>.")

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
            
            elif relic.get("Name") == "Mark of Pain":
                self.set_energyGain(1)
                self.add_CardToDrawpile({"Name": "Wound", "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>."})
                self.add_CardToDrawpile({"Name": "Wound", "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>."})

            elif relic.get("Name") == "Runic Cube":
                self.runicCube = True

            elif relic.get("Name") == "Paper Phrog":
                self.paperPhrog = True

            elif relic.get("Name") == "Red Skull":
                self.redSkull = True
                self.set_redSkull()

            elif relic.get("Name") == "Self-Forming Clay":
                self.selfFormingClay = True

            elif relic.get("Name") == "Charon's Ashes":
                self.charonsAshes = True

            elif relic.get("Name") == "Magic Flower":
                self.magicFlower = True

            elif relic.get("Name") == "Brim Stone":
                self.brimStone = True

            elif relic.get("Name") == "Champion Belt":
                self.championBelt = True

            elif relic.get("Name") == "Burning Blood":
                self.burningBlood = True
                
            elif relic.get("Name") == "Black Blood":                
                self.blackBlood = True

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

            elif relic.get("Name") == "Runic Pyramid":
                self.runicPyramid = 1

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
        
        for relic in self.relics:
            if relic.get("Name") == "Happy Flower":
                
                relic["Counter"] += 1
                
                if relic.get("Counter")%3 == 0:
                    self.gainEnergy(1)              

        if self.mercuryHourglass > 0:
            ansiprint("All Enemies receive <red>3 Damage</red> because of <light-red>Mercury Hourglass</light-red>")
            i = 0
            while i < len(entities.list_of_enemies):
                enemy_check = len(entities.list_of_enemies)
                entities.list_of_enemies[i].receive_recoil_damage(3)
                if enemy_check == len(entities.list_of_enemies):
                    i += 1

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
                
                upgradedCard = rd.choices(list(test),k=1)[0]
                
                cardIndex = self.hand.index(upgradedCard)

                helping_functions.upgradeCard(self.hand.pop(self.hand.index(upgradedCard)),"Hand",index = cardIndex)


    def relicFirstTurnEffects_afterDrawing(self):
        
        for relic in self.relics:
            
            if relic.get("Name") == "Toolbox":
                colorless_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == "Colorless" and v.get("Rarity") != "Special" and v.get("Upgraded") == None}
                cards = rd.choices(list(colorless_cards.items()),k=3)
                
                three_options = []
                for card in cards:
                    three_options.append((copy.deepcopy(card[1])))
                
                helping_functions.pickCard(three_options,place="Hand")

            if relic.get("Name") == "Enchiridion":
                random_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == self.name and v.get("Rarity") == "Rare" and v.get("Upgraded") != True and v.get("Type") == "Power"}
                    
                card_add = copy.deepcopy(rd.choices(list(random_cards.items()))[0][1])
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
        
            if self.frozenCore == True:
                if len(self.orbs) < self.maxOrbs:
                    self.channelOrb("Frost")

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
                    self.strength += decrease[1]
                    ansiprint(f"{self.displayName} lost <red>{decrease[1]} Strength</red>.")

        if len(self.dexterityDecrease) > 0:
            for decrease in self.dexterityDecrease:
                if decrease[0] == helping_functions.turn_counter:
                    self.dexterity += decrease[1]
                    ansiprint(f"{self.displayName} lost <green>{decrease[1]} Dexterity</green>.")                   
                    

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

        if self.combustDamage > 0:
            i = 0
            while i < len(entities.list_of_enemies):
                
                enemy_check = len(entities.list_of_enemies)
                entities.list_of_enemies[i].receive_recoil_damage(self.combustDamage)
                if enemy_check == len(entities.list_of_enemies):
                    i+=1
            
        if self.combustSelfharm > 0:
            self.receive_recoil_damage(self.combustSelfharm,directDamage=True)
            ansiprint("<blue>Combust</blue> did this.")

        if self.brutality > 0:
            self.receive_recoil_damage(self.brutality,directDamage=True)

    def play_card(self,card_index,turn_counter):
        
        if self.check_CardPlayRestrictions() == True:
            return
        
        if len(self.hand) == 0:
            ansiprint("You don't have any cards in your hand to play.")
            return
        if len(entities.list_of_enemies) == 0:
            ansiprint("There are no opponents left.")
            return
        
        while True:

            try:
                #self.showEnemies(skip=false)
                #self.showHand(battlemode=True,skip=True)
                
                #ansiprint("\nYou have <yellow>"+str(self.energy)+" Energy</yellow> available.")
                
                #card_index = input("\nPick the number of the card you want to play\n")
                #card_index = int(card_index)-1
                #if card_index == len(self.hand):
                 #   return

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
            
            except ValueError:
                if len(card_index) > 0:
                        self.explainer_function(card_index)
                else:
                    ansiprint("You have to type a number.")
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
        
        elif "Clash" in self.hand[card_index].get("Name"):
            for card in self.hand:
                if card.get("Type") != "Attack":
                    ansiprint(f"You can't play{self.hand[card_index].get('Name')} because you still have non-attacks in your hand.")
                    return
        
        if self.entangled == True and self.hand[card_index]["Type"] == "Attack":
            ansiprint("You can't play <red>Attacks</red> this turn because you are <light-cyan>entangled</light-cyan>")
            return

        self.cardIndex = card_index
        self.card_is_played(self.hand.pop(card_index),turn_counter)

    def card_is_played (self,card,turn_counter,repeat: bool = False,exhaust:bool=False):
        
        self.card_in_play = card
        enemy_check = len(entities.list_of_enemies)
        
        if repeat or exhaust:
            color = self.get_cardColor(self.card_in_play.get("Type"))
            ansiprint(f"<{color}>{self.card_in_play.get('Name')}</{color}> was played!")

        if self.card_in_play["Owner"] == "Silent":
            
            if self.card_in_play.get("Name") == "Strike":               
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
            elif self.card_in_play.get("Name") == "Strike +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
            
            elif self.card_in_play.get("Name") == "Defend":
                self.blocking(self.card_in_play["Block"])
            
            elif self.card_in_play.get("Name") == "Defend +":
                self.blocking(self.card_in_play["Block"])

            elif self.card_in_play.get("Name") == "Neutralize":             
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_weakness(self.card_in_play["Weakness"])
                
            elif self.card_in_play.get("Name") == "Neutralize +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_weakness(self.card_in_play["Weakness"])

            elif self.card_in_play.get("Name") == "Survivor":
                self.blocking(self.card_in_play["Block"])
                self.discard(self.card_in_play["Discard"])
            
            elif self.card_in_play.get("Name") == "Survivor +":
                self.blocking(self.card_in_play["Block"])
                self.discard(self.card_in_play["Discard"])

            elif self.card_in_play.get("Name") == "Bane":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    if entities.list_of_enemies[self.target].poison > 0:                        
                        self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Bane +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    if entities.list_of_enemies[self.target].poison > 0:                        
                        self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Dagger Spray":
                i = 0

                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i += 1
                
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    self.target = i                 
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i += 1

            elif self.card_in_play.get("Name") == "Dagger Spray +":
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i += 1
                
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    self.target = i                 
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i += 1

            elif self.card_in_play.get("Name") == "Dagger Throw":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.draw(self.card_in_play["Draw"])
                self.discard(self.card_in_play["Discard"])

            elif self.card_in_play.get("Name") == "Dagger Throw +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.draw(self.card_in_play["Draw"])
                self.discard(self.card_in_play["Discard"])
            
                
            elif self.card_in_play.get("Name") == "Flying Knee":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.energyBoost(self.card_in_play["Energy Gain"])

            elif self.card_in_play.get("Name") == "Flying Knee +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.energyBoost(self.card_in_play["Energy Gain"])

            elif self.card_in_play.get("Name") == "Poisoned Stab":
                enemy_check = len(entities.list_of_enemies)
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_poison(self.card_in_play["Poison"])
            
            elif self.card_in_play.get("Name") == "Poisoned Stab +":
                enemy_check = len(entities.list_of_enemies)
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_poison(self.card_in_play["Poison"])

            elif self.card_in_play.get("Name") == "Quick Slash":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.draw(self.card_in_play["Draw"])

            elif self.card_in_play.get("Name") == "Quick Slash +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.draw(self.card_in_play["Draw"])

            elif self.card_in_play.get("Name") == "Slice":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Slice +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Sneaky Strike":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if self.discard_counter > 0:
                    self.gainEnergy(self.card_in_play["Energy Gain"])

            elif self.card_in_play.get("Name") == "Sneaky Strike +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if self.discard_counter > 0:
                    self.gainEnergy(self.card_in_play["Energy Gain"])

            elif self.card_in_play.get("Name") == "Sucker Punch":
                
                self.choose_enemy()     
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_weakness(self.card_in_play["Weakness"])

            elif self.card_in_play.get("Name") == "Sucker Punch +":
                self.choose_enemy()     
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_weakness(self.card_in_play["Weakness"])


            elif self.card_in_play.get("Name") == "All-Out Attack":
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i += 1

                self.discard(self.card_in_play["Discard"],True)
            
            elif self.card_in_play.get("Name") == "All-Out Attack +":
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i += 1
        
                self.discard(self.card_in_play["Discard"],True)


            elif self.card_in_play.get("Name") == "Backstab":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Backstab +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Choke":
                self.choose_enemy()         
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_choke(self.card_in_play["Choking"])

            elif self.card_in_play.get("Name") == "Choke +":
                self.choose_enemy()         
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_choke(self.card_in_play["Choking"])

            elif self.card_in_play.get("Name") == "Dash":
                self.choose_enemy()
                self.blocking(self.card_in_play["Block"])
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Dash +":
                self.choose_enemy()
                self.blocking(self.card_in_play["Block"])
                self.attack(self.card_in_play["Damage"])
            
            elif self.card_in_play.get("Name") == "Endless Agony":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                #needs to create copy on draw and exhauste on play.
            
            elif self.card_in_play.get("Name") == "Endless Agony +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Eviscerate":
                self.choose_enemy()             
                i = 0
                while i < 3:
                    self.attack(self.card_in_play["Damage"])                    
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1

            elif self.card_in_play.get("Name") == "Eviscerate +":
                self.choose_enemy()             
                i = 0
                while i < 3:
                    self.attack(self.card_in_play["Damage"])                    
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1        

            elif self.card_in_play.get("Name") == "Finisher":
                self.choose_enemy()             
                i = 0
                while i < self.attack_counter:
                    self.attack(self.card_in_play["Damage"])
            
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1

            elif self.card_in_play.get("Name") == "Finisher +":
                self.choose_enemy()             
                i = 0
                while i < self.attack_counter:
                    self.attack(self.card_in_play["Damage"])
            
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1
            
            elif self.card_in_play.get("Name") == "Flechettes":
                self.choose_enemy()
                k = 0
                for card in self.hand:
                    if card.get("Type") == "Skill":
                        k += 1
                i = 0
                while i < k:
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1

            elif self.card_in_play.get("Name") == "Flechettes +":
                self.choose_enemy()
                k = 0
                for card in self.hand:
                    if card.get("Type") == "Skill":
                        k += 1
                i = 0
                while i < k:
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1

            elif self.card_in_play.get("Name") == "Heel Hook":
                self.choose_enemy()
                heelhooky = False
                if entities.list_of_enemies[self.target].weak > 0:
                        heelhooky = True
                self.attack(self.card_in_play["Damage"])
                if heelhooky:
                    self.gainEnergy(self.card_in_play["Energy Gain"])
                    self.draw(self.card_in_play["Draw"])
            
            elif self.card_in_play.get("Name") == "Heel Hook +":
                self.choose_enemy()
                heelhooky = False
                if entities.list_of_enemies[self.target].weak > 0:
                        heelhooky = True
                self.attack(self.card_in_play["Damage"])
                if heelhooky:
                    self.gainEnergy(self.card_in_play["Energy Gain"])
                    self.draw(self.card_in_play["Draw"])

            elif self.card_in_play.get("Name") == "Masterful Stab":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Masterful Stab +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                        
            elif self.card_in_play.get("Name") == "Predator":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.set_tempDraw(self.card_in_play["Drawboost"])

            elif self.card_in_play.get("Name") == "Predator +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.set_tempDraw(self.card_in_play["Drawboost"])


            elif self.card_in_play.get("Name") == "Riddle with Holes":
                self.choose_enemy()
                i = 0
                while i < 5:
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1

            elif self.card_in_play.get("Name") == "Riddle with Holes +":
                self.choose_enemy()
                i = 0
                while i < 5:
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1
                

            elif self.card_in_play.get("Name") == "Skewer":
                self.choose_enemy()
                i = 0
                while i < self.energy:
                    self.attack(self.card_in_play["Damage"])            
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1

            elif self.card_in_play.get("Name") == "Skewer +":
                self.choose_enemy()
                i = 0
                while i < self.energy:
                    self.attack(self.card_in_play["Damage"])            
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1
            

            elif self.card_in_play.get("Name") == "Die Die Die":
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check =len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check != len(entities.list_of_enemies):
                        pass
                    else:
                        i+=1
            
            elif self.card_in_play.get("Name") == "Die Die Die +":
                i = 0
                while i < len(entities.list_of_enemies):                    
                    enemy_check =len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check != len(entities.list_of_enemies):
                        pass
                    else:
                        i+=1


            elif self.card_in_play.get("Name") == "Glass Knife":
                self.choose_enemy()             
                i = 0
                while i < 2:
                    self.attack(self.card_in_play["Damage"])                
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1
                self.card_in_play["Damage"] -= 2

            elif self.card_in_play.get("Name") == "Glass Knife +":
                self.choose_enemy()             
                i = 0
                while i < 2:
                    self.attack(self.card_in_play["Damage"])                
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1
                self.card_in_play["Damage"] -= 2
            

            elif self.card_in_play.get("Name") == "Grand Finale":
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check =len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check != len(entities.list_of_enemies):
                        pass
                    else:
                        i+=1

            elif self.card_in_play.get("Name") == "Grand Finale +":
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check =len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check != len(entities.list_of_enemies):
                        pass
                    else:
                        i+=1
                
            elif self.card_in_play.get("Name") == "Unload":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.discard_cards_by_type_opposite(self.card_in_play["DiscardType"])

            elif self.card_in_play.get("Name") == "Unload +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.discard_cards_by_type_opposite(self.card_in_play["DiscardType"])

            elif self.card_in_play.get("Name") == "Acrobatics":
                self.draw(self.card_in_play["Draw"])
                self.discard(self.card_in_play["Discard"])

            elif self.card_in_play.get("Name") == "Acrobatics +":
                self.draw(self.card_in_play["Draw"])
                self.discard(self.card_in_play["Discard"])


            elif self.card_in_play.get("Name") == "Backflip":
                self.blocking(self.card_in_play["Block"])
                self.draw(self.card_in_play["Draw"])

            elif self.card_in_play.get("Name") == "Backflip +":
                self.blocking(self.card_in_play["Block"])
                self.draw(self.card_in_play["Draw"])


            elif self.card_in_play.get("Name") == "Blade Dance":
                i = 0
                while i < self.card_in_play["Shivs"]:
                    if len(self.hand) < 10:
                        self.add_CardToHand({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
                    else:
                        self.add_CardToDiscardpile({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
                    i += 1

            elif self.card_in_play.get("Name") == "Blade Dance +":
                i = 0
                while i < self.card_in_play["Shivs"]:
                    if len(self.hand) < 10:
                        self.add_CardToHand({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
                    else:
                        self.add_CardToDiscardpile({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
                    i += 1      

            elif self.card_in_play.get("Name") == "Cloak and Dagger":
                self.blocking(self.card_in_play["Block"])
                i = 0
                while i < self.card_in_play["Shivs"]:
                    if len(self.hand) < 10:
                        self.hand.append({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
                    else:
                        self.discard_pile.append({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
                    i += 1

            elif self.card_in_play.get("Name") == "Cloak and Dagger +":
                self.blocking(self.card_in_play["Block"])
                i = 0
                while i < self.card_in_play["Shivs"]:
                    if len(self.hand) < 10:
                        self.hand.append({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
                    else:
                        self.discard_pile.append({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
                    i += 1

            elif self.card_in_play.get("Name") == "Deadly Poison":
                self.choose_enemy()
                entities.list_of_enemies[self.target].set_poison(self.card_in_play["Poison"])
            
            elif self.card_in_play.get("Name") == "Deadly Poison +":
                self.choose_enemy()
                entities.list_of_enemies[self.target].set_poison(self.card_in_play["Poison"])

            elif self.card_in_play.get("Name") == "Deflect":
                self.blocking(self.card_in_play["Block"])
            
            elif self.card_in_play.get("Name") == "Deflect +":
                self.blocking(self.card_in_play["Block"])

            elif self.card_in_play.get("Name") == "Dodge and Roll":
                self.blocking(self.card_in_play["Block"])
                self.blockingNextTurn(self.card_in_play["Block"])

            elif self.card_in_play.get("Name") == "Dodge and Roll +":
                self.blocking(self.card_in_play["Block"])
                self.blockingNextTurn(self.card_in_play["Block"])

            elif self.card_in_play.get("Name") == "Outmaneuver":
                self.energyBoost(self.card_in_play["Energy Gain"])

            elif self.card_in_play.get("Name") == "Outmaneuver +":
                self.energyBoost(self.card_in_play["Energy Gain"])

            elif self.card_in_play.get("Name") == "Piercing Wail":
                for enemy in entities.list_of_enemies:
                    enemy.set_tempStrength(self.card_in_play["Strength Modifier"])
                    

            elif self.card_in_play.get("Name") == "Piercing Wail +":
                for enemy in entities.list_of_enemies:
                    enemy.set_tempStrength(self.card_in_play["Strength Modifier"])
                    

            elif self.card_in_play.get("Name") == "Prepared":
                self.draw(self.card_in_play["Draw"])
                self.discard(self.card_in_play["Discard"])

            elif self.card_in_play.get("Name") == "Prepared +":
                self.draw(self.card_in_play["Draw"])
                self.discard(self.card_in_play["Discard"])

            elif self.card_in_play.get("Name") == "Blur":
                self.blocking(self.card_in_play["Block"])
                self.set_dontLoseBlock(self.card_in_play["KeepBlock"])

            elif self.card_in_play.get("Name") == "Blur +":
                self.blocking(self.card_in_play["Block"])
                self.set_dontLoseBlock(self.card_in_play["KeepBlock"])

            elif self.card_in_play.get("Name") == "Bouncing Flask":
                i = 0
                while i < self.card_in_play["Bounces"]:
                    if len(entities.list_of_enemies) > 0:
                        entities.list_of_enemies[rd.randint(0,len(entities.list_of_enemies)-1)].set_poison(self.card_in_play.get("Poison"))
                    i += 1

            elif self.card_in_play.get("Name") == "Bouncing Flask +":
                i = 0
                while i < self.card_in_play["Bounces"]:
                    if len(entities.list_of_enemies) > 0:
                        entities.list_of_enemies[rd.randint(0,len(entities.list_of_enemies)-1)].set_poison(self.card_in_play("Poison"))
                    i += 1

            elif self.card_in_play.get("Name") == "Calculated Gamble":
                draw_power = len(self.hand)
                self.discard(len(self.hand), True)
                self.draw(draw_power)

            elif self.card_in_play.get("Name") == "Calculated Gamble +":
                draw_power = len(self.hand)
                self.discard(len(self.hand), True)
                self.draw(draw_power)

            elif self.card_in_play.get("Name") == "Catalyst":
                self.choose_enemy()
                entities.list_of_enemies[self.target].multiply_poison(self.card_in_play["Multiplikator"])

            elif self.card_in_play.get("Name") == "Catalyst +":
                self.choose_enemy()
                entities.list_of_enemies[self.target].multiply_poison(self.card_in_play["Multiplikator"])

            elif self.card_in_play.get("Name") == "Concentrate":                
                self.discard(self.card_in_play["Discard"])
                self.gainEnergy(self.card_in_play["Energy Gain"])

            elif self.card_in_play.get("Name") == "Concentrate +":
                self.discard(self.card_in_play["Discard"])
                self.gainEnergy(self.card_in_play["Energy Gain"])

            elif self.card_in_play.get("Name") == "Crippling Cloud":                    
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    entities.list_of_enemies[i].set_poison(self.card_in_play["Poison"])
                    if enemy_check == len(entities.list_of_enemies):
                        enemy_check = len(entities.list_of_enemies)
                        entities.list_of_enemies[i].set_weakness(self.card_in_play["Weakness"])
                        if enemy_check == len(entities.list_of_enemies):
                            i += 1      

            elif self.card_in_play.get("Name") == "Crippling Cloud +":
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    entities.list_of_enemies[i].set_poison(self.card_in_play["Poison"])
                    if enemy_check == len(entities.list_of_enemies):
                        enemy_check = len(entities.list_of_enemies)
                        entities.list_of_enemies[i].set_weakness(self.card_in_play["Weakness"])
                        if enemy_check == len(entities.list_of_enemies):
                            i += 1  

            elif self.card_in_play.get("Name") == "Distraction":
                skill_cards = {k:v for k,v in entities.cards.items() if v.get("Type") == "Skill" and v.get("Owner") == self.name and v.get("Rarity") != "Basic" and v.get("Upgraded") == None}
                card = rd.choices(list(skill_cards.items()))[0][1]              
                card["This turn Energycost changed"] = True
                card["Energy"] = 0              
                self.add_CardToHand(card)

            elif self.card_in_play.get("Name") == "Distraction +":
                skill_cards = {k:v for k,v in entities.cards.items() if v.get("Type") == "Skill" and v.get("Owner") == self.name and v.get("Rarity") != "Basic" and v.get("Upgraded") == None}
                card = rd.choices(list(skill_cards.items()))[0][1]              
                card["This turn Energycost changed"] = True
                card["Energy"] = 0              
                self.add_CardToHand(card)

            elif self.card_in_play.get("Name") == "Escape Plan":
                self.draw(self.card_in_play["Draw"])
                if self.hand[-1]["Type"] == "Skill":
                    self.blocking(self.card_in_play["Block"])

            elif self.card_in_play.get("Name") == "Escape Plan +":
                self.draw(self.card_in_play["Draw"])
                if self.hand[-1]["Type"] == "Skill":
                    self.blocking(self.card_in_play["Block"])

            elif self.card_in_play.get("Name") == "Expertise":
                while len(self.hand) < self.card_in_play["Draw"]:
                    self.draw(1)

            elif self.card_in_play.get("Name") == "Expertise +":
                while len(self.hand) < self.card_in_play["Draw"]:
                    self.draw(1)

            elif self.card_in_play.get("Name") == "Leg Sweep":
                self.choose_enemy()
                self.blocking(self.card_in_play["Block"])
                entities.list_of_enemies[self.target].set_weakness(self.card_in_play["Weakness"])

            elif self.card_in_play.get("Name") == "Leg Sweep +":
                self.choose_enemy()
                self.blocking(self.card_in_play["Block"])
                entities.list_of_enemies[self.target].set_weakness(self.card_in_play["Weakness"])

            elif self.card_in_play.get("Name") == "Reflex":
                print("This card is unplayable.")

            elif self.card_in_play.get("Name") == "Reflex +":
                print("This card is unplayable.")

            elif self.card_in_play.get("Name") == "Tactician":
                print("This card is unplayable.")

            elif self.card_in_play.get("Name") == "Tactician +":
                print("This card is unplayable.")

            elif self.card_in_play.get("Name") == "Setup":
                self.putBackOnDeckFromHand(self.card_in_play["Back Putter"],0,"Energy changed until played")

            elif self.card_in_play.get("Name") == "Setup +":                
                self.putBackOnDeckFromHand(self.card_in_play["Back Putter"],0,"Energy changed until played")

            elif self.card_in_play.get("Name") == "Terror":
                self.choose_enemy()
                entities.list_of_enemies[self.target].set_vulnerable(self.card_in_play["Vulnerable"])

            elif self.card_in_play.get("Name") == "Terror +":
                self.choose_enemy()
                entities.list_of_enemies[self.target].set_vulnerable(self.card_in_play["Vulnerable"])

            elif self.card_in_play.get("Name") == "Adrenaline":
                self.gainEnergy(self.card_in_play["Energy Gain"])
                self.draw(self.card_in_play["Draw"])

            elif self.card_in_play.get("Name") == "Adrenaline +":
                self.gainEnergy(self.card_in_play["Energy Gain"])
                self.draw(self.card_in_play["Draw"])

            elif self.card_in_play.get("Name") == "Alchemize":
                
                onePotionAlchemize = helping_functions.generatePotionRewards(event = True,amount = 1)[0]
                self.add_potion(onePotionAlchemize)
                
            elif self.card_in_play.get("Name") == "Alchemize +":
                onePotionAlchemize = helping_functions.generatePotionRewards(event = True,amount = 1)[0]
                self.add_potion(onePotionAlchemize)
                
            elif self.card_in_play.get("Name") == "Corpse Explosion":
                self.choose_enemy()
                entities.list_of_enemies[self.target].set_poison(self.card_in_play["Poison"])
                entities.list_of_enemies[self.target].set_corpseExplosion(True)

            elif self.card_in_play.get("Name") == "Corpse Explosion +":
                self.choose_enemy()
                entities.list_of_enemies[self.target].set_poison(self.card_in_play["Poison"])
                entities.list_of_enemies[self.target].set_corpseExplosion(True)
                
            elif self.card_in_play.get("Name") == "Doppelganger":
                self.energyBoost(self.energy)
                self.set_tempDraw(self.energy)

            elif self.card_in_play.get("Name") == "Doppelganger +":
                self.energyBoost(self.energy + 1)
                self.set_tempDraw(self.energy + 1)

            elif self.card_in_play.get("Name") == "Malaise":
                self.choose_enemy()
                entities.list_of_enemies[self.target].set_weakness(self.energy)
                entities.list_of_enemies[self.target].set_strength(-self.energy)

            elif self.card_in_play.get("Name") == "Malaise +":
                self.choose_enemy()
                entities.list_of_enemies[self.target].set_weakness(self.energy + 1)
                entities.list_of_enemies[self.target].set_strength(-(self.energy +1))

            elif self.card_in_play.get("Name") == "Nightmare":
                self.copyCardsForNextTurn(self.card_in_play["Nightmare"])

            elif self.card_in_play.get("Name") == "Nightmare":
                self.copyCardsForNextTurn(self.card_in_play["Nightmare"])

            elif self.card_in_play.get("Name") == "Phantasmal Killer":
                i = 0
                while i < self.card_in_play["DoubleDamage"]:
                    self.doubleDamage.append(turn_counter+1+len(self.doubleDamage))
                    i += 1

            elif self.card_in_play.get("Name") == "Phantasmal Killer +":
                i = 0
                while i < self.card_in_play["DoubleDamage"]:
                    self.doubleDamage.append(turn_counter+1+len(self.doubleDamage))
                    i += 1

            elif self.card_in_play.get("Name") == "Bullet Time":
                self.set_cantDraw()
                for card in self.hand:
                    card["This turn Energycost changed"] = True 
                    card["Energy"] = 0

            elif self.card_in_play.get("Name") == "Bullet Time +":
                self.set_cantDraw()
                for card in self.hand:
                    card["This turn Energycost changed"] = True 
                    card["Energy"] = 0

            elif self.card_in_play.get("Name") == "Storm of Steel":
                shiv_draw_power = len(self.hand)
                self.discard(len(self.hand), True)
                i = 0
                while i < shiv_draw_power:
                    self.add_CardToHand({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
                    i += 1
            
            elif self.card_in_play.get("Name") == "Storm of Steel +":
                shiv_draw_power = len(self.hand)
                self.discard(len(self.hand), True)
                i = 0
                while i < shiv_draw_power:
                    self.add_CardToHand({"Name":"Shiv","Energy":0,"Damage":4,"Exhaust":True,"Type":"Attack","Rarity": "Common","Owner":"Silent"})
                    i += 1

            elif self.card_in_play.get("Name") == "Shiv":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Shiv +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Accuracy":
                self.set_accuracy(self.card_in_play["Accuracy"])

            elif self.card_in_play.get("Name") == "Accuracy +":
                self.set_accuracy(self.card_in_play["Accuracy"])

            elif self.card_in_play.get("Name") == "Caltrops":
                self.set_spikes(self.card_in_play["Spikes"])
            
            elif self.card_in_play.get("Name") == "Caltrops +":
                self.set_spikes(self.card_in_play["Spikes"])            

            elif self.card_in_play.get("Name") == "Footwork":
                self.set_dexterity(self.card_in_play["Dexterity"])

            elif self.card_in_play.get("Name") == "Footwork +":
                self.set_dexterity(self.card_in_play["Dexterity"])

            elif self.card_in_play.get("Name") == "Infinite Blades":
                self.set_infiniteBlades(self.card_in_play["Infinite Blades"])

            elif self.card_in_play.get("Name") == "Infinite Blades +":
                self.set_infiniteBlades(self.card_in_play["Infinite Blades"])

            elif self.card_in_play.get("Name") == "Noxious Fumes":
                self.set_noxiousFumes(self.card_in_play["Noxiousness"])

            elif self.card_in_play.get("Name") == "Noxious Fumes +":
                self.set_noxiousFumes(self.card_in_play["Noxiousness"])

            elif self.card_in_play.get("Name") == "Well-Laid Plans":
                self.set_wellLaidPlans(self.card_in_play["Well Planed"])
            
            elif self.card_in_play.get("Name") == "Well-Laid Plans +":
                self.set_wellLaidPlans(self.card_in_play["Well Planed"])
            
            elif self.card_in_play.get("Name") == "A Thousand Cuts":
                self.set_thousandCuts(self.card_in_play["Thousand Cuts"])

            elif self.card_in_play.get("Name") == "A Thousand Cuts +":
                self.set_thousandCuts(self.card_in_play["Thousand Cuts"])

            elif self.card_in_play.get("Name") == "After Image":
                self.set_afterImage(self.card_in_play["After Image"])

            elif self.card_in_play.get("Name") == "After Image +":
                self.set_afterImage(self.card_in_play["After Image"])

            elif self.card_in_play.get("Name") == "Envenom":
                self.set_envenom(self.card_in_play["Envenom"])

            elif self.card_in_play.get("Name") == "Envenom +":
                self.set_envenom(self.card_in_play["Envenom"])

            elif self.card_in_play.get("Name") == "Tools of the Trade":
                self.set_toolsOfTheTrade(self.card_in_play["Tools"])
            
            elif self.card_in_play.get("Name") == "Tools of the Trade +":
                self.set_toolsOfTheTrade(self.card_in_play["Tools"])

            elif self.card_in_play.get("Name") == "Wraith Form":
                self.set_intangible(self.card_in_play["Intangible"])
                self.set_wraithForm(self.card_in_play["Wraithness"])
            
            elif self.card_in_play.get("Name") == "Wraith Form +":
                self.set_intangible(self.card_in_play["Intangible"])
                self.set_wraithForm(self.card_in_play["Wraithness"])

            elif self.card_in_play.get("Name") == "Burst":
                preBurst = self.card_in_play.get("Burst")

            elif self.card_in_play.get("Name") == "Burst +":
                preBurst = self.card_in_play.get("Burst")

        elif self.card_in_play["Owner"] == "Ironclad":
            
            if self.card_in_play.get("Name") == "Strike":               
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
            elif self.card_in_play.get("Name") == "Strike +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
            
            elif self.card_in_play.get("Name") == "Defend":
                self.blocking(self.card_in_play["Block"])
            
            elif self.card_in_play.get("Name") == "Defend +":
                self.blocking(self.card_in_play["Block"])

            elif self.card_in_play.get("Name") == "Bash":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_vulnerable(self.card_in_play["Vulnerable"])
                
            elif self.card_in_play.get("Name") == "Bash +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_vulnerable(self.card_in_play["Vulnerable"])

            elif self.card_in_play.get("Name") == "Anger":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                self.add_CardToDiscardpile(self.card_in_play)

            elif self.card_in_play.get("Name") == "Anger +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                self.add_CardToDiscardpile(self.card_in_play)

            elif self.card_in_play.get("Name") == "Body Slam":
                self.choose_enemy()
                self.attack(self.block)
            
            elif self.card_in_play.get("Name") == "Body Slam +":
                self.choose_enemy()
                self.attack(self.block)
            
            elif self.card_in_play.get("Name") == "Clash":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Clash +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Cleave":
                i = 0

                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i += 1

            elif self.card_in_play.get("Name") == "Cleave +":
                i = 0

                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i += 1

            elif self.card_in_play.get("Name") == "Clothesline":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_weakness(self.card_in_play["Weakness"])

            elif self.card_in_play.get("Name") == "Clothesline +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_weakness(self.card_in_play["Weakness"])

            elif self.card_in_play.get("Name") == "Headbutt":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                self.putBackOnDeckFromDiscardPile(amount = 1, energyChange = None, energyChangeType = None, bottom = False, skip = False)

            elif self.card_in_play.get("Name") == "Headbutt +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                self.putBackOnDeckFromDiscardPile(amount = 1, energyChange = None, energyChangeType = None, bottom = False, skip = False)

            elif self.card_in_play.get("Name") == "Heavy Blade":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
            elif self.card_in_play.get("Name") == "Heavy Blade +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Iron Wave":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.blocking(self.card_in_play.get("Block"))

            elif self.card_in_play.get("Name") == "Iron Wave +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.blocking(self.card_in_play.get("Block"))

            elif self.card_in_play.get("Name") == "Perfected Strike":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Perfected Strike +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
            
            elif self.card_in_play.get("Name") == "Pommel Strike":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.draw(self.card_in_play.get("Draw"))

            elif self.card_in_play.get("Name") == "Pommel Strike +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.draw(self.card_in_play.get("Draw"))

            elif self.card_in_play.get("Name") == "Sword Boomerang":
                i = 0
                while i < self.card_in_play["Attacks"]:
                    if len(entities.list_of_enemies) > 0: #length needs to be checked because all enemies could die and then the random number would throw an exception
                        self.target = rd.randint(0,len(entities.list_of_enemies)-1)
                        self.attack(self.card_in_play["Damage"])    
                    i += 1
            elif self.card_in_play.get("Name") == "Sword Boomerang +":
                i = 0
                while i < self.card_in_play["Attacks"]:
                    if len(entities.list_of_enemies) > 0:
                        self.target = rd.randint(0,len(entities.list_of_enemies)-1)
                        self.attack(self.card_in_play["Damage"])    
                    i += 1
            
            elif self.card_in_play.get("Name") == "Thunderclap":
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i += 1
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    self.target = i
                    entities.list_of_enemies[self.target].set_vulnerable(self.card_in_play["Vulnerable"])
                    if enemy_check == len(entities.list_of_enemies):
                        i += 1

            elif self.card_in_play.get("Name") == "Thunderclap +":
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i += 1
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    self.target = i
                    entities.list_of_enemies[self.target].set_vulnerable(self.card_in_play["Vulnerable"])
                    if enemy_check == len(entities.list_of_enemies):
                        i += 1

            elif self.card_in_play.get("Name") == "Twin Strike":
                self.choose_enemy()
                i = 0
                while i < 2:
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1

            elif self.card_in_play.get("Name") == "Twin Strike +":
                self.choose_enemy()
                i = 0
                while i < 2:
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1

            elif self.card_in_play.get("Name") == "Wild Strike":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.add_CardToDiscardpile({"Name": "Wound", "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>."})

            elif self.card_in_play.get("Name") == "Wild Strike +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.add_CardToDiscardpile({"Name": "Wound", "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>."})

            elif self.card_in_play.get("Name") == "Blood for Blood":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
            elif self.card_in_play.get("Name") == "Blood for Blood +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Carnage":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])                

            elif self.card_in_play.get("Name") == "Carnage +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Dropkick":
                self.choose_enemy()
                vulnerable = False
                if entities.list_of_enemies[self.target].vulnerable > 0:
                    vulnerable = True                   
                self.attack(self.card_in_play["Damage"])

                if vulnerable:
                    self.draw(self.card_in_play.get("Draw"))
                    self.gainEnergy(self.card_in_play["Energy Gain"])
                
            elif self.card_in_play.get("Name") == "Dropkick +":
                self.choose_enemy()
                vulnerable = False
                if entities.list_of_enemies[self.target].vulnerable > 0:
                    vulnerable = True                   
                self.attack(self.card_in_play["Damage"])

                if vulnerable:
                    self.draw(self.card_in_play.get("Draw"))
                    self.gainEnergy(self.card_in_play["Energy Gain"])
            
            elif self.card_in_play.get("Name") == "Hemokinesis":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.receive_recoil_damage(self.card_in_play.get("Selfhurt"),directDamage= True)

            elif self.card_in_play.get("Name") == "Hemokinesis +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.receive_recoil_damage(self.card_in_play.get("Selfhurt"),directDamage= True)

            elif self.card_in_play.get("Name") == "Pummel":
                self.choose_enemy()
                i = 0
                while i < self.card_in_play.get("Attacks"):
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1

            elif self.card_in_play.get("Name") == "Pummel +":
                self.choose_enemy()
                i = 0
                while i < self.card_in_play.get("Attacks"):
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1

            elif self.card_in_play.get("Name") == "Rampage":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.card_in_play["Damage"] += self.card_in_play["Damage Gain"]

            elif self.card_in_play.get("Name") == "Rampage +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.card_in_play["Damage"] += self.card_in_play["Damage Gain"]

            elif self.card_in_play.get("Name") == "Reckless Charge":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.add_CardToDrawpile({"Name": "Dazed", "Ethereal": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire","Info":"<BLUE>Ethereal</BLUE>. <RED>Unplayable</RED>."})

            elif self.card_in_play.get("Name") == "Reckless Charge +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.add_CardToDrawpile({"Name": "Dazed", "Ethereal": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire","Info":"<BLUE>Ethereal</BLUE>. <RED>Unplayable</RED>."})

            elif self.card_in_play.get("Name") == "Searing Blow":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
            elif self.card_in_play.get("Name") == "Searing Blow +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Sever Soul":
                self.choose_enemy()
                i = 0
                while i < len(self.hand):
                    if self.hand[i].get("Type") != "Attack":
                        self.add_CardToExhaustQueue(self.hand.pop(i))
                    else:
                        i+=1
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Sever Soul +":
                self.choose_enemy()
                i = 0
                while i < len(self.hand):
                    if self.hand[i].get("Type") != "Attack":
                        self.add_CardToExhaustQueue(self.hand.pop(i))
                    else:
                        i+=1
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Uppercut":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_weakness(self.card_in_play["Weakness"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_vulnerable(self.card_in_play["Vulnerable"])

            elif self.card_in_play.get("Name") == "Uppercut +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_weakness(self.card_in_play["Weakness"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_vulnerable(self.card_in_play["Vulnerable"])


            elif self.card_in_play.get("Name") == "Whirlwind":                              
                e = 0
                while e < self.energy:
                    i = 0
                    while i < len(entities.list_of_enemies):
                        enemy_check = len(entities.list_of_enemies)
                        self.target = i
                        self.attack(self.card_in_play["Damage"])
                        if enemy_check == len(entities.list_of_enemies):
                            i+=1
                    e+=1

            elif self.card_in_play.get("Name") == "Whirlwind +":                                
                e = 0
                while e < self.energy:
                    i = 0
                    while i < len(entities.list_of_enemies):
                        enemy_check = len(entities.list_of_enemies)
                        self.target = i
                        self.attack(self.card_in_play["Damage"])
                        if enemy_check == len(entities.list_of_enemies):
                            i+=1
                    e+=1

            elif self.card_in_play.get("Name") == "Bludgeon":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Bludgeon +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Feed":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                if enemy_check != len(entities.list_of_enemies):
                    self.set_maxHealth(self.card_in_play.get("MaxHealth Gain"))

            elif self.card_in_play.get("Name") == "Feed +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                if enemy_check != len(entities.list_of_enemies):
                    self.set_maxHealth(self.card_in_play.get("MaxHealth Gain"))

            elif self.card_in_play.get("Name") == "Fiend Fire":
                self.choose_enemy()
                i = 0
                while i < len(self.hand):
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1
                i = 0
                while i < len(self.hand):
                    self.add_CardToExhaustQueue(self.hand.pop(i))

            elif self.card_in_play.get("Name") == "Fiend Fire +":
                self.choose_enemy()
                i = 0
                while i < len(self.hand):
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1

                i = 0
                while i < len(self.hand):
                    self.add_CardToExhaustQueue(self.hand.pop(i))

            elif self.card_in_play.get("Name") == "Immolate":                               

                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i+=1
                
                self.add_CardToDiscardpile({"Name": "Burn", "DiscardDamage": 2, "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>. At the end of your turn, take <red>2 damage</red>."})
            
            elif self.card_in_play.get("Name") == "Immolate +":                             

                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i+=1
                
                self.add_CardToDiscardpile({"Name": "Burn", "DiscardDamage": 2, "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>. At the end of your turn, take <red>2 damage</red>."})    


            elif self.card_in_play.get("Name") == "Reaper":                             
                healamount = 0
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    health_check = entities.list_of_enemies[i].health
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        healamount += health_check - entities.list_of_enemies[i].health
                        i+=1
                    else:
                        healamount += health_check

                self.heal(healamount)

            elif self.card_in_play.get("Name") == "Reaper +":                               
                healamount = 0
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    health_check = entities.list_of_enemies[i].health
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        healamount += health_check - entities.list_of_enemies[i].health
                        i+=1
                    else:
                        healamount += health_check

                self.heal(healamount)
            
            elif self.card_in_play.get("Name") == "Armaments":                              
                self.blocking(self.card_in_play["Block"])
                self.removeCardsFromHand(amount = 1 , removeType = "Upgrade")
                
            elif self.card_in_play.get("Name") == "Armaments +":                                
                i = 0
                while i < len(self.hand):
                    if self.hand[i].get("Type") != "Status" and self.hand[i].get("Type") != "Curse" and self.hand[i].get("Upgraded") != True:
                        helping_functions.upgradeCard(self.hand.pop(i),"Hand",i)
                    else:
                        i+=1

            elif self.card_in_play.get("Name") == "Flex":                               
                self.set_strengthDecrease(self.card_in_play["Strength"])
                self.set_strength(self.card_in_play["Strength"])
            
            elif self.card_in_play.get("Name") == "Flex +":                             
                self.set_strengthDecrease(self.card_in_play["Strength"])
                self.set_strength(self.card_in_play["Strength"])            

            elif self.card_in_play.get("Name") == "Havoc":                              
                storedHavoc = self.card_in_play.copy()
                try:
                    self.playCardFromTopOfDeck(exhaust=True)
                except Exception as e:
                    print(e)
                self.card_in_play = storedHavoc.copy()

            elif self.card_in_play.get("Name") == "Havoc +":
                storedHavoc = self.card_in_play.copy()
                try:
                    self.playCardFromTopOfDeck(exhaust=True)
                except Exception as e:
                    print(e)
                self.card_in_play = storedHavoc.copy()
            
            elif self.card_in_play.get("Name") == "Shrug It Off":
                self.blocking(self.card_in_play.get("Block"))
                self.draw(self.card_in_play.get("Draw"))

            elif self.card_in_play.get("Name") == "Shrug It Off +":
                self.blocking(self.card_in_play.get("Block"))
                self.draw(self.card_in_play.get("Draw"))
            
            elif self.card_in_play.get("Name") == "True Grit":
                self.blocking(self.card_in_play.get("Block"))
                self.exhaust(1,random = True)

            elif self.card_in_play.get("Name") == "True Grit +":
                self.blocking(self.card_in_play.get("Block"))
                self.exhaust(1,random = False)
            
            elif self.card_in_play.get("Name") == "War Cry":
                self.draw(self.card_in_play.get("Draw"))
                self.putBackOnDeckFromHand(1,bottom = False,skip=False)
            
            elif self.card_in_play.get("Name") == "War Cry +":
                self.draw(self.card_in_play.get("Draw"))
                self.putBackOnDeckFromHand(1,bottom = False,skip=False)

            elif self.card_in_play.get("Name") == "Battle Trance":
                self.draw(self.card_in_play.get("Draw"))
                self.set_cantDraw()

            elif self.card_in_play.get("Name") == "Battle Trance +":
                self.draw(self.card_in_play.get("Draw"))
                self.set_cantDraw()

            elif self.card_in_play.get("Name") == "Blood Letting":
                self.receive_recoil_damage(self.card_in_play.get("Selfhurt"),directDamage=True)
                self.gainEnergy(self.card_in_play["Energy Gain"])
            
            elif self.card_in_play.get("Name") == "Blood Letting +":
                self.receive_recoil_damage(self.card_in_play.get("Selfhurt"),directDamage=True)
                self.gainEnergy(self.card_in_play["Energy Gain"])
            
            elif self.card_in_play.get("Name") == "Burning Pact":
                self.exhaust(self.card_in_play.get("Exhaustion Amount"))
                self.draw(self.card_in_play.get("Draw"))

            elif self.card_in_play.get("Name") == "Burning Pact +":
                self.exhaust(self.card_in_play.get("Exhaustion Amount"))
                self.draw(self.card_in_play.get("Draw"))

            elif self.card_in_play.get("Name") == "Disarm":
                self.choose_enemy()
                entities.list_of_enemies[self.target].set_strength(self.card_in_play.get("Strength"))

            elif self.card_in_play.get("Name") == "Disarm +":
                self.choose_enemy()
                entities.list_of_enemies[self.target].set_strength(self.card_in_play.get("Strength"))

            elif self.card_in_play.get("Name") == "Dual Wield":
                self.removeCardsFromHand(amount = self.card_in_play.get("Copy Amount"), removeType = "Duplicate")
            
            elif self.card_in_play.get("Name") == "Dual Wield +":
                    self.removeCardsFromHand(amount = self.card_in_play.get("Copy Amount"), removeType = "Duplicate")

            elif self.card_in_play.get("Name") == "Entrench":
                self.blocking(self.block)
            
            elif self.card_in_play.get("Name") == "Entrench +":
                self.blocking(self.block)

            elif self.card_in_play.get("Name") == "Flame Barrier":
                self.blocking(self.card_in_play.get("Block"))
                self.set_tempSpikes(self.card_in_play.get("Spikes"))
            
            elif self.card_in_play.get("Name") == "Flame Barrier +":
                self.blocking(self.card_in_play.get("Block"))
                self.set_tempSpikes(self.card_in_play.get("Spikes"))
            
            elif self.card_in_play.get("Name") == "Ghostly Armor":
                self.blocking(self.block)
            
            elif self.card_in_play.get("Name") == "Ghostly Armor +":
                self.blocking(self.block)

            elif self.card_in_play.get("Name") == "Infernal Blade":
                try:
                    attack_cards = {k:v for k,v in entities.cards.items() if v.get("Type") == "Attack" and v.get("Owner") == self.name and v.get("Rarity") != "Basic" and v.get("Upgraded") == None}
                    card = rd.choices(list(attack_cards.items()))[0][1]             
                    card["This turn Energycost changed"] = True
                    card["Energy"] = 0
                    self.add_CardToHand(card)
                except Exception as e:
                    print("Infernal Blade:",e)
            elif self.card_in_play.get("Name") == "Infernal Blade +":
                try:
                    attack_cards = {k:v for k,v in entities.cards.items() if v.get("Type") == "Attack" and v.get("Owner") == self.name and v.get("Rarity") != "Basic" and v.get("Upgraded") == None}
                    card = rd.choices(list(attack_cards.items()))[0][1]             
                    card["This turn Energycost changed"] = True
                    card["Energy"] = 0
                    self.add_CardToHand(card)
                except Exception as e:
                    print("Infernal Blade:",e)

            elif self.card_in_play.get("Name") == "Intimidate":
                i = 0
                while i < len(entities.list_of_enemies):
                    entities.list_of_enemies[i].set_weakness(self.card_in_play["Weakness"])
                    if enemy_check == len(entities.list_of_enemies):
                        i+=1
            
            elif self.card_in_play.get("Name") == "Intimidate +":
                i = 0
                while i < len(entities.list_of_enemies):
                    entities.list_of_enemies[i].set_weakness(self.card_in_play["Weakness"])
                    if enemy_check == len(entities.list_of_enemies):
                        i+=1

            elif self.card_in_play.get("Name") == "Power Through":
                self.blocking(self.card_in_play.get("Block"))
                self.add_CardToHand({"Name": "Wound", "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>."})
                self.add_CardToHand({"Name": "Wound", "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>."})

            elif self.card_in_play.get("Name") == "Power Through +":
                self.blocking(self.card_in_play.get("Block"))
                self.add_CardToHand({"Name": "Wound", "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>."})
                self.add_CardToHand({"Name": "Wound", "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"<RED>Unplayable</RED>."})

            elif self.card_in_play.get("Name") == "Rage":
                self.set_rage(self.card_in_play.get("Block"))
            
            elif self.card_in_play.get("Name") == "Rage +":
                self.set_rage(self.card_in_play.get("Block"))

            elif self.card_in_play.get("Name") == "Second Wind":
                lencheck = len(self.hand)
                i = 0
                while i < len(self.hand):
                    if self.hand[i].get("Type") != "Attack":
                        self.add_CardToExhaustQueue(self.hand.pop(i))
                    else:
                        i+=1
                
                blocking = (lencheck - len(self.hand)) * self.card_in_play.get("Block")
                self.blocking(blocking)
            
            elif self.card_in_play.get("Name") == "Second Wind +":
                lencheck = len(self.hand)
                i = 0
                while i < len(self.hand):
                    if self.hand[i].get("Type") != "Attack":
                        self.add_CardToExhaustQueue(self.hand.pop(i))
                    else:
                        i+=1

                blocking = (lencheck - len(self.hand)) * self.card_in_play.get("Block")
                self.blocking(blocking)

            elif self.card_in_play.get("Name") == "Seeing Red":
                self.gainEnergy(self.card_in_play["Energy Gain"])
            
            elif self.card_in_play.get("Name") == "Seeing Red +":
                self.gainEnergy(self.card_in_play["Energy Gain"])

            elif self.card_in_play.get("Name") == "Sentinel":
                self.blocking(self.card_in_play["Block"])
            
            elif self.card_in_play.get("Name") == "Sentinel +":
                self.blocking(self.card_in_play["Block"])
    
            elif self.card_in_play.get("Name") == "Shockwave":
                
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    entities.list_of_enemies[i].set_weakness(self.card_in_play["Weakness"])
                    if enemy_check == len(entities.list_of_enemies):
                        enemy_check = len(entities.list_of_enemies)
                        entities.list_of_enemies[i].set_vulnerable(self.card_in_play["Vulnerable"])
                        if enemy_check == len(entities.list_of_enemies):
                            i += 1

            elif self.card_in_play.get("Name") == "Shockwave +":

                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    entities.list_of_enemies[i].set_weakness(self.card_in_play["Weakness"])
                    if enemy_check == len(entities.list_of_enemies):
                        enemy_check = len(entities.list_of_enemies)
                        entities.list_of_enemies[i].set_vulnerable(self.card_in_play["Vulnerable"])
                        if enemy_check == len(entities.list_of_enemies):
                            i += 1              

            elif self.card_in_play.get("Name") == "Spot Weakness":
                self.choose_enemy()

                if self.enemy_preview(self.target,spotWeaknessCheck=True):
                    self.set_strength(self.card_in_play.get("Strength"))
            
            
            elif self.card_in_play.get("Name") == "Spot Weakness +":
                self.choose_enemy()
                
                if self.enemy_preview(self.target,spotWeaknessCheck=True):
                    self.set_strength(self.card_in_play.get("Strength"))

            elif self.card_in_play.get("Name") == "Double Tap":
                self.set_doubleTap(self.card_in_play.get("Tap"))
            
            elif self.card_in_play.get("Name") == "Double Tap +":
                self.set_doubleTap(self.card_in_play.get("Tap"))

            elif self.card_in_play.get("Name") == "Exhume":
                self.draw_specific_cards_from_place(amount = 1,place = "Exhaustpile")

            elif self.card_in_play.get("Name") == "Exhume +":
                self.draw_specific_cards_from_place(amount = 1,place = "Exhaustpile")

            elif self.card_in_play.get("Name") == "Impervious":
                self.blocking(self.card_in_play.get("Block"))

            elif self.card_in_play.get("Name") == "Impervious +":
                self.blocking(self.card_in_play.get("Block"))   

            elif self.card_in_play.get("Name") == "Limit Break":                
                if self.strength >= 0:
                    self.set_strength(self.strength)
                else:
                    self.set_strength(-self.strength)
            elif self.card_in_play.get("Name") == "Limit Break +":
                if self.strength >= 0:
                    self.set_strength(self.strength)
                else:
                    self.set_strength(-self.strength)

            elif self.card_in_play.get("Name") == "Offering":
                self.receive_recoil_damage(self.card_in_play.get("Selfhurt"),directDamage=True)
                self.draw(self.card_in_play.get("Draw"))
                self.gainEnergy(self.card_in_play["Energy Gain"])

            elif self.card_in_play.get("Name") == "Offering +":
                self.receive_recoil_damage(self.card_in_play.get("Selfhurt"),directDamage=True)
                self.draw(self.card_in_play.get("Draw"))
                self.gainEnergy(self.card_in_play["Energy Gain"])  

            elif self.card_in_play.get("Name") == "Combust":
                self.set_combust(damage=5,selfharm=1)

            elif self.card_in_play.get("Name") == "Combust +":
                self.set_combust(damage=5,selfharm=1)

            elif self.card_in_play.get("Name") == "Dark Embrace":
                self.set_darkEmbrace(self.card_in_play.get("Draw"))

            elif self.card_in_play.get("Name") == "Dark Embrace +":
                self.set_darkEmbrace(self.card_in_play.get("Draw"))

            elif self.card_in_play.get("Name") == "Evolve":
                self.set_evolve(self.card_in_play.get("Draw"))
            
            elif self.card_in_play.get("Name") == "Evolve +":
                self.set_evolve(self.card_in_play.get("Draw"))

            elif self.card_in_play.get("Name") == "Feel No Pain":
                self.set_feelNoPain(self.card_in_play.get("Block"))

            elif self.card_in_play.get("Name") == "Feel No Pain +":
                self.set_feelNoPain(self.card_in_play.get("Block"))

            elif self.card_in_play.get("Name") == "Fire Breathing":
                self.set_fireBreathing(self.card_in_play.get("Damage"))

            elif self.card_in_play.get("Name") == "Fire Breathing +":
                self.set_fireBreathing(self.card_in_play.get("Damage"))

            elif self.card_in_play.get("Name") == "Inflame":
                self.set_strength(self.card_in_play.get("Strength"))

            elif self.card_in_play.get("Name") == "Inflame +":
                self.set_strength(self.card_in_play.get("Strength"))

            elif self.card_in_play.get("Name") == "Metallicize":
                self.set_metallicice(self.card_in_play.get("Block"))

            elif self.card_in_play.get("Name") == "Metallicize +":
                self.set_metallicice(self.card_in_play.get("Block"))

            elif self.card_in_play.get("Name") == "Rupture":
                self.set_rupture(self.card_in_play.get("Strength"))

            elif self.card_in_play.get("Name") == "Rupture +":
                self.set_rupture(self.card_in_play.get("Strength"))

            elif self.card_in_play.get("Name") == "Barricade":
                self.set_barricade()

            elif self.card_in_play.get("Name") == "Barricade +":
                self.set_barricade()
            
            elif self.card_in_play.get("Name") == "Berserk":
                self.set_vulnerable(self.card_in_play.get("Vulnerable"))
                self.set_energyGain(1)
            
            elif self.card_in_play.get("Name") == "Berserk +":
                self.set_vulnerable(self.card_in_play.get("Vulnerable"))
                self.set_energyGain(1)

            elif self.card_in_play.get("Name") == "Brutality":
                self.set_drawStrength(self.card_in_play.get("Draw"))
                self.set_brutality(self.card_in_play.get("Selfhurt"))

            elif self.card_in_play.get("Name") == "Brutality +":
                self.set_drawStrength(self.card_in_play.get("Draw"))
                self.set_brutality(self.card_in_play.get("Selfhurt")) 

            elif self.card_in_play.get("Name") == "Corruption":
                self.set_corruption()
                
            elif self.card_in_play.get("Name") == "Corruption +":
                self.set_corruption()   

            elif self.card_in_play.get("Name") == "Demon Form":             
                self.set_demonForm(self.card_in_play.get("Strength"))

            elif self.card_in_play.get("Name") == "Demon Form +":
                self.set_demonForm(self.card_in_play.get("Strength"))
        
            elif self.card_in_play.get("Name") == "Juggernaut":
                self.set_juggernaut(self.card_in_play.get("Damage"))

            elif self.card_in_play.get("Name") == "Juggernaut +":
                self.set_juggernaut(self.card_in_play.get("Damage"))
        
        elif self.card_in_play["Owner"] == "Defect":

            if self.card_in_play.get("Name") == "Strike":               
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
            elif self.card_in_play.get("Name") == "Strike +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Defend":
                self.blocking(self.card_in_play["Block"])

            elif self.card_in_play.get("Name") == "Defend +":
                self.blocking(self.card_in_play["Block"])

            elif self.card_in_play.get("Name") == "Zap":                                        
                self.channelOrb("Lightning")
                
            elif self.card_in_play.get("Name") == "Zap +":
                self.channelOrb("Lightning")

            elif self.card_in_play.get("Name") == "Dualcast":
                self.evokeOrb(amount=2)

            elif self.card_in_play.get("Name") == "Dualcast +":
                self.evokeOrb(amount=2)

            elif self.card_in_play.get("Name") == "Ball Lightning":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.channelOrb("Lightning")

            elif self.card_in_play.get("Name") == "Ball Lightning +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.channelOrb("Lightning")

            elif self.card_in_play.get("Name") == "Barrage":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                i = 0
                while i < len(self.orbs):
                    self.attack(self.card_in_play["Damage"])          
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1

            elif self.card_in_play.get("Name") == "Barrage +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                i = 0
                while i < len(self.orbs):
                    self.attack(self.card_in_play["Damage"])          
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1

            elif self.card_in_play.get("Name") == "Beam Cell":             
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_vulnerable(self.card_in_play["Vulnerable"])

            elif self.card_in_play.get("Name") == "Beam Cell +":             
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_vulnerable(self.card_in_play["Vulnerable"])

            elif self.card_in_play.get("Name") == "Claw":             
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.claw += self.card_in_play["Increase"]

            elif self.card_in_play.get("Name") == "Claw +":             
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.claw += self.card_in_play["Increase"]

            elif self.card_in_play.get("Name") == "Cold Snap":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.channelOrb("Frost")

            elif self.card_in_play.get("Name") == "Cold Snap +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.channelOrb("Frost")

            elif self.card_in_play.get("Name") == "Compile Driver":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])                    
                self.draw(self.count_unique_orbs())

            elif self.card_in_play.get("Name") == "Compile Driver +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])                    
                self.draw(self.count_unique_orbs())

            elif self.card_in_play.get("Name") == "Go for the Eyes":             
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    if self.enemy_preview(self.target,spotWeaknessCheck=True):
                        entities.list_of_enemies[self.target].set_weakness(self.card_in_play["Weakness"])

            elif self.card_in_play.get("Name") == "Go for the Eyes +":             
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    if self.enemy_preview(self.target,spotWeaknessCheck=True):
                        entities.list_of_enemies[self.target].set_weakness(self.card_in_play["Weakness"])

            elif self.card_in_play.get("Name") == "Rebound":             
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.preRebound += 1

            elif self.card_in_play.get("Name") == "Rebound +":             
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.preRebound += 1

            elif self.card_in_play.get("Name") == "Streamline":             
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.card_in_play["Pending Energy Reduction"] = True                    

            elif self.card_in_play.get("Name") == "Streamline +":             
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.card_in_play["Pending Energy Reduction"] = True

            elif self.card_in_play.get("Name") == "Sweeping Beam":             
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check =len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i+=1
                self.draw(self.card_in_play["Draw"])

            elif self.card_in_play.get("Name") == "Sweeping Beam +":             
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check =len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i+=1
                self.draw(self.card_in_play["Draw"])

            elif self.card_in_play.get("Name") == "Blizzard":             
                i = 0
                while i < self.frostCounter:
                    enemy_check =len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i+=1
                
            elif self.card_in_play.get("Name") == "Blizzard +":
                i = 0
                while i < self.frostCounter:
                    enemy_check =len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i+=1

            elif self.card_in_play.get("Name") == "Bullseye":             
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_lockon(self.card_in_play["Lock-On"])

            elif self.card_in_play.get("Name") == "Bullseye +":             
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if enemy_check == len(entities.list_of_enemies):
                    entities.list_of_enemies[self.target].set_lockon(self.card_in_play["Lock-On"])

            elif self.card_in_play.get("Name") == "Doom and Gloom":             
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check =len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i+=1
                self.channelOrb(self.card_in_play["Orb"])

            elif self.card_in_play.get("Name") == "Doom and Gloom +":             
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check =len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i+=1
                self.channelOrb(self.card_in_play["Orb"])

            elif self.card_in_play.get("Name") == "FTL":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if self.card_counter <= self.card_in_play["Max"]:
                    self.draw(self.card_in_play["Draw"])
                    
            elif self.card_in_play.get("Name") == "FTL +":             
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                
                if self.card_counter <= self.card_in_play["Max"]:
                    self.draw(self.card_in_play["Draw"])

            elif self.card_in_play.get("Name") == "Melter":             
                self.choose_enemy()
                entities.list_of_enemies[self.target].block = 0
                self.attack(self.card_in_play["Damage"])
                
            elif self.card_in_play.get("Name") == "Melter +":             
                self.choose_enemy()
                entities.list_of_enemies[self.target].block = 0
                self.attack(self.card_in_play["Damage"])
                

            elif self.card_in_play.get("Name") == "Rip and Tear":
                randomEnemy = rd.randint(0,len(entities.list_of_enemies)-1)
                self.target = randomEnemy
                i = 0
                while i < 2:
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1
                 
            elif self.card_in_play.get("Name") == "Rip and Tear +":             
                randomEnemy = rd.randint(0,len(entities.list_of_enemies)-1)
                self.target = randomEnemy
                i = 0
                while i < 2:
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check != len(entities.list_of_enemies):
                        break
                    i+=1

            elif self.card_in_play.get("Name") == "Scrape":             
                handLength = len(self.hand)
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])                    
                self.draw(self.card_in_play["Draw"],silent=False)
                
                differenceAfterDraw = len(self.hand) - handLength
                discardList = []
                i = 0

                while i < differenceAfterDraw:
                    if self.hand[(i)].get("Energy") != 0:                            
                        discardList.append(-(i+1)+len(self.hand)) #i am making these indexes positive because a list of -1,-2 bugs out when discarding.                        
                    i+=1

                if len(discardList) > 0:
                
                    self.discard(len(discardList),index=discardList,noMessage=False)
                
            elif self.card_in_play.get("Name") == "Scrape +":             
                handLength = len(self.hand)
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.draw(self.card_in_play["Draw"],silent=False)
                handLength = len(self.hand) - handLength
                discardList = []
                i = 0
                while i < handLength:
                    if self.hand[-(i+1)].get("Energy") != 0:
                         discardList.append(-(i+1)+len(self.hand)) #i am making these indexes positive because a list of -1,-2 bugs out when discarding.                                           
                    i+=1
                if len(discardList) > 0:
                    self.discard(len(discardList),index=discardList,noMessage=False)

            elif self.card_in_play.get("Name") == "Sunder":             
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                if enemy_check != len(entities.list_of_enemies):
                    self.gainEnergy(self.card_in_play.get("Energy Gain"))

            elif self.card_in_play.get("Name") == "Sunder +":             
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                if enemy_check != len(entities.list_of_enemies):
                    self.gainEnergy(self.card_in_play.get("Energy Gain"))
                
            elif self.card_in_play.get("Name") == "All for One":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                if enemy_check == len(entities.list_of_enemies):
                    indexList = []
                    i = 0
                    for card in self.discard_pile:
                        if card.get("Energy") == 0:
                            indexList.append(i)
                        i+=1
                    if len(indexList) > 0:
                        self.draw_specific_cards_from_place(len(indexList),place="Discardpile",indexes = indexList)

            elif self.card_in_play.get("Name") == "All for One +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                if enemy_check == len(entities.list_of_enemies):
                    indexList = []
                    i = 0
                    for card in self.discard_pile:
                        if card.get("Energy") == 0:
                            indexList.append(i)
                        i+=1
                    if len(indexList) > 0:
                        self.draw_specific_cards_from_place(len(indexList),place="Discardpile",indexes = indexList)

            elif self.card_in_play.get("Name") == "Core Surge":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.set_artifact(self.card_in_play["Artifact"])

            elif self.card_in_play.get("Name") == "Core Surge +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.set_artifact(self.card_in_play["Artifact"])

            elif self.card_in_play.get("Name") == "Hyperbeam":
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i += 1
                self.set_focus(self.card_in_play["Focus"])

            elif self.card_in_play.get("Name") == "Hyperbeam +":
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check == len(entities.list_of_enemies):
                        i += 1
                self.set_focus(self.card_in_play["Focus"])

            elif self.card_in_play.get("Name") == "Meteor Strike":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.channelOrb(self.card_in_play["Orb"])
                self.channelOrb(self.card_in_play["Orb"])
                self.channelOrb(self.card_in_play["Orb"])

            elif self.card_in_play.get("Name") == "Meteor Strike +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.channelOrb(self.card_in_play["Orb"])
                self.channelOrb(self.card_in_play["Orb"])
                self.channelOrb(self.card_in_play["Orb"])


            elif self.card_in_play.get("Name") == "Thunder Strike":
                
                i = 0
                while i < self.lightningCounter:
                    if len(entities.list_of_enemies) > 0:
                        randomEnemy = rd.randint(0,len(entities.list_of_enemies)-1)
                        self.target = randomEnemy
                        self.attack(self.card_in_play["Damage"])

                    i += 1

            elif self.card_in_play.get("Name") == "Thunder Strike +":
                
                i = 0
                while i < self.lightningCounter:
                    if len(entities.list_of_enemies) > 0:                        
                        randomEnemy = rd.randint(0,len(entities.list_of_enemies)-1)
                        self.target = randomEnemy
                        self.attack(self.card_in_play["Damage"])

                    i += 1
            elif self.card_in_play.get("Name") == "Charge Battery":
                self.blocking(self.card_in_play.get("Block"))
                self.energyBoost(self.card_in_play["Energy Gain"])

            elif self.card_in_play.get("Name") == "Charge Battery +":
                self.blocking(self.card_in_play.get("Block"))
                self.energyBoost(self.card_in_play["Energy Gain"])

            elif self.card_in_play.get("Name") == "Coolheaded":
                self.channelOrb(self.card_in_play.get("Orb"))
                self.draw(self.card_in_play["Draw"])

            elif self.card_in_play.get("Name") == "Coolheaded +":
                self.channelOrb(self.card_in_play.get("Orb"))
                self.draw(self.card_in_play["Draw"])

            elif self.card_in_play.get("Name") == "Hologram":
                self.blocking(self.card_in_play.get("Block"))
                self.draw_specific_cards_from_place(amount=1,place="Discardpile")

            elif self.card_in_play.get("Name") == "Hologram +":
                self.blocking(self.card_in_play.get("Block"))
                self.draw_specific_cards_from_place(amount=1,place="Discardpile")

            elif self.card_in_play.get("Name") == "Leap":
                self.blocking(self.card_in_play.get("Block"))

            elif self.card_in_play.get("Name") == "Leap +":
                self.blocking(self.card_in_play.get("Block"))

            elif self.card_in_play.get("Name") == "Recursion":
                if len(self.orbs) > 0:
                    self.channelOrb(copy.copy(self.orbs[0]))

            elif self.card_in_play.get("Name") == "Recursion +":
                if len(self.orbs) > 0:
                    self.channelOrb(copy.copy(self.orbs[0]))

            elif self.card_in_play.get("Name") == "Stack":
                self.blocking(len(self.discard_pile))

            elif self.card_in_play.get("Name") == "Stack +":
                self.blocking(len(self.discard_pile) + 3)

            elif self.card_in_play.get("Name") == "Steam Barrier":
                
                self.blocking(self.card_in_play.get("Block"))
                if self.card_in_play["Block"] > 0:
                    self.card_in_play["Block"] -= 1

            elif self.card_in_play.get("Name") == "Steam Barrier +":
                
                self.blocking(self.card_in_play.get("Block"))
                if self.card_in_play["Block"] > 0:
                    self.card_in_play["Block"] -= 1

            elif self.card_in_play.get("Name") == "TURBO":
                
                self.gainEnergy(self.card_in_play.get("Energy Gain"))
                self.add_CardToDiscardpile({"Name": "Void", "Ethereal": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire","Info":"Unplayable Whenever this card is drawn, lose 1 Energy. Ethereal."})

            elif self.card_in_play.get("Name") == "TURBO +":
                
                self.gainEnergy(self.card_in_play.get("Energy Gain"))
                self.add_CardToDiscardpile({"Name": "Void", "Ethereal": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire","Info":"Unplayable Whenever this card is drawn, lose 1 Energy. Ethereal."})

            elif self.card_in_play.get("Name") == "Aggregate":
                energyGain = math.floor(len(self.draw_pile)/self.card_in_play["Energy Divider"])
                self.gainEnergy(energyGain)

            elif self.card_in_play.get("Name") == "Aggregate +":
                energyGain = math.floor(len(self.draw_pile)/self.card_in_play["Energy Divider"])
                self.gainEnergy(energyGain)

            elif self.card_in_play.get("Name") == "Auto-Shields":
                if self.block == 0:
                    self.blocking(self.card_in_play.get("Block"))

            elif self.card_in_play.get("Name") == "Auto-Shields +":
                if self.block == 0:
                    self.blocking(self.card_in_play.get("Block"))

            elif self.card_in_play.get("Name") == "Boot Sequence":
                self.blocking(self.card_in_play.get("Block"))

            elif self.card_in_play.get("Name") == "Boot Sequence +":
                self.blocking(self.card_in_play.get("Block"))

            elif self.card_in_play.get("Name") == "Chaos":
                orbs = ["Lightning","Frost","Dark","Plasma"]
                orbs = rd.sample(orbs,counts=[2,2,2,2],k=self.card_in_play["Orb Amount"])
                i = 0
                while i < len(orbs):
                    self.channelOrb(orbs[i])
                    i+=1

            elif self.card_in_play.get("Name") == "Chaos +":
                orbs = ["Lightning","Frost","Dark","Plasma"]
                orbs = rd.sample(orbs,counts=[2,2,2,2],k=self.card_in_play["Orb Amount"])
                i = 0
                while i < len(orbs):
                    self.channelOrb(orbs[i])
                    i+=1

            elif self.card_in_play.get("Name") == "Chill":
                i = 0
                while i < len(entities.list_of_enemies):
                    self.channelOrb("Frost")
                    i+=1

            elif self.card_in_play.get("Name") == "Chill +":
                i = 0
                while i < len(entities.list_of_enemies):
                    self.channelOrb("Frost")
                    i+=1

            elif self.card_in_play.get("Name") == "Consume":
                self.set_focus(self.card_in_play["Focus"])
                self.set_orbslots(-self.card_in_play["Orb Loss"])

            elif self.card_in_play.get("Name") == "Consume +":
                self.set_focus(self.card_in_play["Focus"])
                self.set_orbslots(-self.card_in_play["Orb Loss"])

            elif self.card_in_play.get("Name") == "Darkness":
                self.channelOrb(self.card_in_play["Orb"])
                
            elif self.card_in_play.get("Name") == "Darkness +":
                self.channelOrb(self.card_in_play["Orb"])
                for orb in self.orbs:
                    if orb.get("Name") == "Dark":
                        darkchange = orb.get("Value") + self.focus
                        if darkchange < 0:
                            darkchange = 0
                        orb["Evokation"] += darkchange

            elif self.card_in_play.get("Name") == "Double Energy":
                if self.energy > 0:
                    self.gainEnergy(self.energy - 1)
                    
            elif self.card_in_play.get("Name") == "Double Energy +":
                if self.energy > 0:
                    self.gainEnergy(self.energy)

            elif self.card_in_play.get("Name") == "Equilibrium":
                self.blocking(self.card_in_play.get("Block"))
                self.equilibrium += 1

            elif self.card_in_play.get("Name") == "Equilibrium +":
                self.blocking(self.card_in_play.get("Block"))
                self.equilibrium += 1

            elif self.card_in_play.get("Name") == "Force Field":
                self.blocking(self.card_in_play.get("Block"))

            elif self.card_in_play.get("Name") == "Force Field +":
                self.blocking(self.card_in_play.get("Block"))

            elif self.card_in_play.get("Name") == "Fusion":
                self.channelOrb(self.card_in_play["Orb"])

            elif self.card_in_play.get("Name") == "Fusion +":
                self.channelOrb(self.card_in_play["Orb"])

            elif self.card_in_play.get("Name") == "Genetic Algorithm":
                self.blocking(self.card_in_play.get("Block"))
                    
                for card in self.deck:
                    if card.get("Unique ID") == self.card_in_play.get("Unique ID"):
                        card["Block"] += self.card_in_play["Increase"]
                self.card_in_play["Block"] += self.card_in_play["Increase"]

            elif self.card_in_play.get("Name") == "Genetic Algorithm +":
                self.blocking(self.card_in_play.get("Block"))
                    
                for card in self.deck:
                    if card.get("Unique ID") == self.card_in_play.get("Unique ID"):
                        card["Block"] += self.card_in_play["Increase"]
                self.card_in_play["Block"] += self.card_in_play["Increase"]

            elif self.card_in_play.get("Name") == "Glacier":
                self.blocking(self.card_in_play.get("Block"))
                self.channelOrb(self.card_in_play["Orb"])
                self.channelOrb(self.card_in_play["Orb"])

            elif self.card_in_play.get("Name") == "Glacier +":
                self.blocking(self.card_in_play.get("Block"))
                self.channelOrb(self.card_in_play["Orb"])
                self.channelOrb(self.card_in_play["Orb"])

            elif self.card_in_play.get("Name") == "Overclock":
                self.draw(self.card_in_play.get("Draw"))
                self.add_CardToDiscardpile({"Name": "Burn", "DiscardDamage": 2, "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"Unplayable. At the end of your turn, take 2 damage."})

            elif self.card_in_play.get("Name") == "Overclock +":
                self.draw(self.card_in_play.get("Draw"))
                self.add_CardToDiscardpile({"Name": "Burn", "DiscardDamage": 2, "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"Unplayable. At the end of your turn, take 2 damage."})

            elif self.card_in_play.get("Name") == "Overclock +":
                self.draw(self.card_in_play.get("Draw"))
                self.add_CardToDiscardpile({"Name": "Burn", "DiscardDamage": 2, "Type": "Status", "Rarity": "Enemy","Owner":"The Spire","Info":"Unplayable. At the end of your turn, take 2 damage."})

            elif self.card_in_play.get("Name") == "Recycle":

                if len(self.hand) > 0:
                    energyGain = 0
                    card_index = 0
                    if len(self.hand) == 1:
                        
                        if type(self.hand[0].get("Energy")) == int:
                            energyGain = self.hand[0].get("Energy")
                        
                        elif type(self.hand[0].get("Energy")) == str:
                            energyGain = self.energy
                    else:
                        
                        card_index = self.exhaust(1)
                                                
                        if type(self.hand[card_index[0]].get("Energy")) == int:
                            energyGain = self.hand[card_index[0]].get("Energy")
                        
                        elif type(self.hand[card_index[0]].get("Energy")) == str:
                            energyGain = self.energy_gain
                    
                    self.gainEnergy(energyGain)
                    

            elif self.card_in_play.get("Name") == "Recycle +":
                answers = ["Yes","No"]
                if len(self.hand) > 0:
                    energyGain = 0
                    card_index = 0
                    if len(self.hand) == 1:
                        
                        if type(self.hand[0].get("Energy")) == int:
                            energyGain = self.hand[0].get("Energy")
                        
                        elif type(self.hand[0].get("Energy")) == str:
                            energyGain = self.energy_gain
                    else:
                        
                        card_index = self.exhaust(1)
                        
                        if type(self.hand[card_index[0]].get("Energy")) == int:
                            energyGain = self.hand[card_index[0]].get("Energy")
                        
                        elif type(self.hand[card_index[0]].get("Energy")) == str:
                            energyGain = self.energy
                    
                    self.gainEnergy(energyGain)
                    

            elif self.card_in_play.get("Name") == "Reinforced Body":
                e = 0
                while e < self.energy:
                    if len(entities.list_of_enemies) > 0:
                        self.blocking(self.card_in_play.get("Block"))
                    e+=1

            elif self.card_in_play.get("Name") == "Reinforced Body +":
                e = 0
                while e < self.energy:
                    if len(entities.list_of_enemies) > 0:
                        self.blocking(self.card_in_play.get("Block"))
                    e+=1            

            elif self.card_in_play.get("Name") == "Reprogram":
                self.set_strength(self.card_in_play.get("Changer"))
                self.set_dexterity(self.card_in_play.get("Changer"))
                self.set_focus(- self.card_in_play.get("Changer"))

            elif self.card_in_play.get("Name") == "Reprogram +":
                self.set_strength(self.card_in_play.get("Changer"))
                self.set_dexterity(self.card_in_play.get("Changer"))
                self.set_focus(- self.card_in_play.get("Changer"))

            elif self.card_in_play.get("Name") == "Skim":
                self.draw(self.card_in_play.get("Draw"))

            elif self.card_in_play.get("Name") == "Skim +":
                self.draw(self.card_in_play.get("Draw"))                    

            elif self.card_in_play.get("Name") == "Tempest":
                e = 0
                while e < self.energy:
                    self.channelOrb(self.card_in_play["Orb"])
                    e+=1

            elif self.card_in_play.get("Name") == "Tempest +":
                e = -1
                while e < self.energy:
                    self.channelOrb(self.card_in_play["Orb"])
                    e+=1

            elif self.card_in_play.get("Name") == "White Noise":

                power_cards = {k:v for k,v in entities.cards.items() if v.get("Type") == "Power" and v.get("Owner") == self.name and v.get("Rarity") != "Basic" and v.get("Upgraded") == None}
                card = rd.choices(list(power_cards.items()))[0][1]               
                card = card.copy()
                card["This turn Energycost changed"] = True
                card["Energy"] = 0              
                self.add_CardToHand(card,unConfusable=True)

            elif self.card_in_play.get("Name") == "White Noise +":

                power_cards = {k:v for k,v in entities.cards.items() if v.get("Type") == "Power" and v.get("Owner") == self.name and v.get("Rarity") != "Basic" and v.get("Upgraded") == None}
                card = rd.choices(list(power_cards.items()))[0][1]               
                card = card.copy()
                card["This turn Energycost changed"] = True
                card["Energy"] = 0              
                self.add_CardToHand(card,unConfusable=True)

            elif self.card_in_play.get("Name") == "Amplify":
                self.set_amplify(self.card_in_play.get("Amplificicy"))

            elif self.card_in_play.get("Name") == "Amplify +":
                self.set_amplify(self.card_in_play.get("Amplificicy"))

            elif self.card_in_play.get("Name") == "Fission":
                if len(self.orbs) > 0:
                    drawAndEnergy = len(self.orbs)
                    self.orbs = []
                    self.draw(drawAndEnergy)
                    self.gainEnergy(drawAndEnergy)

            elif self.card_in_play.get("Name") == "Fission +":
                if len(self.orbs) > 0:
                    drawAndEnergy = len(self.orbs)
                    
                    while len(self.orbs) >0:
                        self.evokeOrb()

                    self.draw(drawAndEnergy)
                    self.gainEnergy(drawAndEnergy)

            elif self.card_in_play.get("Name") == "Multicast":
                self.evokeOrb(amount=self.energy)

            elif self.card_in_play.get("Name") == "Multicast +":
                self.evokeOrb(amount=self.energy+1)

            elif self.card_in_play.get("Name") == "Rainbow":
                self.channelOrb("Lightning")
                self.channelOrb("Frost")
                self.channelOrb("Dark")

            elif self.card_in_play.get("Name") == "Rainbow +":
                self.channelOrb("Lightning")
                self.channelOrb("Frost")
                self.channelOrb("Dark")

            elif self.card_in_play.get("Name") == "Reboot":
                self.putBackOnDeckFromHand(len(self.hand),allCards=True)
                self.discardBackInDrawpile()
                self.draw(self.card_in_play["Draw"])

            elif self.card_in_play.get("Name") == "Reboot +":
                self.putBackOnDeckFromHand(len(self.hand),allCards=True)
                self.discardBackInDrawpile()
                self.draw(self.card_in_play["Draw"])

            elif self.card_in_play.get("Name") == "Seek":
                self.draw_specific_cards_from_place(amount = self.card_in_play["Draw"],place = "Drawpile")

            elif self.card_in_play.get("Name") == "Seek +":
                self.draw_specific_cards_from_place(amount = self.card_in_play["Draw"],place = "Drawpile")

            elif self.card_in_play.get("Name") == "Capacitor":
                self.set_orbslots(self.card_in_play["Orb"])

            elif self.card_in_play.get("Name") == "Capacitor +":
                self.set_orbslots(self.card_in_play["Orb"])

            elif self.card_in_play.get("Name") == "Defragment":
                self.set_focus(self.card_in_play.get("Focus"))

            elif self.card_in_play.get("Name") == "Defragment +":
                self.set_focus(self.card_in_play.get("Focus"))

            elif self.card_in_play.get("Name") == "Heatsinks":
                self.set_heatsinks(self.card_in_play.get("Draw"))

            elif self.card_in_play.get("Name") == "Heatsinks +":
                self.set_heatsinks(self.card_in_play.get("Draw"))

            elif self.card_in_play.get("Name") == "Hello World":
                self.set_helloWorld(1)

            elif self.card_in_play.get("Name") == "Hello World +":
                self.set_helloWorld(1)

            elif self.card_in_play.get("Name") == "Loop":
                self.set_loop(self.card_in_play.get("Loop"))

            elif self.card_in_play.get("Name") == "Loop +":
                self.set_loop(self.card_in_play.get("Loop"))

            elif self.card_in_play.get("Name") == "Self Repair":
                self.set_selfRepair(self.card_in_play.get("Heal"))

            elif self.card_in_play.get("Name") == "Self Repair +":
                self.set_selfRepair(self.card_in_play.get("Heal"))

            elif self.card_in_play.get("Name") == "Static Discharge":
                self.set_staticDischarge(1)

            elif self.card_in_play.get("Name") == "Static Discharge +":
                self.set_staticDischarge(2)

            elif self.card_in_play.get("Name") == "Storm":
                self.set_storm(1)

            elif self.card_in_play.get("Name") == "Storm +":
                self.set_storm(1)

            elif self.card_in_play.get("Name") == "Biased Cognition":
                self.set_focus(self.card_in_play["Focus"])
                self.set_biasedCognition(1)

            elif self.card_in_play.get("Name") == "Biased Cognition +":
                self.set_focus(self.card_in_play["Focus"])
                self.set_biasedCognition(1)

            elif self.card_in_play.get("Name") == "Buffer":
                self.set_buffer(self.card_in_play["Buffer"])

            elif self.card_in_play.get("Name") == "Buffer +":
                self.set_buffer(self.card_in_play["Buffer"])

            elif self.card_in_play.get("Name") == "Creative AI":
                self.set_creativeAI(1)

            elif self.card_in_play.get("Name") == "Creative AI +":
                self.set_creativeAI(1)

            elif self.card_in_play.get("Name") == "Echo Form":                    
                self.set_echoForm(1)

            elif self.card_in_play.get("Name") == "Echo Form +":
                self.set_echoForm(1)

            elif self.card_in_play.get("Name") == "Electrodynamics":
                self.channelOrb(orb="Lightning",amount=self.card_in_play["Orbs"])
                self.set_electrodynamics()

            elif self.card_in_play.get("Name") == "Electrodynamics +":
                self.channelOrb(orb="Lightning",amount=self.card_in_play["Orbs"])
                self.set_electrodynamics()

            elif self.card_in_play.get("Name") == "Machine Learning":
                self.set_drawStrength(self.card_in_play["Draw"])

            elif self.card_in_play.get("Name") == "Machine Learning +":
                self.set_drawStrength(self.card_in_play["Draw"])




        elif self.card_in_play["Owner"] == "Colorless":

            if self.card_in_play.get("Name") == "Bandage Up":
                self.heal(self.card_in_play["Heal"])

            elif self.card_in_play.get("Name") == "Bandage Up +":
                self.heal(self.card_in_play["Heal"])

            elif self.card_in_play.get("Name") == "Blind":
                self.choose_enemy()
                entities.list_of_enemies[self.target].set_weakness(self.card_in_play["Weakness"])

            elif self.card_in_play.get("Name") == "Blind +":
                i = 0
                while i < len(entities.list_of_enemies):
                    entities.list_of_enemies[i].set_weakness(self.card_in_play["Weakness"])
                    if enemy_check != len(entities.list_of_enemies):
                        pass
                    else:
                        i+=1

            elif self.card_in_play.get("Name") == "Dark Shackles":
                self.choose_enemy()
                entities.list_of_enemies[self.target].set_tempStrength(self.card_in_play["Strength Modifier"])
                entities.list_of_enemies[self.target].set_strength(-self.card_in_play["Strength Modifier"])

            elif self.card_in_play.get("Name") == "Dark Shackles +":
                self.choose_enemy()
                entities.list_of_enemies[self.target].set_tempStrength(self.card_in_play["Strength Modifier"])
                entities.list_of_enemies[self.target].set_strength(-self.card_in_play["Strength Modifier"])

            
            elif self.card_in_play.get("Name") == "Deep Breath":
                self.discardBackInDrawpile()
                self.draw(self.card_in_play["Draw"])
                
            elif self.card_in_play.get("Name") == "Deep Breath +":
                self.discardBackInDrawpile()                
                self.draw(self.card_in_play["Draw"])
                
            elif self.card_in_play.get("Name") == "Discovery":
                
                neutral_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == "Colorless"}
                cards = rd.choices(list(neutral_cards.items()),k=3)
                
                three_options = []
                for card in cards:
                    card[1]["This turn Energycost changed"] = True
                    card[1]["Energy"] = 0
                    three_options.append(copy.deepcopy(card[1]))

                helping_functions.pickCard(three_options,"Hand")

            elif self.card_in_play.get("Name") == "Discovery +":
                
                neutral_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == "Colorless"}
                cards = rd.choices(list(neutral_cards.items()),k=3)
                
                three_options = []
                for card in cards:
                    card[1]["This turn Energycost changed"] = True
                    card[1]["Energy"] = 0
                    three_options.append(copy.deepcopy(card[1]))

                helping_functions.pickCard(three_options,"Hand")

            elif self.card_in_play.get("Name") == "Dramatic Entrance":
                i = 0
                while i < len(entities.list_of_enemies):                    
                    enemy_check = len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])                    
                    if enemy_check != len(entities.list_of_enemies):
                        pass
                    else:
                        i+=1

            elif self.card_in_play.get("Name") == "Dramatic Entrance +":
                i = 0
                while i < len(entities.list_of_enemies):
                    enemy_check = len(entities.list_of_enemies)
                    self.target = i
                    self.attack(self.card_in_play["Damage"])
                    if enemy_check != len(entities.list_of_enemies):
                        pass
                    else:
                        i+=1

            elif self.card_in_play.get("Name") == "Enlightenment":
                for card in self.hand:
                    if type(card.get("Energy")) == int:
                        if card["Energy"] > 0:
                            card["This turn Energycost changed"] = True
                            card["Energy"] = 1
                ansiprint("All cards in your hand now cost <yellow>1 Energy</yellow> for the rest of the turn.")
            
            elif self.card_in_play.get("Name") == "Enlightenment +":
                for card in self.hand:
                    if type(card.get("Energy")) == int:
                        if card["Energy"] > 0:
                            card["Energy changed for the battle"] = True
                            card["Energy"] = 1  
                    ansiprint("All cards in your hand now cost <yellow>1 Energy</yellow> for the rest of the battle.")


            elif self.card_in_play.get("Name") == "Finesse":
                self.blocking(self.card_in_play["Block"])
                self.draw(self.card_in_play["Draw"])

            elif self.card_in_play.get("Name") == "Finesse +":
                self.blocking(self.card_in_play["Block"])
                self.draw(self.card_in_play["Draw"])

            elif self.card_in_play.get("Name") == "Flash of Steel":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.draw(self.card_in_play["Draw"])

            elif self.card_in_play.get("Name") == "Flash of Steel +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.draw(self.card_in_play["Draw"])
            
            elif self.card_in_play.get("Name") == "Forethought":

                self.putBackOnDeckFromHand(self.card_in_play["Back Putter"],self.card_in_play["Energy Change"],self.card_in_play["Energy Change Type"],bottom = True)
            
            elif self.card_in_play.get("Name") == "Forethought +":

                self.putBackOnDeckFromHand(len(self.hand),self.card_in_play["Energy Change"],self.card_in_play["Energy Change Type"],bottom = True,skip=True)

            elif self.card_in_play.get("Name") == "Good Instincts":
                self.blocking(self.card_in_play["Block"])

            elif self.card_in_play.get("Name") == "Good Instincts +":
                self.blocking(self.card_in_play["Block"])   

            elif self.card_in_play.get("Name") == "Impatience":
                attackCheck = [card for card in self.hand if card.get("Type") == "Attack"]
                if len(attackCheck) == 0:
                    self.draw(self.card_in_play["Draw"])                
                else:
                    print("This card is only playable if you have no attack cards in hand.")
                    self.hand.append(self.card_in_play)
                    self.card_in_play = None
                    return

            elif self.card_in_play.get("Name") == "Impatience +":
                attackCheck = [card for card in self.hand if card.get("Type") == "Attack"]
                if len(attackCheck) == 0:
                    self.draw(self.card_in_play["Draw"])                
                else:
                    print("This card is only playable if you have no attack cards in hand.")
                    self.hand.append(self.card_in_play)
                    self.card_in_play = None
                    return
            
            elif self.card_in_play.get("Name") == "Jack of All Trades":
                neutral_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == "Colorless" and v.get("Upgraded") == None}
                card = rd.choices(list(neutral_cards.items()))[0][1]
                card["This turn Energycost changed"] = True
                card["Energy"] = 0
                self.add_CardToHand(card)

            elif self.card_in_play.get("Name") == "Jack of All Trades +":
                i = 0
                while i < 2:
                    neutral_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == "Colorless" and v.get("Upgraded") == None}
                    card = rd.choices(list(neutral_cards.items()))[0][1]                    
                    card["This turn Energycost changed"] = True
                    card["Energy"] = 0
                    self.add_CardToHand(card)
                    i+=1

            elif self.card_in_play.get("Name") == "Madness":
                if len(self.hand) > 0:
                    indexOfRandomCardInHand = rd.randint(0,len(self.hand)-1)
                    self.hand[indexOfRandomCardInHand]["Energy changed for the battle"] = True
                    self.hand[indexOfRandomCardInHand]["Energy"] = 0
                    ansiprint("<blue>"+self.hand[indexOfRandomCardInHand]["Name"]+"</blue>","now costs 0 <yellow>Energy</yellow> for the rest of the battle.")
                else:
                    print("You have no cards left in your hand.")       

            elif self.card_in_play.get("Name") == "Madness +":
                if len(self.hand) > 0:
                    indexOfRandomCardInHand = rd.randint(0,len(self.hand)-1)
                    self.hand[indexOfRandomCardInHand]["Energy changed for the battle"] = True
                    self.hand[indexOfRandomCardInHand]["Energy"] = 0
                    ansiprint("<blue>"+self.hand[indexOfRandomCardInHand]["Name"]+"</blue>","now costs 0 <yellow>Energy</yellow> for the rest of the battle.")
                else:
                    print("You have no cards left in your hand.")

            elif self.card_in_play.get("Name") == "Mind Blast":
                self.choose_enemy()
                self.attack(len(self.draw_pile))

            elif self.card_in_play.get("Name") == "Mind Blast +":
                self.choose_enemy()
                self.attack(len(self.draw_pile))

            elif self.card_in_play.get("Name") == "Panacea":
                self.set_artifact(self.card_in_play["Artifact"])

            elif self.card_in_play.get("Name") == "Panacea +":
                self.set_artifact(self.card_in_play["Artifact"])

            elif self.card_in_play.get("Name") == "Panic Button":
                self.blocking(self.card_in_play["Block"])
                self.set_noBlock(2)

            elif self.card_in_play.get("Name") == "Panic Button +":
                self.blocking(self.card_in_play["Block"])
                self.set_noBlock(2)

            elif self.card_in_play.get("Name") == "Purify":             
                i = 0
                self.showHand()
                answers = ["1","2"]
                while i < self.card_in_play["Exhausting"]:
                    snap = input("Do you want to exhaust another card? (Yes/No)")
                    if snap not in answers:
                        print("You have to type either 1 or 2.")
                    if snap == "1":
                        self.exhaust(1)
                        i += 1
                    elif snap == "2":
                        break
                    else:
                        print("Please type either 1 or 2.")
                        self.explainer_function(snap,answer=False)

            elif self.card_in_play.get("Name") == "Purify +":               
                i = 0
                self.showHand()
                answers = ["1","2"]
                while i < self.card_in_play["Exhausting"]:
                    snap = input("Do you want to exhaust another card? (Yes/No)")
                    if snap not in answers:
                        print("You have to type either 1 or 2.")
                    if snap == "1":
                        self.exhaust(1)
                        i += 1
                    elif snap == "2":
                        break
                    else:
                        print("Please type either 1 or 2.")
                        self.explainer_function(snap,answer=False)

            elif self.card_in_play.get("Name") == "Swift Strike":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Swift Strike +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Trip":
                self.choose_enemy()
                entities.list_of_enemies[self.target].set_vulnerable(self.card_in_play["Vulnerable"])

            elif self.card_in_play.get("Name") == "Trip +":
                i = 0
                while i < len(entities.list_of_enemies):
                    entities.list_of_enemies[i].set_weakness(self.card_in_play["Weakness"])
                    if enemy_check == len(entities.list_of_enemies):
                        i+=1

            elif self.card_in_play.get("Name") == "Apotheosis":
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
            
            elif self.card_in_play.get("Name") == "Apotheosis +":
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

            elif self.card_in_play.get("Name") == "Chrysalis":
                while i < self.card_in_play["Cards"]:
                    skill_cards = {k:v for k,v in entities.cards.items() if v.get("Type") == "Skill" and v.get("Owner") == self.name and v.get("Rarity") != "Basic"}
                    #create a list of banned cards and exclude them from this pool via "not in list"
                    card = rd.choices(list(skill_cards.items()))[0][1]
                    card["Energy changed for the battle"] = True
                    card["Energy"] = 0
                    self.add_CardToDrawpile(card)
                    i += 1
            
            elif self.card_in_play.get("Name") == "Chrysalis +":
                while i < self.card_in_play["Cards"]:
                    skill_cards = {k:v for k,v in entities.cards.items() if v.get("Type") == "Skill" and v.get("Owner") == self.name and v.get("Rarity") != "Basic"}
                    #create a list of banned cards and exclude them from this pool via "not in list"
                    card = rd.choices(list(skill_cards.items()))[0][1]
                    card["Energy changed for the battle"] = True
                    card["Energy"] = 0
                    self.add_CardToDrawpile(card)
                    i += 1

            elif self.card_in_play.get("Name") == "Metamorphosis":
                while i < self.card_in_play["Cards"]:
                    attack_cards = {k:v for k,v in entities.cards.items() if v.get("Type") == "Attack" and v.get("Owner") == self.name and v.get("Rarity") != "Basic"}
                    card = rd.choices(list(skill_cards.items()))[0][1]                  
                    card["Energy changed for the battle"] = True
                    card["Energy"] = 0
                    self.add_CardToDrawpile(card)
                    i += 1

            elif self.card_in_play.get("Name") == "Metamorphosis +":
                while i < self.card_in_play["Cards"]:
                    attack_cards = {k:v for k,v in entities.cards.items() if v.get("Type") == "Attack" and v.get("Owner") == self.name and v.get("Rarity") != "Basic"}
                    card = rd.choices(list(skill_cards.items()))[0][1]                  
                    card["Energy changed for the battle"] = True
                    card["Energy"] = 0
                    self.add_CardToDrawpile(card)
                    i += 1

            elif self.card_in_play.get("Name") == "Swift Strike":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
            
            elif self.card_in_play.get("Name") == "Swift Strike +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Hand of Greed":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                if len(entities.list_of_enemies) < enemy_check:
                    self.set_gold(self.card_in_play["Gold"])
            
            elif self.card_in_play.get("Name") == "Hand of Greed +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                if len(entities.list_of_enemies) < enemy_check:
                    self.set_gold(self.card_in_play["Gold"])

            elif self.card_in_play.get("Name") == "Magnetism":
                self.set_magnetism(1)
            
            elif self.card_in_play.get("Name") == "Magnetism +":
                self.set_magnetism(1)

            elif self.card_in_play.get("Name") == "Master of Strategy":             
                self.draw(self.card_in_play["Draw"])
            
            elif self.card_in_play.get("Name") == "Master of Strategy +":               
                self.draw(self.card_in_play["Draw"])
            
            elif self.card_in_play.get("Name") == "Mayhem":             
                self.set_mayhem(1)
            
            elif self.card_in_play.get("Name") == "Mayhem +":
                self.set_mayhem(1)

            elif self.card_in_play.get("Name") == "Panache":
                self.set_panache(self.card_in_play["Damage"])
            
            elif self.card_in_play.get("Name") == "Panache +":
                self.set_panache(self.card_in_play["Damage"])

            elif self.card_in_play.get("Name") == "Secret Technique":
                self.draw_specific_cards_from_place(self.card_in_play["Draw"],self.card_in_play["Place"],self.card_in_play["Typing"])
            
            elif self.card_in_play.get("Name") == "Secret Technique +":
                self.draw_specific_cards_from_place(self.card_in_play["Draw"],self.card_in_play["Place"],self.card_in_play["Typing"])           

            elif self.card_in_play.get("Name") == "Secret Weapon":
                self.draw_specific_cards_from_place(self.card_in_play["Draw"],self.card_in_play["Place"],self.card_in_play["Typing"])

            elif self.card_in_play.get("Name") == "Secret Weapon +":
                self.draw_specific_cards_from_place(self.card_in_play["Draw"],self.card_in_play["Place"],self.card_in_play["Typing"])               

            elif self.card_in_play.get("Name") == "The Bomb":
                self.set_theBomb(self.card_in_play["Damage"],turn_counter)
            
            elif self.card_in_play.get("Name") == "The Bomb +":
                self.set_theBomb(self.card_in_play["Damage"],turn_counter)

            elif self.card_in_play.get("Name") == "Transmutation":
                neutral_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == "Colorless"}
                while i < self.energy:
                    card = rd.choices(list(neutral_cards.items()))[0][1]
                    card["This turn Energycost changed"] = True
                    card["Energy"] = 0
                    self.add_CardToHand(card)
                    i += 1

            elif self.card_in_play.get("Name") == "Transmutation +":
                neutral_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == "Colorless" and v.get("Upgraded") == True}
                while i < self.energy:
                    card = rd.choices(list(neutral_cards.items()))[0][1]
                    card["This turn Energycost changed"] = True
                    card["Energy"] = 0
                    self.add_CardToHand(card)
                    i += 1

            elif self.card_in_play.get("Name") == "Violence":               
                self.draw_specific_cards_from_place(self.card_in_play["Draw"],self.card_in_play["Place"],self.card_in_play["Typing"],random = True)
            
            elif self.card_in_play.get("Name") == "Violence +": 
                self.draw_specific_cards_from_place(self.card_in_play["Draw"],self.card_in_play["Place"],self.card_in_play["Typing"],random = True)
            
            elif self.card_in_play.get("Name") == "Thinking Ahead":
                self.draw(self.card_in_play["Draw"])
                self.putBackOnDeckFromHand(self.card_in_play["Back Putter"],bottom = True)
            
            elif self.card_in_play.get("Name") == "Thinking Ahead +":
                self.draw(self.card_in_play["Draw"])
                self.putBackOnDeckFromHand(self.card_in_play["Back Putter"],bottom = True)

            elif self.card_in_play.get("Name") == "Apparition":
                self.set_intangible(self.card_in_play["Intangible"])
            
            elif self.card_in_play.get("Name") == "Apparition +":
                self.set_intangible(self.card_in_play["Intangible"])

            elif self.card_in_play.get("Name") == "Ritual Dagger":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                if enemy_check != len(entities.list_of_enemies):
                    for card in self.deck:
                        if card.get("Unique ID") == self.card_in_play.get("Unique ID"):
                            card["Damage"] += self.card_in_play["FatalBonus"]
                            self.card_in_play["Damage"] += self.card_in_play["FatalBonus"]
                                            
            elif self.card_in_play.get("Name") == "Ritual Dagger +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                if enemy_check != len(entities.list_of_enemies):
                    for card in self.deck:
                        if card.get("Unique ID") == self.card_in_play.get("Unique ID"):
                            card["Damage"] += self.card_in_play["FatalBonus"]
                            self.card_in_play["Damage"] += self.card_in_play["FatalBonus"]

            elif self.card_in_play.get("Name") == "JAX":
                self.receive_recoil_damage(-self.card_in_play.get("Harm"),directDamage=True)
                self.set_strength(self.card_in_play.get("Strength"))
                
            elif self.card_in_play.get("Name") == "JAX +":
                self.receive_recoil_damage(-self.card_in_play.get("Harm"),directDamage=True)
                self.set_strength(self.card_in_play.get("Strength"))

            elif self.card_in_play.get("Name") == "Bite":               

                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.heal(self.card_in_play["Heal"])

            elif self.card_in_play.get("Name") == "Bite +":
                self.choose_enemy()
                self.attack(self.card_in_play["Damage"])
                self.heal(self.card_in_play["Heal"])

            else:
                print(self.card_in_play.get("Name"),"<--- this card is not implemented. Snap Snap Snap.")
        
        elif self.card_in_play.get("Type") == "Curse" and exhaust == True:              
            ansiprint("<m>"+self.card_in_play.get("Name")+"</m> is exhausted and is removed from play!")

        elif self.card_in_play.get("Type") == "Curse":
            ansiprint("<m>"+self.card_in_play.get("Name")+"</m> is exhausted and is removed from play because of <light-red>Blue Candle</light-red>!")
            self.receive_recoil_damage(-1,directDamage=True)
        
        elif self.card_in_play.get("Name") == "Slimed":
            ansiprint("You are no longer <green>slimed</green>.")

        elif self.card_in_play.get("Type") == "Status":
            ansiprint("<black>"+self.card_in_play.get("Name")+"</black> is exhausted and is removed from play because of <light-red>Medical Kit</light-red>!")

        else:
            print("This is a weird card",self.card_in_play)

        self.add_CardsFromExhaustQueueToExhaustPile()
        try:
            if self.card_in_play != None:
            
                self.resolveCardPlay(turn_counter,repeat,exhaust)
            
        except Exception as e:
            print("Failing to resolve a card at the end of card_is_played. Error:",e)
    
    def resolveCardPlay(self,turn_counter,repeat,exhaust):
        #if self.card_in_play != None:

        self.check_CardPlayPenalties()

        if self.card_in_play.get("Type") == "Attack":
            self.set_attackCounter()

        elif self.card_in_play.get("Type") == "Skill":
            self.set_skillCounter()
        
        elif self.card_in_play.get("Type") == "Power":
            self.set_powerCounter()

        self.set_cardCounter()

        #if not repeat and self.card_in_play.get("Type") != "Curse" and self.card_in_play.get("Type") != "Status":
        if not repeat and self.card_in_play.get("Energy") != None:
            self.reduce_energy()

        if self.afterImage > 0:
            self.blocking(self.afterImage,unaffectedBlock= True)

        if self.thousandCuts > 0:
            i = 0
            while i < len(entities.list_of_enemies):
                enemy_check = len(entities.list_of_enemies)
                entities.list_of_enemies[i].receive_recoil_damage(self.thousandCuts)
                if enemy_check == len(entities.list_of_enemies):
                    i+=1
                
            ansiprint("<blue>A Thousand Cuts</blue> did this!")

        i = 0
        while i < len(entities.list_of_enemies):
            enemy_check = len(entities.list_of_enemies)
            if entities.list_of_enemies[i].choke > 0:
                entities.list_of_enemies[i].receive_recoil_damage(entities.list_of_enemies[i].choke)

            if enemy_check == len(entities.list_of_enemies):
                i+=1

        for enemy in entities.list_of_enemies:
            enemy.cardTypeCheck(self.card_in_play.get("Type"))
            if enemy.choke > 0:
                enemy.receive_recoil_damage(enemy.choke)

        if not repeat:
            
            if self.burst > 0 and self.card_in_play.get("Type") == "Skill":
                self.burst -= 1
                self.randomTarget = True
                self.double_play_card = copy.deepcopy(self.card_in_play)

            elif self.doubleTap > 0 and self.card_in_play.get("Type") == "Attack":
                self.doubleTap -= 1
                self.randomTarget = True
                self.double_play_card = copy.deepcopy(self.card_in_play)
            
            elif self.necronomicon > 0 and self.card_in_play.get("Energy") >= 2:
                self.necronomicon = 0
                self.randomTarget = True
                self.double_play_card = copy.deepcopy(self.card_in_play)
                
            elif self.duplication > 0 and self.card_in_play.get("Type") != "Curse" and self.card_in_play.get("Type") != "Status":
                self.duplication -= 1
                self.randomTarget = True
                self.double_play_card = copy.deepcopy(self.card_in_play)
            
            if exhaust:             
                self.add_CardToExhaustpile(self.card_in_play)
                self.card_in_play = None
            
            elif self.card_in_play.get("Exhaust") == True:                      
                self.add_CardToExhaustpile(self.card_in_play)
                self.card_in_play = None

            elif self.corruption == True and self.card_in_play.get("Type") == "Skill":
                self.add_CardToExhaustpile(self.card_in_play)
                self.card_in_play = None
                
            elif self.card_in_play.get("Type") == "Power":
                self.power_pile.append(self.card_in_play)
                self.card_in_play = None
            
            elif self.card_in_play.get("Type") == "Curse":
                self.add_CardToExhaustpile(self.card_in_play)
                self.card_in_play = None
                
            elif self.card_in_play.get("Type") == "Status":
                self.add_CardToExhaustpile(self.card_in_play)
                self.card_in_play = None

            else:

                self.add_CardToDiscardpile(self.card_in_play,noMessage=True)
                self.card_in_play = None

            if self.double_play_card != None:
                self.card_is_played(self.double_play_card,turn_counter,repeat=True)

        
        if self.panache > 0 and self.card_counter % 5 == 0:
            i = 0
            while i < len(entities.list_of_enemies):
                enemy_check = len(entities.list_of_enemies)
                self.target = i
                entities.list_of_enemies[i].receive_recoil_damage(self.panache)
                
                if len(entities.list_of_enemies) == enemy_check:
                    i+=1

        #this happens after the card has been exhausted so the first burst doesn't duplicate itself.
        try:
            if preBurst > 0:
                self.set_burst(preBurst)
                preBurst = 0
        except Exception as e:
            pass

        if repeat:
            self.randomTarget = False
            self.double_play_card = None
        
        if exhaust:
            self.randomTarget = False

    def play_potion(self,turn_counter,potion_index=False):
        
        if potion_index == False:
            if potion_index == 0:
                pass
            else:
                return
        
        potion_in_play = []

        if len(self.potionBag) == 0:
            ansiprint("You don't have any <c>Potions</c> in your <c>Potion Bag</c>.")
            return
        
        while True:
            try:
                if potion_index == len(self.potionBag):
                    return
                
                if potion_index in range(len(self.potionBag)):
                    
                    if self.potionBag[potion_index]["Name"] == "Fairy in a Bottle":
                        ansiprint("<c>Fairy in a Bottle</c> can't be played. It will revive you automatically if you die. I hope.")
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
                return
        
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
                attack_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == self.name and v.get("Type") == "Attack" and v.get("Upgraded") == None}
                cards = rd.choices(list(attack_cards.items()),k=3)
                
                three_options = []
                for card in cards:
                    three_options.append(copy.deepcopy(card[1]))

                
                print("") #just for readability
                for card in three_options:
                    if type(card.get("Energy")) == int:
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
            colorless_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == "Colorless" and v.get("Rarity") != "Special" and v.get("Upgraded") == None}
            cards = rd.choices(list(colorless_cards.items()),k=3)
            
            three_options = []
            for card in cards:
                three_options.append(copy.deepcopy(card[1]))

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
                self.playCardFromTopOfDeck(exhaust=False)
                i+=1

        elif potion_in_play[0]["Name"] == "Duplication Potion":
            self.set_duplication(potion_in_play[0]["Potion Yield"])
            if sacredBark:
                self.set_duplication(potion_in_play[0]["Potion Yield"])

        elif potion_in_play[0]["Name"] == "Elixir":
            i = 0
            self.showHand()
            while i < len(self.hand):
                snap = input("Do you want to exhaust another card? (Yes/No)")
                if snap == "Yes":
                    self.exhaust(1)
                    i += 1
                elif snap == "No":
                    break
                else:
                    print("Please type Yes or No.")
                    self.explainer_function(snap,answer=False)

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
                check = input("Do you want to discard cards?(Yes/No)You draw as many as you discard.")
                
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
        
        elif potion_in_play[0]["Name"] == "Heart Of Iron":
            self.set_metallicice(potion_in_play[0]["Potion Yield"])
            if sacredBark:
                self.set_metallicice(potion_in_play[0]["Potion Yield"])
                
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

            power_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == self.name and v.get("Type") == "Power" and v.get("Upgraded") == None}
            cards = rd.choices(list(power_cards.items()),k=3)
            
            three_options = []
            for card in cards:
                three_options.append(copy.deepcopy(card[1]))

            
            print("") #just for readability
            for card in three_options:
                card["This turn Energycost changed"] = True
                card["Energy"] = 0
            
            helping_functions.pickCard(three_options,"Hand")


        elif potion_in_play[0]["Name"] == "Regen Potion": 
            self.set_regen(potion_in_play[0]["Potion Yield"])
            if sacredBark:
                self.set_regen(potion_in_play[0]["Potion Yield"])

        elif potion_in_play[0]["Name"] == "Skill Potion": 
            skill_cards = {k:v for k,v in entities.cards.items() if v.get("Owner") == self.name and v.get("Type") == "Skill" and v.get("Upgraded") == None}
            cards = rd.choices(list(skill_cards.items()),k=3)
            
            three_options = []
            for card in cards:
                three_options.append(copy.deepcopy(card[1]))

            
            print("") #just for readability
            for card in three_options:
                if type(card.get("Energy")) == int:
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
        self.doubleTap = 0
        
        self.attack_counter = 0
        self.skill_counter = 0
        self.power_counter = 0

        self.card_counter = 0

        if self.dontLoseBlock > 0:
            self.dontLoseBlock -= 1
        self.tempSpikes = 0

        if self.intangible > 0:
            self.intangible -= 1

        for relic in self.relics:
            if relic.get("name") == "Orange Pellets":
                relic["Power Counter"] = 0
                relic["Attack Counter"] = 0
                relic["Skill Counter"] = 0

                

    def draw_specific_cards_from_place(self,amount,place,typeOfCard = None,random = False):
        
        if place == "Drawpile":
            i = 0
            while i < amount:   
                if len(self.draw_pile) == 0:
                    print("The drawpile is currently empty.")
                    break

                if typeOfCard != None:
                    typeCheck = [card for card in self.draw_pile if card.get("Type") == typeOfCard]
                            
                    if len(typeCheck) == 0:
                        print("You don't have any",typeOfCard,"cards in your drawpile.")
                        break

                try:
                    if random:
                        card_index = rd.randint(0,len(self.draw_pile)-1)
                    else:
                        self.show_drawpile()
                        card_index = input("Which card do you want to draw?\n")
                        card_index = int(card_index)-1
                    if card_index in range(len(self.draw_pile)):
                        
                        if typeOfCard == None:
                            card = self.get_shuffledDrawpile()[card_index]
                            uniqueIDIndex = self.get_indexOfUniqueIDInDrawpile(card.get("Unique ID")) 
                            self.add_CardToHand(self.draw_pile.pop(uniqueIDIndex))
                        
                        else:
                                    
                            if self.get_shuffledDrawpile()[card_index].get("Type") != typeOfCard:
                                if not random:
                                    ansiprint("You need to choose a",typeOfCard,"card!")
                                continue
                            
                            else:
                                card = self.get_shuffledDrawpile()[card_index]
                                uniqueIDIndex = self.get_indexOfUniqueIDInDrawpile(card.get("Unique ID")) 
                                self.add_CardToHand(self.draw_pile.pop(uniqueIDIndex))
                        i += 1
                except ValueError:
                    if len(card_index) > 0:
                        self.explainer_function(card_index)
                    else:
                        ansiprint("You have to type a number.")

                except Exception as e:
                    self.explainer_function(card_index)
                    print("You need to type a corresponding number. This is one of the more... fragile functions so just in case here is the error: draw_specific_cards_from_place",e)
        
        elif place == "Discardpile":
            i = 0

            while i < amount:
                if len(self.discard_pile) == 0:
                    print("The Discardpile is currently empty.")
                    break


                if typeOfCard != None:
                    typeCheck = [card for card in self.discard_pile if card.get("Type") == typeOfCard]
                                
                    if len(typeCheck) == 0:
                        print("You don't have any",typeOfCard,"cards in your Discardpile.")
                        break
                try:
                    if random:
                        card_index = rd.randint(0,len(self.discard_pile)-1)
                    else:
                        self.show_discardpile()
                        card_index = input("Which card do you want to draw?\n")
                        card_index = int(card_index)-1
                    if card_index in range(len(self.discard_pile)):
                        color = self.get_cardColor(self.discard_pile[card_index]["Type"])
                        if typeOfCard == None:

                            self.add_CardToHand(self.discard_pile.pop(card_index))                      

                        else:
    
                            
                            if self.discard_pile[card_index]["Type"] != typeOfCard:
                                if not random:
                                    ansiprint("You need to choose a",typeOfCard,"card!")
                                continue
                            
                            else:
                                self.add_CardToHand(self.discard_pile.pop(card_index))

                        i += 1
                    
                except ValueError:
                    if len(card_index) > 0:
                        self.explainer_function(card_index)
                    else:
                        ansiprint("You have to type a number.") 
                except Exception as e:
                    self.explainer_function(card_index)
                    print("You need to type a corresponding number. This is one of the more... fragile functions so just in case here is the error: draw_specific_cards_from_place",e)

        elif place == "Exhaustpile":
            i = 0
            while i < amount:
                if len(self.exhaust_pile) == 0:
                    print("The Exhaustpile is currently empty.")
                    break

                if typeOfCard != None:
                    typeCheck = [card for card in self.exhaust_pile if card.get("Type") == typeOfCard]
                                
                    if len(typeCheck) == 0:
                        print("You don't have any",typeOfCard,"cards in your Exhaustpile.")
                        break
                try:
                    if random:
                        card_index = rd.randint(0,len(self.exhaust_pile)-1)
                    else:
                        self.show_exhaustpile()
                        card_index = input("Which card do you want to draw?\n")
                        card_index = int(card_index)-1
                    if card_index in range(len(self.exhaust_pile)):
                        color = self.get_cardColor(self.exhaust_pile[card_index]["Type"])
                        if typeOfCard == None:

                            self.add_CardToHand(self.exhaust_pile.pop(card_index))
        
                        else:
                            
                            
                            if self.exhaust_pile[card_index]["Type"] != typeOfCard:
                                if not random:
                                    ansiprint("You need to choose a",typeOfCard,"card!")
                                continue
                            
                            else:
                                self.add_CardToHand(self.exhaust_pile.pop(card_index))

                            i += 1
                    
                except ValueError:
                    if len(card_index) > 0:
                        self.explainer_function(card_index)
                    else:
                        ansiprint("You have to type a number.")
                                            
                except Exception as e:
                    self.explainer_function(card_index)
                    print("You need to type a corresponding number. This is one of the more... fragile functions so just in case here is the error:draw_specific_cards_from_place",e)


    def draw_innates(self):
        i = 0
        otherCards = len(self.hand) #these are cards you get from relics Ninja scroll
        while i < len(self.draw_pile):
            
                if self.draw_pile[i].get("Innate") == True:
                    self.add_CardToHand(self.draw_pile.pop(i),silent=True)

                else:
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
        
        if self.cantDraw == True:
            ansiprint(self.displayName,"can't draw anything this turn.")
            return

        i = 0
        while i < draw_power:
                
            if len(self.draw_pile) == 0:
                
                self.discardBackInDrawpile()

            if len(self.draw_pile) > 0:
                
                self.add_CardToHand(self.draw_pile.pop(0),silent=True)
                
            else:
                print("You don't have any cards left to draw.")
            
            i += 1
        
        self.cardsDrawnEffectCheck(i)

    def cardsDrawnEffectCheck (self,cardsDrawn):
        i = 0
        agonyCount = 0
        agonyPlusCount = 0
        evolveCount = 0
        try:
            while i < cardsDrawn:
                if self.hand[-(i+1)].get("Name") == "Void":
                    self.gainEnergy(-1)
                    if self.evolve > 0:
                        evolveCount += self.evolve
                elif self.hand[-(i+1)].get("Name") == "Endless Agony":
                    agonyCount += 1
                    
                elif self.hand[-(i+1)].get("Name") == "Endless Agony":
                    agonyPlusCount += 1
                
                elif self.hand[-(i+1)].get("Type") == "Status":
                    evolveCount += self.evolve
                i+=1
        except Exception as e:
            print("cardsDrawnEffectCheck",e)
        while agonyCount > 0:
            self.add_CardToHand({"Name": "Endless Agony", "Damage":4,"Exhaust":True,"Energy": 0, "Type": "Attack" ,"Rarity": "Uncommon","Owner":"Silent"}) 
            agonyCount -= 1

        while agonyPlusCount > 0:
            self.add_CardToHand({"Name": "Endless Agony +","Damage":6,"Exhaust":True,"Energy": 0, "Type": "Attack" ,"Upgraded": True,"Rarity": "Uncommon","Owner":"Silent"})

        if evolveCount > 0:
            self.draw(evolveCount)
    
    def discardBackInDrawpile(self):
        
        self.draw_pile.extend(self.discard_pile)
        self.discard_pile = []
        self.shuffleDrawPile()

    def blockingNextTurn(self,value):
        self.blockNextTurn += value + self.dexterity
        #looks unaffected by frail
        ansiprint(self.displayName,"blocks for",self.blockNextTurn,"next turn!")

    def reduce_energy(self):
        
        try:
            if self.card_in_play.get("Energy") == "X":
                self.energy = 0
            else:
                if self.energy - self.card_in_play.get("Energy") < 0:
                    ansiprint("Somehow there is negativ energy now:",self.energy,"\nYou just played:",self.card_in_play.get("Name"))
                else:
                                        
                    if self.cardsCostNothing > 0:
                        pass
                    else:
                        self.energy -= self.card_in_play.get("Energy")
                    
                    ansiprint(self.displayName, "has <yellow>"+str(self.energy)+ " Energy</yellow>.")
        
        except Exception as e:
            print(e,"issue in reduce_energy")
    

        self.changeEnergyCostAfterPlayed()

    def changeEnergyCostAfterPlayed(self):
        try:
            if self.card_in_play.get("Energy changed until played") == True:
                self.card_in_play.pop("Energy changed until played",None)
                self.card_in_play["Energy"] = entities.cards[self.card_in_play.get("Name")].get("Energy")
    
        except Exception as e:
            print(e,"changeEnergyCostAfterPlayed")

    def changeEnergyCostAfterTurn(self):
        try:

            for card in self.hand:
                if card.get("This turn Energycost changed") == True:
                    #print(card)
                    card.pop("This turn Energycost changed",None)                   
                    card["Energy"] = entities.cards[card.get("Name")].get("Energy")
                    #print(entities.cards[card.get("Name")].get("Energy"))
            for card in self.draw_pile:
                if card.get("This turn Energycost changed") == True:
                    #print(card)
                    card.pop("This turn Energycost changed",None)
                    card["Energy"] = entities.cards[card.get("Name")].get("Energy")
                    #print(entities.cards[card.get("Name")].get("Energy"))
            for card in self.discard_pile:
                if card.get("This turn Energycost changed") == True:
                    #print(card)
                    card.pop("This turn Energycost changed",None)
                    card["Energy"] = entities.cards[card.get("Name")].get("Energy")
                    #print(entities.cards[card.get("Name")].get("Energy"))
            for card in self.exhaust_pile:
                if card.get("This turn Energycost changed") == True:
                    #print(card)
                    card.pop("This turn Energycost changed",None)
                    card["Energy"] = entities.cards[card.get("Name")].get("Energy")
                    #print(entities.cards[card.get("Name")].get("Energy"))
        except Exception as e:
            print(e)

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
                relic["Attack Counter"] += 1
                if relic.get("Attack Counter") > 0 and relic.get("Skill Counter") > 0 and relic.get("Power Counter") > 0:
                    relic["Attack Counter"] = 0
                    relic["Skill Counter"] = 0
                    relic["Power Counter"] = 0
                    self.remove_allDebuffs()
                    
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
            elif relic.get("Name") == "Orange Pellets":
                relic["Skill Counter"] += 1
                if relic.get("Attack Counter") > 0 and relic.get("Skill Counter") > 0 and relic.get("Power Counter") > 0:
                    relic["Attack Counter"] = 0
                    relic["Skill Counter"] = 0
                    relic["Power Counter"] = 0
                    self.remove_allDebuffs()

                    print("This is not implemented yet but you should be cleared of all your negative effects.")


    def set_powerCounter(self):
        self.power_counter += 1
        storedCardIndexes = []

        if self.mummifiedHand > 0:
            #this needs to be implemented smarter. Just too lazy now.
            i = 0
            while i < len(self.hand):
                if self.hand[i].get("Energy") != None:
                    if self.hand[i].get("Energy") > 0:
                        storedCardIndexes.append(i)
                
                i+= 1
        
        if len(storedCardIndexes) > 0:
            changedCardIndex = storedCardIndexes[rd.randint(0,len(storedCardIndexes)-1)]
            
            self.hand[changedCardIndex]["This turn Energycost changed"] = True
            self.hand[changedCardIndex]["Energy"] = 0
            color = self.get_cardColor(self.hand[changedCardIndex].get("Type"))

            ansiprint(f"<{color}>{self.hand[changedCardIndex].get('Name')}</{color}> costs <yellow>0 Energy</yellow> this turn because of <light-red>Mummified Hands</light-red>!")

        if self.birdFacedUrn > 0:
            self.heal(2)
            ansiprint("You <red>heal 2</red> because of <light-red>Bird-Faced Urn</light-red>!")

        for relic in self.relics:
            if relic.get("Name") == "Orange Pellets":
                relic["Power Counter"] += 1
                if relic.get("Attack Counter") > 0 and relic.get("Skill Counter") > 0 and relic.get("Power Counter") > 0:
                    relic["Attack Counter"] = 0
                    relic["Skill Counter"] = 0
                    relic["Power Counter"] = 0
                    self.remove_allDebuffs()

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
            if self.randomTarget == False:
                self.showEnemies()
            while True:
                try:
                    if self.randomTarget == False:
                        target = input("\nPick the opponent you want to target\n")
                        target = int(target)-1
                    else:
                        target = rd.randint(0,len(entities.list_of_enemies)-1)

                    if target == len(entities.list_of_enemies):
                        self.hand.insert(self.cardIndex,self.card_in_play)
                        self.card_in_play = None
                        break

                    if target in range(len(entities.list_of_enemies)):
                        break

                    else:
                        ansiprint("There is no opponent at that place.")
                        continue
                except ValueError:
                    if len(target) > 0:
                        self.explainer_function(target)
                    else:
                        ansiprint("You have to type a number.")
                        
                except Exception as e:
                    self.explainer_function(target)
                    print("choose_enemy",e)
                    ansiprint("You have to type a corresponding number!")
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

    def channelOrb(self,orb, amount = 1):
        i = 0

        while i < amount:
            if self.maxOrbs <= 0:
                ansiprint("You don't have any Orbslots!")
                return

            if type(orb) == dict:
                self.orbs.append(orb)
                self.evokeOrb(amount=1)                
                if orb.get("Name") == "Lightning":
                    self.lightningCounter += 1
                elif orb.get("Name") == "Frost":
                    self.frostCounter += 1
                ansiprint(f"You channeled a {orb.get('Name')} Orb!")
            else:
                if len(self.orbs) == self.maxOrbs:
                    self.evokeOrb(amount=1)
                
                if orb == "Lightning":
                    self.orbs.append({"Name": "Lightning", "Value":3,"Evokation":8})
                    self.lightningCounter += 1
                elif orb == "Frost":
                    self.orbs.append({"Name":"Frost","Value":2,"Evokation":5})
                    self.frostCounter += 1
                elif orb == "Dark":
                    self.orbs.append({"Name":"Dark","Value":6,"Evokation":6})
                elif orb == "Plasma":
                    self.orbs.append({"Name":"Plasma","Value":1,"Evokation":2})
                else:
                    print("This is your broken Orb text",orb)
            
                ansiprint(f"You channeled a {orb} Orb!")
            i +=1


    def evokeOrb(self,amount=1):
        if len(self.orbs) <= 0:
            ansiprint(f"You don't have any Orbs to evoke!")
            return

        i = 0
        while i < amount:
            if len(entities.list_of_enemies) == 0:
                break

            if self.orbs[0].get("Name") == "Lightning":
                if self.electrodynamics == False:
                    randomEnemy = rd.randint(0,len(entities.list_of_enemies)-1)
                    entities.list_of_enemies[randomEnemy].receive_recoil_damage(self.getOrbEvokation(self.orbs[0]),orbDamage = True)
                else:
                    i = 0
                    while i < len(entities.list_of_enemies):
                        enemy_check =len(entities.list_of_enemies)
                        entities.list_of_enemies[i].receive_recoil_damage(self.getOrbEvokation(self.orbs[0]),orbDamage = True)
                        if enemy_check != len(entities.list_of_enemies):
                            pass
                        else:
                            i+=1
            elif self.orbs[0].get("Name") == "Dark":
                enemyIndex = 0
                smallestHPIndex = 0
                smallestHPValue = entities.list_of_enemies[0].health
                while enemyIndex < len(entities.list_of_enemies) -1:
                    if entities.list_of_enemies[enemyIndex].health < smallestHPValue:
                        smallestHPValue = entities.list_of_enemies[enemyIndex].health
                        smallestHPIndex = enemyIndex
                    
                    enemyIndex += 1

                entities.list_of_enemies[smallestHPIndex].receive_recoil_damage(self.getOrbEvokation(self.orbs[0]),orbDamage=True)

            elif self.orbs[0].get("Name") == "Frost":
                self.blocking(self.getOrbEvokation(self.orbs[0]),unaffectedBlock=True)

            elif self.orbs[0].get("Name") == "Plasma":
                self.gainEnergy(self.getOrbEvokation(self.orbs[0]))
            
            else:
                print("This is the broken Orb->",self.orbs[0])

            ansiprint(f"You evoked a {self.orbs[0].get('Name')} orb!")
            i+=1

        self.orbs.pop(0)
        
    def passiveOrbsTurnStart(self):
        i = 0
        for orb in self.orbs:
            if orb.get("Name") == "Plasma":
                self.gainEnergy(orb.get("Value"))
                if self.goldPlatedCables == True and i == 0:
                    self.gainEnergy(orb.get("Value"))
            i+= 1

    def passiveOrbsTurnEnd(self,loopTrigger = False):
        if len(entities.list_of_enemies) == 0:
            return
        i = 0
        for orb in self.orbs:
            if len(entities.list_of_enemies) == 0:
                break

            if orb.get("Name") == "Lightning":
                if self.electrodynamics == False:
                    randomEnemy = rd.randint(0,len(entities.list_of_enemies)-1)
                    damage = orb.get("Value") + self.focus
                    if damage < 0:
                        damage = 0
                    entities.list_of_enemies[randomEnemy].receive_recoil_damage(damage,orbDamage=True)
                else:
                    i = 0
                    while i < len(entities.list_of_enemies):
                        enemy_check =len(entities.list_of_enemies)
                        damage = self.orbs[i].get("Value") + self.focus
                        if damage < 0:
                            damage = 0
                        entities.list_of_enemies[i].receive_recoil_damage(damage,orbDamage = True)
                        if enemy_check == len(entities.list_of_enemies):
                            i+=1


            elif orb.get("Name") == "Frost":
                block = orb.get("Value") + self.focus
                if block < 0:
                    block = 0
                self.blocking(block,unaffectedBlock=True)

            elif orb.get("Name") == "Dark":
                darkchange = orb.get("Value") + self.focus
                if darkchange < 0:
                    darkchange = 0
                orb["Evokation"] += darkchange

            elif orb.get("Name") == "Plasma":
                pass

            else:
                print("Non existent Orb ->",orb)

            if loopTrigger == True:
                break

    def getOrbPassive(self,orb):
        
        if orb.get("Name") == "Lightning":
            damage = orb.get("Value") + self.focus
            if damage < 0:
                damage = 0
        elif orb.get("Name") == "Frost":
            damage = orb.get("Value") + self.focus
            if damage < 0:
                damage = 0
        elif orb.get("Name") == "Dark":
            damage = orb.get("Value") + self.focus
            if damage < 0:
                damage = 0
        elif orb.get("Name") == "Plasma":
            damage = orb.get("Value")
            if damage < 0:
                damage = 0

        return damage

    def getOrbEvokation(self,orb):
        
        if orb.get("Name") == "Lightning":
            damage = orb.get("Evokation") + self.focus
            if damage < 0:
                damage = 0
        elif orb.get("Name") == "Frost":
            damage = orb.get("Evokation") + self.focus
            if damage < 0:
                damage = 0
        elif orb.get("Name") == "Dark":
            damage = orb.get("Evokation")
            if damage < 0:
                damage = 0
        elif orb.get("Name") == "Plasma":
            damage = orb.get("Evokation")
            if damage < 0:
                damage = 0

        return damage

    def attack(self,attack,preview:bool=False):

        strength = self.strength
        if self.card_in_play.get("Name") == "Heavy Blade":
            strength *= 3
        elif self.card_in_play.get("Name") == "Heavy Blade +":
            strength *= 5
        else:
            pass

        if len(entities.list_of_enemies) > 0 or preview == True:
            
            attack += strength

            if self.card_in_play.get("Name") == "Shiv" or self.card_in_play.get("Name") == "Shiv+":
                attack += self.accuracy

            if self.strikeDummy > 0 and "Strike" in self.card_in_play.get("Name"):
                attack += 3

            if self.wristBlade == 1 and self.card_in_play.get("Energy") == 0:
                attack += 4
            
            if self.card_in_play.get("Name") == "Perfected Strike":
                for card in self.hand:
                    if "Strike" in card.get("Name"):
                        attack += 2
                for card in self.draw_pile:
                    if "Strike" in card.get("Name"):
                        attack += 2
                for card in self.discard_pile:
                    if "Strike" in card.get("Name"):
                        attack += 2
                for card in self.exhaust_pile:
                    if "Strike" in card.get("Name"):
                        attack += 2

            elif self.card_in_play.get("Name") == "Perfected Strike +":
                for card in self.hand:
                    if "Strike" in card.get("Name"):
                        attack += 3
                for card in self.draw_pile:
                    if "Strike" in card.get("Name"):
                        attack += 3
                for card in self.discard_pile:
                    if "Strike" in card.get("Name"):
                        attack += 3
                for card in self.exhaust_pile:
                    if "Strike" in card.get("Name"):
                        attack += 3

            if preview:
                if self.card_in_play.get("Energy") == "X":
                    attack *= self.energy

            if self.akabeko > 0 and self.attack_counter == 0:
                attack *= 2

            if len(self.doubleDamage) > 0:
                if self.doubleDamage[0] == helping_functions.turn_counter:
                    attack *= 2

            if self.penNip > 0:
                attack*=2

            if self.weak > 0:
                attack = attack - math.floor(attack * 0.25)

            if attack < 0:
                attack = 0
            
            if preview:
                return attack
            else:
                entities.list_of_enemies[self.target].receive_damage(attack)
            
        else:
            print("You tried to attack but there is no enemy. def attack")
            pass

    def blocking(self,block_value,unaffectedBlock: bool = False,preview:bool=False):
        
        if self.noBlock > 0:
            ansiprint(self.displayName,"can't receive block for",self.noBlock,"turns.")
        else:
            if unaffectedBlock:
                self.block += block_value

            else:

                if self.frail > 0:
                    block_value = (block_value + self.dexterity) - int((block_value + self.dexterity) * 0.25)
                    
                else:
                    block_value = block_value + self.dexterity
                    

                if preview:
                    return block_value
                else:
                    self.block += block_value
                
                if self.juggernaut > 0 and block_value > 0:
                    randomEnemy = rd.randint(0,len(entities.list_of_enemies)-1)
                    entities.list_of_enemies[randomEnemy].receive_recoil_damage(self.juggernaut)
                    ansiprint(f"<blue>Juggernaut</blue> did this <red>damage</red>")

                if self.block < 0:
                    self.block = 0
                
            ansiprint(f"{self.displayName} blocked for <green>{block_value}</green> and now has <green>{self.block} Block</green>!")

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
        
        if self.runicPyramid > 0:
            ansiprint("You keep your hand because of <light-red>Runic Pyramid</light-red>.")

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
                print("You don't have any cards in your hand.")
                break
            else:
                if random == False:
                    self.showHand()
                try:
                    if random:
                        card_index = rd.randint(0,len(self.hand) - 1)
                    else:
                        card_index = input("Pick the number of the card you want to exhaust\n")
                        card_index = int(card_index)-1
                    
                    if card_index < len(self.hand):
                        self.add_CardToExhaustQueue(self.hand.pop(card_index))
                        i += 1
                        
                        self.exhaust_counter += 1
                
                
                except Exception as e:
                    self.explainer_function(card_index)
                    ansiprint("You have to type the number of the Card you want to exhaust. exhaust function")
                    pass

        self.add_CardsFromExhaustQueueToExhaustPile()
        return card_index

    def exhaust_ethereals(self):
        i = 0
        while i < len(self.hand):
            if self.hand[i].get("Ethereal") == True:
                self.add_CardToExhaustpile(self.hand.pop(i))
                ansiprint("Because it was <light-cyan>Ethereal</light-cyan>!")
            else:
                i += 1

    def putBackOnDeckFromHand(self, amount, energyChange = None, energyChangeType = None, bottom: bool = False,skip: bool = True):

        i = 0
        while i < amount:
            if len(self.hand) == 0:
                print("You don't have any cards in your hand")
                break
            else:
                self.showHand()
                if skip:
                    print(f"{len(self.hand)+1}.  Skip")
                try:
                    
                    card_index = input("Pick the number of the card you want to put back on your Deck.\n")
                    card_index = int(card_index) - 1
                    
                    if card_index in range(len(self.hand)):
                        color = self.get_cardColor(self.hand[card_index].get("Type"))   
                        if energyChangeType == "For Battle":
                            self.hand[card_index]["Energy changed for the battle"] = True
                            self.hand[card_index]["Energy"] = energyChange
                            ansiprint(f"The cost of <{color}>{self.hand[card_index].get('Name')}</{color}> changed to <yellow>{energyChange} Energy</yellow> for the rest of the battle.")

                        elif energyChangeType == "Until Played":
                            self.hand[card_index]["Energy changed until played"] = True
                            self.hand[card_index]["Energy"] = energyChange
                            ansiprint(f"The cost of <{color}>{self.hand[card_index].get('Name')}</{color}> changed to <yellow>{energyChange} Energy</yellow> until played.")

                        if bottom:
                            self.draw_pile.insert(len(self.draw_pile),self.hand.pop(card_index))
                            ansiprint(f"<{color}>{self.draw_pile[-1].get('Name')}</{color}> is now at the bottom of your deck.")
                        else:
                            self.draw_pile.insert(0,self.hand.pop(card_index))
                            ansiprint(f"<{color}>{self.draw_pile[0].get('Name')}</{color}> is now at the top of your deck.")

                        i += 1
                        
                    elif card_index == len(self.hand) and skip:
                        print("You decided to put no more cards back in your deck.")
                        break
                    else:
                        pass    
                
                except Exception as e:
                    self.explainer_function(card_index)
                    ansiprint("You have to type the number of the Card you want to put back on your deck. putBackOnDeckFromHand")
                    print(e)
                    pass

    def putBackOnDeckFromDiscardPile(self, amount, energyChange = None, energyChangeType = None, bottom: bool = False, skip: bool = False):

        i = 0
        while i < amount:
            if len(self.discard_pile) == 0:
                print("You don't have any cards in your Discardpile")
                break
            else:
                self.show_discardpile()
                if skip == True:
                    print(f"{len(self.discard_pile)+1}.  Skip")
                try:
                    
                    card_index = input("Pick the number of the card you want to put back on your Deck.\n")
                    card_index = int(card_index) - 1
                    if card_index in range(len(self.discard_pile)):
                        color = self.get_cardColor(self.discard_pile[card_index].get("Type"))
                        
                        if energyChangeType == "For Battle":
                            self.hand[card_index]["Energy changed for the battle"] = True
                            self.hand[card_index]["Energy"] = energyChange
                            ansiprint(f"The cost of <{color}>{self.hand[card_index].get('Name')}</{color}> changed to <yellow>{energyChange} Energy</yellow> for the rest of the battle.")

                        elif energyChangeType == "Until Played":
                            self.hand[card_index]["Energy changed until played"] = True
                            self.hand[card_index]["Energy"] = energyChange
                            ansiprint(f"The cost of <{color}>{self.hand[card_index].get('Name')}</{color}> changed to <yellow>{energyChange} Energy</yellow> until played.")

                        if bottom:
                            self.draw_pile.insert(len(self.draw_pile),self.discard_pile.pop(card_index))
                            ansiprint(f"<{color}>{self.draw_pile[-1].get('Name')}</{color}> is now at the bottom of your deck.")
                        else:
                            self.draw_pile.insert(0,self.discard_pile.pop(card_index))
                            ansiprint(f"<{color}>{self.draw_pile[0].get('Name')}</{color}> is now on top of your deck.")

                        i+=1
                    
                    elif card_index == len(self.hand) and skip:
                        print("You decided to skip.")
                        break
                    else:
                        pass    
                
                except Exception as e:
                    self.explainer_function(card_index)
                    ansiprint("You have to type the number of the Card you want to put back on your deck. putBackOnDeckFromDiscardPile")
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
        
        if self.noBlock > 0:
            self.noBlock -= 1

        if len(self.doubleDamage) > 0:
            if helping_functions.turn_counter == self.doubleDamage[0]:
                self.doubleDamage.pop(0)

        if self.cardsCostNothing > 0:
            self.cardsCostNothing -= 1
        
        self.cantDraw = False
        self.entangled = False

        self.damage_counter = 0
        
        self.rage = 0

        if self.akabeko > 0 and self.attack_counter > 0:
            self.akabeko = 0

        self.timeWarp = False

    def showRelics(self):
        for relic in self.relics:
            if "Counter" in relic:
                ansiprint("<light-red>"+relic.get("Name")+"</light-red> | Counter:",relic.get("Counter"),"| Effect:",relic.get("Info"))
            else:
                ansiprint("<light-red>"+relic.get("Name")+"</light-red>","| Effect:",relic.get("Info"))

    def showHand(self, noUpgrades: bool = False,battlemode: bool = False,skip:bool=False):
           
        blockAttackCard = False
        for card in self.hand:
            if card.get("Block") != None and card.get("Damage") != None and card.get("Energy") != None:
                blockAttackCard = True

        length = 0
        for card in self.hand:
            if len(card.get("Name")) > length:
                length = len(card.get("Name"))
        
        i = 0
        savedCard = None
        if self.card_in_play != None:
            savedCard = self.card_in_play
        for card in self.hand:
            self.card_in_play = card
            color = self.get_cardColor(card.get("Type"))
            if i+1 < 10:
                numberSpacing = " "
            else:
                numberSpacing = "  "
            

            lineSpacing = " " * (length+3-len(card.get("Name")))

            if blockAttackCard == False:
                energySpacing = "     " 
            else:
                energySpacing = "        "

            try:
                if noUpgrades == True and card.get("Upgrade") == True:
                    pass
                elif battlemode == True:
                    
                    if card.get("Block") != None and card.get("Damage") != None and card.get("Energy") != None:
                        damage = self.attack(card.get("Damage"),preview=True)
                        block = self.blocking(card.get("Block"),preview=True)                       
                        blockDamageString = f"<red>{damage}</red>/<green>{block}</green>"
                        actualBlockDamageStringLength = len(blockDamageString) - (5 + 6 + 7 + 8)
                        energySpacing = energySpacing[:-actualBlockDamageStringLength]
                        ansiprint(f"{i+1}.{numberSpacing}<{color}>{card.get('Name')}</{color}>{lineSpacing}{blockDamageString}{energySpacing}<yellow>{card.get('Energy')}</yellow>")    
                    
                    elif card.get("Block") != None:
                        block = self.blocking(card.get("Block"),preview=True)
                        energySpacing = energySpacing[:-len(str(block))]
                        ansiprint(f"{i+1}.{numberSpacing}<{color}>{card.get('Name')}</{color}>{lineSpacing}<green>{block}</green>{energySpacing}<yellow>{card.get('Energy')}</yellow>")
                        
                    elif card.get("Damage") != None:
                    
                        damage = self.attack(card.get("Damage"),preview=True)
                        energySpacing = energySpacing[:-len(str(damage))]
                        ansiprint(f"{i+1}.{numberSpacing}<{color}>{card.get('Name')}</{color}>{lineSpacing}<red>{damage}</red>{energySpacing}<yellow>{card.get('Energy')}</yellow>")
                    
                    elif card.get("Energy") == None:
                        energySpacing = energySpacing[:-1]
                        ansiprint(f"{i+1}.{numberSpacing}<{color}>{card.get('Name')}</{color}>{lineSpacing}<red>Unplayable</red>")

                    else:
                        energySpacing = energySpacing[:-1]
                        ansiprint(f"{i+1}.{numberSpacing}<{color}>{card.get('Name')}</{color}>{lineSpacing} {energySpacing}<yellow>{card.get('Energy')}</yellow>")      
                
                elif card.get("Energy") == None:
                    ansiprint(f"{i+1}.{numberSpacing}<{color}>{card.get('Name')}</{color}>{lineSpacing}<red>Unplayable</red>")
                else:
                    ansiprint(f"{i+1}.{numberSpacing}<{color}>{card.get('Name')}</{color}>{lineSpacing}<yellow>{card.get('Energy')}</yellow>")
                
            
            except Exception as e:
                print(e,"Show Hand")

            i = i + 1
        if skip:
            print(f"{i+1}.{numberSpacing}Skip")

        if savedCard:
            self.card_in_play = savedCard
        else:
            self.card_in_play = None

    def show_drawpile(self):
        ansiprint("This is your Drawpile:\n\n")
        if self.frozenEye:
            i = 0
            for card in self.draw_pile:
                color = self.get_cardColor(card.get("Type"))
                if i+1 < 10:
                    numberSpacing = "  "
                else:
                    numberSpacing = " "
                
                lineSpacing = " " * (20-len(card.get("Name")))
                
                if card.get("Energy") == None:
                    ansiprint(f"{i+1}.{numberSpacing}<{color}>{card.get('Name')}</{color}>{lineSpacing}<red>Unplayable</red>")
                else:
                    ansiprint(f"{i+1}.{numberSpacing}<{color}>{card.get('Name')}</{color}>{lineSpacing}<yellow>{card.get('Energy')}</yellow>")
                
                i = i + 1
        else:
            try:
                i = 0
                if i+1 < 10:
                    numberSpacing = "  "
                else:
                    numberSpacing = " "
                for card in sorted(self.draw_pile,key=str):
                    color = self.get_cardColor(card.get("Type"))
                    lineSpacing = " " * (20-len(card.get("Name")))
                    if card.get("Energy") == None:
                        ansiprint(f"{i+1}.{numberSpacing}<{color}>{card.get('Name')}</{color}>{lineSpacing}<red>Unplayable</red>")
                    else:
                        ansiprint(f"{i+1}.{numberSpacing}<{color}>{card.get('Name')}</{color}>{lineSpacing}<yellow>{card.get('Energy')}</yellow>")

                    i = i + 1
            except Exception as e:
                print(e)
    def get_indexOfUniqueIDInDrawpile(self,uniqueID):
        i = 0
        for card in self.draw_pile:
            if uniqueID == card.get("Unique ID"):
                break
            i+=1
        return i

    def get_shuffledDrawpile(self):
        if self.frozenEye == True:
            randomDrawpile = self.draw_pile
        else:
            randomDrawpile = sorted(self.draw_pile,key=str)

        return randomDrawpile

    def show_discardpile(self):

        i = 0
        for card in self.discard_pile:
            color = self.get_cardColor(card.get("Type"))
            if i+1 < 10:
                numberSpacing = "  "
            else:
                numberSpacing = " "
            
            lineSpacing = " " * (20-len(card.get("Name")))
            
            if card.get("Energy") == None:
                ansiprint(f"{i+1}.{numberSpacing}<{color}>{card.get('Name')}</{color}>{lineSpacing}<red>Unplayable</red>")
            else:
                ansiprint(f"{i+1}.{numberSpacing}<{color}>{card.get('Name')}</{color}>{lineSpacing}<yellow>{card.get('Energy')}</yellow>")
            
            i = i + 1

    def show_exhaustpile(self):

        i = 0
        for card in self.exhaust_pile:
            color = self.get_cardColor(card.get("Type"))
            if i+1 < 10:
                numberSpacing = "  "
            else:
                numberSpacing = " "
            
            lineSpacing = " " * (20-len(card.get("Name")))
            
            if card.get("Energy") == None:
                ansiprint(f"{i+1}.{numberSpacing}<{color}>{card.get('Name')}</{color}>{lineSpacing}<red>Unplayable</red>")
            else:
                ansiprint(f"{i+1}.{numberSpacing}<{color}>{card.get('Name')}</{color}>{lineSpacing}<yellow>{card.get('Energy')}</yellow>")      
            i = i + 1
    
    def showDeck(self,noUpgrades:bool = False,remove:bool = False):
        
        i = 0
        for card in self.deck:
            color = self.get_cardColor(card.get("Type"))
            if i+1 < 10:
                numberSpacing = "  "
            else:
                numberSpacing = " "
            
            lineSpacing = " " * (20-len(card.get("Name")))
            if noUpgrades == True and card.get("Upgrade") == True:
                pass
            elif card.get("Energy") == None:
                ansiprint(f"{i+1}.{numberSpacing}<{color}>{card.get('Name')}</{color}>{lineSpacing}<red>Unplayable</red>")
            else:
                ansiprint(f"{i+1}.{numberSpacing}<{color}>{card.get('Name')}</{color}>{lineSpacing}<yellow>{card.get('Energy')}</yellow>")
            
            i = i + 1
   

    def showPotions(self,skip=False,battlemode=True):
        try:
            if battlemode:
                potions = ""
                i = 0
                for potion in self.potionBag:
                    potions += "{}. <c>{}</c>\n".format(i+1+len(self.hand),potion.get("Name"))
                    i = i + 1
                ansiprint(potions)
            else:
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

    def showEnemies(self,skip=True,numbers=True):
        
        if numbers == False and len(entities.list_of_enemies)>0:
            ansiprint("\n<red>Enemies</red>:")
        gegner = ""
        i = 0
        for opponent in entities.list_of_enemies:
            if numbers == True:
                gegner += "\n{}.) {} (<red>{}</red>/<red>{}</red>)".format(i+1,opponent.name,opponent.health,opponent.max_health)
            else:
                gegner += "\n{} (<red>{}</red>/<red>{}</red>)".format(opponent.name,opponent.health,opponent.max_health)
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
                gegner += " |<light-blue> Intangible: "+str(opponent.intangible)+"</light-blue>"
            if opponent.artifact > 0:
                gegner += " |<light-blue> Artifact: "+str(opponent.artifact)+"</light-blue>"
            if opponent.metallicize > 0:
                gegner += " |<light-blue> Metallicize: "+str(opponent.metallicize)+"</light-blue>"
            if opponent.barricade == True:
                gegner += " |<light-blue> Barricade</light-blue>"
            if opponent.choke > 0:
                gegner += " |<light-cyan> Choke: "+str(opponent.choke)+"</light-cyan>"
            if opponent.temp_strength > 0:
                gegner += " |<light-cyan> Shackled: "+str(opponent.temp_strength)+"</light-cyan>"
            if opponent.strengthChange > 0:
                gegner += " |<light-cyan> Shifting: -"+str(opponent.strengthChange)+"</light-cyan>"
            if opponent.sadisticNature > 0:
                gegner += " |<light-blue> Sadistic Nature: "+str(opponent.sadisticNature)+"</light-blue>"
            if opponent.heartVincibility > 0:
                gegner += " |<light-blue> Heart Vincibility: "+str(opponent.heartVincibility)+"</light-blue>"
            if opponent.slow > 0:
                gegner += " |<light-blue> Slow: "+str(opponent.slow)+"</light-blue>"
            for effect in opponent.on_hit_or_death:
                if type(effect[0]) == str:
                    if "Curl" in effect[0]:
                        gegner += " |<light-blue> Curl: "+effect[0].split(" ")[1]+"</light-blue>"
                elif type(effect[0]) == int:
                    gegner += " |<light-blue> Spikes: "+str(effect[0])+"</light-blue>"
            if self.runicDome == 0:
                if opponent.move:
                    gegner += " | "+ self.enemy_preview(i)
                if self.card_in_play != None:
                    if self.card_in_play.get("Damage"):
                        gegner += " | "+ self.determine_damage_to_enemy(i)
            
            i = i + 1
        if skip:
            gegner += "\n" +str(i+1) + ".) Skip" 
        ansiprint(gegner)

    def enemy_preview(self,index,spotWeaknessCheck=False):
        previewString = ""
        if self.runicDome == 1 and spotWeaknessCheck == False:
            previewString = "???"
        
        else:
            damage = None
            if type(entities.list_of_enemies[index].move) == int:
                
                damage = self.determine_damage_to_character(entities.list_of_enemies[index].move,index)

                previewString = "Attacks for <red>" + str(damage)+"</red>"
                
            elif "Multiattack" in entities.list_of_enemies[index].move:
                
                amount = entities.list_of_enemies[index].move.split(" ")[1].split("*")[1]
                damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1].split("*")[0]),index)

                previewString = "Attacks "+str(amount)+" times for <red>"+str(damage)+" Damage</red>."

            elif "Thrash" in entities.list_of_enemies[index].move:

                damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1].split("/")[0]),index)
                previewString = "Attacks for <red>"+str(damage)+"</red>. <green>Blocks</green>"

            elif "Blocking" in entities.list_of_enemies[index].move:

                previewString = "Will <green>Block</green>"

            elif "Weak" in entities.list_of_enemies[index].move:
                
                previewString = "Applies <light-cyan>Debuff</light-cyan>"

            elif "Vulnerable" in entities.list_of_enemies[index].move:
                
                previewString = "Applies <light-cyan>Debuff</light-cyan>"

            elif "Frail" in entities.list_of_enemies[index].move:
                
                previewString = "Applies <light-cyan>Debuff</light-cyan>"

            elif "Ritual" in entities.list_of_enemies[index].move:

                previewString = "<light-blue>Buff</light-blue>"

            elif "Grow" in entities.list_of_enemies[index].move:
            
                previewString = "<light-blue>Buff</light-blue>"

            elif "Bellow" in entities.list_of_enemies[index].move:
                
                previewString = "Will <green>Block</green> and <light-blue>Buff</light-blue> itself"

            elif "GoopSpray" in entities.list_of_enemies[index].move:

                previewString = "Applies strong <light-cyan>Debuff</light-cyan>"

            elif "Support Automaton" in entities.list_of_enemies[index].move:

                previewString = "<light-blue>Buff</light-blue>"

            elif "Entangle" in entities.list_of_enemies[index].move:

                previewString = "Applies <light-cyan>Debuff</light-cyan>"

            elif "Suck" in entities.list_of_enemies[index].move:

                damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1]),index)
                previewString = "Attacks for <red>"+str(damage)+" damage</red>. Buffs itself"
            
            elif "CenturionDefendAlly" in entities.list_of_enemies[index].move:

                previewString = "<light-blue>Buff</light-blue>"

            elif "MysticBuff" in entities.list_of_enemies[index].move:

                previewString = "<light-blue>Buff</light-blue>"

            elif "MysticHeal" in entities.list_of_enemies[index].move:

                previewString = "<light-blue>Buff</light-blue>"

            elif "SmokeBomb" in entities.list_of_enemies[index].move:

                previewString = "Will <green>Block</green>"

            elif "CenturionDefendAlly" in entities.list_of_enemies[index].move:
                
                previewString = "Will <green>Block</green>"         

            elif "Protect" in entities.list_of_enemies[index].move:

                previewString = "Will <green>Block</green>"

            elif "VentSteam" in entities.list_of_enemies[index].move:

                previewString = "Applies <light-cyan>Debuff</light-cyan>"

            elif "DefensiveMode" in entities.list_of_enemies[index].move:

                previewString = "<light-blue>Buff</light-blue>"

            elif "TwinSlam" in entities.list_of_enemies[index].move:
                
                amount = entities.list_of_enemies[index].move.split(" ")[1].split("*")[1]
                damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1].split("*")[0]),index)

                previewString = "Attacks "+str(amount)+" times for <red>"+str(damage)+" Damage</red>. Buffs itself"

            elif "Haste" in entities.list_of_enemies[index].move:

                previewString = "<light-blue>Buff</light-blue>"

            elif "TimeSlam" in entities.list_of_enemies[index].move:

                amount = entities.list_of_enemies[index].move.split(" ")[1].split("/")[1]
                damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1].split("/")[0]),index)

                previewString = "Attacks "+str(amount)+" times for <red>"+str(damage)+" damage</red>. Applies a negative effect"

            elif "Divider" in entities.list_of_enemies[index].move:
                damage = self.determine_damage_to_character(6,index)
                previewString = f"Attacks {self.health // 12 + 1} times for <red> {damage} </red>"

            elif "Inferno" in entities.list_of_enemies[index].move:
                
                amount = entities.list_of_enemies[index].move.split(" ")[1].split("*")[1]
                damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1].split("*")[0]),index)

                previewString = "Attacks "+str(amount)+" times for <red>"+str(damage)+" Damage</red>. Applies Debuff"

            elif "Enrage" in entities.list_of_enemies[index].move:

                previewString = "<light-blue>Buff</light-blue>"

            elif "Hex" in entities.list_of_enemies[index].move:
                
                previewString = "Applies strong <light-cyan>Debuff</light-cyan>"

            elif "SiphonSoul" in entities.list_of_enemies[index].move:
                
                previewString = "Applies strong <light-cyan>Debuff</light-cyan>"

            elif "Bolt" in entities.list_of_enemies[index].move:

                previewString = "Applies <light-cyan>Debuff</light-cyan>"

            elif "Encourage" in entities.list_of_enemies[index].move:

                previewString = "<light-blue>Buff</light-blue>"

            elif "Ripple" in entities.list_of_enemies[index].move:

                previewString = "Will <green>Block</green> and apply a Debuff"

            elif "BurningDebuff" in entities.list_of_enemies[index].move:

                previewString = "Applies <light-cyan>Debuff</light-cyan>"

            elif "SnakeStrike" in entities.list_of_enemies[index].move:

                amount = entities.list_of_enemies[index].move.split(" ")[1].split("*")[1]
                damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1].split("*")[0]),index)

                previewString = "Attacks "+amount+" times for <red>"+damage+"</red>. Applies Debuff"

            elif "Gloat" in entities.list_of_enemies[index].move:

                previewString = "<light-blue>Buff</light-blue>"

            elif "ChampAnger" in entities.list_of_enemies[index].move:

                previewString = "<light-blue>Buff</light-blue>"

            elif "DefensiveStance" in entities.list_of_enemies[index].move:
                
                previewString = "<light-blue>Buff</light-blue>"

            elif "Roar" in entities.list_of_enemies[index].move:

                previewString = "Applies <light-cyan>Debuff</light-cyan>"

            elif "MegaDebuff" in entities.list_of_enemies[index].move:

                previewString = "Applies <light-cyan>Debuff</light-cyan>"
                
            elif "TorchBuff" in entities.list_of_enemies[index].move:
                
                previewString = "Will <green>Block</green> and <light-blue>Buff</light-blue>"

            elif "BearHug" in entities.list_of_enemies[index].move:

                previewString = "Applies <light-cyan>Debuff</light-cyan>"

            elif "SpikeUp" in entities.list_of_enemies[index].move:

                previewString = "<light-blue>Buff</light-blue>"

            elif "Repulse" in entities.list_of_enemies[index].move:

                previewString = "Applies <light-cyan>Debuff</light-cyan>"

            elif "Constrict" in entities.list_of_enemies[index].move:

                previewString = "Applies strong <light-cyan>Debuff</light-cyan>"

            elif "Implant" in entities.list_of_enemies[index].move:

                previewString = "Applies strong <light-cyan>Debuff</light-cyan>"

            elif "GiantHead" in entities.list_of_enemies[index].move:

                additionalDamage = entities.list_of_enemies[index].counter * 5

                damage = self.determine_damage_to_character(int(entities.split(" ")[1]) + additionalDamage)
                previewString = "Attacks for "+str(damage)+" damage"

            elif "Fortify" in entities.list_of_enemies[index].move:

                previewString = "<light-blue>Buff</light-blue>"

            elif "BurnStrike" in entities.list_of_enemies[index].move:

                amount = entities.list_of_enemies[index].move.split(" ")[1].split("*")[1]
                damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1].split("*")[0]),index)

                previewString = "Attacks "+str(amount)+" times for <red>"+str(damage)+" damage</red>. Applies Debuff"

            elif "DazeBeam" in entities.list_of_enemies[index].move:

                amount = entities.list_of_enemies[index].move.split(" ")[1].split("*")[1]
                damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1].split("*")[0]),index)

                previewString = "Attacks "+str(amount)+" times for <red>"+str(damage)+" damage</red>. Applies Debuff"

            elif "SquareOfDeca" in entities.list_of_enemies[index].move:
                
                previewString = "<light-blue>Buff</light-blue>"

            elif "Debilitate" in entities.list_of_enemies[index].move:

                previewString = "Applies strong <light-cyan>Debuff</light-cyan>"            

            elif "HeartBuff" in entities.list_of_enemies[index].move:

                previewString = "<light-blue>Buff</light-blue>"

            elif "Transientattack" in entities.list_of_enemies[index].move:

                damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1])+(helping_functions.turn_counter-1)*10,index)
                previewString = "Attacks for <red>"+str(damage)+"</red>"

            elif "/" in entities.list_of_enemies[index].move:
                
                damage = self.determine_damage_to_character(int(entities.list_of_enemies[index].move.split(" ")[1].split("/")[0]),index)
                previewString = "Attacks for <red>"+str(damage)+"</red>. Applies Debuff"

            elif "|" in entities.list_of_enemies[index].move:
                
                previewString = "<light-blue>Buff</light-blue>"

            else:

                previewString = "???"
        
        if spotWeaknessCheck:
            return damage

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

    def determine_damage_to_enemy(self,index):
        #this function needs to pull from the enemy receive damage function
        attack = self.attack(self.card_in_play.get("Damage"),preview=True)
                
        attack = entities.list_of_enemies[index].receive_damage(attack,preview=True)
    
        return f"Receives <red>{attack} damage</red> from <red>{self.card_in_play.get('Name')}</red>"


    def receive_damage(self,attack_damage):
        if attack_damage > 0:

            if self.vulnerable > 0:
                
                if self.oddMushroom > 0:
                    attack_damage += attack_damage * 0.25
                else:
                    attack_damage += attack_damage * 0.50
                
            attack_damage = math.floor(attack_damage)
            
            if self.intangible > 0:
                attack_damage = 1
                
            damage = attack_damage - self.block
                
            if damage > 0:
                
                if self.check_buffer():             
                    
                    self.block = 0
                    
                    if self.torii > 0 and damage <= 5:
                        damage = 1
                        ansiprint(f"<light-red>Torii</light-red> reduced <red>damage</red> to <red>1 damage</red>")

                    if self.tungstenRod > 0:
                        damage -= 1
                        ansiprint(f"<light-red>Tungsten Rod</light-red> reduced <red>damage</red> by <red>1</red> to <red>{damage}</red>")


                    if damage > 0:
                        self.health -= damage
                        
                        if self.selfFormingClay == True:
                            self.blockNextTurn += 3

                        if self.runicCube == True:
                            self.draw(1)

                        if self.redSkull == True:
                            self.set_redSkull()

                        self.damageCounter()

                    if self.health < 1:
                        self.alive = False
                    else:
                        ansiprint(f"The {self.displayName} has taken <red>{damage} damage</red> and now has <red>{self.health} Health</red> left.")
                else:
                    self.block = 0

            else:
                self.block -= attack_damage

                ansiprint(self.displayName, "has <green>"+str(self.block)+" Block</green> and <red>"+str(self.health)+" Health</red> left.")
            
            if self.alive == False:
                entities.check_if_character_dead()

    def receive_recoil_damage(self,attack_damage,directDamage: bool = False):
        #there are some differences between recoil and normal damage. Therefore there are separate functions for that.
        
        if attack_damage > 0:
            
            if directDamage:
                damage = attack_damage
            else:
                damage = attack_damage - self.block

            if self.intangible > 0:
                ansiprint(f"<light-blue>Intangible</light-blue> reduced <red>damage</red> to <red>1</red>.")
                damage = 1          
            
            if damage > 0:

                if self.check_buffer():             

                    if self.torii > 0 and damage <= 5:
                        damage = 1
                        ansiprint(f"<light-red>Torii</light-red> reduced <red>damage</red> to <red>1 damage</red>")

                    if self.tungstenRod > 0:
                        damage -= 1
                        ansiprint(f"<light-red>Tungsten Rod</light-red> reduced <red>damage</red> by <red>1</red> to <red>{damage}</red>")
                
                    if damage > 0:
                        
                        if directDamage == True:
                            if self.rupture > 0:
                                self.set_strength(self.rupture)
                        
                        if directDamage == False:
                            self.block = 0

                        self.damageCounter()
                        self.health -= damage

                        if self.selfFormingClay == True:
                            self.blockNextTurn += 3

                        if self.runicCube == True:
                            self.draw(1)

                        if self.redSkull == True:
                            self.set_redSkull()
                        
                        if self.health < 1:
                            ansiprint("The",self.displayName,"has been defeated")
                            self.alive = False
                        else:
                            ansiprint(f"The {self.displayName} has taken <red>{damage} damage</red> and now has <red>{self.health} Health</red> left.")
                        
                    else:
                        self.block -= attack_damage
                        if self.block < 0:
                            self.block = 0
                        
                        ansiprint(f"{self.displayName} has <green>{self.block} block</green> left and <red>{self.health} health</red> left.")

                    if self.alive == False:
                            entities.check_if_character_dead()

                else:
                    self.block = 0



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

    def set_deck(self):
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
                {"Name": "Ascender's Bane","Ethereal":True,"Type": "Curse","Irremovable":True,"Rarity": "Special","Owner":"The Spire","Info":"<BLUE>Ethereal</BLUE>. <RED>Unplayable</RED>."}
                ]

        ironclad_deck = [ {"Name": "Strike", "Damage":6, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Ironclad"},
                {"Name": "Strike", "Damage":6, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Ironclad"},
                {"Name": "Strike", "Damage":6, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Ironclad"},
                {"Name": "Strike", "Damage":6, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Ironclad"},
                {"Name": "Strike", "Damage":6, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Ironclad"},
                {"Name": "Defend", "Block":5, "Energy": 1,"Type": "Skill" ,"Rarity": "Basic","Owner":"Ironclad"},
                {"Name": "Defend", "Block":5, "Energy": 1,"Type": "Skill" ,"Rarity": "Basic","Owner":"Ironclad"},
                {"Name": "Defend", "Block":5, "Energy": 1,"Type": "Skill" ,"Rarity": "Basic","Owner":"Ironclad"},
                {"Name": "Defend", "Block":5, "Energy": 1,"Type": "Skill" ,"Rarity": "Basic","Owner":"Ironclad"},
                {"Name":"Bash","Damage":8, "Vulnerable":2,"Energy":2,"Type":"Attack","Rarity":"Basic","Owner":"Ironclad","Info":"Deal <red>8 damage</red>. Apply <light-blue>2 Vulnerable</light-blue>"},
                {"Name": "Ascender's Bane","Ethereal":True,"Type": "Curse","Irremovable":True,"Rarity": "Special","Owner":"The Spire","Info":"<BLUE>Ethereal</BLUE>. <RED>Unplayable</RED>."}
                ]

        defect_deck = [
               
                {"Name": "Dualcast", "Energy": 1,"Type": "Skill" ,"Rarity": "Basic","Owner":"Defect","Info":"Evoke your next Orb twice."},
                {"Name": "Zap", "Energy": 1,"Type": "Skill" ,"Rarity": "Basic","Owner":"Defect","Info":"Channel 1 Lightning."},
                {"Name": "Defend", "Block":5, "Energy": 1,"Type": "Skill" ,"Rarity": "Basic","Owner":"Defect","Info":"Gain 5 Block."},
                {"Name": "Defend", "Block":5, "Energy": 1,"Type": "Skill" ,"Rarity": "Basic","Owner":"Defect","Info":"Gain 5 Block."},
                {"Name": "Defend", "Block":5, "Energy": 1,"Type": "Skill" ,"Rarity": "Basic","Owner":"Defect","Info":"Gain 5 Block."},
                {"Name": "Defend", "Block":5, "Energy": 1,"Type": "Skill" ,"Rarity": "Basic","Owner":"Defect","Info":"Gain 5 Block."},
                {"Name": "Strike", "Damage":6, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Defect","Info":"Deal 6 damage."},
                {"Name": "Strike", "Damage":6, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Defect","Info":"Deal 6 damage."},
                {"Name": "Strike", "Damage":6, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Defect","Info":"Deal 6 damage."},
                {"Name": "Strike", "Damage":6, "Energy": 1,"Type": "Attack" ,"Rarity": "Basic","Owner":"Defect","Info":"Deal 6 damage."},
                {"Name": "Ascender's Bane","Ethereal":True,"Type": "Curse","Irremovable":True,"Rarity": "Special","Owner":"The Spire","Info":"Ethereal. Unplayable."}
                ]

        if self.name == "Silent":
            for card in silent_deck:
                self.add_CardToDeck(card,silence=True)
        
        elif self.name == "Ironclad":
            for card in ironclad_deck:
                self.add_CardToDeck(card,silence=True)

        elif self.name == "Defect":
            for card in defect_deck:
                self.add_CardToDeck(card,silence=True)
        
    def heal(self,value):

        if self.markOfTheBloom > 0:
            ansiprint("You can't heal because of <light-red>Mark of the Bloom</light-red>.")

        else:
            if self.magicFlower == True:
                value += math.floor(value*0.5)
            
            self.health += value
            
            if self.redSkull == True:
                self.set_redSkull()

            if self.health > self.max_health:
                displayValue = self.health - self.max_health
                self.health = self.max_health

                ansiprint(f"{self.displayName} <red>heals</red> for <red>{value - displayValue}</red> and now has <red>{self.health} Health</red>.")
            else:
                ansiprint(f"{self.displayName} <red>heals</red> for <red>{value}</red> and now has <red>{self.health} Health</red>.")

    def regenerate(self):

        self.heal(self.regen)
        self.regen -= 1
        ansiprint(f"{self.displayName} now has <red>{self.regen} Regen</red> left.")

    def set_regen(self, value):

        self.regen += value
        
        ansiprint(f"{self.displayName} now has <red>{self.regen} Regen</red>.")

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

        if value < 0:
            if self.intangible > 0:
                value = -1

            if tungstenRod:
                value += 1

        self.health += value
        ansiprint(f"{self.displayName} changed <red>health</red> for <red>{value}</red> and has <red>{self.health} health</red> left.\n")

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
            
            i = 0
            
            for potion in self.potionbag:
                if potion.get("Name") == "Fairy in a Bottle":
                    break
                i+=1
            
            self.remove_Potion(index=i)

        elif source == "Lizard Tail":
            self.health = math.floor((self.max_health/100)*50)

        ansiprint(self.displayName,"resurrected and now has",self.health,"health.")

        self.alive = True

    def set_cardsCostZero(self,value):

        self.cardsCostNothing += value
        
        ansiprint(f"{self.displayName} cards cost nothing for {self.cardsCostNothing} turn(s).")

    def set_rage(self,value):

        self.rage += value
        
        ansiprint(f"You will receive <green>{self.rage} Block</green> everytime you plan an <red>attack</red>.")

    def set_accuracy(self,value):

        self.accuracy += value
        ansiprint(self.displayName,"has",self.accuracy,"Accuracy.")

    def set_spikes(self,value):
        
        self.spikes += value
        ansiprint(f"{self.displayName} has <light-blue>{self.spikes+self.tempSpikes} Spikes</light-blue>.")

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
        ansiprint(f"{self.displayName} has <light-blue>{self.spikes+self.tempSpikes} Spikes</light-blue>.")
    
    def set_ritual(self,value):

        self.ritual += value
        ansiprint(self.displayName,"has",self.ritual,"Ritual.",self.displayName,"will receive",self.ritual,"Strength per turn.")

    def set_strength(self,value):
        
        if value < 0:
            if self.check_artifact():
                self.strength += value
                ansiprint(f"{self.displayName} has lost <red>{value} Strength</red>.")
        else:
            self.strength += value
            ansiprint(f"{self.displayName} gained <red>{value} Strength</red>.")
    
    def set_dexterity (self,value):
            #have to add check artifact here in case negativity is applied
            if value < 0:
                if self.check_artifact():
                    self.dexterity += value
                    ansiprint(f"{self.displayName} has lost <green>{value} Dexterity</green>.")
            else:
                self.dexterity += value
                ansiprint(f"{self.displayName} gained <green>{value} Dexterity</green>.")

    def set_focus(self,value):
        
        if value < 0:
            if self.check_artifact():
                self.focus += value
                ansiprint(f"{self.displayName} has lost {value} <blue>Focus</blue>.")
        else:
            self.focus += value
            if value != 0:
                ansiprint(f"{self.displayName} gained {value} <blue>Focus</blue>.")
    
    def set_orbslots(self,value):
        
        if value < 0:            
            self.maxOrbs += value

            ansiprint(f"{self.displayName} has lost {abs(value)} <blue>Orbslot</blue>.")
        else:
            self.maxOrbs += value
            if value != 0:
                if self.maxOrbs > 10:
                    self.maxOrbs = 10
                    ansiprint(f"{self.displayName} you can't have more than 10 <blue>Orbslots</blue>.")
                else:    
                    ansiprint(f"{self.displayName} gained {value} <blue>Orbslots</blue>:.")


    def set_strengthDecrease(self,value):

        if self.check_artifact():
            decrease = [helping_functions.turn_counter+1,-value]            
            self.strengthDecrease.append(decrease)          
            ansiprint(self.displayName,"will lose",value,"<red>Strength</red> next turn.")
    
    def set_dexterityDecrease(self, value):

        if self.check_artifact():
            decrease = [turn_counter+1,-value]          
            self.dexterityDecrease.append(decrease)         
            ansiprint(self.displayName,"will lose",value,"Dexterity next turn.")

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
        ansiprint("Whenever you deal <red>damage</red> to an enemies health they will be <green>poisoned</green> for",self.envenom,".")

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
            self.confused = True
            ansiprint(self.displayName,"is confused. All cards have random cost.")


    def remove_allDebuffs(self):

        self.strengthDecrease = []
        self.dexterityDecrease = []
        self.confused = False
        self.cantDraw = False
        self.hex = False
        self.constriction = 0
        self.wraithForm = 0
        self.reducedDrawByTurns = []
        self.entangled = False
        #self.fasting = False

        if self.strength < 0:
            self.strength = 0
        if self.dexterity < 0:
            self.dexterity = 0

        self.frail = 0
        self.weak = 0
        self.vulnerable = 0
        self.noBlock = 0

        ansiprint("<light-red>Orange Pellets</red> removed all <light-cyan>Debuffs</light-cyan>")
    
    def set_weakness(self,value):
        if self.ginger > 0:
            ansiprint("You are immune to <light-cyan>Weakness</light-cyan> thanks to <light-red>Ginger</light-red>!")
        else:
            if self.check_artifact():
                self.weak += value
                ansiprint(f"{self.displayName} has now <light-cyan>{self.weak} Weakness</light-cyan>.\n")
            
    def set_vulnerable(self,value):
        if self.check_artifact():
            self.vulnerable += value
            ansiprint(f"{self.displayName} has now <light-cyan>{self.vulnerable} Vulnerable</light-cyan>.\n")

    def set_frail(self,value):
        if self.turnip > 0:
            ansiprint("You are immune to being <light-cyan>Frail</light-cyan> thanks to <light-red>Turnip</light-red>!\n")
        else:
            if self.check_artifact():
                self.frail += value
                ansiprint(f"{self.displayName} has <light-cyan>{self.frail} Frail</light-cyan>.\n")

    def set_constriction (self,value):
        if self.check_artifact():
            self.constriction += value
            ansiprint(self.displayName,"is constricted by the <red>Spire Growth</red> and you take <red>"+str(self.constriction)+"</red> damage at the start of each turn.\n")

    def set_hex(self):
        if self.check_artifact():
            self.hex = True
            ansiprint(self.displayName,"will receive 1 <light-cyan>Dazed</light-cyan> everytime you play a <red>non-attack</red> Card\n")

    def set_entangled(self):
        if self.check_artifact():
            self.entangled = True
            ansiprint(self.displayName, "is now entangled for 1 turn.\n")

    def set_cantDraw(self):
        if self.check_artifact():
            self.cantDraw = True
            ansiprint(self.displayName, "can't draw any more cards this turn.\n")
            

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
            ansiprint("You lose one buffer instead of suffering <red>damage</red>.")
            return False
        elif self.artifact == 0:
            return True

    def set_burst (self,value):
        
        self.burst += value
        ansiprint("The next",self.burst,"<green>Skill Card(s)</green> this turn are going to be played twice.") 

    def set_doubleTap (self,value):
        
        self.doubleTap += value
        ansiprint("The next",self.doubleTap,"<red>Attack Card(s)</red> this turn are going to be played twice.")    

    def set_duplication (self, value):

        self.duplication += value
        ansiprint("The next",self.duplication,"card(s) are going to be played twice.")  

    def set_artifact(self,value):

        self.artifact += value
        ansiprint("The next",self.artifact,"times negative effects are applied to you, will be negated.")

    def set_combust(self,damage,selfharm):
        self.combustDamage += damage
        self.combustSelfharm += selfharm
        #needs to trigger damage effects like cetennial puzzle.
        ansiprint(f"{self.displayName} is dealing <red>{self.combustDamage}</red> to ALL enemies at the start of each turn and takes <red>{self.combustSelfharm} damage</red> itself.")
    
    def set_darkEmbrace(self,value):
        
        self.darkEmbrace += value
        ansiprint(f"{self.displayName} will draw {self.darkEmbrace} cards whenever they <BLUE>exhaust</BLUE> a card.")

    def set_evolve(self,value):
        
        self.evolve += value
        ansiprint(f"{self.displayName} will draw {self.evolve} cards each turn they draw a <light-cyan>Status</light-cyan> card.")

    def set_feelNoPain(self,value):
        
        self.feelNoPain += value
        ansiprint(f"{self.displayName} will gain <green>{self.feelNoPain} Block</green> whenever they <BLUE>exhaust</BLUE> a card.")

    def set_fireBreathing(self,value):
    
        self.fireBreathing += value
        ansiprint(f"Whenever you draw a <light-cyan>Status</light-cyan> or a <m>Curse</m> Card you deal <red>{self.fireBreathing} damage</red> to ALL enemies.")

    def set_rupture(self,value):
        self.rupture += value
        ansiprint(f"Whenever you lose <red>HP</red> from a Card, gain <red>{self.rupture} Strength</red>.")     

    def set_barricade(self):
        self.barricade = True
        ansiprint("<green>Block</green> is not removed at the start of the turn.")

    def set_brutality(self,value):
        self.brutality += value
        ansiprint(f"At the start of your turn, you lose <red>{self.brutality} HP</red> and draw {self.brutality} Card(s).")

    def set_corruption(self):
        self.corruption = True
        for card in self.hand:
            if card.get("Type") == "Skill":
                card["Energy changed for the battle"] = True 
                card["Energy"] = 0

        for card in self.draw_pile:
            if card.get("Type") == "Skill":
                card["Energy changed for the battle"] = True 
                card["Energy"] = 0

        for card in self.discard_pile:
            if card.get("Type") == "Skill":
                card["Energy changed for the battle"] = True 
                card["Energy"] = 0

        for card in self.exhaust_pile:
            if card.get("Type") == "Skill":
                card["Energy changed for the battle"] = True 
                card["Energy"] = 0
        ansiprint("<green>Skills</green> cost 0 <yellow>Energy</yellow>. Whenever you play a <green>Skill</green>, <BLUE>Exhaust</BLUE> it.")


    def set_juggernaut(self,value):
        self.juggernaut += value
        ansiprint(f"Whenever you gain <green>Block</green>, deal <red>{self.juggernaut} damage</red> to a random enemy.")

    def set_heatsinks(self,value):
    
        self.heatsinks += value
        ansiprint(f"{self.displayName} will draw {self.heatsinks} cards each turn play a Power card.")

    def set_helloWorld(self,value):
    
        self.hello_world += value
        if self.hello_world == 1:
            ansiprint(f"{self.displayName} will get a random common card into their hand at the start of the turn.")
        else:
            ansiprint(f"{self.displayName} will get {self.hello_world} random common cards into their hand at the start of the turn.")
    
    def set_loop(self,value):
    
        self.loop += value
        if self.loop == 1:
            ansiprint(f"At the start of your turn, the passive ability of your first Orb will trigger {self.loop} more time.")
        else:
            ansiprint(f"At the start of your turn, the passive ability of your first Orb will trigger {self.loop} more times.")

    def set_selfRepair(self,value):
    
        self.selfRepair += value
        ansiprint(f"At the end of combat, {self.displayName} will heal {self.selfRepair} HP.")
        
    def set_staticDischarge(self,value):
    
        self.staticDischarge += value
        ansiprint(f"Whenever you receive unblocked attack damage, you Channel {self.staticDischarge} Lightning.")
    
    def set_storm(self,value):
    
        self.storm += value
        ansiprint(f"Whenever you play a Power card, you Channel {self.storm} Lightning.")
        
    def set_biasedCognition(self,value):
        if self.check_artifact():

            self.biasedCognition += value
            ansiprint(f"You lose {self.biasedCognition} Focus at the start of each turn.")
    
    def set_creativeAI(self,value):
    
        self.creativeAI += value
        if self.creativeAI == 1:
            ansiprint(f"{self.displayName} will get a random power card into their hand at the start of the turn.")
        else:
            ansiprint(f"{self.displayName} will get {self.creativeAI} random power cards into their hand at the start of the turn.")
     
    def set_echoForm(self,value):
    
        self.echoForm += value
        if self.echoForm == 1:
            ansiprint(f"The first card you play each turn is played twice")
        else:
            ansiprint(f"The first {self.echoForm} cards you play each turn are played twice")

    def set_electrodynamics(self,value):   
        self.electrodynamics = True
        ansiprint(f"Lightning now hits ALL enemies.")



    def set_drawPile(self):

        self.draw_pile = copy.deepcopy(self.deck)
        self.shuffleDrawPile()

    def print_all_cards(self):
        i = 0
        for card in self.hand:
            print(i+1,card)
            i+=1
        for card in self.discard_pile:
            print(i+1,card)
            i+=1
        for card in self.draw_pile:
            print(i+1,card)
            i+=1
        for card in self.exhaust_pile:
            print(i+1,card)
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
                    print("A generated Unique ID was identical to one in your deck.\nThat's not so bad as long as this prompt is not spammed to you endlessly.\nAlthough you should be sad because the likelyhood of this happening is around 1 in a million and I presume you'd want your luck spent elsewhere.\n Therefore you may have <yellow>1 Gold</yellow>.")
                    self.set_gold(1)
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
                    ansiprint("You increased your <red>Max HP by 6</red> because of adding a <m>Curse</m> to the deck while owning <light-red>Darkstone Periapt</light-red>.")

                self.deck.insert(index,card)

        else:
            
            self.deck.insert(index,card)

            color = self.get_cardColor(card.get("Type"))

            if silence == False:
                ansiprint(self.displayName, "added <"+color+">"+card.get("Name")+"</"+color+">", "to the deck.\n")
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
            color = self.get_cardColor(card.get("Type"))
            if index == None:
                index = len(self.hand)

            if len(self.hand) == 10:
                self.add_CardToDiscardpile(card,noMessage = True)
                ansiprint(f"{self.displayName} added <{color}>{card.get('Name')}</{color}> to the Discardpile because the Hand was full.\n")

            else:
                if self.confused and type(card.get("Energy")) == int:
                    card["Energy changed for the battle"] = True
                    card["Energy"] = rd.randint(0,3)

                if self.fireBreathing > 0:
                    if card.get("Type") == "Status" or card.get("Type") == "Curse":
                        i = 0
                        while i < len(entities.list_of_enemies):
                            enemy_check = len(entities.list_of_enemies)
                            entities.list_of_enemies[i].receive_recoil_damage(self.fireBreathing)
                            if enemy_check == len(entities.list_of_enemies):
                                i+=1

                if self.corruption == True and card.get("Type") == "Skill":
                    card["Energy changed for the battle"] = True 
                    card["Energy"] = 0

                self.hand.insert(index,card)
                
                if silent == False:
                    ansiprint(f"{self.displayName} added <{color}>{card.get('Name')}</{color}> to the Hand.\n")

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
            color = self.get_cardColor(card.get("Type"))
            
            ansiprint(f"{self.displayName} added <{color}>{card.get('Name')}</{color}> to the Drawpile.\n")
        
        except Exception as e:
            print(e,"Card To Drawpile")


    def add_CardToDiscardpile(self,card,index=None,noMessage=False):
        try:
            card = card.copy()
            if index == None:
                index = len(self.discard_pile)
            
            self.discard_pile.insert(index,card)
            color = self.get_cardColor(card.get("Type"))
            if noMessage == True:
                pass
            else:
                ansiprint(f"{self.displayName} added <{color}>{card.get('Name')}</{color}> to the Discardpile.\n")
        
        except Exception as e:
            print(e,"Card To Discardpile")

    def add_CardToExhaustQueue(self,card):
        card = card.copy()
        self.exhaustQueue.append(card)

    def add_CardsFromExhaustQueueToExhaustPile(self):
        for card in self.exhaustQueue:
            self.add_CardToExhaustpile(card)

        self.exhaustQueue = []

    def add_CardToExhaustpile(self,card,index=None):
        try:
            card = card.copy()

            color = self.get_cardColor(card.get("Type"))
                
            if index == None:
                index = len(self.exhaust_pile)
            #exhaustpile Stuff needs to be handled properly so when you exhaust your entire hand and something comes back it doesn't loop indefinitely 
            if card.get("Name") == "Necronomicurse":
                ansiprint("<c>"+card.get("Name")+ "</c> can't be removed!")
                self.add_CardToHand(card)
            else:
                if self.strangeSpoon > 0 and rd.randint(0,1) == 0:
                    self.add_CardToDiscardpile(card,index)
                    ansiprint(f"<{color}>{card.get('Name')}</{color}> was discarded instead of exhausted because of <light-red>Strange Spoon</light-red>.")
                
                else:
                    self.exhaust_pile.insert(index,card)
                    ansiprint(f"<{color}>{card.get('Name')}</{color}> exhausted and is removed from play.")
                    
                    if card.get("Name").startswith("Sentinel"):
                        self.gainEnergy(card.get("Energy Gain"))

                    if self.darkEmbrace > 0:
                        self.draw(self.darkEmbrace)
                        ansiprint("You draw because of <blue>Dark Embrace</blue>")

                    if self.feelNoPain > 0:
                        self.blocking(self.feelNoPain,unaffectedBlock=True)
                        ansiprint("<blue>Feel No Pain</blue> did this.")

                    if self.charonsAshes == True:
                        i = 0
                        while i < len(entities.list_of_enemies):
                            enemy_check = len(entities.list_of_enemies)
                            entities.list_of_enemies[i].receive_recoil_damage(3)
                            if enemy_check == len(entities.list_of_enemies):
                                i+=1                        

                    if self.deadBranch > 0:
                        randomCard = {k:v for k,v in entities.cards.items() if v.get("Owner") == self.name and v.get("Upgraded") == None}
                        self.add_CardToHand(rd.choices(list(randomCard.items()))[0][1])
        
        except Exception as e:
            print("Error in Card to ExhaustPile:",e)
    
    def get_cardColor(self,cardType):
        color = ""
        if cardType == "Attack":
            color = "red"
        elif cardType == "Skill":
            color = "green"
        elif cardType == "Power":
            color = "blue"
        elif cardType == "Status":
            color = "light-cyan"
        elif cardType == "Curse":
            color = "m"
        return color

    def add_potion(self,potion):
        
        sozu = False

        for relic in self.relics:
            if relic.get("Name") == "Sozu":
                sozu = True

        if sozu == True:
            ansiprint("You can't obtain any more <c>Potions</c> due to <light-red>Sozu</light-red>.")
        else:
            discardOptions = ["1. Replace one of your <c>Potions</c>.","2. Don't replace one of your <c>Potions</c>."]
        
            checkNumbers = ["1","2"]

            if len(self.potionBag) == self.potionBagSize:
                ansiprint(f"You can't have more than {self.potionBagSize} <c>Potions</c> in your <c>Potion Bag</c>.\n")
                
                self.showPotions(battlemode=False)

                for option in discardOptions:
                    ansiprint(option)

                choice = input("\nDo you want to discard one of your current potions?\n")

                while choice not in checkNumbers:
                    self.explainer_function(choice,answer=False)
                    choice = input("Do you want to discard one of your current potions? Type 1 or 2.\n")

                if choice == "1":
                    self.remove_Potion()
                    self.add_potion(potion)
                elif choice == "2":
                    ansiprint("You have chosen to not take this <c>Potion</c>.")
            else:
                self.potionBag.append(potion)
                ansiprint("<c>"+potion.get("Name")+"</c> is now in your <c>Potion Bag</c>.")
    
    def remove_Potion(self,index = None):
        
        while True:
            
            if index:
                choice = index
            else:
                self.showPotions(battlemode=False)
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
            except ValueError:
                self.explainer_function(choice)
            except Exception as e:
                
                print ("You have to type a number\n",e)
                
    
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
            ansiprint(f"{self.displayName} can now hold <c>{self.potionBagSize} Potions</c>.")

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
                three_options.append(copy.deepcopy(card[1]))


            helping_functions.pickPotion(five_options)
    
        elif relic.get("Name") == "Ring of the Serpent":
            self.remove_Relic("Ring of the Snake")

        elif relic.get("Name") == "Black Blood":
            self.remove_Relic("Burning Blood")

        elif relic.get("Name") == "Empty Cage":
            
            self.removeCardsFromDeck(amount = 2,removeType = "Remove")

        elif relic.get("Name") == "Necronomicon":
            
            self.add_CardToDeck({"Name":"Necronomicon","Rarity":"Event","Owner":"The Spire","Type":"Relic","Info":"The first <red>Attack</red> played each turn that costs 2 or more is played twice. When you take this <light-red>Relic</light-red>, become <m>Cursed</m>."})

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
            onePotion = helping_functions.generatePotionRewards(event=True,amount=1)
            self.add_potion(onePotion[0])
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
                    print("You have to type a number.")
                    

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
                        snap = input("Which Attack Card do you want to bottle?\n")
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
                        snap = input("Which Skill Card do you want to bottle?\n")
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
                        snap = input("Which Power do you want to bottle?\n")
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

        ansiprint(f"{self.displayName} receives <green>{self.metallicize} Block</green> at the start of each turn.")

    def set_block_by_metallicice (self,value):
        
        self.blocking(self.metallicize,unaffectedBlock=True)
        ansiprint(f"{self.displayName}  received <green>{self.metallicize} Block</green> through Metallicize.")

    def set_platedArmor(self,value):
        self.platedArmor += value

        ansiprint(f"{self.displayName} receives <green>{self.platedArmor} Block</green> at the start of each turn.")

    def set_block_by_platedArmor(self,value):

        self.blocking(self.platedArmor,unaffectedBlock=True)
        
        ansiprint(f"{self.displayName} received <green>{self.platedArmor} Block</green> through <light-blue>Plated Armor</light-blue>.")

    def damageCounter(self):
        self.damage_counter += 1
        
        for card in self.hand:
            
            if "Masterful Stab" in card["Name"]:

                card["Energy changed for the battle"] = True
                card["Energy"] = card["Energy"]+1
                
            elif "Blood for Blood" in card["Name"]:
                card["Energy changed for the battle"] = True
                card["Energy"] = card["Energy"]-1
                if card["Energy"] < 0:
                    card["Energy"] = 0
        
        for card in self.discard_pile:
        
            if "Masterful Stab" in card["Name"]:
                card["Energy changed for the battle"] = True
                card["Energy"] = card["Energy"]+1
            
            elif "Blood for Blood" in card["Name"]:
                card["Energy changed for the battle"] = True
                card["Energy"] = card["Energy"]-1
                if card["Energy"] < 0:
                    card["Energy"] = 0
        
        for card in self.draw_pile:
            
            if "Masterful Stab" in card["Name"]:
                card["Energy changed for the battle"] = True
                card["Energy"] = card["Energy"]+1
            
            elif "Blood for Blood" in card["Name"]:
                card["Energy changed for the battle"] = True
                card["Energy"] = card["Energy"]-1
                if card["Energy"] < 0:
                    card["Energy"] = 0

        for card in self.exhaust_pile:
            
            if "Masterful Stab" in card["Name"]:
                card["Energy changed for the battle"] = True
                card["Energy"] = card["Energy"]+1
            
            elif "Blood for Blood" in card["Name"]:
                card["Energy changed for the battle"] = True
                card["Energy"] = card["Energy"]-1
                if card["Energy"] < 0:
                    card["Energy"] = 0

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

    def set_gold(self,value,thievery = False):
        ectoplasm = False
        ansiprint("")
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

                
                ansiprint(self.displayName,"lost",stolenGold,"Gold and has now only <yellow>"+str(self.gold)+" Gold</yellow> left!")
                return stolenGold
            else:
                self.gold += value
                
                if self.gold < 0:
                    self.gold = 0
                if value >= 0:
                    ansiprint(f"{self.displayName} received <yellow>{value} Gold</yellow> and now has <yellow>{self.gold} Gold</yellow>.")
                if value > 0 and self.bloodyIdol > 0:
                    self.heal(5)
                    ansiprint("You <red>healed</red> because you own a <light-red>Bloody Idol</light-red>.")

                if value < 0:
                    ansiprint(f"{self.displayName} lost <yellow>{abs(value)} Gold</yellow> and now has <yellow>{self.gold} Gold</yellow>.")

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
                    print("Type a number.")
                    continue
            try:
                color = self.get_cardColor(self.deck[choice].get("Type"))

                if choice in range(len(self.deck)):
                    if removeType == "Transform":
                        if self.deck[choice].get("Irremovable") == True:
                            ansiprint("<m>"+self.deck[choice].get("Name")+"</m> can't be transformed.")
                            continue

                        ansiprint(f"<{color}>{self.deck[choice].get('Name')}</{color}> is transformed to...")
                        helping_functions.transformCard(self.deck.pop(choice),"Deck",index = choice)
                    

                    elif removeType == "Upgrade":
                        if self.deck[choice].get("Upgraded") == True:
                            ansiprint("You can only upgrade unupgraded cards. Try again!")
                            continue
                        elif self.deck[choice].get("Type") == "Curse":
                            ansiprint("<m>Curses</m> can't be upgraded.")
                            continue
                        else:
                            ansiprint(f"<{color}>{self.deck[choice].get('Name')}</{color}> is upgraded.")
                            
                            helping_functions.upgradeCard(self.deck.pop(choice),"Deck",index = choice)

                    elif removeType == "Remove":

                        if self.deck[choice].get("Irremovable") == True:
                            ansiprint("<m>"+self.deck[choice].get("Name")+"</m> can't be removed.")
                            continue

                        if self.deck[choice]["Name"] == "Parasite":
                            ansiprint("<m>The Parasite</m> reeks and wretches as you attempt to <light-blue>remove it from your body</light-blue>. At the end you manage... but at what <red>price</red>?")
                            self.set_maxHealth(-3)

                        if purpleFire:
                            ansiprint(f"<{color}>{self.deck[choice].get('Name')}</{color}> is removed from the deck.")
                            offerCard = self.deck.pop(choice)
                            return offerCard
                        
                        else:
                            ansiprint(f"<{color}>{self.deck[choice].get('Name')}</{color}> is removed from the deck.")
                            self.deck.pop(choice)

                    elif removeType == "Duplicate":
                        ansiprint(f"<{color}>{self.deck[choice].get('Name')}</{color}> is duplicated!")
                        self.add_CardToDeck(self.deck[choice])
                    
                    i+=1
                else:
                    print("Type the number of one of the cards in your deck shown.")
                    pass
            except Exception as e:

                print ("You have to type a number.\n",e)
                pass
    

    def check_if_upgradable_cards_in_hand(self):
        upgradePossible = False
        for card in self.hand:
            if card.get("Type") == "Status":
                pass
            elif card.get("Type") == "Curse":
                pass
            elif card.get("Upgrade") == None:
                upgradePossible = True

        return upgradePossible
    
    def removeCardsFromHand(self,amount:int =1,removeType: str = "Upgrade",index = None):
        
        i = 0
        while i < amount:
            if len(self.hand) == 0:
                ansiprint("You don't have any cards in your hand.")
                break
            if removeType == "Upgrade":
                if self.check_if_upgradable_cards_in_hand() == False:
                    ansiprint("You don't have anymore cards in your hand that can be upgraded.")
                    break
            if index or index == 0:
                choice = index
            
            else:
                if removeType == "Upgrade":
                    self.showHand(noUpgrades = True)
                else:
                    self.showHand()
                try:

                    if removeType == "Upgrade":
                        choice = input("Which card do you want to upgrade?\n")

                    elif removeType == "Duplicate":
                        choice = input("Which card do you want to duplicate?\n")

                    else:
                        print(removeType,"<-- What is this?\n")

                    choice = int(choice)-1
                except:
                    self.explainer_function(choice)
                    print("You have to type a number.")
                    continue
            try:
                color = self.get_cardColor(self.hand[choice].get("Type"))

                if choice in range(len(self.hand)):
                    
                    if removeType == "Upgrade":
                        if self.hand[choice].get("Upgraded") == True:
                            ansiprint("You can only upgrade unupgraded cards. Try again!")
                            continue
                        elif self.hand[choice].get("Type") == "Curse":
                            ansiprint("<m>Curses</m> can't be upgraded.")
                            continue
                        elif self.hand[choice].get("Type") == "Status":
                            ansiprint("<light-cyan>Status</light-cyan> can't be upgraded.")
                            continue
                        else:
                            ansiprint(f"<{color}>{self.hand[choice].get('Name')}</{color}> is upgraded.")
                            
                            helping_functions.upgradeCard(self.hand.pop(choice),"Hand",index = choice)

                    elif removeType == "Duplicate":
                        ansiprint(f"<{color}>{self.hand[choice].get('Name')}</{color}> is duplicated!")
                        duplicate = 0
                        while duplicate < amount:
                            self.add_CardToHand(self.hand[choice])
                            duplicate +=1
                        break
                    i+=1
                else:
                    print("Type the number of one of the cards in your hand shown.")
                    pass
            except Exception as e:

                print ("You have to type a number.\n",e)
                pass

    def check_CardPlayPenalties(self):

        for card in self.hand:
            if card["Name"] == "Pain":
                self.receive_recoil_damage(1,directDamage = True)
                ansiprint("<m>"+card["Name"]+"</m> did this.")

        if self.hex == True:
            if self.card_in_play.get("Type") != "Attack":
                self.add_CardToDrawpile({"Name": "Dazed","Ethereal": True, "Type": "Status", "Rarity": "Enemy", "Owner":"The Spire"})
    
    def check_CardPlayRestrictions(self):

        for card in self.hand:
            if card["Name"] == "Normality" and self.card_counter >= 3:
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
            ansiprint("Death, Taxes and...")
        elif searchName == "":
            pass
        else:
            try:
                if searchName in entities.cards:
                    info = {k:v for k,v in entities.cards.items() if v.get("Name") == searchName}
                    info = list(info.items())[0][1]
                    
                    color = self.get_cardColor(info.get("Type"))

                    ansiprint("\n<"+color+">"+info.get("Type")+"</"+color+"> | "+info.get("Name")+":",info.get("Info"),"| <yellow>Energy</yellow>:",str(info.get("Energy"))+"\n")

                elif searchName in entities.potions:
                    info = {k:v for k,v in entities.potions.items() if v.get("Name") == searchName}
                    info = list(info.items())[0][1]
                
                    ansiprint(f"\n<c>Potion</c> | <c>{info.get('Name')}</c>: {info.get('Info')}\n")

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
                        ansiprint("<light-blue>You can't save here. Saving during fights works best!</light-blue>")
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
            except ValueError:
                if len(searchName) > 0:
                    print("This is neither a Card, a <light-red>Relic</light-red> or a <c>Potion</c>.")
                else:
                    ansiprint("You have to type a number.")
            except Exception as e:
                print("This is neither a Card, a <light-red>Relic</light-red> or a <c>Potion</c>.",e)
                pass

    def playCardFromTopOfDeck(self,exhaust:bool= False):
        self.randomTarget = True
        if len(self.draw_pile) == 0:
            self.discardBackInDrawpile()
        if len(self.draw_pile) == 0:
            anisprint("Your Discardpile and your Drawpile are empty.")
        else:
            if type(self.draw_pile[0].get("Energy")) == int:
                self.draw_pile[0]["Energy changed until played"] = True
                self.draw_pile[0]["Energy"] = 0
                self.card_is_played(self.draw_pile.pop(0),helping_functions.turn_counter,exhaust=exhaust)
            elif type(self.draw_pile[0].get("Energy")) == str:
                energyStorage = self.energy
                self.card_is_played(self.draw_pile.pop(0),helping_functions.turn_counter,exhaust=exhaust)
                self.energy = energyStorage
            elif self.draw_pile[0].get("Energy") == None:
                if exhaust or self.draw_pile[0].get("Exhaust") == True:
                    self.add_CardToExhaustpile(self.draw_pile.pop(0))
                else:
                    self.add_CardToDiscardpile(self.draw_pile.pop(0))
        
        self.randomTarget = False
    
    def set_redSkull(self):
        if self.redSkullStrength == True and self.health > self.max_health // 2:
            self.set_strength(-3)
            self.redSkullStrength = False

        elif self.redSkullStrength == False and self.health < self.max_health // 2:
            self.set_strength(3)
            self.redSkullStrength = True

    def getOrbSituation(self):
        
        templist = copy.deepcopy(self.orbs)

        difference = self.maxOrbs - len(self.orbs)

        i = 0
        while i < len(templist):
            if type(templist[i]) == dict:
                templist[i] = f"{templist[i].get('Name')} ({self.getOrbPassive(templist[i])}/{self.getOrbEvokation(templist[i])})"
            i+=1

        while difference > 0:
            templist.append("Empty Orbslot")
            difference -= 1
        
        templist.reverse()    

        orbString = ' | '.join(templist)

        return orbString

    def show_status(self,event = False):
        status = "\n{} (<red>{}</red>/<red>{}</red>)".format(self.displayName,self.health,self.max_health)
        if event == False:
            if self.block > 0:
                status += f" |<green> Block: {self.block}</green>"

            status += f" |<yellow> Energy: {self.energy}</yellow>"
            
            if self.maxOrbs > 0:
                status += f" | {self.getOrbSituation()}"
            if self.weak > 0:
                status += f" |<light-cyan> Weakness: {self.weak}</light-cyan>"
            if self.vulnerable > 0:
                status += f" |<light-cyan> Vulnerable: {self.vulnerable}</light-cyan>"
            if self.frail > 0:
                status += f" |<light-cyan> Frail: {self.frail}</light-cyan>"
            if self.constriction > 0:
                status += f" |<light-cyan> Constricted: {self.constriction}</light-cyan>"
            if len(self.strengthDecrease) > 0:
                status += f" |<light-cyan> Strength Decrease:{self.strengthDecrease[0][1]}</light-cyan>" 
            if len(self.dexterityDecrease) > 0:
                status += f" |<light-cyan> Dexterity Decrease:{self.dexterityDecrease[0][1]}</light-cyan>" 
            if self.confused == True:
                status += f" |<light-cyan> Confused</light-cyan>"
            if self.cantDraw == True:
                status += f" |<light-cyan> No Draw</light-cyan>"
            if self.hex == True:
                status += f" |<light-cyan> Hex</light-cyan>"
            if self.wraithForm > 0:
                status += f" |<light-cyan> Wraith Form: {self.wraithForm}</light-cyan>"
            if len(self.reducedDrawByTurns) > 1:
                status += f" |<light-cyan> Draw Reduction </light-cyan>"
            if self.entangled == True:
                status += f" |<light-cyan> Entangle </light-cyan>"
            if self.strength != 0:
                status += f" |<red> Strength: {self.strength}</red>"
            if self.dexterity != 0:
                status += f" |<green> Dexterity: {self.dexterity}</green>"
            if self.ritual > 0:
                status += f" |<red> Ritual: {self.ritual}</red>"
            if self.regen > 0:
                status += f" |<red> Regen: {self.regen}</red>"
            if self.invulnerable > 0:
                status += f" |<light-blue> Invulnerable: {self.invulnerable}</light-blue>"
            if self.intangible > 0:
                status += f" |<light-blue> Invincible: {self.intangible}</light-blue>"
            if self.artifact > 0:
                status += f" |<light-blue> Artifact: {self.artifact}</light-blue>"
            if self.spikes > 0:
                status += f" |<light-blue> Spikes: {self.spikes}</light-blue>"
            if self.barricade == True:
                status += f" |<light-blue> Barricade</light-blue>"
            if self.corruption == True:
                status += f" |<light-blue> Corruption</light-blue>"
            if self.metallicize > 0:
                status += f" |<light-blue> Metallicize: {self.metallicize}</light-blue>"
            if self.juggernaut > 0:
                status += f" |<light-blue> Juggernaut: {self.juggernaut}</light-blue>"
            if self.feelNoPain > 0:
                status += f" |<light-blue> Feel No Pain: {self.feelNoPain}</light-blue>"
            if self.darkEmbrace > 0:
                status += f" |<light-blue> Dark Embrace: {self.darkEmbrace}</light-blue>"
            if self.rage > 0:
                status += f" |<light-blue> Rage: {self.rage}</light-blue>"
            if self.dontLoseBlock > 0:
                status += f" |<light-blue> Blur: {self.dontLoseBlock}</light-blue>"
            if self.evolve > 0:
                status += f" |<light-blue> Evolve: {self.evolve}</light-blue>"
            if self.fireBreathing > 0:
                status += f" |<light-blue> Fire Breathing: {self.fireBreathing}</light-blue>"
            if self.demonForm > 0:
                status += f" |<light-blue> Demon Form: {self.demonForm}</light-blue>"
            if self.rupture > 0:
                status += f" |<light-blue> Rupture: {self.rupture}</light-blue>"
            if self.combustDamage > 0:
                status += f" |<light-blue> Combust:{self.combustDamage} </light-blue>, <red>Damage: {self.combustSelfharm}</red>" 
            if len(self.doubleDamage) > 0:
                status += " | <red>Attacks</red> deal <red>Double Damage</red><."
            if self.brutality > 0:
                status += f" |<light-blue> Brutality:{self.brutality} </light-blue>" 
            if self.heatsinks > 0:
                status += f" | Heatsinks: {self.heatsinks}"
            if self.hello_world > 0:
                status += f" | Hello World: {self.hello_world}"
            if self.loop > 0:
                status += f" | Loop: {self.loop}"
            if self.selfRepair > 0:
                status += f" | Self Repair: {self.selfRepair}"
            if self.staticDischarge > 0:
                status += f" | Static Discharge: {self.staticDischarge}"
            if self.storm > 0:
                status += f" | Storm: {self.storm}"
            if self.biasedCognition > 0:
                status += f" | Biased Cognition: {self.biasedCognition}"
            if self.creativeAI > 0:
                status += f" | Creative AI: {self.creativeAI}"
            if self.echoForm > 0:
                status += f" | Echo Form: {self.echoForm}"
        else:
            
            relics = ""
            i = 0 
            for relic in self.relics:
                if i == 0:
                    relics += f"<light-red>{relic.get('Name')}</light-red>"
                else:
                    relics += f", <light-red>{relic.get('Name')}</light-red>"
                i+=1
            
            status += f" |<yellow> Gold</yellow>: <yellow>{self.gold}</yellow> | <light-red>Relics</light-red>: {relics}"
            

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

        self.cantDraw = False
        self.cardsCostNothing = 0
        self.tempSpikes = 0

        self.intangible = 0

        self.discard_counter = 0
        self.temp_energy = 0
        self.tempDraw = 0
        
        self.burst = 0
        self.doubleTap = 0

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
        
        self.weak = 0
        self.frail = 0
        self.vulnerable = 0
        self.entangled = False
        self.block = 0
        self.artifact = 0
        
        self.magnetism = 0

        self.runicDome = 0
        self.velvetChoker = 0
        self.runicPyramid = 0
        self.confused = False
        
        self.artOfWar = 0
        
        self.akabeko = 0

        self.energy_gain = 3
        self.draw_strength = 5
        self.sneckoSkull = 0

        self.mercuryHourglass = 0
        self.mummifiedHand = 0
        self.paperPhrog = False
        self.selfFormingClay = False
        self.charonsAshes = False
        self.magicFlower = False
        self.championBelt = False
        self.brimStone = False
        self.orangePellets = False

        self.runicCube = False
        self.redSkull = False
        self.redSkullStrength = False
        
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
        self.frozenEye = False
        self.hoveringKite = 0
        self.bloodyIdol = 0
        self.oddMushroom = 0
        self.theAbacus = 0
        self.pocketWatch = 0
        self.stoneCalender = 0
        self.handDrill = 0
        self.necronomicon = 0
        self.randomTarget = False
        self.warpedTongs = 0
        self.nilrysCodex = 0
        self.centennialPuzzle = 0
        self.tungstenRod = 0
        self.wristBlade = 0
        self.strengthDecrease = []
        self.hex = False
        self.constriction = 0
        self.cardIndex = None
        
        self.rage = 0
        self.combustDamage = 0
        self.combustSelfharm = 0
        self.darkEmbrace = 0
        self.evolve = 0
        self.feelNoPain = 0
        self.fireBreathing = 0
        self.barricade = False
        self.brutality = 0
        self.corruption = False
        self.juggernaut = 0
        self.rupture = 0
        self.metallicize = 0
        self.demonForm = 0

        self.hand = []
        self.discard_pile = []
        self.exhaust_pile = []
        self.draw_pile = []
        self.exhaustQueue = []

        if self.name == "Defect":
            self.maxOrbs = 3
        else:
            self.maxOrbs = 0
        self.orbs = []
        self.focus = 0
        self.claw = 0
        self.rebound = 0
        self.preRebound = 0
        self.frostCounter = 0
        self.equilibrium = 0
        self.heatsinks = 0
        self.hello_world = 0
        self.loop = 0
        self.selfRepair = 0
        self.staticDischarge = 0
        self.storm = 0
        self.biasedCognition = 0
        self.creativeAI = 0
        self.echoForm = 0
        self.electrodynamics = False
        self.goldPlatedCables = False
        self.emotionChipTriggered = False
        self.emotionChip = False
        self.frozenCore = False
        self.lightningCounter = 0
        self.frostCounter = 0
        self.frozenCore = False
