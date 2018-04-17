from time import gmtime, strftime
import ssl
import time
import tweet
import urllib.request

timeBetweenTests = 10 # in seconds

urls = [
( 'http://root.cern.ch', b'ROOT a Data analysis Framework', 2000),
( 'https://root.cern.ch', b'ROOT a Data analysis Framework', 2000),
( 'http://root-forum.cern.ch', b'ROOT Forum', 200),
( 'https://root-forum.cern.ch', b'ROOT Forum', 200),
( 'http://root.cern.ch/download/cling/', b'Index of /download/cling', 300),
( 'https://root.cern.ch/doc/master/', b'ROOT Reference Documentation', 600),
]

state = {}

noVerifContext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

def report_state_change(url, newState):
  print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), newState, url)
  tweet.tweet(to = 'n_axel_n', text = url.replace('://', ': //') + ' is ' + newState)

def check_url(url, text, readlen):
  try:
    response = urllib.request.urlopen(url, timeout=2, context=noVerifContext)
    if text in response.read(readlen):
      return 'UP'
  except:
    pass
  try:
    xcheck = urllib.request.urlopen('https://www.google.fr', timeout=2, context=noVerifContext)
    if b'<title>Google</' in xcheck.read(600):
      return 'DOWN' # can reach google but not url
  except:
    pass
  return 'UP' # if Google and url are down, we are down and url is up!

def init():
  for url in urls:
    state[url[0]] = 'UP'

def check_all():
  prev=[]
  while True:
    #print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    #timeBefore = time.time()
    for url in urls:
      res = check_url(url[0], url[1], url[2])
      if res != state[url[0]]:
        if url in prev:
          state[url[0]] = res
          del prev[url[0]]
          report_state_change(url[0], res)
        else:
          prev.append(url[0])
    #print('Check duration:', time.time() - timeBefore, 'seconds')
    if len(prev) or 'DOWN' in state.values():
      time.sleep(20)
    else:
      time.sleep(60)

init()
check_all()

