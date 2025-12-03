from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, and_

from ..models.product import Product
from ..routes.auth import get_current_user
from ..schemas.auth import AuthUser
from ..schemas.product import CreateProduct, ReadProduct
from ..utilities.database import get_db_session
from ..utilities.helper import get_utc_now
from ..utilities.logger import get_logger

logger = get_logger(__name__)
product_router = APIRouter()


@product_router.post("/create", response_model=ReadProduct, status_code=201)
def create_product(
    product: CreateProduct,
    db_session: Session = Depends(get_db_session),
    current_user: AuthUser = Depends(get_current_user),
):
    try:
        logger.info(f"User : {current_user}")
        db_product = db_session.exec(
            select(Product).where(and_(Product.name == product.name))
        ).first()
        if db_product:
            detail = "Product already exists"
            logger.error(detail)
            raise HTTPException(status_code=409, detail=detail)

        now = get_utc_now()
        db_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            in_stock=product.in_stock,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        db_session.add(db_product)
        db_session.commit()

        return db_product

    except HTTPException as e:
        raise e
    except Exception:
        detail = "Failed to create product"
        logger.exception(detail)
        raise HTTPException(status_code=500, detail=detail)
