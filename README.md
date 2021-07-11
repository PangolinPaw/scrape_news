# scrape.py
## purpose
Search the front page of https://thefly.com/news.php for articles containing the specified phrase. If the matching article(s) have not been encountered before, save details to a text file named after today's date.

## installation
Pyton dependencies:

`pip install -r requirements.txt`

Geckodriver binary (Mac OSX):

`/geckodriver-install.sh`

**Important:** Make sure the path to the geckodriver binary is in your PATH environment variables or save the binary in the same directory as the _scrape_ python script.

## usage
 Usage:
 ``` 
   python scrape.py "<search term>" [interval]

   search term                  A word or phrase which articles must contain.
   interval                     (Optional) The number of minutes between each repetition
                                of the search. If blank, seach is completed only once.
```
