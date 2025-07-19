import os
import sys
from alembic.config import Config
from alembic import command

# 設定 Alembic 配置
alembic_cfg = Config(alembic.ini)

# 產生 migration
command.revision(alembic_cfg, autogenerate=True, message="create test tables")

print(Migration 檔案已產生完成！") 