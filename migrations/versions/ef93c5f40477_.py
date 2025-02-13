"""empty message

Revision ID: ef93c5f40477
Revises: 94b3454216f6
Create Date: 2025-02-13 01:58:18.497767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef93c5f40477'
down_revision = '94b3454216f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book_to_author',
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], )
    )
    op.drop_table('author_to_book')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('author_to_book',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('book_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], name='author_to_book_author_id_fkey'),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], name='author_to_book_book_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='author_to_book_pkey')
    )
    op.drop_table('book_to_author')
    # ### end Alembic commands ###
