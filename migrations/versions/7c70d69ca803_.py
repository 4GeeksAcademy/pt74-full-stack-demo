"""empty message

Revision ID: 7c70d69ca803
Revises: 65dbb0096576
Create Date: 2025-02-07 23:16:10.305988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c70d69ca803'
down_revision = '65dbb0096576'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('author',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('isbn10', sa.String(length=32), nullable=True),
    sa.Column('isbn13', sa.String(length=32), nullable=True),
    sa.Column('cover', sa.String(length=256), nullable=True),
    sa.Column('have_read', sa.Boolean(), nullable=True),
    sa.Column('is_awesome', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('isbn10'),
    sa.UniqueConstraint('isbn13')
    )
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key')
    )
    op.drop_table('book')
    op.drop_table('author')
    # ### end Alembic commands ###
