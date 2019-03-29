import re
from nltk.stem.porter import PorterStemmer

def handle_emojis(tweet):
	# Smile -- :), : ), :-), (:, ( :, (-:, :')
    tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', ' EMO_POS ', tweet)
    # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
    tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' EMO_POS ', tweet)
    # Love -- <3, :*
    tweet = re.sub(r'(<3|:\*)', ' EMO_POS ', tweet)
    # Wink -- ;-), ;), ;-D, ;D, (;,  (-;
    tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', ' EMO_POS ', tweet)
    # Sad -- :-(, : (, :(, ):, )-:
    tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' EMO_NEG ', tweet)
    # Cry -- :,(, :'(, :"(
    tweet = re.sub(r'(:,\(|:\'\(|:"\()', ' EMO_NEG ', tweet)
    return tweet

def preprocess_word(word):
	# remove punctation
	word = word.strip('\'"?!,.():;')
	# more than 3 letter repetition removed
	word = re.sub(r'(.)\1\1+', r'\1\1\1', word)
	# remove - & '
	word = word.strip('-&\'')
	return word

def is_valid_word(word):
    # Check if word begins with an alphabet
    return (re.search(r'^[a-zA-Z][a-z0-9A-Z\._]*$', word) is not None)

def preprocess_tweet(tweet, use_stemmer = False):
	# convert tweet to lowercase
	tweet = tweet.lower()
	# replace urls with 'URL'
	tweet = re.sub(r'((www\.[\S]+)|(https?://\.[\S]+))', 'URL', tweet)
	# replace user mentions @user with 'USER_MENTION'
	tweet = re.sub(r'@[\S]+', 'USER_MENTION', tweet)
	# replace #hashtag with hastag
	tweet = re.sub(r'#(\S+)', r' \1', tweet)
	# remove retweet RT
	tweet = re.sub(r'\brt\b', '', tweet)
	# replace 2+ dots with space
	tweet = re.sub(r'\.{2,}', ' ', tweet)
	# remove space, " and ' 
	tweet.strip('" \'')
	# handle emojis. Use only EMO_POS and EMO_NEG
	tweet = handle_emojis(tweet)
	# replace multiple spaces with only one space
	tweet = re.sub(r'\s+', ' ', tweet)
	# preprocess words
	words = tweet.split()

	processed_words = []
	porter_stemmer = PorterStemmer()
	for word in words:
		word = preprocess_word(word)
		if is_valid_word(word):
			if use_stemmer:
				# use stemmer
				word = str(porter_stemmer.stem(word))
			processed_words.append(word)
	return ' '.join(processed_words)
