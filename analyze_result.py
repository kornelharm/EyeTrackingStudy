import sys
import getopt
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import pylab
import graphing


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

def getCSVFiles(directory):
	files = os.listdir(directory)
	return [csvFile for csvFile in files if csvFile.endswith('.csv')]

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
	
	return x, y, t

def analyzeCSV(x, y, t, directory, filename):
	yFlipped = [1080 - a for a in y]
	# colors = [(x/_t[-1], 0.5, 1) for x in _t]
	colors1 = np.linspace(0, 1, len(x))
	colors2 = pylab.cm.rainbow(np.linspace(0, 1, len(x)))


	exportPlotName = f"{directory}/plots/{filename.rsplit('_')[0]}"
	exportAnimName = f"{directory}/anims/{filename.rsplit('_')[0]}"

	# x vs t
	graphing.save_graph(f"{exportPlotName}_x_vs_t_points.svg", [], [], colors1, "rainbow", [t], [x], [t[-1], 1920], "Horizontal Position vs Time", "Time (ms)", "Horizontal Position (px)")
	graphing.save_graph(f"{exportPlotName}_x_vs_t_line.svg", [t], [x], colors1, "rainbow", [], [], [t[-1], 1920], "Horizontal Position vs Time", "Time (ms)", "Horizontal Position (px)")
	debugPrint(f"Saving {exportAnimName}_x_vs_t_points.gif...")
	graphing.save_animation(f"{exportAnimName}_x_vs_t_points.gif", [], [], colors1, "rainbow", [t], [x], [t[-1], 1920], len(x), 1, False, "Horizontal Position vs Time", "Time (ms)", "Horizontal Position (px)")
	debugPrint(f"Saving {exportAnimName}_x_vs_t_line.gif...")
	graphing.save_animation(f"{exportAnimName}_x_vs_t_line.gif", [t], [x], colors1, "rainbow", [], [], [t[-1], 1920], len(x), 1, False, "Horizontal Position vs Time", "Time (ms)", "Horizontal Position (px)")

	# y vs t
	graphing.save_graph(f"{exportPlotName}_y_vs_t_points.svg", [], [], colors1, "rainbow", [t], [yFlipped], [t[-1], 1080], "Vertical Position vs Time", "Time (ms)", "Vertical Position (px)")
	graphing.save_graph(f"{exportPlotName}_y_vs_t_line.svg", [t], [yFlipped], colors1, "rainbow", [], [], [t[-1], 1080], "Vertical Position vs Time", "Time (ms)", "Vertical Position (px)")
	debugPrint(f"Saving {exportAnimName}_y_vs_t_points.gif...")
	graphing.save_animation(f"{exportAnimName}_y_vs_t_points.gif", [], [], colors1, "rainbow", [t], [yFlipped], [t[-1], 1080], len(x), 1, False, "Vertical Position vs Time", "Time (ms)", "Vertical Position (px)")
	debugPrint(f"Saving {exportAnimName}_y_vs_t_line.gif...")
	graphing.save_animation(f"{exportAnimName}_y_vs_t_line.gif", [t], [yFlipped], colors1, "rainbow", [], [], [t[-1], 1080], len(x), 1, False, "Vertical Position vs Time", "Time (ms)", "Vertical Position (px)")

	# y vs x
	graphing.save_graph(f"{exportPlotName}_y_vs_x_points.svg", [], [], colors1, "rainbow", [x], [yFlipped], [1920, 1080], "Vertical vs Horizontal Position", "Horizontal Position (px)", "Vertical Position (px)")
	graphing.save_graph(f"{exportPlotName}_y_vs_x_line.svg", [x], [yFlipped], colors1, "rainbow", [], [], [1920, 1080], "Vertical vs Horizontal Position", "Horizontal Position (px)", "Vertical Position (px)")
	debugPrint(f"Saving {exportAnimName}_y_vs_x_points.gif...")
	graphing.save_animation(f"{exportAnimName}_y_vs_x_points.gif", [], [], colors1, "rainbow", [x], [yFlipped], [1920, 1080], len(x), 1, False, "Vertical vs Horizontal Position", "Horizontal Position (px)", "Vertical Position (px)")
	debugPrint(f"Saving {exportAnimName}_y_vs_x_line.gif...")
	graphing.save_animation(f"{exportAnimName}_y_vs_x_line.gif", [x], [yFlipped], colors1, "rainbow", [], [], [1920, 1080], len(x), 1, False, "Vertical vs Horizontal Position", "Horizontal Position (px)", "Vertical Position (px)")

	# for i in range(len(_x)):
		# plt.plot(_x[i], _y[i], color=colors[i], marker="+", markersize=5, linestyle="dashed", linewidth=2)


def main():
	args = getopts()
	if(len(args) != 1):
		error("Invalid arguments provided.\nPlease provide target directory to run in")
	targetDirectory = args[0]
	files = getCSVFiles(targetDirectory)
	for csvFile in files:
		x, y, t = importPoints(f"{targetDirectory}/{csvFile}")
		analyzeCSV(x, y, t, targetDirectory, csvFile)
		break
	exit(0)


if __name__ == "__main__":
	main()