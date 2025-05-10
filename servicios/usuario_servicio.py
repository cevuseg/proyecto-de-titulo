from modelos.usuario import Usuario
from modelos.rol import Rol
from configuracion import SessionLocal
from esquemas.usuario_schema import UsuarioCrear
from passlib.context import CryptContext
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def obtener_password_hash(password):
    return pwd_context.hash(password)
def autenticar_usuario(db: Session, correo: str, contrasena: str):
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if not usuario:
        print("❌ Usuario no encontrado")
        return False

    print("📧 Correo encontrado:", usuario.correo)
    print("🔐 Hash en la base:", usuario.contrasena)
    print("🔑 Contraseña ingresada:", contrasena)

    try:
        if not pwd_context.verify(contrasena, usuario.contrasena):
            print("❌ Contraseña incorrecta (bcrypt)")
            return False
    except Exception as e:
        print("⚠️ Error al verificar contraseña:", e)
        return False

    print("✅ Contraseña verificada correctamente")
    return usuario


def crear_usuario(db: Session, usuario: UsuarioCrear):
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        contrasena=obtener_password_hash(usuario.contrasena),
        id_rol=usuario.id_rol
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def obtener_usuarios(db: Session):
    return db.query(Usuario).all()

