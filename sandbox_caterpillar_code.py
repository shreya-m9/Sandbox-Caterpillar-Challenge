import requests

url = "https://recruitment.sandboxnu.com/api/eyJkYXRhIjp7ImNoYWxsZW5nZSI6IkZsb3ciLCJlbWFpbCI6Im1vb2toZXJqZWUuc0Bub3J0aGVhc3Rlcm4uZWR1IiwiZHVlRGF0ZSI6IjIwMjUtMTItMTlUMDU6MDA6MDAuMDAwWiJ9LCJoYXNoIjoibU5YTVRNZ3RCSHEyUWVmbDZUZyJ9"
response = requests.get(url)
data = response.json()

'''
Data Definition: data represents information on sessions, rounds, and participant information for Flow in the Field users

data = Dictionary with 3 keys: sessions, rounds, and participantInfo

sessions = list of dictionaries, with each dictionary being a session containing...
    participantId (int): id of participant who completed the session
    sessionId (int): this session's id
    language (str): name of language studied during session
    rounds (list of ints): round id's associated with session (non-zero)
    startTime (int): starting time of session
    endTime (int): ending time of session

rounds = list of dictionaries, with each dictionary being a round containing...
    roundId (int): this round's id
    sessionId (int): session id associated with  round
    score (int): score of round
    startTime (int): starting time of round
    endTime (int): ending time of round

participantInfo = list of dictionaries, with each dictionary being a participant containing...
    participantId (int): this participant's id
    name (str): participant's name
	age (int): participant's age
	sessions (list of ints): session id's associated with participant
'''

def getLangSessions(sessions, lang):
    '''
    Does: gets only sessions in specified language
    Args:
        sessions (list) = session objects to sort through 
        language (str) = language of sessions to be returned
    Returns:
        langSessions (list) = all session objects completed in specified language
    '''
    langSessions = []
    for session in sessions:
        if session['language'] == lang:
            langSessions.append(session) 

    return langSessions

def getRounds(sessions, data):
    '''
    Does: gets the rounds within a list of sessions
    Args:
        sessions (list) = session objects to find rounds of
        data (dict) = full dataset, which includes a key named 'rounds'
    Returns
        rounds (list) = all round objects within the specified sessions
    '''
    rounds = []
    roundIds = [roundId for session in sessions for roundId in session['rounds']]
    for id in roundIds:
        idRound = next(filter(lambda round: round['roundId'] == id, data['rounds']))
        rounds.append(idRound)

    return rounds

def getAvgDuration(iterable):
    '''
    Does: gets the average duration of sessions or rounds
    Args:
        iterable (list) = session or round objects to get average duration of
    Returns:
        avgDuration (float or int) = average duration of sessions or rounds in iterable, returns an int if average is a whole number
    '''
    if not iterable:
        return 'N/A'
    
    totalDuration = 0
    for item in iterable:
            duration = abs(item['startTime'] - item['endTime'])
            totalDuration += duration            
    count = len(iterable)
    avgDuration = round(totalDuration/count, 2)

    if abs(avgDuration - int(avgDuration)) < .000000005:
        avgDuration = int(avgDuration)
    else:
        avgDuration = round(totalDuration/count, 2)

    return avgDuration


def getAvgRoundScore(rounds):
    '''
    Does: gets the average score of sessions or rounds
    Args:
        iterable (list) = round objects to get average score of
    Returns:
        avgScore (float or int) = average score of rounds, returns an int if average is a whole number
    '''
    if not rounds:
        return 'N/A'
    
    totalScore = sum([round['score'] for round in rounds])
    count = len(rounds)
    avgScore = round(totalScore/count, 2)

    if abs(avgScore - int(avgScore)) < .000000005:
        avgScore = int(avgScore)
    else:
        avgScore = round(totalScore/count, 2)

    return avgScore

def getParticipantStats(data):
    '''
    Does: gets participant statistics based on data
    Args:
        data (dict) = data containing 3 keys: sessions, rounds, and participantInfo
    Returns:
        participantStats (list) = list of dictionaries, with each dictionary being a participant and their statistics:
            structure = {
                         'id' (int): participantId,
                         'name' (str): name of participant,
                         'languages' (list): dictionary objects, with each one containing...
                                            [{
                                               'language' (str): language sessions were completed in
                                               'averageScore' (float): average score of sessions in language
                                               'averageRoundDuration' (float): average length of round completed in sessions of language
                                            }],
                         'averageRoundScore' (float): average score of round for all sessions a participant completed,
                         'averageSessionDuration' (float): average score of session for all sessions a participant completed,
                        }
    '''
    participantStats = []
    for participant in data['participantInfo']:
        id = participant['participantId']
        participantSessions = list(filter(lambda person: person['participantId'] == id, data['sessions']))
        participantRounds = getRounds(participantSessions, data)
        langs = set({session['language'] for session in participantSessions})

        participantData = {
                           'id': id, 
                           'name': participant['name'], 
                           'languages': [],    
                           'averageRoundScore': 'N/A',
                           'averageSessionDuration': 'N/A'
                          }
        
        participantStats.append(participantData)
        participantStat = next(filter(lambda person: person['id'] == id, participantStats))

        languagesData = []
        for lang in langs:
            langRounds = getRounds(getLangSessions(participantSessions, lang), data)
            totalScore = sum(rnd['score'] for rnd in langRounds)
            avgScore = getAvgRoundScore(langRounds)
            avgRoundDuration = getAvgDuration(langRounds)
            langData = {
                        'language': lang,
                        'averageScore': avgScore,
                        'averageRoundDuration': avgRoundDuration,
                        'totalScore': totalScore
                        }
            languagesData.append(langData)

        participantStat['averageRoundScore'] = getAvgRoundScore(participantRounds)
        participantStat['averageSessionDuration'] = getAvgDuration(participantSessions)

        if languagesData:
            sortedData = sorted(languagesData, key = lambda language: language['totalScore'], reverse = True) 
            for lang in sortedData:
                del lang['totalScore']
            participantStat['languages'] = sortedData
      
    return sorted(participantStats, key = lambda participant: participant['name'])

participantStats = getParticipantStats(data)
r = requests.post(url, json=participantStats)
print(r)

