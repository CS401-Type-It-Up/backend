import uuid

def generate_uuid():
    """
    Generate unique uuid for the user
    """
    unique_id = uuid.uuid4()
    unique_id_str = str(unique_id)
