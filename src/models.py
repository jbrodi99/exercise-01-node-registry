"""
SQLAlchemy model for the nodes table.

Table: nodes
- id: SERIAL PRIMARY KEY
- name: VARCHAR UNIQUE NOT NULL
- host: VARCHAR NOT NULL
- port: INTEGER NOT NULL
- status: VARCHAR DEFAULT 'active'
- created_at: TIMESTAMP DEFAULT NOW()
- updated_at: TIMESTAMP DEFAULT NOW()
"""

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, func
from src.database import Base
from datetime import datetime

class Node(Base):
    __tablename__ = "nodes"

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name : Mapped[str] = mapped_column(type_=String(30),unique=True,nullable=False)
    host : Mapped[str] = mapped_column(type_=String(255),nullable=False) #host: xxx.xxx.xxx.xxx
    port : Mapped[int] = mapped_column(type_=Integer,nullable=False) #port: xxxxx
    status : Mapped[str] = mapped_column(type_=String(10), default='active')
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), 
        onupdate=func.now()
    )
