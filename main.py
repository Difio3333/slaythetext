#import random as rd
import entities
import helping_functions
import colorama
import sys
import time
import save_handlery
from pathlib import Path
from ansimarkup import parse, ansiprint


colorama.init()

#KNOWN ISSUES:

#events are not following any rules.
#no tutorial
#no proper error logging yet.
#Skipping Black Star second artifact makes it inaccessible.
#you can also skip green key forever I think 
#just saw 4 shops in a row.
#5169 exhaustpile Stuff needs to be handled properly so when you exhaust your entire hand and something comes back it doesn't loop indefinitely  -> fixed
#need to make exhaust pile and discard pile watchable -> done
#Boss Slime splits wildly -> probably fixed
#shops need to update when buying membership card

def main():
	try:
		ansiprint("Slay the Spire is a registered trademark by Mega Crit, LLC")
		ansiprint("Please consider supporting the Developers by purchasing Slay the Spire on Steam/Gog/Epic etc.\n\n")
		ansiprint("This game requires a base understanding of Slay the Spire.")
		ansiprint("If you don't know what a <blue>Card</blue>, <light-red>Relic</light-red> or <c>Potion</c> does just type out its name wherever you are and you should get a short explanation of it.")
		ansiprint("In 99 out of 100 cases you can navigate the game by typing in the corresponding numbers of the options presented to you.")
		ansiprint("You can Save only during battles by typing \"Save\" and hitting \"Enter\" afterwards.\n\n")

		save_handlery.the_question_of_safety()

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
		
		crash=["Error on line {}".format(sys.exc_info()[-1].tb_lineno),"\n",e]
		timeX=str(time.time())
		devPath = str(Path.cwd())+"/documents/slaythetext/CRASH-"+timeX+".txt"
		prodPath = str(Path.cwd())+"/slaythetext_CRASH-"+timeX+".txt" 
		with open(prodPath,"w") as crashLog:
			for i in crash:
				i=str(i)
				crashLog.write(i)
		input("Sorry the game crashed. You can find the crashlog in the same location where your game is located.\nIt would be really nice if you could copy paste your game text to a txt. file and send it to slaythetext@gmail.com. Thanks and sorry for the inconveniences.")

if __name__ == "__main__":
	main()
