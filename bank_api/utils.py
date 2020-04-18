from uuid import uuid4

def generate_random_account_number() -> str:
    """Generate a pseudo random number from uuid4, trucated to 20 digits"""
    return str(uuid4().int)[0:20]