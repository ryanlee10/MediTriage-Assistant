import json
import re
from time import time
def get_lexicon(symptoms):
	global lexiconContents
	with open('medical_lexicon.txt') as lexicon:
		lexiconContents = set(map(lambda x: x.lower(),lexicon.read().split())) #optimize search time to O(1) using set()
		(lexiconContents.add(symptom) for symptom in symptoms)

def ask_for_input():
	filepath = "Symptoms.json"
	with open(filepath) as fp:
		symptomData = json.load(fp)
		symptomList = symptomData["symptoms"]
	return symptomList	#list of symptoms from user

def retrieve_ontology():
	filepath = "DOSFinal.json"
	with open(filepath) as fp:
		ontologyData = json.load(fp)
	for index,disease in enumerate(ontologyData['diseases']):
		ontologyData['diseases'][index]['keywords'] = list(filter(search_lexicon,disease['keywords']))
	return ontologyData	#ontology JSON containing keywords

def remove_delims(phrase):
	return (set(re.split('[ `~?!!@#$%^&*()-/;:,":]', phrase.lower())))

def search_lexicon(phrase):
	words  = remove_delims(phrase)
	words = set(map(lambda x: x.lower(),words)) # make all words lowercase and remove duplicates
	return (words & lexiconContents) # return if there is an intersection between words and lexicon
		
def search_for_candidates(ontologyData, symptomList):
	candidateList = []
	for disease in ontologyData["diseases"]:
		diagnosis = {'name':disease['name'],'search terms':[]}
		keywords = disease["keywords"]
		keywordSum = 0
		for symptom in symptomList:
			keywordFoundCounter = 0	#take record of number of matches for each symptom (may be higher than what appears because of removal of duplicates but more accurately accounts for how important a keyword was)
			nameMatch = (disease['name']).count(symptom) #count how many query matches in the names of the diseases
			query = ('.'.join((keywords)).lower()).count(symptom.lower()) #count how many query matches in the keywords
			keywordFoundCounter += (query) + nameMatch
			keywordSum += keywordFoundCounter
			if keywordFoundCounter:	#only run code if the ontology entry contained the keyword
				diagnosis["search terms"].append({"# of '" + symptom + "' found": keywordFoundCounter})
		if (len(symptomList) == len(diagnosis['search terms'])):	#check diagnosis is not empty because there was no match
			diagnosis["keywords"] = keywords
			diagnosis["total # of keywords"] = len(disease["keywords"])+len(disease["name"].split()) #have to divide by number of symptoms because total keywords amount is duplicated for each loop of a symptom
			diagnosis["sum of search terms found"] = keywordSum
			candidateList.append(diagnosis)
	return candidateList	#candidates have any of the symptoms but may not have all the symptoms the user provided

def create_JSON(symptomList, rankedDiagnosesList):
	data = {}
	data["patient"] = {"symptoms": symptomList,
					   "diagnoses": rankedDiagnosesList
					  }	
	return data

def write_to_json(data):
	filename = "Diagnosis.json"
	with open(filename, "w", encoding = "utf-8") as file:
		json.dump(data, file, indent = 4)


symptomList = ask_for_input()
get_lexicon(symptomList)
ontologyData = retrieve_ontology()
t = time()
diagnosesList = search_for_candidates(ontologyData, symptomList);
print(time()-t)
print(len(diagnosesList))
rankedDiagnosesList = sorted(diagnosesList, key = lambda x: (x['sum of search terms found']), reverse = True)#sort diagnosesList according to the 2nd index entry which is the total # of keywords
data = create_JSON(symptomList, rankedDiagnosesList)
write_to_json(data)








