from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""
解决AttributeError: module 'bcrypt' has no attribute '__about__' with new 4.1.1 version
https://github.com/pyca/bcrypt/issues/684
pip install bcrypt==4.0.1
"""


class PasslibHelper:

    # plain_password 明文密码，hashed_password哈希密码
    @staticmethod
    def verity_password(plain_password: str, hashed_password: str):
        """对密码进行校验"""
        return pwd_context.verify(plain_password, hashed_password)

    # 进行哈希 密码加密
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)


if __name__ == "__main__":
    print(PasslibHelper.hash_password("123456"))
