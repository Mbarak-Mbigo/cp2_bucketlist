"""empty message

Revision ID: bce0a4b70a34
Revises: 
Create Date: 2017-04-19 00:50:14.331728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bce0a4b70a34'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bucketlist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=30), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('accomplished_date', sa.DateTime(), nullable=True),
    sa.Column('closed_date', sa.DateTime(), nullable=True),
    sa.Column('open_duration', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('bucket',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('accomplished_date', sa.DateTime(), nullable=True),
    sa.Column('closed_date', sa.DateTime(), nullable=True),
    sa.Column('open_duration', sa.Integer(), nullable=True),
    sa.Column('bucket_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['bucket_id'], ['bucketlist.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bucket')
    op.drop_table('user')
    op.drop_table('bucketlist')
    # ### end Alembic commands ###
