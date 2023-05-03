import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import babel
from datetime import datetime
from dateutil.parser import parse
from models import setup_db, db_drop_and_create_all, Couple, Hall
import collections
import traceback
from auth import AuthError, requires_auth
from dotenv import load_dotenv
load_dotenv()

collections.Callable = collections.abc.Callable

#  RESET_DB environment variable is to be set to False from second run to avoid database resetting
RESET_DB = os.getenv('RESET_DB', True)


class DateError(Exception):
    '''
    Exception raised when date misformat or invalid date
    '''
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def create_app(reset_db=RESET_DB, test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['DEBUG'] = True
    if test_config:
        setup_db(app, test_config.get("SQLALCHEMY_DATABASE_URI"))
    else:
        setup_db(app)

    if reset_db:
        db_drop_and_create_all()

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        response.headers.add(
            'Access-Control-Allow-Origin', '*')
        return response

    @app.route('/')
    def health_check():
        '''
        Health checkup for production environment
        '''
        return "Healthy"

    @app.route("/couples", methods=["POST"])
    @requires_auth()
    def create_couple(payload):
        '''
        Creates a new couple, no permission required
        '''
        body = request.get_json()

        bride_name = body.get("bride_name", None)
        groom_name = body.get("groom_name", None)
        marriage_date = body.get("marriage_date", None)
        email_id = body.get("email_id", None)
        wedding_theme = body.get("wedding_theme", None)
        hall = body.get("hall", None)

        try:
            if marriage_date:
                marriage_date = parse(marriage_date)
        except ValueError as e:
            raise DateError({
                'success': False,
                'error': '400',
                'message': 'Bad request - Error in parsing Marriage date : ' + str(e)
            }, 400)

        try:
            couple = Couple(bride_name=bride_name, groom_name=groom_name, marriage_date=marriage_date,
                            email_id=email_id, wedding_theme=wedding_theme, hall=hall)
            couple.insert()
            return jsonify({
                "success": True,
                "created": couple.format()
            })
        except Exception as e:
            abort(422)

    @app.route('/couples')
    @requires_auth('view:couples')
    def get_couples(payload):
        '''
        View the list of all couples with details
        '''
        couples = Couple.query.order_by(Couple.id).all()

        if len(couples) == 0:
            abort(404)  # When couple table is empty

        return jsonify(
            {
                "success": True,
                "couples": [couple.format() for couple in couples],
                "total_couples": len(couples)
            }
        )

    @app.route('/couples/<int:couple_id>')
    @requires_auth('view:couple')
    def get_couple_by_id(payload, couple_id):
        '''
        View the couple detail provided the couple id
        '''
        couple = Couple.query.filter_by(id=couple_id).one_or_none()

        if couple is None:
            abort(404)  # When No couple is found with given couple id

        return jsonify(
            {
                "success": True,
                "couple": couple.format()
            }
        )

    @app.route('/couples/<int:couple_id>', methods=["PATCH"])
    @requires_auth('update:couple')
    def update_couple(payload, couple_id):
        ''''
        Update the couple with the details passed in request body
        '''
        body = request.get_json()
        couple = Couple.query.filter_by(id=couple_id).one_or_none()

        if couple is None:
            abort(404)  # When No couple is found with given couple id

        couple.bride_name = body.get("bride_name", couple.bride_name)
        couple.groom_name = body.get("groom_name", couple.groom_name)

        try:
            couple.marriage_date = parse(body.get("marriage_date", str(couple.marriage_date)))
        except ValueError as e:
            raise DateError({
                'success': False,
                'error': '400',
                'message': 'Bad request - Error in parsing Marriage date : ' + str(e)
            }, 400)

        couple.email_id = body.get("email_id", couple.email_id)
        couple.wedding_theme = body.get("wedding_theme", couple.wedding_theme)
        couple.hall = body.get("hall", couple.hall)

        try:
            couple.update()
            return jsonify({
                "success": True,
                "updated": couple.format()
            })
        except Exception as e:
            abort(422)

    @app.route("/couples/<int:couple_id>", methods=["DELETE"])
    @requires_auth('remove:couple')
    def delete_couple(payload, couple_id):
        '''
        Remove the couple with given couple id
        '''
        couple = Couple.query.filter_by(id=couple_id).one_or_none()

        if couple is None:
            abort(404)  # When No couple is found with given couple id

        try:
            couple.delete()
            couples = Couple.query.order_by(Couple.id).all()

            return jsonify(
                {
                    "success": True,
                    "deleted": couple_id,
                    "couples": [couple.format() for couple in couples],
                    "total_couples": len(couples),
                }
            )
        except Exception as e:
            abort(422)

    @app.route('/halls')
    @requires_auth('view:halls')
    def get_halls(payload):
        '''
        View the list of all halls with details
        '''
        halls = Hall.query.order_by(Hall.id).all()

        if len(halls) == 0:
            abort(404)  # When hall table is empty

        return jsonify(
            {
                "success": True,
                "halls": [hall.format() for hall in halls],
                "total_halls": len(halls)
            }
        )

    @app.route('/halls/<int:hall_id>')
    @requires_auth('view:hall')
    def get_hall_by_id(payload, hall_id):
        '''
        View the hall detail provided the hall id
        '''
        hall = Hall.query.filter_by(id=hall_id).one_or_none()

        if hall is None:
            abort(404)  # When No hall is found with given hall id

        return jsonify(
            {
                "success": True,
                "hall": hall.format()
            }
        )

    @app.route("/halls", methods=["POST"])
    @requires_auth('create:hall')
    def create_hall(payload):
        '''
        Creates a new hall with the details provided
        '''
        body = request.get_json()

        name = body.get("name", None)
        capacity = body.get("capacity", None)
        price = body.get("price", None)
        address = body.get("address", None)

        try:
            hall = Hall(name=name, capacity=capacity, price=price, address=address)
            hall.insert()
            return jsonify({
                "success": True,
                "created": hall.format()
            })
        except Exception as e:
            abort(422)

    @app.route('/halls/<int:hall_id>', methods=["PATCH"])
    @requires_auth('update:hall')
    def update_hall(payload, hall_id):
        ''''
        Update the hall with the details passed in request body
        '''
        body = request.get_json()
        hall = Hall.query.filter_by(id=hall_id).one_or_none()

        if hall is None:
            abort(404)  # When No hall is found with given hall id

        hall.name = body.get("name", hall.name)
        hall.capacity = body.get("capacity", hall.capacity)
        hall.price = body.get("price", hall.price)
        hall.address = body.get("address", hall.address)

        try:
            hall.update()
            return jsonify({
                "success": True,
                "updated": hall.format()
            })
        except Exception as e:
            abort(422)

    @app.route("/halls/<int:hall_id>", methods=["DELETE"])
    @requires_auth('remove:hall')
    def delete_hall(payload, hall_id):
        '''
        Remove the hall with given hall id
        '''
        hall = Hall.query.filter_by(id=hall_id).one_or_none()

        if hall is None:
            abort(404)  # When No hall is found with given hall id

        try:
            hall.delete()
            halls = Hall.query.order_by(Hall.id).all()

            return jsonify(
                {
                    "success": True,
                    "deleted": hall_id,
                    "halls": [hall.format() for hall in halls],
                    "total_halls": len(halls),
                }
            )
        except Exception as e:
            abort(422)

    """
    Create error handlers for all expected errors
    """

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"success": False, "error": 500, "message": "internal server error"}), 500

    @app.errorhandler(DateError)
    def handle_date_error(exeption):
        '''
        error handler for DateError
        '''
        response = jsonify(exeption.error)
        response.status_code = exeption.status_code
        return response

    @app.errorhandler(AuthError)
    def handle_auth_error(exeption):
        '''
        error handler for AuthError
        '''
        exeption.error.update({'success': False})
        response = jsonify(exeption.error)
        response.status_code = exeption.status_code
        return response

    return app


if __name__ == "__main__":
    app = create_app()
