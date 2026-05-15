import os
import sqlite3
from sqlmodel import create_engine, Session, select

from backend.models.data_models import RegisteredCases, PublicSubmissions

sqlite_url = "sqlite:///config/sqlite_database.db"
engine = create_engine(sqlite_url)


def create_db():
    try:
        RegisteredCases.__table__.create(engine)
        PublicSubmissions.__table__.create(engine)
    except:
        pass
    # Add new columns to existing tables if they don't exist (SQLite migration)
    _migrate_db()


def _migrate_db():
    """Add any new columns to existing tables without dropping data."""
    new_columns = [
        ("registeredcases", "complainant_email", "TEXT"),
        ("registeredcases", "city", "TEXT"),
        ("registeredcases", "description", "TEXT"),
        ("publicsubmissions", "state", "TEXT"),
    ]
    try:
        con = sqlite3.connect("config/sqlite_database.db")
        cursor = con.cursor()
        for table, column, col_type in new_columns:
            try:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
            except sqlite3.OperationalError:
                pass  # Column already exists
        con.commit()
        con.close()
    except Exception:
        pass


def register_new_case(case_details: RegisteredCases):
    with Session(engine) as session:
        session.add(case_details)
        session.commit()


def fetch_registered_cases(submitted_by: str, status: str):
    print(f"submitted_by: {submitted_by}")
    if status == "All":
        status = ["F", "NF"]
    elif status == "Found":
        status = ["F"]
    elif status == "Not Found":
        status = ["NF"]

    with Session(engine) as session:
        result = session.exec(
            select(
                RegisteredCases.id,
                RegisteredCases.name,
                RegisteredCases.age,
                RegisteredCases.status,
                RegisteredCases.last_seen,
                RegisteredCases.matched_with,
            )
            .where(RegisteredCases.submitted_by == submitted_by)
            .where(RegisteredCases.status.in_(status))
        ).all()
        return result


def fetch_public_cases(train_data: bool, status: str):
    if train_data:
        with Session(engine) as session:
            if status == "All":
                result = session.exec(
                    select(
                        PublicSubmissions.id,
                        PublicSubmissions.face_mesh,
                    )
                ).all()
            else:
                result = session.exec(
                    select(
                        PublicSubmissions.id,
                        PublicSubmissions.face_mesh,
                    ).where(PublicSubmissions.status == status)
                ).all()
            return result

    with Session(engine) as session:
        if status == "All":
            result = session.exec(
                select(PublicSubmissions)
            ).all()
        else:
            result = session.exec(
                select(PublicSubmissions).where(PublicSubmissions.status == status)
            ).all()
        return result


def get_not_confirmed_registered_cases(submitted_by: str):
    with Session(engine) as session:
        result = session.exec(
            select(RegisteredCases)
            .where(RegisteredCases.submitted_by == submitted_by)
            .where(RegisteredCases.status == "NF")
        ).all()
        return result


def get_all_registered_cases():
    """Get all registered cases regardless of who submitted them"""
    with Session(engine) as session:
        result = session.exec(
            select(RegisteredCases)
        ).all()
        return result


def get_training_data(submitted_by: str):
    with Session(engine) as session:
        result = session.exec(
            select(RegisteredCases.id, RegisteredCases.face_mesh)
            .where(RegisteredCases.submitted_by == submitted_by)
            .where(RegisteredCases.status == "NF")
        ).all()
        return result


def new_public_case(public_case_details: PublicSubmissions):
    with Session(engine) as session:
        session.add(public_case_details)
        session.commit()


def get_public_case_detail(case_id: str):
    with Session(engine) as session:
        result = session.exec(
            select(
                PublicSubmissions.name,
                PublicSubmissions.location,
                PublicSubmissions.submitted_by,
                PublicSubmissions.mobile,
                PublicSubmissions.email,
                PublicSubmissions.birth_marks,
                PublicSubmissions.city,
                PublicSubmissions.state,
            ).where(PublicSubmissions.id == case_id)
        ).all()
        return result


def get_registered_case_detail(case_id: str):
    with Session(engine) as session:
        result = session.exec(
            select(
                RegisteredCases.name,
                RegisteredCases.complainant_mobile,
                RegisteredCases.complainant_email,
                RegisteredCases.age,
                RegisteredCases.last_seen,
                RegisteredCases.birth_marks,
                RegisteredCases.complainant_name,
                RegisteredCases.city,
                RegisteredCases.state,
                RegisteredCases.description,
            ).where(RegisteredCases.id == case_id)
        ).all()
        return result


def list_public_cases():
    with Session(engine) as session:
        result = session.exec(select(PublicSubmissions)).all()
        return result


def update_found_status(register_case_id: str, public_case_id: str):
    with Session(engine) as session:
        registered_case_details = session.exec(
            select(RegisteredCases).where(RegisteredCases.id == str(register_case_id))
        ).one()
        registered_case_details.status = "F"
        registered_case_details.matched_with = str(public_case_id)

        public_case_details = session.exec(
            select(PublicSubmissions).where(PublicSubmissions.id == str(public_case_id))
        ).one()
        public_case_details.status = "F"

        session.add(registered_case_details)
        session.add(public_case_details)
        session.commit()


def get_registered_cases_count(submitted_by: str, status: str):
    with Session(engine) as session:
        result = session.exec(
            select(RegisteredCases)
            .where(RegisteredCases.submitted_by == submitted_by)
            .where(RegisteredCases.status == status)
        ).all()
        return result


def get_all_found_cases():
    """Get all found cases regardless of who submitted them"""
    with Session(engine) as session:
        result = session.exec(
            select(RegisteredCases).where(RegisteredCases.status == "F")
        ).all()
        return result


def get_all_not_found_cases():
    """Get all not found cases regardless of who submitted them"""
    with Session(engine) as session:
        result = session.exec(
            select(RegisteredCases).where(RegisteredCases.status == "NF")
        ).all()
        return result


def get_case_counts_by_city():
    """Return a dict mapping city -> {found: int, not_found: int}."""
    with Session(engine) as session:
        result = session.exec(
            select(RegisteredCases.city, RegisteredCases.status)
        ).all()
    counts = {}
    for city, status in result:
        if not city:
            city = "Unknown"
        if city not in counts:
            counts[city] = {"found": 0, "not_found": 0}
        if status == "F":
            counts[city]["found"] += 1
        else:
            counts[city]["not_found"] += 1
    return counts


def delete_registered_case(case_id: str):
    with Session(engine) as session:
        case = session.exec(
            select(RegisteredCases).where(RegisteredCases.id == case_id)
        ).one()
        session.delete(case)
        session.commit()
    # Remove image from disk
    image_path = f"./resources/{case_id}.jpg"
    if os.path.exists(image_path):
        os.remove(image_path)


def update_registered_case(case_id: str, fields: dict):
    with Session(engine) as session:
        case = session.exec(
            select(RegisteredCases).where(RegisteredCases.id == case_id)
        ).one()
        for key, value in fields.items():
            setattr(case, key, value)
        session.add(case)
        session.commit()


def update_public_submission(submission_id: str, fields: dict):
    with Session(engine) as session:
        submission = session.exec(
            select(PublicSubmissions).where(PublicSubmissions.id == submission_id)
        ).one()
        for key, value in fields.items():
            setattr(submission, key, value)
        session.add(submission)
        session.commit()


def delete_public_submission(submission_id: str):
    """Delete a public submission and its associated image file"""
    with Session(engine) as session:
        submission = session.exec(
            select(PublicSubmissions).where(PublicSubmissions.id == submission_id)
        ).one_or_none()
        
        if submission is None:
            raise ValueError(f"Submission with ID {submission_id} not found")
        
        session.delete(submission)
        session.commit()
    
    # Delete the associated image file if it exists
    image_path = f"./resources/{submission_id}.jpg"
    if os.path.exists(image_path):
        try:
            os.remove(image_path)
        except Exception as e:
            print(f"Warning: Could not delete image file {image_path}: {e}")


def reset_found_case(case_id: str):
    """Reset a found case back to Not Found status"""
    with Session(engine) as session:
        case = session.exec(
            select(RegisteredCases).where(RegisteredCases.id == case_id)
        ).one()
        case.status = "NF"
        case.matched_with = None  # Clear the match reference
        session.add(case)
        session.commit()


def reset_all_found_cases():
    """Reset all found cases back to Not Found status"""
    with Session(engine) as session:
        found_cases = session.exec(
            select(RegisteredCases).where(RegisteredCases.status == "F")
        ).all()
        
        for case in found_cases:
            case.status = "NF"
            case.matched_with = None  # Clear the match reference
            session.add(case)
        
        session.commit()
        return len(found_cases)  # Return number of cases reset
