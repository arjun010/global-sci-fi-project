import json, csv, time

# time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1347517370))
dataMap = {}

reader = csv.reader(open('data.csv','rb'))
header = reader.next()

with open('idToEntityMap.json') as f:
    idToEntityMap = json.load(f)

with open('idToSentimentMap.json') as f:
    idToSentimentMap = json.load(f)

with open('idToTopicsMap.json') as f:
    idToTopicsMap = json.load(f)


entityTypes = []
for postId in idToEntityMap:
	for entityType in idToEntityMap[postId]:
		if entityType not in entityTypes:
			entityTypes.append(entityType)

for line in reader:
	postId = line[header.index('id')]
	body = line[header.index('body')]
	title = line[header.index('title')]
	postScore = line[header.index('score')]
	commentsCount = line[header.index('comms_num')]
	date = time.strftime('%Y-%m-%d', time.localtime(float(line[header.index('created')])))

	positiveScore = idToSentimentMap[postId]['positive']
	negativeScore = idToSentimentMap[postId]['negative']
	topics = idToTopicsMap[postId]

	postEntityMap = idToEntityMap[postId]

	dataMap[postId] = {
		'body' : body,
		'title' : title,
		'postScore' : int(postScore),
		'commentsCount' : int(commentsCount),
		'date' : date,
		'positiveScore' : positiveScore,
		'negativeScore' : negativeScore,
		'topics' : '|'.join(topics),
		'topicsWordCount' : len(topics)
	}

	for entityType in entityTypes:
		if entityType in postEntityMap:
			dataMap[postId]['entity'+"_"+str(entityType)+"_count"] = postEntityMap[entityType]['count']
			dataMap[postId]['entity'+"_"+str(entityType)+"_values"] = '|'.join(postEntityMap[entityType]['values'])
		else:
			dataMap[postId]['entity'+"_"+str(entityType)+"_count"] = 0
			dataMap[postId]['entity'+"_"+str(entityType)+"_values"] = ""

writer = csv.writer(open('compiledData.csv','wb'))

firstRow = True

outputData = []

for postId in dataMap:
	if firstRow == True:
		curRow = []
		for key in dataMap[postId]:
			curRow.append(key)
		writer.writerow(curRow)
		firstRow = False

	curRow = []
	curDataObj = {}
	for key in dataMap[postId]:
		curRow.append(dataMap[postId][key])
		curDataObj[key] = dataMap[postId][key]

	curDataObj['id'] = postId
	outputData.append(curDataObj)

	writer.writerow(curRow)

with open('compiledData.json', 'w') as outfile:
    json.dump(outputData, outfile, indent=1)