# string_utils.py
def reverse_string(s):
    return s[::-1]

def is_palindrome(s):
    return s == s[::-1]

def capitalize_words(sentence):
    return ' '.join(word.capitalize() for word in sentence.split())
