from passlib.context import CryptContext

password_encoder = CryptContext(schemes=["bcrypt"], deprecated="auto");

def password_encode(password: str):
    return password_encoder.hash(password);

def verify(plain_password, hashed_password):
    return password_encoder.verify(plain_password, hashed_password);