# Flask Rest Paginate

A Pagination Extension for Flask RESTful and Flask RESTplus.

## Installation

Install the extension using 
```
pip install flask-rest-paginate
```

## Usage
In your app, add the extension as follows

```py
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_rest_paginate import Pagination

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///paginate-test.db"
db = SQLAlchemy(app)

pagination = Pagination(app, db)

```

## Example:

Check the `example` folder for an example of the extension.

## Contributing

We are always grateful for any kind of contribution including but not limited to bug reports, code enhancements, bug fixes, and even functionality suggestions.

You can report any bug you find or suggest new functionality with a new [issue](https://github.com/mtShaikh/flask-rest-paginate/issues).

If you want to add yourself some functionality to the extension:
 
- Open an [issue](https://github.com/mtShaikh/flask-rest-paginate/issues)
- Comment there you are working on a new functionality
- Fork the [repo](https://github.com/mtShaikh/flask-rest-paginate/)
- Create your feature branch (git checkout -b my-new-feature)
- Commit your changes (git commit -am 'Adds my new feature')
- Push to the branch (git push origin my-new-feature)
- Create a new Pull Request
- mention the issue number in the PR description as `fixes #123, #321`
