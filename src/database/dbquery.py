from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "Componentes"
    item_id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column()
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

# class Address(Base):
#     __tablename__ = "address"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email_address: Mapped[str]
#     user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
#     user: Mapped["User"] = relationship(back_populates="addresses")
#     def __repr__(self) -> str:
        # return f"Address(id={self.id!r}, email_address={self.email_address!r})"
        

engine = create_engine('sqlite:///database//PCdb.sqlite3', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()




with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())

# stmt = select("Component").where("Component".c.name == "spongebob")
# print(stmt)

# with Session(engine) as session:
#     spongebob = User(
#         name="spongebob",
#         fullname="Spongebob Squarepants",
#         addresses=[Address(email_address="spongebob@sqlalchemy.org")],
#     )
#     sandy = User(
#         name="sandy",
#         fullname="Sandy Cheeks",
#         addresses=[
#             Address(email_address="sandy@sqlalchemy.org"),
#             Address(email_address="sandy@squirrelpower.org"),
#         ],
#     )
#     patrick = User(name="patrick", fullname="Patrick Star")
#     session.add_all([spongebob, sandy, patrick])
#     session.commit()

# class DBQuery():
#     def __init__(self, database="PCdb.sqlite3") -> None:        
#         try:
#             self.conexion = sqlite3.connect(database=database)
#             self.cursor = self.conexion.cursor()
#             self.cursor.execute("")
#         except Exception as ex:
#             print(ex)