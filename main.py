#import random as rd
import entities
import helping_functions
import colorama
import sys
import time
import save_handlery
from pathlib import Path

colorama.init()

#KNOWN ISSUES:
#bottle relics should only be offered if you have a corresponding card to bottle.
#guardian modeshift seems broken. maybe fixed.
#events are not following any rules yet.
#most enemies follow the same pattern
#no tutorial

print("Slay the Spire is a registered trademark by Mega Crit, LLC")
print("Please support the Developers by purchasing Slay the Spire on Steam/Gog/Epic etc.\n\n")
try:
	save_handlery.the_question_of_safety()
	
	running = True
	while running and helping_functions.gameAct < 5:
		if save_handlery.snap == "Yes":
			save_handlery.snap = "No"
			
		else:
			entities.active_character[0].resetChar()
			entities.active_character[0].set_drawPile()
			entities.update_encounter()
			
		while len(entities.list_of_enemies) > 0:

			helping_functions.turn_counter = helping_functions.count_up(helping_functions.turn_counter)
			entities.active_character[0].turn(helping_functions.turn_counter)
			
			for enemy in entities.list_of_enemies:
				enemy.turn(helping_functions.turn_counter)

			if entities.active_character[0].alive == False:
				running = False

			entities.check_if_enemy_dead()
		helping_functions.afterBattleScreen()

	if helping_functions.gameAct == 5:
		print("You won and beat the heart!!")
	elif helping_functions.gameAct == 4:
		print("You won!")
	else:
		print("You have lost!")

	input("Thanks so much for playing!")

except Exception as e:
	crash=["Error on line {}".format(sys.exc_info()[-1].tb_lineno),"\n",e]
	print(crash)
	timeX=str(time.time())
	devPath = str(Path.cwd())+"/documents/slaythetext/CRASH-"+timeX+".txt"
	prodPath = str(Path.cwd())+"/slaythetext_CRASH-"+timeX+".txt" 
	with open(prodPath,"w") as crashLog:
		for i in crash:
			i=str(i)
			crashLog.write(i)
	input("Sorry the game crashed. You can find the crashlog in the same location where your game is located.")