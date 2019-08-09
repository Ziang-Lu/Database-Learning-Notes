#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main driver module.
"""

import bleach
from flask import Flask, request, redirect, url_for

import forumdb as db

app = Flask(__name__)

# HTML template for the forum page
PAGE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>DB Forum</title>
    <style>
        h1, form { text-align: center; }
        textarea { width: 400px; height: 100px; }
        div.post { border: 1px solid #999;
                   padding: 10px 10px;
                   margin: 10px 20%%; }
        hr.postbound { width: 50%%; }
        em.date { color: #999 }
    </style>
</head>
<body>
    <h1>DB Forum</h1>
    <form method="POST">
        <div>
            <textarea id="content" name="content"></textarea>
        </div>
        <div>
            <button id="go" type="submit">Post message</button>
        </div>
    </form>
    <!-- post content will go here -->
    %s
</body>
</html>
'''

# HTML template for an individual post
POST_TEMPLATE = '''\
<div class=post>
    <em class=date>%s</em>
    <br>
    %s
</div>
'''


@app.route('/', methods=['GET'])
def main_page():
    """
    Forum main page.
    When a "GET" request is forwarded to "/", this function gets called.
    :return:
    """
    posts = ''.join(
        POST_TEMPLATE % (bleach.clean(content), date)
        for content, date in db.get_posts()
    )  # Output sanitization
    return PAGE_TEMPLATE % posts


@app.route('/', methods=['POST'])
def post():
    """
    Forum main page, with post submission.
    When a "POST" request is forwarded to "/", this function gets called.
    :return:
    """
    # Note:
    # When a "POST" request is forwarded, the request is carrying the filled
    # form, stored in "request.form"
    msg = request.form['content']
    db.add_post(msg)
    return redirect(url_for('main_page'))


# @app.route('/', methods=['GET', 'POST'])
# def main_page():
#     """
#     A more common pattern that combines the previous two view functions into
#     one, which can handle both "GET" and "POST" requests.
#     :return:
#     """
#     if request.method == 'POST':
#         msg = request.form['content']
#         db.add_post(msg)
#         return redirect(url_for('main_page'))

#     posts = ''.join(
#         POST_TEMPLATE % (bleach.clean(content), date)
#         for content, date in db.get_posts()
#     )  # Output sanitization
#     return PAGE_TEMPLATE % posts


if __name__ == '__main__':
    db.init_db()
    app.run(host='0.0.0.0')  # Default port: 5000
