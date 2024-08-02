from enum import Enum


class ReadTools(Enum):
    DETERMINE_CRUD = {
        "type": "function",
        "function": {
            "name": "determine_crud",
            "description": "Determing which CRUD operation the user is requesting",
            "parameters": {
                "type": "object",
                "properties": {
                    "is_crud": {
                        "type": "boolean",
                        "description": "Does the user request specify a crud operation?",
                    },
                    "requested_operation": {
                        "type": "string",
                        "enum": [
                            "GET_CLIENT_INFO",
                            "GET_SALES_REPORT",
                            "GET_INVENTORY_REPORT",
                            "UPDATE_CLIENT_INFO",
                            "UPDATE_INVENTORY",
                            "ADD_CLIENT",
                            "ADD_TO_INVENTORY",
                            "DELETE_CLIENT",
                            "DELETE_INVENTORY",
                        ]
                    }
                },
                "required": ["contact_number"],
            },
        }
    }
    GET_CLIENT_INFO = {
        "type": "function",
        "function": {
            "name": "get_client_info",
            "description": "Get a clients information for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "contact_number": {
                        "type": "string",
                        "description": "Contact number for the client which will be used to search a database for the clients details",
                    },
                },
                "required": ["contact_number"],
            },
        }
    }
    GET_ALL_CLIENTS = {
        "type": "function",
        "function": {
            "name": "get_all_clients",
            "description": "retrieve all clients currently on the system if the user requests it",
            "parameters": {
                "type": "object",
                "properties": {
                    "is_request_all": {
                        "type": "boolean",
                        "description": "Is the user requesting all clients or just one",
                    }
                }
            }
        }
    }
    GET_SALES_REPORT = {
        "type": "function",
        "function": {
            "name": "get_sales_report",
            "description": "retriev sales report for the requested date range, todays date is {date_placeholder} (YYYY-MM-DD)",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "the start date for when the sales report must be retrieved in format YYYY-MM-DD",
                    },
                    "end_date": {
                        "type": "string",
                        "description": "the end date for when the sales report must be retrieved in format YYYY-MM-DD",
                    },
                    "requires_pdf": {
                        "type": "boolean",
                        "description": "does the user want a pdf document of the sales report or just sent in chat?",
                    }
                },
                "required": ["start_date", "end_date", "requires_pdf"]
            },
        }
    }
    GET_INVENTORY_REPORT = {
        "type": "function",
        "function": {
            "name": "get_inventory_report",
            "description": "retrieve current invetory levels from database",
            "parameters": {
                "type": "object",
                "properties": {
                    "requires_pdf": {
                        "type": "boolean",
                        "description": "does the user want a pdf document of the inventory report or just sent in chat?",
                    }
                },
                "required": ["requires_pdf"]
            },
        }
    }


class UpdateTools(Enum):
    UPDATE_CLIENT_INFO = {
        "type": "function",
        "function": {
            "name": "update_client_info",
            "description": "update client information for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "contact_number": {
                        "type": "string",
                        "description": "Contact number for the client which will be updated",
                    },
                    "update_first_name": {
                        "type": "boolean",
                        "description": "does the user want to update the clients first name",
                    },
                    "update_last_name": {
                        "type": "boolean",
                        "description": "does the user want to update the clients last name",
                    },
                    "update_email": {
                        "type": "boolean",
                        "description": "does the user want to update the clients email",
                    },
                    "new_first_name": {
                        "type": "string",
                        "description": "the clients new first name that will be updated if applicable",
                    },
                    "new_last_name": {
                        "type": "string",
                        "description": "the clients new last name that will be updated if applicable",
                    },
                    "new_email": {
                        "type": "string",
                        "description": "the clients email that will be updated if applicable",
                    },
                },
                "required": ["contact_number"],
            },
        }
    }
    UPDATE_INVETORY = {
        "type": "function",
        "function": {
            "name": "update_inventory",
            "description": "update inventory for a particular existing product",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_to_update": {
                        "type": "string",
                        "enum": [
                            "{product_list_placeholder}"
                        ],
                        "description": "the product that the user wants to update",
                    },
                    "update_product_name": {
                        "type": "boolean",
                        "description": "does the user request a product name update",
                    },
                    "update_quantity": {
                        "type": "boolean",
                        "description": "does the user request a product quantity update",
                    },
                    "update_cost_price": {
                        "type": "boolean",
                        "description": "does the user request a product cost price update",
                    },
                    "new_quantity": {
                        "type": "integer",
                        "description": "new quantity to be updated if applicable",
                    },
                    "new_cost_price": {
                        "type": "integer",
                        "description": "new cost_price to be updated if applicable",
                    },
                    "new_product_name": {
                        "type": "string",
                        "description": "new cost_price to be updated if applicable",
                    },
                },
                "required": ["product_to_update"]
            },
        }
    }


class CreateTools(Enum):
    ADD_CLIENT = {
        "type": "function",
        "function": {
            "name": "add_client",
            "description": "add a new client to the database",
            "parameters": {
                "type": "object",
                "properties": {
                    "contact_number": {
                        "type": "string",
                        "description": "Contact number for the client which will be added to a database",
                    },
                    "email": {
                        "type": "string",
                        "description": "email address for the client which will be added to a database",
                    },
                    "first_name": {
                        "type": "string",
                        "description": "first name of the client which will be added to a database",
                    },
                    "last_name": {
                        "type": "string",
                        "description": "last name of the client which will be added to a database",
                    },
                },
                "required": ["contact_number", "email", "first_name", "last_name" ],
            },
        }
    }
    ADD_TO_INVENTORY = {
        "type": "function",
        "function": {
            "name": "add_to_inventory",
            "description": "add new products to the database",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "the name of the product",
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "the number of products to be added",
                    },
                    "cost_price": {
                        "type": "integer",
                        "description": "how much each product costs",
                    },
                },
                "required": ["product_name", "quantity", "cost_price"]
            },
        }
    }
    SEND_EMAIL = {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "send an email message to a recipient",
            "parameters": {
                "type": "object",
                "properties": {
                    "email_address": {
                        "type": "string",
                        "description": "The recipients email address",
                    },
                    "message": {
                        "type": "string",
                        "description": "message to send the recipient",
                    },
                    "subject": {
                        "type": "string",
                        "description": "the subject of the email",
                    },
                },
                "required": ["email_address", "message", "subject"],
            },
        }
    }


class DeleteTools(Enum):
    DELETE_CLIENT = {
        "type": "function",
        "function": {
            "name": "delete_client",
            "description": "delete a client from the database",
            "parameters": {
                "type": "object",
                "properties": {
                    "contact_number": {
                        "type": "string",
                        "description": "Contact number for the client which will be added to a database",
                    },
                },
                "required": ["contact_number"],
            },
        }
    }
    DELETE_INVENTORY = {
        "type": "function",
        "function": {
            "name": "delete_inventory",
            "description": "delete a product from the database",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_to_delete": {
                        "type": "string",
                        "enum": [
                            "{product_list_placeholder}"
                        ],
                        "description": "the product that the user wants to delete from the database",
                    },
                },
                "required": ["product_to_delete"],
            },
        }
    }
# Accessing the enum values
OperationMap= {
    "GET_CLIENT_INFO": ReadTools.GET_CLIENT_INFO.value,
    "GET_SALES_REPORT": ReadTools.GET_SALES_REPORT.value,
    "GET_INVENTORY_REPORT": ReadTools.GET_INVENTORY_REPORT.value,
    "UPDATE_CLIENT_INFO": UpdateTools.UPDATE_CLIENT_INFO.value,
    "UPDATE_INVENTORY": UpdateTools.UPDATE_INVETORY.value,
    "ADD_CLIENT": CreateTools.ADD_CLIENT.value,
    "ADD_TO_INVENTORY": CreateTools.ADD_TO_INVENTORY.value,
    "DELETE_CLIENT": DeleteTools.DELETE_CLIENT.value,
    "DELETE_INVENTORY": DeleteTools.DELETE_INVENTORY.value,
    }

all_functions= [
    CreateTools.SEND_EMAIL.value,
    ReadTools.DETERMINE_CRUD.value,
    ReadTools.GET_CLIENT_INFO.value,
    ReadTools.GET_INVENTORY_REPORT.value,
    ReadTools.GET_SALES_REPORT.value,
    UpdateTools.UPDATE_CLIENT_INFO.value,
    UpdateTools.UPDATE_INVETORY.value,
    CreateTools.ADD_CLIENT.value,
    CreateTools.ADD_TO_INVENTORY.value,
    DeleteTools.DELETE_CLIENT.value,
    DeleteTools.DELETE_INVENTORY.value,
    ReadTools.GET_ALL_CLIENTS.value,
]

