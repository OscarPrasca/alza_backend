from sqlalchemy.orm import Session
from app.models.tag_model import Tag
from app.serializers.tag_serializer import TagCreateSerializer, TagUpdateSerializer
from app.permissions.ownership import check_ownership
from app.utils.exceptions import not_found_exception

def get_all_tags(db: Session, user_id: str):
    return db.query(Tag).filter(Tag.user_id == user_id).all()

def get_tag_by_id(db: Session, tag_id: str, user_id: str):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        not_found_exception("Tag")
    check_ownership(tag.user_id, user_id)
    return tag

def create_tag(db: Session, data: TagCreateSerializer, user_id: str):
    tag = Tag(
        user_id=user_id,
        name=data.name
    )
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

def update_tag(db: Session, tag_id: str, data: TagUpdateSerializer, user_id: str):
    tag = get_tag_by_id(db, tag_id, user_id)
    if data.name is not None:
        tag.name = data.name
    db.commit()
    db.refresh(tag)
    return tag

def delete_tag(db: Session, tag_id: str, user_id: str):
    tag = get_tag_by_id(db, tag_id, user_id)
    db.delete(tag)
    db.commit()
    return True