from sqlalchemy.orm import Session
from app.models.category_model import Category
from app.serializers.category_serializer import CategoryCreateSerializer, CategoryUpdateSerializer
from app.permissions.ownership import check_ownership
from app.utils.exceptions import not_found_exception

def get_all_categories(db: Session, user_id: str):
    return db.query(Category).filter(Category.user_id == user_id).all()

def get_category_by_id(db: Session, category_id: str, user_id: str):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        not_found_exception("Categoría")
    check_ownership(category.user_id, user_id)
    return category

def create_category(db: Session, data: CategoryCreateSerializer, user_id: str):
    category = Category(
        user_id=user_id,
        name=data.name
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def update_category(db: Session, category_id: str, data: CategoryUpdateSerializer, user_id: str):
    category = get_category_by_id(db, category_id, user_id)
    if data.name is not None:
        category.name = data.name
    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, category_id: str, user_id: str):
    category = get_category_by_id(db, category_id, user_id)
    db.delete(category)
    db.commit()
    return True