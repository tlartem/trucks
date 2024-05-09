"""empty message

Revision ID: 6ea1f424410e
Revises: 
Create Date: 2024-05-08 23:35:07.462727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '6ea1f424410e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('car',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('car_number', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('car_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('payload', sa.Float(), nullable=False),
    sa.Column('length', sa.Float(), nullable=False),
    sa.Column('width', sa.Float(), nullable=False),
    sa.Column('height', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('car')
    # ### end Alembic commands ###