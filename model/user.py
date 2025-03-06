from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
from datetime import datetime, timedelta
from enum import Enum as PyEnum

Base = declarative_base()

class SubscriptionPlanType(PyEnum):
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    BUSINESS = "business"
    PAY_AS_YOU_GO = "pay_as_you_go"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    clerkId = Column(String, unique=True)
    username = Column(String, unique=True, nullable=False)
    pic = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_type = Column(Enum(SubscriptionPlanType), nullable=False)
    max_conversions_per_month = Column(Integer, default=5)  # Free plan limit
    ai_editor_enabled = Column(Boolean, default=False)
    watermark_enabled = Column(Boolean, default=True)
    allow_download = Column(Boolean, default=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=30))
