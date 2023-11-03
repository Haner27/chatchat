from pydantic import BaseModel
from databases import Database

DATABASE_URL = "sqlite:///./user.db"
database = Database(DATABASE_URL)


class ChatLog(BaseModel):
    user_key: str
    request: str
    response: str


# Initialize the database
def initdb():
    database.connect()
    query = """
    CREATE TABLE IF NOT EXISTS chat_logs (
        id INTEGER PRIMARY KEY,
        user_key TEXT NOT NULL,
        request TEXT NOT NULL,
        response TEXT NOT NULL
    )
    """
    database.execute(query=query)


def save_chat_log(chat_log: ChatLog, user_key: str):
    query = "INSERT INTO chat_logs(user_key, request, response) VALUES (:user_key, :request, :response)"
    database.execute(query=query, values=chat_log.dict())
    return {"message": "Chat log saved successfully"}
