# to run coverage
# pytest --cov-report term-missing --cov=. from /app dir
import asyncio
import requests
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


#test static
def test_static():
    response = client.get("/")
    assert response.status_code == 200

    response = client.get("/css/index.css")
    assert response.status_code == 200

    response = client.get("/css/loader.css")
    assert response.status_code == 200

    response = client.get("/delete/")
    assert response.status_code == 200

    response = client.get("/html/login-form.html")
    assert response.status_code == 200

    response = client.get("/html/register-form.html")
    assert response.status_code == 200

    response = client.get("/html/user-page.html")
    assert response.status_code == 200

    response = client.get("/js/index.js")
    assert response.status_code == 200

    response = client.get("/js/login.js")
    assert response.status_code == 200

    response = client.get("/js/register.js")
    assert response.status_code == 200

    response = client.get("/js/delete.js")
    assert response.status_code == 200

    response = client.get("/js/rsa.js")
    assert response.status_code == 200

    response = client.get("/favicon.ico")
    assert response.status_code == 200
    
    response = requests.get("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css")
    assert response.status_code == 200

#test ru-static
def test_ru_static():
    response = client.get("/ru/")
    assert response.status_code == 200

    response = client.get("/ru/html/login-form.html")
    assert response.status_code == 200

    response = client.get("/ru/html/register-form.html")
    assert response.status_code == 200

    response = client.get("/ru/html/user-page.html")
    assert response.status_code == 200

    response = client.get("/ru/js/index.js")
    assert response.status_code == 200

    response = client.get("/ru/js/login.js")
    assert response.status_code == 200

    response = client.get("/ru/js/register.js")
    assert response.status_code == 200

    response = client.get("/ru/js/delete.js")
    assert response.status_code == 200

from dependencies import get_db, get_cookie, get_preferred_language

#test dependencies
def test_get_cookie():
    assert asyncio.run(
        get_cookie("cookies=abc; def=123", "cookies")
    ) == "abc"
    assert asyncio.run(
        get_cookie("cookies=abc; def=123", "def")
    ) == "123"
    assert asyncio.run(
        get_cookie("cookies=abc; def=123", "not")
    ) is None

def test_get_db():
    assert get_db()

def test_preffered_language():
    assert get_preferred_language('en-US,en;q=0.5') == 'en'
    assert get_preferred_language('ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3') == 'ru'
    assert get_preferred_language('') == 'en'
    assert get_preferred_language(None) == 'en'

#test crud
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from fastapi import Depends
from database import Base
from dependencies import get_db

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite://"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(
    class_= AsyncSession,
    expire_on_commit=False,
    bind=engine
)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())

async def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        await db.close()

app.dependency_overrides[get_db] = override_get_db

from cruds import user_crud
from schemas import user_schema as schema
from crypto.argon2 import check_user_password

async def crud_testing():
    try:
        db = TestingSessionLocal()
        assert await user_crud.create_user(db, schema.UserCreate(email="test", password="test"))
        
        user = await user_crud.get_user_by_email(db, "test")
        assert user is not None
        assert await check_user_password(user, "test")
        assert await check_user_password(user, "not_test") == False

        assert await user_crud.change_password(db, user, "new_test")
        assert await check_user_password(user, "new_test")
        assert await user_crud.delete_user(db, user)

        user = await user_crud.get_user_by_email(db, "test")
        assert user is None
    finally:
        await db.close()

def test_user_crud():
    asyncio.run(crud_testing())

#test crypto
import crypto

def test_argon2():
    password = "test"
    hashed_password = crypto.argon2.password_handler.hash(password)
    assert crypto.argon2.password_handler.verify(hashed_password, password)

def test_rsa():
    plaintext = "test"
    encrypted = asyncio.run(crypto.rsa.encrypt(plaintext))
    assert asyncio.run(crypto.rsa.decrypt(encrypted)) == plaintext
    assert asyncio.run(crypto.rsa.get_rsa_public_key())
    assert asyncio.run(crypto.rsa.get_rsa_private_key())

def test_jwtoken():
    user = {"email": "test"}
    token = asyncio.run(crypto.jwtoken.generate_access_token(user))
    assert asyncio.run(crypto.jwtoken.decrypt_token("not.token")) is None
    assert asyncio.run(crypto.jwtoken.decrypt_token("is.wrong.token")) is None
    payload = asyncio.run(crypto.jwtoken.decrypt_token(token))
    assert payload is not None
    assert payload['email'] == user['email']

#test schema
from schemas import user_schema as schema

def test_email_validation():
    assert schema.validate_email("test") == False
    assert schema.validate_email("test@") == False
    assert schema.validate_email("test@.com") == False
    assert schema.validate_email("test@.com.") == False
    assert schema.validate_email("test@.com.com") == True
    assert schema.validate_email("test@com") == False

def test_password_validation():
    assert schema.validate_password("test") == False
    assert schema.validate_password("test1234") == True
    #assert schema.validate_password("test1") == False
    #assert schema.validate_password("test1$") == False
    #assert schema.validate_password("Test1$") == True
    #assert schema.validate_password("Test") == False

#test /urers/ url
from routers import user
from dependencies import ACCESS_TOCKEN_NAME

cookies = {ACCESS_TOCKEN_NAME: asyncio.run(crypto.jwtoken.generate_access_token({"sub": "test@test.test"}))}

async def encrypt(plaintext):
    return await crypto.rsa.encrypt(plaintext)

def test_get_public_key():
    response = client.get("/user/public-key/")
    assert response.status_code == 200
    assert response.json().get("key")

from dependencies import get_error_detail, ru_error_detail, en_error_detail, get_user_by_token

def test_signup():
    password = "toshort"
    email = "wrongemail"
    response = client.post(
        "/user/signup/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "en"},
        json={"email": email, "password": password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == en_error_detail["invalid encryption"]

    email = asyncio.run(encrypt("wrongemail"))
    response = client.post(
        "/user/signup/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "en"},
        json={"email": email, "password": password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == en_error_detail["invalid email"]

    email = asyncio.run(encrypt("test@test.test"))
    response = client.post(
        "/user/signup/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "en"},
        json={"email": email, "password": password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == en_error_detail["invalid encryption"]

    password = asyncio.run(encrypt("toshort"))
    response = client.post(
        "/user/signup/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "en"},
        json={"email": email, "password": password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == en_error_detail["invalid password validation"]

    password = asyncio.run(encrypt("test1234"))
    response = client.post(
        "/user/signup/",
        headers={"X-Token": "coneofsilence"},
        json={"email": email, "password": password}
        )
    assert response.status_code == 201

    response = client.post(
        "/user/signup/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "en"},
        json={"email": email, "password": password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == en_error_detail["user already exists"]

def test_get_user_by_token():
    try:
        db = TestingSessionLocal()
        
        payload = {"sub":"test@test.test"}
        assert asyncio.run(get_user_by_token(db, payload))

        payload = {"sub":"not@test.email"}
        asyncio.run(get_user_by_token(db, payload))
    except Exception as e:
        assert e.status_code == 404
    finally:
        asyncio.run(db.close())

def test_module_test():
    client.cookies = cookies
    response = client.get(
        "/model/test/0.5",
        headers={"X-Token": "coneofsilence"},
        )
    assert response.status_code == 403#200
    #assert response.json().get("result")

    client.cookies = {}
    response = client.get(
        "/model/test/0.5",
        headers={"X-Token": "coneofsilence"},
        )
    assert response.status_code == 401

    response = client.post(
        "/model/test/0.5",
        headers={"X-Token": "coneofsilence"},
        json={"token": ""}
        )
    assert response.status_code == 401

    response = client.post(
        "/model/test/0.5",
        headers={"X-Token": "coneofsilence"},
        json={"token": cookies[ACCESS_TOCKEN_NAME]}
        )
    assert response.status_code == 403#200
    #assert response.json().get("result")

def test_login():
    client.cookies = {}
    response = client.get(
        "/user/login/",
        headers={"X-Token": "coneofsilence"},
        )
    assert response.status_code == 401

    client.cookies = {user.ACCESS_TOCKEN_NAME: asyncio.run(crypto.jwtoken.generate_access_token({"sub": "notuser"}))}
    response = client.get(
        "/user/login/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "ru"},
        )
    assert response.status_code == 404
    assert response.json().get("detail") == ru_error_detail["user not found"]

    client.cookies = cookies
    response = client.get(
        "/user/login/",
        headers={"X-Token": "coneofsilence"},
        )
    assert response.status_code == 200
    assert response.json().get("email")
    assert response.json().get("created_at")

def test_change_password():
    current_password = ""
    new_password = ""

    client.cookies = {}
    response = client.put(
        "/user/change-password/",
        headers={"X-Token": "coneofsilence"},
        json={"current_password": current_password,
            "new_password": new_password}
        )
    assert response.status_code == 401

    client.cookies = cookies
    response = client.put(
        "/user/change-password/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "ru"},
        json={"current_password": current_password,
            "new_password": new_password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == ru_error_detail["invalid encryption"]

    current_password = asyncio.run(encrypt("toshort"))
    response = client.put(
        "/user/change-password/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "ru"},
        json={"current_password": current_password, "new_password": new_password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == ru_error_detail["invalid password validation"]

    current_password = asyncio.run(encrypt("notpassword"))
    response = client.put(
        "/user/change-password/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "ru"},
        json={"current_password": current_password, "new_password": new_password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == ru_error_detail["invalid password"]

    current_password = asyncio.run(encrypt("test1234"))
    response = client.put(
        "/user/change-password/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "ru"},
        json={"current_password": current_password, "new_password": new_password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == ru_error_detail["invalid encryption"]

    new_password = asyncio.run(encrypt("toshort"))
    response = client.put(
        "/user/change-password/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "ru"},
        json={"current_password": current_password, "new_password": new_password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == ru_error_detail["invalid password validation"]

    new_password = asyncio.run(encrypt("test12345"))
    response = client.put(
        "/user/change-password/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "ru"},
        json={"current_password": current_password, "new_password": new_password}
        )
    assert response.status_code == 200

def test_web_token():
    password = "toshort"
    email = "wrongemail"
    response = client.post(
        "/user/web-token/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "ru"},
        json={"email": email, "password": password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == ru_error_detail["invalid encryption"]

    email = asyncio.run(encrypt("wrongemail"))
    response = client.post(
        "/user/web-token/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "ru"},
        json={"email": email, "password": password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == ru_error_detail["invalid email"]

    email = asyncio.run(encrypt("really@not.email"))
    response = client.post(
        "/user/web-token/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "ru"},
        json={"email": email, "password": password}
        )
    assert response.status_code == 404
    assert response.json().get("detail") == ru_error_detail["user not found"]

    email = asyncio.run(encrypt("test@test.test"))
    response = client.post(
        "/user/web-token/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "ru"},
        json={"email": email, "password": password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == ru_error_detail["invalid encryption"]

    password = asyncio.run(encrypt("toshort"))
    response = client.post(
        "/user/web-token/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "ru"},
        json={"email": email, "password": password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == ru_error_detail["invalid password validation"]

    password = asyncio.run(encrypt("wrong_password"))
    response = client.post(
        "/user/web-token/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "ru"},
        json={"email": email, "password": password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == ru_error_detail["invalid password"]

    password = asyncio.run(encrypt("test12345"))

    client.cookies = {}
    response = client.post(
        "/user/web-token/",
        headers={"X-Token": "coneofsilence"},
        json={"email": email, "password": password},
    )
    assert response.status_code == 200

def test_token():
    password = "toshort"
    email = "wrongemail"
    response = client.post(
        "/user/token/",
        headers={"X-Token": "coneofsilence"},
        json={"email": email, "password": password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == en_error_detail["invalid encryption"]

    email = asyncio.run(encrypt("wrongemail"))
    response = client.post(
        "/user/token/",
        headers={"X-Token": "coneofsilence"},
        json={"email": email, "password": password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == en_error_detail["invalid email"]

    email = asyncio.run(encrypt("really@not.email"))
    response = client.post(
        "/user/token/",
        headers={"X-Token": "coneofsilence"},
        json={"email": email, "password": password}
        )
    assert response.status_code == 404
    assert response.json().get("detail") == en_error_detail["user not found"]

    email = asyncio.run(encrypt("test@test.test"))
    response = client.post(
        "/user/token/",
        headers={"X-Token": "coneofsilence"},
        json={"email": email, "password": password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == en_error_detail["invalid encryption"]

    password = asyncio.run(encrypt("toshort"))
    response = client.post(
        "/user/token/",
        headers={"X-Token": "coneofsilence"},
        json={"email": email, "password": password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == en_error_detail["invalid password validation"]

    password = asyncio.run(encrypt("wrong_password"))
    response = client.post(
        "/user/token/",
        headers={"X-Token": "coneofsilence"},
        json={"email": email, "password": password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == en_error_detail["invalid password"]

    password = asyncio.run(encrypt("test12345"))

    client.cookies = {}
    response = client.post(
        "/user/token/",
        headers={"X-Token": "coneofsilence"},
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    assert response.json().get("token")

def test_logout():
    client.cookies = cookies
    response = client.get(
        "/user/logout/",
        headers={"X-Token": "coneofsilence"},
        )
    assert response.status_code == 200

def test_delete_user():
    password = ""

    client.cookies = {}
    response = client.post(
        "/user/delete/",
        headers={"X-Token": "coneofsilence"},
        json={"password": password}
        )
    assert response.status_code == 401

    client.cookies = {user.ACCESS_TOCKEN_NAME: asyncio.run(crypto.jwtoken.generate_access_token({"sub": "not@test.email"}))}
    response = client.post(
        "/user/delete/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "en"},
        json={"password": password}
        )
    assert response.status_code == 404
    assert response.json().get("detail") == en_error_detail["user not found"]

    client.cookies = cookies
    response = client.post(
        "/user/delete/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "en"},
        json={"password": password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == en_error_detail["invalid encryption"]

    password = asyncio.run(encrypt("toshort"))
    response = client.post(
        "/user/delete/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "en"},
        json={"password": password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == en_error_detail["invalid password validation"]

    password = asyncio.run(encrypt("notpassword"))
    response = client.post(
        "/user/delete/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "en"},
        json={"password": password}
        )
    assert response.status_code == 400
    assert response.json().get("detail") == en_error_detail["invalid password"]

    password = asyncio.run(encrypt("test12345"))
    response = client.post(
        "/user/delete/",
        headers={"X-Token": "coneofsilence"},
        json={"password": password}
        )
    assert response.status_code == 200

    response = client.post(
        "/user/delete/",
        headers={"X-Token": "coneofsilence",
                 "Accept-Language": "en"},
        json={"password": password}
        )
    assert response.status_code == 404
    assert response.json().get("detail") == en_error_detail["user not found"]
