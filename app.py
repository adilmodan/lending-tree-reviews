# importing dependecies
from flask import Flask, jsonify, request
import requests
import json
from bs4 import BeautifulSoup

# initializing a variable of Flask
app = Flask(__name__)


# pull all the html in from a webite
def get_page(url):
    try:
        r = requests.get(url)
        page = BeautifulSoup(r.text, 'html.parser')
        return page
    except:
        return "Invalid url"


# parsing html to get the reviews
def get_reviews(page):
    
    # there are 2 types of review: those that are shown on load and those that are hidden and be shown by clicking 'view more reviews' 
    mainReviews = page.find_all('div', {'class': 'col-xs-12 mainReviews'})
    hiddenReviews = page.find_all('div', {'class': 'col-xs-12 mainReviews hiddenReviews'})
    allReviews = mainReviews + hiddenReviews
    reviews = []

    # grabbing attributes from each review
    for i in allReviews:
        review ={
        'lender': page.title.text.replace(' – Personal Loan Company Reviews | LendingTree',''),
        'title' : i.find('p',{'class': 'reviewTitle'}).text.strip(),
        'content' : i.find('p',{'class': 'reviewText'}).text.strip(),
        'author' : i.find('p',{'class': 'consumerName'}).text.strip().replace('                                                                       ',''),
        'rating' : float(i.find('div',{'class': 'numRec'}).text.replace(' of 5)stars','').replace('(','').strip()),
        'date' : i.find('p',{'class': 'consumerReviewDate'}).text.replace('Reviewed in ','').strip(),
        }
        reviews.append(review)
    
    return reviews

# decorating index function with the app.route
@app.route('/', methods=['GET', 'POST'])
def form_example():

    # handle the POST request
    if request.method == 'POST':
        baseurl = str(request.form.get('baseurl'))
        if baseurl != '': 
            reviewList = []       # intialize Reviews List
            page_num = 1          # initialize first page
            last_page = 1         # initialize last page

            # iterating through each page
            while page_num <= last_page:
                url = baseurl + '?pid=' + str(page_num)             # adding a query into the url to handle pagination
                page = get_page(url)                                # grabbing HTML of webpage
                
                if page != 'Invalid url':                           # checking to see if url is invalid
                    print(f"Getting Page {page_num} Reviews")       # provides update in server
                    reviews = get_reviews(page)                     # parsing all parameters into a dictonary
                    last_page = int(page.find('a', {'class': 'pageNum'}).text)
                    reviewList.append(reviews)
                    page_num += 1
                else:
                    return "Invalid url: Please try again"
            
            if reviewList == []:                                    # handle pages with no reviews
                return "No Reviews Found on this page. Please try again."
            
            with open("reviews.json", "w") as outfile:  
                json.dump(reviewList, outfile)

            print(f"Found {len(reviewList)} reviews.")
            return jsonify(reviewList)
        else:
            return "No url entered. Please try again."

    # otherwise handle the GET request
    return '''
           <form method="POST">
               <div><label>Please input the Lender's url: <input type="text" name="baseurl"></label></div>
               <input type="submit" value="Submit">
           </form>'''

# run the web service
if __name__ == "__main__":
    app.run(debug=True)