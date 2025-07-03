from app.utils.database import Base, engine
from app.models.receipt_file import ReceiptFile
from app.models.receipt import Receipt

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created!")

if __name__ == "__main__":
    init_db()