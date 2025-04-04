# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum, TIMESTAMP
# from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
# from passlib.context import CryptContext
# import datetime
# import jwt
# from pydantic import BaseModel, EmailStr  # ✅ Fix: Import BaseModel and EmailStr

# # ✅ MySQL Database Configuration
# DATABASE_URL = "mysql+pymysql://root:Pammu%401528@localhost/lms"

# # ✅ Create Database Engine
# engine = create_engine(DATABASE_URL, echo=True)

# # ✅ Create Session Factory
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # ✅ Declare Base for ORM Models
# Base = declarative_base()


# # ✅ Initialize FastAPI App
# app = FastAPI()

# # ✅ Password Hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # ✅ JWT Secret Key
# SECRET_KEY = "your_secret_key"
# ALGORITHM = "HS256"

# # ✅ User Model
# class User(Base):
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(50), unique=True, nullable=False)
#     first_name = Column(String(50))
#     last_name = Column(String(50))
#     email = Column(String(100), unique=True, nullable=False)
#     hashed_password = Column(String(255), nullable=False)
#     created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    
#     classrooms = relationship("UserClassroom", back_populates="user")

# # ✅ Classrooms Model
# class Classroom(Base):
#     __tablename__ = "classrooms"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), nullable=False)
#     created_by = Column(Integer, ForeignKey("users.id"))
#     created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

#     users = relationship("UserClassroom", back_populates="classroom")  # ✅ Fix: Add relationship

# # ✅ User-Classrooms Relationship Table
# class UserClassroom(Base):
#     __tablename__ = "user_classrooms"

#     user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
#     classroom_id = Column(Integer, ForeignKey("classrooms.id"), primary_key=True)
#     role = Column(Enum("teacher", "student"), nullable=False)

#     user = relationship("User", back_populates="classrooms")
#     classroom = relationship("Classroom", back_populates="users")  # ✅ Fix: Add relationship

# # ✅ Create Tables in MySQL
# Base.metadata.create_all(bind=engine)

# # ✅ Dependency: Get Database Session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # ✅ Hash Password
# def hash_password(password: str):
#     return pwd_context.hash(password)

# # ✅ Verify Password
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# # ✅ Create JWT Token
# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# # ✅ Signup Request Model
# class SignupRequest(BaseModel):
#     username: str
#     first_name: str
#     last_name: str
#     email: EmailStr
#     password: str

# # ✅ Login Request Model
# class LoginRequest(BaseModel):
#     email: EmailStr
#     password: str

# @app.post("/signup/")
# def signup(user_data: SignupRequest, db: Session = Depends(get_db)):
#     existing_user = db.query(User).filter(User.email == user_data.email).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     hashed_password = hash_password(user_data.password)
#     new_user = User(
#         username=user_data.username,
#         first_name=user_data.first_name,
#         last_name=user_data.last_name,
#         email=user_data.email,
#         hashed_password=hashed_password
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"message": "Account created successfully"}

# @app.post("/login/")
# def login(login_data: LoginRequest, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == login_data.email).first()
#     if not user or not verify_password(login_data.password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = create_access_token({"sub": user.email})
#     return {"token": token, "user_id": user.id, "username": user.username}
# from sqlalchemy import LargeBinary

# # ✅ File Model
# class File(Base):
#     __tablename__ = "files"

#     id = Column(Integer, primary_key=True, index=True)
#     filename = Column(String(255), nullable=False)
#     file_data = Column(LargeBinary, nullable=False)  # Store file as binary
#     uploaded_by = Column(Integer, ForeignKey("users.id"))
#     classroom_id = Column(Integer, ForeignKey("classrooms.id"))
#     uploaded_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

#     classroom = relationship("Classroom", back_populates="files")
#     uploader = relationship("User")
# Classroom.files = relationship("File", back_populates="classroom")
