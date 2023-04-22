from typing import TYPE_CHECKING, Any, Dict, Optional

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .. import metadata

if TYPE_CHECKING:
    from .alias import AliasTable
    from .command import CommandTable
    from .user import UserTable


class PermissionGroupTable(metadata.Base):
    __tablename__ = "permission_group"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    created_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=False)
    updated_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "created_on": self.created_on,
            "updated_on": self.updated_on,
        }

    def __repr__(self) -> str:
        return f"PermissionGroup(id={self.id!r}, name={self.name!r}, created_on={self.created_on!r}, updated_on={self.updated_on!r})"
