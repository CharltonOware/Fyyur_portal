"""empty message

Revision ID: 7e2d75423f9b
Revises: 7a3b13f8c0c5
Create Date: 2022-05-30 06:31:43.099674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e2d75423f9b'
down_revision = '7a3b13f8c0c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('website_link', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'website_link')
    # ### end Alembic commands ###