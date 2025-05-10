from configuracion import SessionLocal
from modelos.usuario import Usuario
from passlib.context import CryptContext

# Configuración de bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Datos para probar
correo_prueba = "cesar@empresa.com"
contrasena_prueba = "admin123"

def test_autenticacion():
    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter(Usuario.correo == correo_prueba).first()
        if not usuario:
            print("❌ Usuario no encontrado en la base de datos.")
        else:
            print(f"✅ Usuario encontrado: {usuario.nombre}")
            if pwd_context.verify(contrasena_prueba, usuario.contrasena):
                print("🔐 Contraseña verificada correctamente.")
            else:
                print("❌ La contraseña es incorrecta.")
    except Exception as e:
        print("⚠️ Error al conectar o consultar:", e)
    finally:
        db.close()

if __name__ == "__main__":
    test_autenticacion()
