import re

def clean_text(text):
    """
    Clean and preprocess text by:
    - Converting to lowercase
    - Removing URLs, mentions, and hashtags
    - Removing special characters and numbers
    
    Parameters:
        text (str): Input text to be cleaned
        
    Returns:
        str: Cleaned text
    """
    # Convert to lowercase for consistency
    text = text.lower()
    
    # Remove URLs using regular expression
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove user mentions (@username) and hashtags (#topic)
    text = re.sub(r'@\w+|\#\w+', '', text)
    
    # Remove special characters (keep only alphanumeric and whitespace)
    text = re.sub(r'[^\w\s]', '', text)
    
    # Remove numbers/digits
    text = re.sub(r'\d+', '', text)
    
    return text