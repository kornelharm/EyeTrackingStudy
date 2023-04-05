import json
import os
import copy


def getResults():
	return [f.path for f in os.scandir(f"./results/") if f.path.endswith(".results")]

def getResponses(results):
	responses = dict()
	entry = {
				'RatedDifficulty' : 
				{
					'Not difficult' : 0,
					'Needs slower pace/re-reading' : 0, 
					'Sections are difficult' : 0, 
					'Little understanding is possible' : 0, 
					'Incomprehensible' : 0
				}, 
				'TopicKnowledge' : 
				{
					'No knowledge' : 0,
					'Aware of topic' : 0, 
					'Basic knowledge about topic' : 0, 
					'Knowledgable about topic' : 0, 
					'Could teach others about the topic' : 0
				}, 
				'RelatedKnowledge' :
				{
					'No related knowledge' : 0,
					'Aware of related topics' : 0, 
					'Basic knowledge about related topics' : 0, 
					'Knowledgable about topic' : 0, 
					'Could teach others about related topics' : 0
				}
			}
	responses["fermions"] = copy.deepcopy(entry)
	responses["fluorescense"] = copy.deepcopy(entry)
	responses["hooverDam"] = copy.deepcopy(entry)
	responses["nonEuclideanGeometry"] = copy.deepcopy(entry)
	responses["serialPeripheralInterface"] = copy.deepcopy(entry)
	for result in results:
		with open(result) as respFile:
			respJSON = json.load(respFile)
			for text in respJSON.keys():
				textVal = respJSON.get(text)
				if(not(type(textVal) is dict)):
					continue
				resp = textVal.get('survey')
				responses[text]['RatedDifficulty'][resp.get('RatedDifficulty')] += 1
				responses[text]['TopicKnowledge'][resp.get('PreviousKnowledge')] += 1
				responses[text]['RelatedKnowledge'][resp.get('PreviousKnowledgeRelated')] += 1
	return responses

def main():
	results = getResults()
	responses = getResponses(results)
	for text in responses:
		print(f"{text} responses:")
		for question in responses[text]:
			print(responses[text][question])
	exit(0)


if __name__ == "__main__":
	main()