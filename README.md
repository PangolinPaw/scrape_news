# scrape_news.py
## purpose
Search the front page of https://thefly.com/news.php for articles containing the specified phrase. If the matching article(s) have not been encountered before, save details to a text file named after today's date.

## usage
 Usage:
 ``` 
   python scrape.py "<search term>" [interval]

   search term                  A word or phrase which articles must contain.
   interval                     (Optional) The number of minutes between each repetition
                                of the search. If blank, seach is completed only once.
```

### example
Here's how you can monitor the site for all articles containing the word "low", re-checking every 5 minutes:

![scrape recording](https://user-images.githubusercontent.com/9369383/124463307-9f229080-dd8a-11eb-80e9-5ab6d6604d6a.gif)
[Alternative video link](https://youtu.be/kq15_kyO-Go)

