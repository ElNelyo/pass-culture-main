"""Add table user_session

Revision ID: e51238ae21c5
Revises: 4fc1f5367b4c
Create Date: 2018-10-24 08:45:29.863564

"""
import sqlalchemy as sa
from alembic import op
# revision identifiers, used by Alembic.
from sqlalchemy.dialects.postgresql import UUID

revision = 'e51238ae21c5'
down_revision = '4fc1f5367b4c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_session',
        sa.Column('uuid', UUID(), unique=True, nullable=False),
        sa.Column('userId', sa.BigInteger, unique=True, nullable=False)
    )


def downgrade():
    op.drop_table('user_session')
