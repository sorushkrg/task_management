from typing import List, Optional

from sqlalchemy import BigInteger, DateTime, ForeignKeyConstraint, PrimaryKeyConstraint, SmallInteger, String, Text, \
    UniqueConstraint, text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from flask_login import UserMixin


class Base(DeclarativeBase):
    pass


class Users(Base,UserMixin):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow, onupdate=datetime.utcnow)
    is_admin: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'))

    tasks: Mapped[List['Tasks']] = relationship('Tasks', back_populates='user')


class Tasks(Base):
    __tablename__ = 'tasks'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='fk_tasks_user'),
        PrimaryKeyConstraint('id', name='tasks_pkey')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow, onupdate=datetime.utcnow)
    status: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'))
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime)

    user: Mapped['Users'] = relationship('Users', back_populates='tasks')
    files: Mapped[List['Files']] = relationship('Files', back_populates='task')


class Files(Base):
    __tablename__ = 'files'
    __table_args__ = (
        ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE', name='fk_files_task'),
        PrimaryKeyConstraint('id', name='files_pkey')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    task_id: Mapped[int] = mapped_column(BigInteger)
    file_path: Mapped[str] = mapped_column(String(255))
    original_name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)

    task: Mapped['Tasks'] = relationship('Tasks', back_populates='files')
