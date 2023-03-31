import os
import csv

def getParticipants():
	dirs = [f.path for f in os.scandir("./results/") if f.is_dir()]
	return dirs

def getTexts(dirs):
	texts = []
	for dir in dirs:
		dirTexts = [f.path for f in os.scandir(f"{dir}/") if f.path.endswith(".csv")]
		for text in dirTexts:
			texts.append(text)
	return texts

def getCSVStats(texts):
	totalPoints = 0
	totalTime = 0
	for text in texts:
		with open(text) as csvFile:
			lastTime = 0
			reader = csv.reader(csvFile)
			first = True
			for row in reader:
				if(first):
					first = False
					continue
				totalPoints += 1
				lastTime = float(row[2])
			totalTime += lastTime
	return totalPoints, totalTime


def main():
	dirs = getParticipants()
	print(f"There are {len(dirs)} participants with processed data")
	texts = getTexts(dirs)
	print(f"There are {len(texts)} texts which have been processed")
	points, time = getCSVStats(texts)
	print(f"There are a total of {points} data points spanning {time/1000} seconds or {time/60000} minutes of reading")
	exit(0)


if __name__ == "__main__":
	main()