from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from src.database.models import Contact
from src.schemas import ContactSchema, ContactEmailModel


async def get_contacts(db: Session):
    contacts = db.query(Contact).all()
    return contacts


async def get_contact(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def create_contact(body: ContactSchema, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(body: ContactSchema, contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.born_date = body.born_date
        contact.description = body.description
        db.commit()
    return contact


async def update_contact_email(body: ContactEmailModel, contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        contact.email = body.email
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contact(db: Session, q: str, skip: int, limit: int):
    query = db.query(Contact)
    if q:
        query = query.filter(
            or_(
                Contact.first_name.ilike(f"%{q}%"),
                Contact.last_name.ilike(f"%{q}%"),
                Contact.email.ilike(f"%{q}%"),
            )
        )
    contacts = query.offset(skip).limit(limit)
    return contacts


async def birthdays_per_week(db: Session, days: int, skip: int, limit: int):
    today = datetime.now().date()
    date_to = today + timedelta(days=days)

    upcoming_birthdays_filter = (func.to_char(Contact.born_date, "MM-DD") >= today.strftime("%m-%d")) & (
            func.to_char(Contact.born_date, "MM-DD") <= date_to.strftime("%m-%d"))

    birthday_contacts = (
        db.query(Contact)
        .filter(upcoming_birthdays_filter)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return birthday_contacts