import random as rd
import entities
from ansimarkup import parse, ansiprint

# 0 = normal_fight
# 1 = elite_fight
# 2 = question_mark
# 3 = merchant
# 4 = bon_fire
# 5 = treasure_room 
# 6 = boss_fight
# 7 = start

def move_after_combat(game_map,game_map_dict):
	spots = []
	i = 0
	
	mawBank = False
	for relic in entities.active_character[0].relics:
		if relic.get("Name") == "Maw Bank":
			mawBank = True
			mawBankIndex = entities.active_character[0].relics.index(relic)

	
	for connection in game_map_dict[entities.active_character[0].get_floorAndCoordinates()]["Connections"]:
		spot = [str(i+1)+". " + connection[0]]
		print(spot[0])
		#"\n{}.) {}".format(i+1,active_character[0].position[1]+1)
		i = i + 1

	while True:
		try:
			
			target = input("\nPick the place you want to go\n")
			target = int(target)-1

			if target in range(len(game_map_dict[entities.active_character[0].get_floorAndCoordinates()]["Connections"])):
				if mawBank:
					if entities.active_character[0].relics[mawBankIndex]["Working"] == True:
						entities.active_character[0].set_gold(12)

				break
			else:
				print("You can't go there.")
				continue
		except Exception as e:
			#print (e,"an error has happened in move_after_combat")
			entities.active_character[0].explainer_function(target)
			pass

	y = game_map_dict[entities.active_character[0].get_floorAndCoordinates()]["Connections"][target][1]
	x = game_map_dict[entities.active_character[0].get_floorAndCoordinates()]["Connections"][target][2]
	entities.active_character[0].set_position([y,x])

	#environment_update(maps[target])


def nchoices_with_restrictions(weights=None, restrictions={},k = 100):

    N = 0 # count how many values we have yielded so far
    last_value = None # last value that was yielded
    repeat_count = 0 # how often it has been yielded in a row
    while N < k:
        while True:
            x = rd.choices(range(len(weights)), weights)[0]
            if x == last_value and repeat_count == restrictions.get(x, 0):
                continue
            break
        yield x
        N += 1
        if x == last_value:
            repeat_count += 1
        else:
            repeat_count = 1
            last_value = x


def generate_map(superElite = True):
	
	paths = []
	i = 0
	while i < 5:
		lengthOfPath = 12
		snap = list(nchoices_with_restrictions([0.450,0.155,0.225,0.05,0.12],{0:3,1:1,2:1,3:1,4:1},k=lengthOfPath))
		# snap = list(nchoices_with_restrictions([0.462,0.143,0.225,0.05,0.12],{0:3,1:1,2:1,3:1,4:1},k=lengthOfPath))
		#snap = list(nchoices_with_restrictions([0.480,0.128,0.24,0.05,0.12],{0:2,1:1,2:1,3:1,4:1},k=lengthOfPath))
		#snap = list(nchoices_with_restrictions([0.33,0.13,0.27,0.10,0.17],{0:3,1:1,2:1,3:1,4:1},k=13))
		snap[7] = 5
		snap[0] = 0
		if snap[lengthOfPath-1] == 4:
			randy = rd.randint(0,3)
			
			if randy == 0:
				snap[lengthOfPath-1] = 0
			
			elif randy == 1:
				snap[lengthOfPath-1] = 1
			
			elif randy == 2:
				snap[lengthOfPath-1] = 2
			
			elif randy == 3:
				snap[lengthOfPath-1] = 3

		k = 0
		while k < len(snap):
			if k < 5:
				if snap[k] == 4 or snap[k] == 1:
					
					randy = rd.randint(0,2)
			
					if randy == 0:
						snap[k] = 0
						
					elif randy == 1:
						snap[k] = 2
					
					elif randy == 2:
						snap[k] = 3
					
			if snap[k] == 0:
				snap[k] = "Creep"
			elif snap[k] == 1:
				snap[k] = "Elite"
			elif snap[k] == 2:
				snap[k] = "Event"
			elif snap[k] == 3:
				snap[k] = "Shop$"
			elif snap[k] == 4:
				snap[k] = "Fires"
			elif snap[k] == 5:
				snap[k] = "Chest"

			k += 1	
		
		paths.append(snap)
		i += 1
	

	final_map = []
	
	while len(paths[0]) > 0:
		sub_map =[]
		i = 0
		while i < len(paths): 
			sub_map.append(paths[i].pop(0))
			i += 1
		
		final_map.append(sub_map)

	

	final_map.insert(0,["Start"])
	final_map.insert(len(final_map),["Fires", "Fires", "Fires", "Fires"])
	final_map.insert(len(final_map),["Boss"])

	y = 0
	for row in final_map:
		
		if y > 0:
			if len(row) > 1:
				snap = rd.randint(0,2)
				if snap == 0:
					pass
				elif snap == 1:
					row.pop(len(row)-1)
				elif snap == 2:
					row.pop(len(row)-1)
					row.pop(len(row)-1)
				elif snap == 3:
					row.pop(len(row)-1)
					row.pop(len(row)-1)
					row.pop(len(row)-1)
		
		y += 1
	
	if superElite == True:
	
		while True:
			superElite = rd.randint(0,len(final_map)-1)
			if "Elite" in final_map[superElite]:
				change = final_map[superElite].index("Elite")
				final_map[superElite][change] = "Super"
				break
			else:
				continue

	
	return final_map
	
def generate_connections(map_of_the_game):
	connection_dict = {}
	
	y = 0	
	for row in map_of_the_game:
	
		x = 0
		sub_dict = {}
	
		for tile in row:
	
			connections = []
	
			if y < len(map_of_the_game) - 1:
				xOne = 0
				for gyle in map_of_the_game[y+1]:
					connections.append((gyle,y+1,xOne))
					xOne += 1
			
			sub_dict[tile,y,x] = {"Type": tile,"y": y, "x":x, "Connections": connections}
			x += 1
		
		connection_dict.update(sub_dict)
		y += 1

	
	for k,v in connection_dict.items():
		i = 0
		while i < len(v["Connections"]):
			if v["Type"] != "Start":
				if abs(v["x"] - v["Connections"][i][2]) > 1:
					
					v["Connections"].pop(i)

				else:
					i += 1
			else:
				i+=1
	
	for k,v in connection_dict.items():
		i = 0
		while i < len(v["Connections"]):
			
			if v["Type"] != "Start":	
				snap = rd.randint(0,2)

				if snap == 0:
					pass
					
				elif snap == 1:
					if len(v["Connections"]) > 1:
						v["Connections"].pop(rd.randint(0,len(v["Connections"])-1))
					
				elif snap == 2:
					if len(v["Connections"]) > 2:

						v["Connections"].pop(rd.randint(0,len(v["Connections"])-1))
						v["Connections"].pop(rd.randint(0,len(v["Connections"])-1))
						
					elif len(v["Connections"]) > 1:
						v["Connections"].pop(rd.randint(0,len(v["Connections"])-1))

					else:
						pass
				i += 1
			else:
				i += 1
	

	for k,v in connection_dict.items():
		
		if len(v["Connections"]) == 0 and v["Type"] != "Boss":
				
			v["Connections"].append((map_of_the_game[v["y"]+1] [len(map_of_the_game[v["y"]+1])-1] , v["y"]+1, len(map_of_the_game[v["y"]+1])-1))

	for k,v in connection_dict.items():
		if v["Type"] != "Boss" and v["Type"] != "Start" :
			dict_reference_same_X = (map_of_the_game[v["y"]+1][0],v["y"]+1,v["x"]) 
			dict_reference_same_Y = (map_of_the_game[v["y"]][1],v["y"],v["x"]+1) 
			
			if v["x"] == 0:
				if v["Connections"][0][2] != 0 and connection_dict[dict_reference_same_Y]["Connections"][0][2] != 0:
					v["Connections"].insert(0,dict_reference_same_X)
			
			if v["x"] == len(map_of_the_game[v["y"]]) - 1:
				if len(map_of_the_game[v["y"]]) == len(map_of_the_game[v["y"]+1]):
					check = False
					for connection in v["Connections"]:
						if connection[2] == v["x"]:
							check = True

					if check == False:
						if len(v["Connections"]) == 1:
							v["Connections"].insert(1,dict_reference_same_X)
						elif len(v["Connections"]) == 0:
							v["Connections"].insert(0,dict_reference_same_X)



	rooms_without_connections = []
	
	for k,v in connection_dict.items():
		if v["Type"] != "Boss" and v["Type"] != "Start":
			x = 0
			test_list = []
			while x < len(map_of_the_game[v["y"]-1]):
				
				for connection in connection_dict[(map_of_the_game[v["y"]-1][x],v["y"]-1,x)]["Connections"]:
					test_list.append(connection)
				x += 1
				

			if (v["Type"],v["y"],v["x"]) not in test_list:

				rooms_without_connections.append((v["Type"],v["y"],v["x"]))


	
	for k,v in connection_dict.items():
		y = 0
		while y < len(rooms_without_connections):
			
			if k == rooms_without_connections[y]:
				
				while True:
					try:
						
						room_above = (map_of_the_game[k[1]-1][k[2]],k[1]-1,k[2])	
						break
					
					except Exception as e:
							
							room_on_outside_right_x = len(map_of_the_game[k[1]-1]) - 1
							room_above = (map_of_the_game[k[1]-1][room_on_outside_right_x],k[1]-1,room_on_outside_right_x)
							break



				connection_dict[room_above]["Connections"].append(rooms_without_connections.pop(y))
			else:
				y+=1
	

	for k,v in connection_dict.items():
		
		if len(v["Connections"]) > 2:	
			if v["Connections"][len(v["Connections"])-1][2] == v["Connections"][len(v["Connections"])-2][2]:
					v["Connections"].pop(len(v["Connections"])-2)

	for k,v in connection_dict.items():
		v["Connections"].sort(key=takeThird)

	return connection_dict

def generate_act4Map():
	finalAct4Map = [["Start"],["Shop$"],["Fires"],["Elite"],["Boss"]]
	return finalAct4Map

def generate_act4ConnectionDict(map_of_the_game):
	connection_dict = {}
	
	y = 0	
	for row in map_of_the_game:
	
		x = 0
		sub_dict = {}
	
		for tile in row:
	
			connections = []
	
			if y < len(map_of_the_game) - 1:
				xOne = 0
				for gyle in map_of_the_game[y+1]:
					connections.append((gyle,y+1,xOne))
					xOne += 1
			
			sub_dict[tile,y,x] = {"Type": tile,"y": y, "x":x, "Connections": connections}
			x += 1
		
		connection_dict.update(sub_dict)
		y += 1

	
	return connection_dict


def show_map(map_of_the_game,connection_dict):
	z = 0
	snaperline = ""
	
	yy = 0
	for row in map_of_the_game:
		xx = 0
		tiling = ""
		for tile in row:
			
			if yy == entities.active_character[0].position[0] and xx == entities.active_character[0].position[1]:
				tiling += "<BLUE>"+tile+"</BLUE>    "

			elif yy == entities.active_character[0].position[0] + 1:

				testDing = (map_of_the_game[yy][xx],yy,xx)	

				for connection in connection_dict[entities.active_character[0].get_floorAndCoordinates()]["Connections"]:
					if yy == connection[1] and xx == connection[2]:
						connection[0] == map_of_the_game[yy][xx]

				if testDing in connection_dict[entities.active_character[0].get_floorAndCoordinates()]["Connections"]:
					
					if testDing[0] == "Creep":
						tiling += "<red>"+tile+"</red>    "
					elif testDing[0] == "Shop$":
						tiling += "<yellow>"+tile+"</yellow>    "
					elif testDing[0] == "Event":
						tiling += "<blue>"+tile+"</blue>    "
					elif testDing[0] == "Elite":
						tiling += "<m>"+tile+"</m>    "
					elif testDing[0] == "Fires":
						tiling += "<green>"+tile+"</green>    "
					elif testDing[0] == "Boss":
						tiling += "<black>"+tile+"</black>    "
					elif testDing[0] == "Chest":
						tiling += "<light-red>"+tile+"</light-red>    "
					elif testDing[0] == "Super":
						tiling += "<m>"+tile+"</m>    "
				else:
					tiling += tile + "    "
			else:
				tiling += tile + "    "
				
			xx +=1
		ansiprint("  "+tiling)
		yy+=1

		y = 0
		all_lines = ""
		for tile in row:
			x = 0
			connector_line = ""
			for connection in connection_dict[tile,z,y]["Connections"]:
								
				if connection[0] == "Outsider":
					connector_line += "/"

				elif connection[2] < connection_dict[tile,z,y]["x"]:
					connector_line += "/"
					
				elif connection[2] == connection_dict[tile,z,y]["x"]:
					connector_line += "|"

				elif connection[2] > connection_dict[tile,z,y]["x"]:
					connector_line += "\\"
						
				x += 1
						
				all_lines += connector_line
				connector_line = ""
			y+=1

			back_spaces = ""	
			if len(all_lines) == 1:
				back_spaces = "        "
			elif len(all_lines) == 2:
				back_spaces = "       "
			elif len(all_lines) == 3:
				back_spaces = "      "

			front_spaces = ""	
			if len(all_lines) == 1:
				front_spaces = "    "
			elif len(all_lines) == 2:
				front_spaces = "  "
			elif len(all_lines) == 3:
				front_spaces = " "
			front_spaces = ""


			snaperline += front_spaces + all_lines + back_spaces
			
			all_lines = ""
		
		ansiprint("    " + snaperline)
		snaperline = ""
		z += 1

	


def takeThird(elem):
	return elem[2]




