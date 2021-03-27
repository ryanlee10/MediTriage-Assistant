import json

def retrieve_ontology():
	filepath = "DOSFinal.json"
	with open(filepath) as fp:
		ontologyData = json.load(fp)
	return ontologyData	#ontology JSON containing keywords

def write_to_json(data):
	filename = "sortedDOS.json"
	with open(filename, "w", encoding = "utf-8") as file:
		json.dump(data, file, indent = 4)


ontologyData = retrieve_ontology()

newData = {}
newData["diseases"] = []
for disease in ontologyData["diseases"]:
	name = disease["name"]
	keywords = disease["keywords"]

	if len(keywords) == 0:
		newData["diseases"].append({
			"name": name,
			"keywords": []
		})

	else:
		sortedKeywords = sorted(set(keywords), key = len)
		newData["diseases"].append({
			"name": name,
			"keywords": sortedKeywords
		})
write_to_json(newData)
