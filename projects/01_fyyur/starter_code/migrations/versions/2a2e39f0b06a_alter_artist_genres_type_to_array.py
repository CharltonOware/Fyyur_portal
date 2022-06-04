"""alter artist genres type to array

Revision ID: 2a2e39f0b06a
Revises: c88f853a6c47
Create Date: 2022-06-04 14:14:16.417905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a2e39f0b06a'
down_revision = 'c88f853a6c47'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("COMMIT")
    op.execute('ALTER TABLE "Artist" ALTER COLUMN genres TYPE  character varying ARRAY USING genres::character varying[]')


def downgrade():
    pass
