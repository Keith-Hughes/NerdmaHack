from .models import db, Client

def add_client(first_name, last_name, phone_number, email):
    new_client = Client(
        firstName=first_name,
        lastName=last_name,
        phoneNumber=phone_number,
        email=email
    )
    db.session.add(new_client)
    db.session.commit()
    return new_client

def email_exists(email):
    return db.session.query(Client.id).filter(Client.email.ilike(email)).scalar() is not None

def get_all_clients():
    clients = Client.query.all()

    return [{'firstName': client.firstName,
             'lastName': client.lastName,
             'phoneNumber': client.phoneNumber,
             'email': client.email} for client in clients]

def get_client_by_email(email):
    return Client.query.filter_by(email=email).first()