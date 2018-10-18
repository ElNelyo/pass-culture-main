"""Rename column in Payment table and add another one

Revision ID: d176385d379e
Revises: e0e5b8f53afd
Create Date: 2018-10-18 14:23:53.562424

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'd176385d379e'
down_revision = 'e0e5b8f53afd'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('payment', 'paymentTransactionId', new_column_name='transactionMessageId')
    op.add_column('payment', sa.Column('transactionPaymentInfoId', sa.VARCHAR(50), nullable=True))


def downgrade():
    op.drop_column('payment', 'transactionPaymentInfoId')
    op.alter_column('payment', 'transactionMessageId', new_column_name='paymentTransactionId')
