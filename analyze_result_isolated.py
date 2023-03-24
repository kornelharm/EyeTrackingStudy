import sys
import getopt
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import pylab
import graphing
import math

# ---- Options ----
noAnims = False		# -a  --noanims		Do not save animations
debug = False		# -d, --debug		Print debug messages
noHeats = False		# -h  --noheats		Do not save heatmaps
override = False	# -o, --override	If result has been processed before, override 
noPlots = False		# -p  --noplots		Do not save plots
silent = False		# -s, --silent		fail silently, no progress updates or debug messages


def debugPrint(text):
	if(not silent and debug):
		print(f"DEBUG: {text}")
 

def error(text):
	if(not silent):
		print(f"ERROR: {text}", file=sys.stderr)
	exit(1)


def getopts():
	argList = sys.argv[1:]
	options = "adhops"
	longOptions = ["noanims", "debug", "noheats", "override", "noplots", "silent"]
	try:
		global noAnims
		global debug
		global noHeats
		global override
		global noPlots
		global silent
		options, args  = getopt.getopt(argList, options, longOptions)
		for opt, val in options:
			if opt in ("-a", "--noanims"):
				noAnims = True
			if opt in ("-d", "--debug"):
				debug = True
				debugPrint("Enabled")
			if opt in ("-h", "--noheats"):
				noHeats = True
			if opt in ("-o", "--override"):
				override = True
			if opt in ("-p", "--noplots"):
				noPlots = True
			if opt in ("-s", "--silent"):
				silent = True
	except getopt.error as err:
		error(str(err))

	return args

def getCSVFiles(directory):
	files = os.listdir(directory)
	return [csvFile for csvFile in files if csvFile.endswith('.csv')]

def distance(x1, y1, x2, y2):
	return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def isolateRegions(x, y, t):
	saccadeSize = 100 #pixels
	fixationLength = 250 #ms
	newX = []
	newY = []
	newT = []
	windowStart = 0
	xSum = 0
	ySum = 0
	for windowEnd in range(len(x)):
		xSum += x[windowEnd]
		ySum += y[windowEnd]
		currX = xSum / (windowEnd-windowStart + 1)
		currY = ySum / (windowEnd-windowStart + 1)
		if((distance(currX, currY, x[windowEnd], y[windowEnd]) > saccadeSize) or  (t[windowEnd] - t[windowStart]) > fixationLength):
			newX.append(currX)
			newY.append(currY)
			newT.append(t[windowStart])
			xSum = 0
			ySum = 0
			windowStart = windowEnd + 1
	return newX, newY, newT

def importPoints(fileStr):
	try:
		x = []
		y = []
		t = []

		with open(fileStr) as csvFile:
			reader = csv.reader(csvFile)
			first = True
			for row in reader:
				if(first):
					first = False
					continue
				x.append(float(row[0]))
				y.append(float(row[1]))
				t.append(float(row[2]))

	except FileNotFoundError:
		error(f"Specified result file not found: results/{fileStr}")
	
	return isolateRegions(x, y, t)

def analyzeCSV(x, y, t, directory, filename):
	yFlipped = [1080 - a for a in y]
	# colors = [(x/_t[-1], 0.5, 1) for x in _t]
	colors1 = np.linspace(0, 1, len(x))
	colors2 = pylab.cm.rainbow(np.linspace(0, 1, len(x)))


	exportPlotName = f"{directory}/plots/{filename.rsplit('_')[0]}_isolated"
	exportAnimName = f"{directory}/anims/{filename.rsplit('_')[0]}_isolated"
	exportHeatName = f"{directory}/heatmaps/{filename.rsplit('_')[0]}_isolated"

	# x vs t
	if(not noPlots):
		graphing.save_graph(f"{exportPlotName}_x_vs_t_points.svg", [], [], colors1, "rainbow", [t], [x], [t[-1], 1920], "Horizontal Position vs Time", "Time (ms)", "Horizontal Position (px)")
		graphing.save_graph(f"{exportPlotName}_x_vs_t_line.svg", [t], [x], colors1, "rainbow", [], [], [t[-1], 1920], "Horizontal Position vs Time", "Time (ms)", "Horizontal Position (px)")
	if(not noAnims):
		debugPrint(f"Saving {exportAnimName}_x_vs_t_points.gif...")
		graphing.save_animation(f"{exportAnimName}_x_vs_t_points.gif", [], [], colors1, "rainbow", [t], [x], [t[-1], 1920], len(x), 50, False, "Horizontal Position vs Time", "Time (ms)", "Horizontal Position (px)")
		debugPrint(f"Saving {exportAnimName}_x_vs_t_line.gif...")
		graphing.save_animation(f"{exportAnimName}_x_vs_t_line.gif", [t], [x], colors1, "rainbow", [], [], [t[-1], 1920], len(x), 50, False, "Horizontal Position vs Time", "Time (ms)", "Horizontal Position (px)")

	# # y vs t
	if(not noPlots):
		graphing.save_graph(f"{exportPlotName}_y_vs_t_points.svg", [], [], colors1, "rainbow", [t], [yFlipped], [t[-1], 1080], "Vertical Position vs Time", "Time (ms)", "Vertical Position (px)")
		graphing.save_graph(f"{exportPlotName}_y_vs_t_line.svg", [t], [yFlipped], colors1, "rainbow", [], [], [t[-1], 1080], "Vertical Position vs Time", "Time (ms)", "Vertical Position (px)")
	if(not noAnims):
		debugPrint(f"Saving {exportAnimName}_y_vs_t_points.gif...")
		graphing.save_animation(f"{exportAnimName}_y_vs_t_points.gif", [], [], colors1, "rainbow", [t], [yFlipped], [t[-1], 1080], len(x), 50, False, "Vertical Position vs Time", "Time (ms)", "Vertical Position (px)")
		debugPrint(f"Saving {exportAnimName}_y_vs_t_line.gif...")
		graphing.save_animation(f"{exportAnimName}_y_vs_t_line.gif", [t], [yFlipped], colors1, "rainbow", [], [], [t[-1], 1080], len(x), 50, False, "Vertical Position vs Time", "Time (ms)", "Vertical Position (px)")

	# # y vs x
	if(not noPlots):
		graphing.save_graph(f"{exportPlotName}_y_vs_x_points.svg", [], [], colors1, "rainbow", [x], [yFlipped], [1920, 1080], "Vertical vs Horizontal Position", "Horizontal Position (px)", "Vertical Position (px)")
		graphing.save_graph(f"{exportPlotName}_y_vs_x_line.svg", [x], [yFlipped], colors1, "rainbow", [], [], [1920, 1080], "Vertical vs Horizontal Position", "Horizontal Position (px)", "Vertical Position (px)")
	if(not noAnims):
		debugPrint(f"Saving {exportAnimName}_y_vs_x_points.gif...")
		graphing.save_animation(f"{exportAnimName}_y_vs_x_points.gif", [], [], colors1, "rainbow", [x], [yFlipped], [1920, 1080], len(x), 50, False, "Vertical vs Horizontal Position", "Horizontal Position (px)", "Vertical Position (px)")
		debugPrint(f"Saving {exportAnimName}_y_vs_x_line.gif...")
		graphing.save_animation(f"{exportAnimName}_y_vs_x_line.gif", [x], [yFlipped], colors1, "rainbow", [], [], [1920, 1080], len(x), 50, False, "Vertical vs Horizontal Position", "Horizontal Position (px)", "Vertical Position (px)")

	
	# Generate heatmap for y vs x
	if(not noHeats):
		heatmap = np.zeros((1080//10, 1920//10))
		for i in range(len(x)):
			yIndex = int(yFlipped[i]//10)
			xIndex = int(x[i]//10)
			heatmap[yIndex][xIndex] += 1
		fig, ax = plt.subplots()
		ax.set_title("Gaze Frequency")
		ax.set_xlabel("Horizontal Postion ($10^1$ px)")
		ax.set_ylabel("Vertical Postion ($10^1$ px)")
		im = ax.imshow(heatmap, cmap="inferno", origin="lower")
		fig.tight_layout()
		plt.savefig(f"{exportHeatName}_heat.svg")
		plt.close(fig)


def main():
	args = getopts()
	if(len(args) != 1):
		error("Invalid arguments provided.\nPlease provide target directory to run in")
	targetDirectory = args[0]
	files = getCSVFiles(targetDirectory)
	for csvFile in files:
		x, y, t = importPoints(f"{targetDirectory}/{csvFile}")
		analyzeCSV(x, y, t, targetDirectory, csvFile)
	exit(0)


if __name__ == "__main__":
	main()