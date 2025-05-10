from passlib.context import CryptContext

# Crear contexto de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Generar hash de una contraseña de ejemplo
hash = pwd_context.hash("admin123")

# Mostrar resultado
print("Hash generado:", hash)
