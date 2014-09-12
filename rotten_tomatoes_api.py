from app_config import Config
import requests, json
import time
import urllib

api_key = Config().rotten_tomatoes_api_key

def rate_limited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rateLimitedFunction
    return decorate

def rottenreq(url):
	url += "apikey="+api_key
	response = requests.get(url).content

	return response.strip()

@rate_limited(5)
def search(title, year):
	query = urllib.urlencode({'q': title})
	url = 'http://api.rottentomatoes.com/api/public/v1.0/movies.json?'+query+'&page_limit=5&'
	response = json.loads(rottenreq(url))
	try:
		for movie in response['movies']:
			if year - 1 <= movie['year'] <= year + 1:
				return movie
	except:
		pass
	return {}

@rate_limited(5)
def is_valid(movie):
	try:
		rotten_movie = search(movie['title'], movie['year'])
		if movie['title'].lower.strip() == rotten_movie['title'].lower.strip():
			return True, rotten_movie
	except:
		pass
	return False, {}




