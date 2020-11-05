import random, string

def get_words(filename):
    """reads in all words from a file and returns them as a list"""
    infile = open(filename)
    #all_words = infile.read().split()
    all_lines = infile.read().splitlines()
    infile.close()
    #return all_words
    return all_lines

def generate_dict(all_lines):
    """
    creates a nested dictionary, with each word as a key
    and the values are the frequency of the following words
    """
    following_word_freq = {}
    filtered_words = ['.', '-', '-.', ' ']
    
    for i, line in enumerate(all_lines):
    
	    for j, word in enumerate(line):
		    
		    word = strip_word(word)
		    
		    if word not in filtered_words:

			    if word and j < len(line)-1:
				    following_word = strip_word(words[j+1])
				    if not following_word_freq.get(word):
					    following_word_freq[word] = {following_word:1}
				    else:
					    following_word_freq[word][following_word] = following_word_freq[word].get(following_word, 0) + 1
					    
		    else:
			    print(f"Filtered out '{word}'")
    
    return following_word_freq

def strip_word(word):
    
    word = word.lower()
    word = word.translate(str.maketrans('', '', string.punctuation))
    word = word.strip('*@" ')
    word = word.replace('"', '')
    return word

def toxic_markov(freq_dict, root_word):
    """given a dictionary of following word frequencies and a root word,
    generate a sentence by adding a word to the previous word based on the
    relative frequency of that following word in the data set."""
    
    sentence = [root_word.capitalize()]
    max_sentence_length = 20
    
    for i in range(max_sentence_length):
        
        cur_word = sentence[-1]
        following_words = freq_dict.get(cur_word)
        following_word = ''
        
        if following_words:
            following_word = random.choices(list(following_words.keys()), weights=following_words.values())[0]
        else:
            #Get a new root word to use instead
            following_word = random.choice(list(freq_dict.keys()))
            
        #print(following_word)
        sentence.append(following_word)
        if not following_word or following_word.endswith('.') or following_word.startswith('-'):
            break        
    
    str_sentence = ' '.join(sentence).strip()
    
    if not str_sentence.endswith('.'):
        str_sentence += '.'
        
    return str_sentence
    
def generate_sentence(filename):
    all_lines = get_words(filename)
    following_word_freq = generate_dict(all_lines)
    sentence = toxic_markov(following_word_freq, random.choice(list(following_word_freq.keys())))
    return sentence
    
#print(generate_sentence('boiz_quotes.txt'))