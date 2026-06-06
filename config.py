import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-study-tour-2024")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///study_tour.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
