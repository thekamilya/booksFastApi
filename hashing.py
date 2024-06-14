from passlib.context import CryptContext

pxd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
class Hash:
    def bcrypt(password:str):
        return pxd_ctx.hash(password)

    def verify(hashed:str, plain:str):
        return pxd_ctx.verify(plain, hashed)
