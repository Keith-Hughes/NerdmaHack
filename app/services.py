from .models import db, Client, Project

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

def get_client_by_number(phoneNumber):
    return Client.query.filter_by(phoneNumber=phoneNumber).first()

def get_client_by_project_name(project_name):
    # Query the project by name
    project = Project.query.filter_by(projectName=project_name).first()
    
    if project:
        # Get the client associated with the project
        client = Client.query.get(project.clientID)
        if client:
            # Return client details as a dictionary
            return {
                "projectId": project.id,
                "firstName": client.firstName,
                "lastName": client.lastName,
                "phoneNumber": client.phoneNumber,
                "email": client.email
            }
        else:
            return {"error": "Client not found for the project"}
    else:
        return {"error": "Project not found"}