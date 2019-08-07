#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Flask application module.
"""

import bleach
from flask import Flask, request, redirect, url_for

import forumdb

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
def main_page() -> str:
    """
    Forum main page.
    When a "GET" request is forwarded to "/", this function gets called.
    :return: str
    """
    posts = ''.join(
        POST_TEMPLATE % (bleach.clean(content), date)
        for content, date in forumdb.get_posts()
    )  # Output sanitization
    return PAGE_TEMPLATE % posts


@app.route('/', methods=['POST'])
def post() -> None:
    """
    Forum main page, with post submission.
    When a "POST" request is forwarded to "/", this function gets called.
    :return: None
    """
    msg = request.form['content']
    forumdb.add_post(msg)
    return redirect(url_for('main_page'))


if __name__ == '__main__':
    forumdb.init_db()
    app.run(host='0.0.0.0')  # Default port: 5000
