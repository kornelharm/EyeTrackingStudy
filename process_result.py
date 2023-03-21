import json
import sys
import os
import getopt
import shutil


# ---- Options ----
debug = False    #d - Print debug messages
silent = False   #s - fail silently, no progress updates or debug messages
override = False #o - If result has been processed before, override 


def debugPrint(text):
	if(not silent and debug):
		print(f"DEBUG: {text}")
 

def error(text):
	if(not silent):
		print(f"ERROR: {text}", file=sys.stderr)
	exit(1)


def getopts():
	argList = sys.argv[1:]
	options = "dos"
	longOptions = ["debug", "override", "silent"]
	try:
		global silent
		global override
		global debug
		options, args  = getopt.getopt(argList, options, longOptions)
		for opt, val in options:
			if opt in ("-s", "--silent"):
				silent = True
			if opt in ("-o", "--override"):
				override = True
			if opt in ("-d", "--debug"):
				debug = True
				debugPrint("Enabled")
	except getopt.error as err:
		error(str(err))

	return args


def importData(fileStr):
	try:
		with open(f"results/{fileStr}", "r") as file:
			dataDict = json.load(file)
	except FileNotFoundError:
		error(f"Specified result file not found: results/{fileStr}\n")
	
	return dataDict


def createResultDirectory(id):
	try:
		os.makedirs(f"results/{id}")	
	except FileExistsError:
		if(not override):
			error("Result already processed or partially processed")
		else:
			debugPrint("Overriding existing results")
			shutil.rmtree(f"results/{id}")
			os.makedirs(f"results/{id}")
			os.makedirs(f"results/{id}/anims")
			os.makedirs(f"results/{id}/plots")	


def processData(data):
	resultID = data.get("id") 
	with open(f"results/{resultID}/participant_info.txt", "w") as participant:
		participant.write(f"{data.get('major')}")
	data.pop("id")
	data.pop("major")
	for key in data:
		reading = data.get(key)
		with open(f"results/{resultID}/{key}_webgazer.csv", "w") as csv:
			csv.write("x,y,t\n")
			points = reading.get("webgazer")
			for point in points:
				x = point.get('x')
				y = point.get('y')
				t = point.get('t')
				csv.write(f"{x},{y},{t}\n")



def main():
	args = getopts()

	if(len(args) != 1):
		error("Invalid arguments provided.\nPlease provide only the target result file\n")
	targetResultFile = args[0]
	data = importData(targetResultFile)
	resultID = data.get("id")
	createResultDirectory(resultID)
	processData(data)

	exit(0)


if __name__ == "__main__":
	main()