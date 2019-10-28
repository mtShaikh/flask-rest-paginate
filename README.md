# Flask Paginate

Pagination Extension for Flask RESTful and Flask RESTplus.

##### Installation
Install the extension using 
```
pip install flask-rest-paginate
```

##### Installation
In your app, add the extension as follows

```py
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_restful_paginate import Pagination

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///paginate-test.db"
db = SQLAlchemy(app)

pagination = Pagination(app, db)

```

##### Example:

Check the `example` folder for an example of the extension.

