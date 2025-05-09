"""Se agrega campo descripcion_respuesta al modelo presupuesto

Revision ID: 1d7c0a5b11e9
Revises: 42e246c4b780
Create Date: 2025-04-30 17:22:41.357783

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d7c0a5b11e9'
down_revision = '42e246c4b780'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('presupuesto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('descripcion_solicitud', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('descripcion_respuesta', sa.Text(), nullable=False))
        batch_op.drop_column('descripcion')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('presupuesto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('descripcion', sa.TEXT(), autoincrement=False, nullable=False))
        batch_op.drop_column('descripcion_respuesta')
        batch_op.drop_column('descripcion_solicitud')

    # ### end Alembic commands ###
