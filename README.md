Lending Tree Review Collector Web Service
==============================

Overview
-------------

This is a Python/Flask application intended to accept a request of a Lender's url on https://www.lendingtree.com/reviews and pull all reviews into a dictionary and json file, parsing the lender name, title, content, author, rating and date for each review.

Usaing this Wen Service
---------------

1. Run `pip install -r requirements.txt` to install dependencies
2. Run `python app.py`.
3. Navigate to http://127.0.0.1:5000/ in your browser
4. Input the Lender's url into the text box and click the **Submit** button
5. After the reviews are collected, they will be outputted on the page in json format.
6. All reviews will also be stored in reviews.json
