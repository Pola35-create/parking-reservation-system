from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.person import Person
from app.schemas.person import PersonCreate, PersonResponse


router = APIRouter(
    prefix="/persons",
    tags=["Persons"]
)


@router.post(
    "",
    response_model=PersonResponse,
    status_code=201
)
def create_person(
    person: PersonCreate,
    db: Session = Depends(get_db)
):
    existing_email = db.query(Person).filter(
        Person.email == person.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=409,
            detail="This email already exists"
        )
    
    new_person = Person(
        name=person.name,
        email=person.email,
        can_use_electric=person.can_use_electric,
        can_use_accessible=person.can_use_accessible,
        can_use_dedicated=person.can_use_dedicated
    )

    db.add(new_person)
    db.commit()
    db.refresh(new_person)

    return new_person


@router.get(
    "",
    response_model=list[PersonResponse]
)
def get_persons(
    db: Session = Depends(get_db)
):
    return db.query(Person).all()