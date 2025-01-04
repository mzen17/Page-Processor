from app import fmodels
from sqlalchemy.orm import Session
import app.database.models as models

def create_page(data: fmodels.PageData, bucket_id: int, session: Session):
    if session:
        # No order sets it at -1.
        if not data.porder:
            data.porder = -1
        
        page = models.Page(title=data.title, description=data.content, owner_id=bucket_id, public = data.visibility, porder = -1)
        session.add(page)
        session.commit()
        session.refresh(page)
        return True
    return False


# Retrieves pages. Returns either a list of pages or none in case of non-existent user.
def get_pages(bucket_id: int, session: Session) -> list[models.Page]:
    if session:
        pages = session.query(models.Page).filter_by(owner_id = bucket_id).all()
        return pages
    return []


def get_page(bucket_id: int, page_id: int, session: Session) -> models.Page | None:
    """bucket_id is not used. Just throw random int (e.g, -1)
    This will be cleaned up later.
    """
    if session:
        target_page = session.query(models.Page).filter_by(id=page_id).first()
        return target_page
    return None


def update_page(data: fmodels.PageData, bucket_id: int, page_id: int, session: Session) -> bool:
    if session:
        target_page = session.query(models.Page).filter_by(owner_id=bucket_id).filter_by(id=page_id).first()
        if target_page:
            target_page.title = data.title
            target_page.description = data.content
            target_page.public = data.visibility

            if data.porder:
                target_page.porder = data.porder

            session.commit()
            return True
    return False

def delete_page(data: fmodels.PageData, bucket_id: int, page_id: int, session: Session) -> bool:
    if session:
        target_page = session.query(models.Page).filter_by(owner_id=bucket_id).filter_by(id=page_id)
        if target_page:
            target_page.delete()
            session.commit()
            return True
    return False
    