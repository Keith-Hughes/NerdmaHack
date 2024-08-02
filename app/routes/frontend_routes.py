from flask import Blueprint, request, jsonify
import requests
from ..services import *



front_end_bp = Blueprint('front_end', __name__)

@front_end_bp.route('/add_client', methods=['POST'])
def add_client_route():
    data = request.get_json()
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    phone_number = data.get('phoneNumber')
    email = data.get('email')

    if not first_name or not last_name or not phone_number or not email:
        return jsonify({'error': 'All fields are required'}), 400

    try:
        new_client = add_client(first_name, last_name, phone_number, email)
        return jsonify({'message': 'Client added successfully', 'client': {
            'id': new_client.id,
            'firstName': new_client.firstName,
            'lastName': new_client.lastName,
            'phoneNumber': new_client.phoneNumber,
            'email': new_client.email
        }}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@front_end_bp.route('/clients', methods=['GET'])
def get_clients_route():
    try:
        clients = get_all_clients()
        return jsonify({'clients': clients}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500