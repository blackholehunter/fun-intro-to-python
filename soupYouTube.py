# Import the libraries needed
import unicodedata
import re
import os

# These libraries will need to be installed first before importing
import bs4
import pandas
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from icecream import ic

def getSoupObjFromHTML(HTMLfile: str):
    """This function takes as an input a string representing an HTML file and returns a BeautifulSoup object."""
    # Assuming the HTML file resides in the Data directory located in the same directory as this script
    pathToHTMLfile = os.path.join(os.getcwd(), "Data", HTMLfile)
    # Create a BeautifulSoup object based on the input HTML page
    soup = BeautifulSoup(open(pathToHTMLfile, encoding = "utf8"), "html.parser")

    return soup

def populateDfFromSoupObj(df: pandas.DataFrame, soup: bs4.BeautifulSoup):
    """This function takes as an input a DataFrame and populates it from a BeautifulSoup object.
    It returns the populated DataFrame."""
    # We assume that the DataFrame has two columns: "Video title" and "Time watched"
    # We also assume that specific div classes store video titles and time watched based on inspecting the HTML file
    # We loop through all the div occurrences of the "QTGV3c" class
    for i in range(len(soup.findAll('div', {"class":"QTGV3c"}))):
        # We store the content of the current HTML <div> tag of class "QTGV3c"
        divTitle = soup.findAll('div', {"class":"QTGV3c"})[i]
        # We extract the title that is stored in the <a> tag
        title = divTitle.find('a')
        # We then the content of the current HTML <div> tag of class "H3Q9vf XTnvW"
        divTime = soup.findAll('div', {"class":"H3Q9vf XTnvW"})[i]
        # We extract the watch time text stored in this <div> tag, but remove some extra text we don't need
        timeText = divTime.text.replace(' • Details','')
        # Append these to the DataFrame
        df = df.append({"Video title": title.text, "Time watched": timeText}, ignore_index = True)

    return df

# This function was not written by me but by Ednalyn C. De Dios
# and you can read the whole article here: https://towardsdatascience.com/from-dataframe-to-n-grams-e34e29df3460
def cleanText(text: list):
  """This function will clean up the text. We first perform some encoding and regular expression passing on the
  input text. Then all the words that are not designated as a stop word are lemmatised and then a list of clean
  words is returned."""
  # Wordnet is an large, freely and publicly available lexical database for the English language aiming to establish
  # structured semantic relationships between words
  wnl = nltk.stem.WordNetLemmatizer()
  # NLTK (Natural Language Toolkit) in Python has a list of stopwords stored in many different languages,
  # including English
  stopwords = nltk.corpus.stopwords.words('english')
  # Perform some encoding on the input text
  text = (unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore').lower())
  # Perform some regular expression passing on the input text
  words = re.sub(r'[^\w\s]', '', text).split()
  # Create a list of lemmatised words that are not stopwords
  wordList = [wnl.lemmatize(word) for word in words if word not in stopwords]

  return wordList

def main():
    # The input HTML file containing YouTube watch history
    HTMLfile = "YouTubeWatchHistory.html"

    # Here is an example of using a docstring in Python to read function documentation
    ic(getSoupObjFromHTML.__doc__)

    # Parse this HTML file into a BeautifulSoup object
    soup = getSoupObjFromHTML(HTMLfile)

    # Create a DataFrame with two columns
    column_names = ["Video title", "Time watched"]
    df = pd.DataFrame(columns = column_names)

    # Populate the DataFrame with content from the BeautifulSoup object
    df = populateDfFromSoupObj(df, soup)

    # How many videos are there?
    ic("There are {} videos.".format(len(df)))

    # Create a list of dates videos were watch on, using <h2> tags of class "rp10kf"
    dates = soup.findAll('h2', {"class":"rp10kf"})
    # Print the date range
    ic("The dates range between {} and {}.".format(dates[0].text, dates[-1].text))

    # Convert the video title column of the DataFrame into list of text to prepare for cleaning
    wordList = cleanText(''.join(str(df['Video title'].tolist())))

    # Which bigrams occur the most in this list of video titles? Print the top 10.
    ic("Top 10 bigrams and their occurrence counts:")
    ic((pd.Series(nltk.ngrams(wordList, 2)).value_counts())[:10])

if __name__ == "__main__":
    main()