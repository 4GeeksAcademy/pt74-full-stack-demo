"""empty message

Revision ID: 94b3454216f6
Revises: b82834113ee2
Create Date: 2025-02-13 01:48:53.438991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94b3454216f6'
down_revision = 'b82834113ee2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('author_to_book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_constraint('book_author_id_fkey', type_='foreignkey')
        batch_op.drop_column('author_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('book_author_id_fkey', 'author', ['author_id'], ['id'])

    op.drop_table('author_to_book')
    # ### end Alembic commands ###
