# Import required libraries
from wordcloud import WordCloud  # For generating word clouds
import matplotlib.pyplot as plt  # For data visualization
import seaborn as sns  # For enhanced visualizations
from collections import Counter  # For counting word frequencies
import re  # For regular expressions (text cleaning)
import nltk  # Natural Language Toolkit
from nltk.corpus import stopwords  # For stopword removal
from nltk.tokenize import word_tokenize  # For text tokenization

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

def get_top_words(corpus, n=None, exclude_stopwords=True):
    """
    Extract most frequent words from a text corpus with optional stopword removal
    
    Parameters:
        corpus (iterable): Collection of text documents
        n (int, optional): Number of top words to return. Returns all if None
        exclude_stopwords (bool): Whether to filter out stopwords
        
    Returns:
        list: Tuples of (word, count) sorted by frequency
    """
    try:
        # Load English stopwords if needed
        stop_words = set(stopwords.words('english')) if exclude_stopwords else set()
    except LookupError:
        # Download stopwords if not available
        nltk.download('stopwords')
        stop_words = set(stopwords.words('english')) if exclude_stopwords else set()
    
    words = []  # Initialize empty list to store all words
    
    for text in corpus:
        # Skip non-text or empty entries
        if not isinstance(text, str) or not text.strip():
            continue
            
        try:
            # Clean and tokenize text
            clean = clean_text(text)
            tokens = word_tokenize(clean)
            
            # Filter words based on criteria:
            # - Not in stopwords list (if enabled)
            # - Length > 2 characters
            # - Alphabetic characters only
            words.extend([
                word for word in tokens 
                if word not in stop_words 
                and len(word) > 2
                and word.isalpha()
            ])
        except Exception as e:
            # Print error message for debugging (first 50 chars of problematic text)
            print(f"Error processing text: {text[:50]}... - {str(e)}")
            continue
    
    # Count word frequencies and return top n results
    word_counts = Counter(words)
    return word_counts.most_common(n)

def generate_wordcloud(texts, title):
    """
    Generate and display a word cloud visualization
    
    Parameters:
        texts (iterable): Collection of text documents
        title (str): Title for the visualization
    """
    # Combine all texts into single string after cleaning
    text = ' '.join([clean_text(tweet) for tweet in texts])
    
    # Create WordCloud object with configuration:
    # - Size: 800x500 pixels
    # - White background
    # - Exclude English stopwords
    # - Limit to 100 words
    wordcloud = WordCloud(
        width=800, 
        height=500, 
        background_color='white',
        stopwords=set(stopwords.words('english')),
        max_words=100
    ).generate(text)
    
    # Create figure and display word cloud
    plt.figure(figsize=(10, 7))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Remove axes
    plt.title(title)  # Add title
    plt.show()  # Render visualization