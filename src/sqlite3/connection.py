from sqlmodel import Session, SQLModel, StaticPool, create_engine

from src.config import ServerConfig

config = ServerConfig()


if config.database_type == "sqlite":
    DATABASE_URL = "sqlite:///echo_board.db"
    pool_options = {
        "pool_size": 5,
        "max_overflow": 10,
    }
elif config.database_type == "in-memory":
    DATABASE_URL = "sqlite:///:memory:"
    pool_options = {"poolclass": StaticPool}

else:
    raise ValueError(f"database_type: {config.database_type}")


# TODO: 커넥션 풀에 대해 설명하기.
# TODO: create_engine의 주요 파라미터들에 대해 설명하기.
# TODO: 현재 주입받는 엔드포인트 함수들은 비동기(async)로 되어있는데, DB는 sync 엔진으로 되어 있음. 어떤 문제가 있는지 설명하고 적절하게 수정하기.
ENGINE = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
    **pool_options,
)


def init_db():
    SQLModel.metadata.create_all(ENGINE)


def get_session():
    with Session(ENGINE) as session:
        yield session
