from intel_hub.db.seed.ai_ml_seed import seed_ai_ml_data
from intel_hub.db.seed.crypto_seed import seed_crypto_data
from intel_hub.db.session import SessionLocal

if __name__ == "__main__":
    with SessionLocal() as db:
        seed_crypto_data(db)
        seed_ai_ml_data(db)
        print("seed completed")
