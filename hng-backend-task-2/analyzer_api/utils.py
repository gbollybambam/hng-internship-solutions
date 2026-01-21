import hashlib
import re
from collections import Counter

def calculate_sha256(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def is_string_palindrome(s: str) -> bool:
    normalized = ''.join(filter(str.isalnum, s)).lower()
    return normalized == normalized[::-1]

def get_character_properties(s: str) -> dict:
    freq_map = dict(Counter(s))

    unique_count = len(freq_map)

    words = s.split()
    word_count = len(words)

    return {
        "length": len(s),
        "is_palindrome": is_string_palindrome(s),
        "unique_characters": unique_count,
        "word_count": word_count,
        "character_frequency_map": freq_map
    }

def parse_natural_language_query(query: str) -> dict:
    parsed_filters = {}
    
    normalized_query = query.lower()
    
    if 'palindromic' in normalized_query or 'palindrome' in normalized_query:
        parsed_filters['is_palindrome'] = 'true'
        
    if 'single word' in normalized_query:
        parsed_filters['word_count'] = 1
    elif 'two word' in normalized_query:
        parsed_filters['word_count'] = 2
        
    for part in normalized_query.split():
        if part.isdigit():
            number = int(part)
            
            tokens = normalized_query.split()
            try:
                index = tokens.index(part)
                
                if index > 0 and tokens[index - 1] in ('longer', 'greater', 'over', 'above'):
                    parsed_filters['min_length'] = number + 1
                elif index > 0 and tokens[index - 1] in ('shorter', 'less', 'under', 'below'):
                    parsed_filters['max_length'] = number - 1
                    
            except ValueError:
                pass

    vowels = {'a': 'first vowel', 'e': 'second vowel', 'i': 'third vowel', 'o': 'fourth vowel', 'u': 'fifth vowel'}
    
    for char, name in vowels.items():
        if name in normalized_query or f'vowel {char}' in normalized_query:
            parsed_filters['contains_character'] = char
            
    match = re.search(r'letter\s+([a-z])', normalized_query)
    if match:
        parsed_filters['contains_character'] = match.group(1)
        
    min_len = parsed_filters.get('min_length')
    max_len = parsed_filters.get('max_length')
    
    if min_len is not None and max_len is not None and min_len > max_len:
        raise ValueError("Query resulted in conflicting length filters (min > max).")

    return parsed_filters