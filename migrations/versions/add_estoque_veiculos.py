"""
Migration: Cria tabela estoque_veiculos para controlar quantidade de veículos por loja
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'add_estoque_veiculos'
down_revision = 'e5f6a7b8c9d0'
branch_labels = None
depends_on = None

def upgrade():
    # Adicionar EM_USO ao enum status_veiculo (se não existir)
    op.execute("ALTER TYPE status_veiculo ADD VALUE IF NOT EXISTS 'EM_USO'")
    existing_enum = postgresql.ENUM(
        'DISPONIVEL', 'ALUGADO', 'RESERVADO', 'MANUTENCAO', 'FORA_AREA', 'EM_USO',
        name='status_veiculo', create_type=False
    )
    op.create_table(
        'estoque_veiculos',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('veiculo_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('veiculos.id'), nullable=False),
        sa.Column('loja_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('lojas.id'), nullable=False),
        sa.Column('quantidade', sa.Integer(), nullable=False, default=1),
        sa.Column('status', existing_enum, nullable=False, server_default='DISPONIVEL'),
        sa.Column('criado_em', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('atualizado_em', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )
    # Remover loja_id de veiculos
    op.drop_column('veiculos', 'loja_id')

def downgrade():
    op.add_column('veiculos', sa.Column('loja_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('lojas.id'), nullable=True))
    op.drop_table('estoque_veiculos')
    # Não é possível remover valor do enum em PostgreSQL facilmente
