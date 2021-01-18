import random
from flask import Flask
from flask_restful import Api, Resource, marshal_with_field
from flask_sqlalchemy import SQLAlchemy
from flask_rest_paginate import Pagination
from marshmallow import Schema, fields

"""
Initialize the app
"""
app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///paginate-test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Possible configurations for Paginate
# app.config['PAGINATE_PAGE_SIZE'] = 20
# app.config['PAGINATE_PAGE_PARAM'] = "pagenumber"
# app.config['PAGINATE_SIZE_PARAM'] = "pagesize"
# app.config['PAGINATE_RESOURCE_LINKS_ENABLED'] = False
pagination = Pagination(app, db)

class CalculationSchema(Schema):
    calculation_time = fields.Str()
    value = fields.Str()

"""
Controllers
"""
class CalculationList(Resource):
    def get(self):
        """
        Simulates a long running computation that needs to be
        performed by a backend service.
        :return:
        """
        import time

        def largest_prime_factor(n):
            """
            Returns the largest prime factor of a number
            :param n:
            :return:
            """
            i = 2
            while i * i <= n:
                if n % i:
                    i += 1
                else:
                    n //= i
            return n

        result_list = []
        for i in range(100):
            start = time.time()
            prime = largest_prime_factor(random.randint(100000, 200000))
            result_list.append({"calculation_time": time.time() - start, "value": prime})

        return pagination.paginate(result_list, CalculationSchema(many=True), marshmallow=True)

"""
Register the resources
"""
api.add_resource(CalculationList, '/calculation')


"""
Run the app
"""
if __name__ == '__main__':
    app.run(debug=True)


