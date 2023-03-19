import json
import sys
 
def importData(fileStr):
    file = open(f"results/{fileStr}", "r")
    dataDict = json.load(file)
    return dataDict

def main():
    args = len(sys.argv)
    if(args <= 1):
        print("Not enough arguments provided.\nPlease provide target result file\n")
    targetResultFile = sys.argv[1]
    data = importData(targetResultFile)
    for field in data:
        print(field)

if __name__ == "__main__":
    main()