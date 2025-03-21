from sqlalchemy import String, Text, Index
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

class Base(DeclarativeBase):
    pass


class CandidateModel(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    skills: Mapped[str] = mapped_column(Text)
    experience: Mapped[str] = mapped_column(String(255))
    source: Mapped[str] = mapped_column(String(255), default="dou.ua")


    __table_args__ = (
        Index('idx_name', 'name'),
        Index('idx_skills', 'skills'),
        Index('idx_experience', 'experience')
    )
