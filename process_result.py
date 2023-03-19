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


def createDirectory(fileStr):
	extensionIndex = fileStr.find(".")
	if(extensionIndex == -1):
		error("No file extension on result file, cannot create directory")
	else:
		fileName = fileStr[:fileStr.find(".")]

	try:
		os.makedirs(f"results/{fileName}")	
	except FileExistsError:
		if(not override):
			error("Result already processed or partially processed")
		else:
			debugPrint("Overriding existing results")
			shutil.rmtree(f"results/{fileName}")
			os.makedirs(f"results/{fileName}")	


def main():
	args = getopts()

	if(len(args) != 1):
		error("Invalid arguments provided.\nPlease provide only the target result file\n")
	targetResultFile = args[0]
	data = importData(targetResultFile)
	createDirectory(targetResultFile)
	return 0


if __name__ == "__main__":
	main()