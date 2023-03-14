from datetime import datetime

from sqlalchemy import Column, Boolean, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from fastapi_file_server.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(30), unique=True, index=True)
    password = Column(String(128))
    name = Column(String(30), index=True)
    email = Column(String(50), unique=True, index=True)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    create_date = Column(DateTime(timezone=True), default=datetime.now)
    update_date = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, comment="오리지널 파일명")
    save_name = Column(String(255), index=True, comment="저장된 파일명")
    size = Column(Integer)
    is_active = Column(Boolean, default=False)
    create_date = Column(DateTime(timezone=True), default=datetime.now)
    update_date = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)