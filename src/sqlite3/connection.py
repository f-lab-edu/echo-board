from sqlmodel import Session, SQLModel, create_engine

sqlite_file_name = "echo_board.db"
DATABASE_URL = f"sqlite:///{sqlite_file_name}"

# TODO: 커넥션 풀에 대해 설명하기.
# TODO: create_engine의 주요 파라미터들에 대해 설명하기.
ENGINE = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={
        "check_same_thread": False,
    },
    pool_size=5,
    max_overflow=10,
)

SQLModel.metadata.create_all(ENGINE)


def init_db():
    SQLModel.metadata.create_all(ENGINE)


def get_session():
    with Session(ENGINE) as session:
        yield session
