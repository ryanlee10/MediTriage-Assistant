import json

def ask_for_input():
	# symptomsRaw = input("Please enter your symptoms separated by a comma and space: ")
	# symptomList = symptomsRaw.split(", ")
	filepath = "Symptoms.json"
	with open(filepath) as fp:
		symptomData = json.load(fp)
		symptomList = symptomData["symptoms"]
	return symptomList	#list of symptoms from user

def retrieve_ontology():
	filepath = "DOSFinal.json"
	with open(filepath) as fp:
		ontologyData = json.load(fp)
	return ontologyData	#ontology JSON containing keywords

def search_for_candidates(ontologyData, symptomList):
	candidateList = []
	for disease in ontologyData["diseases"]:
		totalKeywordCounter = len(disease["name"].split())
		diagnosis = {}
		totalRecorded = False 
		unmatchedKeywords = disease["keywords"]
		for symptom in symptomList:
			keywordFoundCounter = 0	#take record of number of matches for each symptom
			nameIsMatch = disease["name"].lower().find(symptom)
			if (nameIsMatch > -1):	#check symptom against disease name
				keywordFoundCounter += 1
				if ("name" not in diagnosis):	#initialize dictionary entry
					diagnosis["name"] = disease["name"]
					diagnosis["search terms"] = []

			if (len(disease["keywords"]) > 0):	#only run code on ontology entries with keywords
				if (totalRecorded == False): #prevents duplication of number of total keywords for each symptom in symptomList
					totalKeywordCounter += len(disease["keywords"])
					totalRecorded = True
				for keyword in disease["keywords"]:
					keywordIsMatch = keyword.lower().find(symptom)
					if (keywordIsMatch > -1):	#check symptom against keywords
						unmatchedKeywords = list(filter(lambda a: a != keyword, unmatchedKeywords))
						keywordFoundCounter += 1
						if ("name" not in diagnosis):	#initialize dictionary entry
							diagnosis["name"] = disease["name"]
							diagnosis["search terms"] = []	

			if keywordFoundCounter != 0:	#only run code if the ontology entry contained the keyword
				diagnosis["search terms"].append({"# of '" + symptom + "' found": keywordFoundCounter})
		if (bool(diagnosis) == True):	#check diagnosis is not empty because there was no match
			diagnosis["unmatched keywords"] = unmatchedKeywords
			diagnosis["total # of keywords"] = totalKeywordCounter #have to divide by number of symptoms because total keywords amount is duplicated for each loop of a symptom
			candidateList.append(diagnosis)
	return candidateList	#candidates have any of the symptoms but may not have all the symptoms the user provided

def filter_candidates(candidateList, symptomList):
	diagnosesList = []
	for diagnosis in candidateList:
		if (len(diagnosis["search terms"]) == len(symptomList)):	#filter only for candidates that have all the user-provided symptoms
			totalSearchTermFoundCounter = 0	#find sum of all keywords found for ranking purposes
			for term in diagnosis["search terms"]:	#check each "# of __ found" entries
				for key in term:
					totalSearchTermFoundCounter += term[key]	#add number of each symptom found to total counter
			diagnosis["sum of search terms found"] = totalSearchTermFoundCounter
			diagnosesList.append(diagnosis)
	return diagnosesList

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
ontologyData = retrieve_ontology()
candidateList = search_for_candidates(ontologyData, symptomList);
diagnosesList = filter_candidates(candidateList, symptomList)
rankedDiagnosesList = sorted(diagnosesList, key = lambda x: list(x.values())[2], reverse = True)	#sort diagnosesList according to the 2nd index entry which is the total # of keywords
data = create_JSON(symptomList, rankedDiagnosesList)
write_to_json(data)









