import requests, json

def getDataDevice(device, attrs):

	# Config da API do Dojot
	host   = "198.199.123.83";
	port   = "8000";
	auth   = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJxSVJCaFlsR0g5ZHl6QlM4WUh0TU1tTU56cjY3dWhJaSIsImlhdCI6MTYwNjE4OTc1NywiZXhwIjoxNjA2MTkwMTc3LCJwcm9maWxlIjoiYWRtaW4iLCJncm91cHMiOlsxXSwidXNlcmlkIjoxLCJqdGkiOiI1M2Q4ZDYxNmFjZTYxODA3NWEzZmI3ZWVhM2QyYzg2YiIsInNlcnZpY2UiOiJhZG1pbiIsInVzZXJuYW1lIjoiYWRtaW4ifQ._mHz6fgGJzh5wCzeNORnPgvADJTDbLOGyXasHb1Mbog";
	
	url = f"http://{host}:{port}/history/device/{device}/history?lastN=1&attr={attrs}"

	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
		'Authorization': f"Bearer {auth}"
	}

	response = requests.get( url, headers=headers, verify=False )

	return response.json()

