"""Default values for is_admin, is_supplier and is_customer in User model

Revision ID: 177b5c19cacb
Revises: 380c90c053de
Create Date: 2025-02-22 14:55:04.980470

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '177b5c19cacb'
down_revision: Union[str, None] = '380c90c053de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
