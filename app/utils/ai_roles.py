from enum import Enum


class Roles(Enum):
    DETERMINE_CRUD = "Determine what operation the user is requesting and Gather relavent information as per function to complete the users request. Always confirm details before calling function. If it doesn't fit in the function advise the user we do not support their request. use casual language"
