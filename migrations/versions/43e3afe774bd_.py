"""empty message

Revision ID: 43e3afe774bd
Revises: f56de57aee37
Create Date: 2023-07-10 17:24:52.551577

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '43e3afe774bd'
down_revision = 'f56de57aee37'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pay_email', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('pay_refno', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('pay_fullname', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('pay_status', sa.Enum('pending', 'failed', 'paid'), server_default='pending', nullable=False))
        batch_op.drop_column('payment_status')

    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rev_subid', sa.Integer(), nullable=False))
        batch_op.drop_constraint('reviews_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'subscribers', ['rev_subid'], ['sub_id'])
        batch_op.drop_column('rev_userid')

    with op.batch_alter_table('subscribers', schema=None) as batch_op:
        batch_op.alter_column('sub_phone',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subscribers', schema=None) as batch_op:
        batch_op.alter_column('sub_phone',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)

    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rev_userid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('reviews_ibfk_1', 'subscribers', ['rev_userid'], ['sub_id'])
        batch_op.drop_column('rev_subid')

    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payment_status', mysql.ENUM('pending', 'failed', 'paid'), server_default=sa.text("'pending'"), nullable=False))
        batch_op.drop_column('pay_status')
        batch_op.drop_column('pay_fullname')
        batch_op.drop_column('pay_refno')
        batch_op.drop_column('pay_email')

    # ### end Alembic commands ###
