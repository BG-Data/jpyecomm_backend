from sqlalchemy.orm import Session


class database_sessions:

    def create_session(self, db: Session, db_action):
        try:
            db.add(db_action)
            db.commit()
            db.refresh(db_action)
            return db_action
        except Exception as e:
            db.rollback()
            raise e

    def update_session(self, db: Session, db_action):
        try:
            db.commit()
            db.flush()
            return db_action
        except Exception as e:
            db.rollback()
            raise e
    
    def delete_session(self, db: Session, db_action):
        try:
            db.delete(db_action)
            db.commit()
            return db_action
        except Exception as e:
            db.rollback()
            raise e