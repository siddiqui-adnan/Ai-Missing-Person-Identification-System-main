import os
import json
import pickle
import traceback

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier

from backend.database import db_queries


def _get_db_row_count(submitted_by: str) -> int:
    """Return the number of NF registered cases (used for cache invalidation)."""
    try:
        from backend.database.db_queries import engine, RegisteredCases
        from sqlmodel import Session, select
        
        with Session(engine) as session:
            result = session.exec(
                select(RegisteredCases.id).where(RegisteredCases.status == "NF")
            ).all()
        return len(result)
    except Exception:
        return -1


def get_train_data(submitted_by: str):
    """
    Gets the training data for all registered cases (not just the current user).
    This ensures the model can match any registered case with public submissions.

    Args:
        submitted_by: str (kept for cache compatibility, but not used for filtering)
    """
    try:
        from backend.database.db_queries import engine, RegisteredCases
        from sqlmodel import Session, select
        
        with Session(engine) as session:
            result = session.exec(
                select(RegisteredCases.id, RegisteredCases.face_mesh)
                .where(RegisteredCases.status == "NF")
            ).all()
        
        if not result:
            return [], pd.DataFrame()

        d1 = pd.DataFrame(result, columns=["label", "face_mesh"])
        
        # Filter out records with empty or invalid face mesh data
        def parse_face_mesh(face_mesh_str):
            try:
                parsed = json.loads(face_mesh_str)
                # Check if parsed data is a non-empty list of numbers
                if isinstance(parsed, list) and len(parsed) > 0:
                    return parsed
                else:
                    return None
            except (json.JSONDecodeError, TypeError):
                return None
        
        d1["face_mesh"] = d1["face_mesh"].apply(parse_face_mesh)
        
        # Remove rows with None face_mesh (invalid/empty data)
        d1 = d1.dropna(subset=["face_mesh"])
        
        if len(d1) == 0:
            return [], pd.DataFrame()  # Return empty data if no valid face mesh records
        
        # Expand face mesh into separate columns
        face_mesh_data = d1["face_mesh"].tolist()
        d2 = pd.DataFrame(face_mesh_data, index=d1.index).rename(
            columns=lambda x: "fm_{}".format(x + 1)
        )
        df = pd.concat([d1["label"], d2], axis=1)
        
        # Ensure all columns except label are float
        for col in df.columns:
            if col != "label":
                df[col] = pd.to_numeric(df[col], errors="coerce")
        
        # Drop rows with NaN values in face mesh columns
        df = df.dropna()
        
        if len(df) == 0:
            return [], pd.DataFrame()
            
        return df["label"].tolist(), df.drop("label", axis=1)

    except Exception as e:
        traceback.print_exc()
        raise e


def train(submitted_by: str):
    """
    Trains a KNN Model on the submitted cases.
    Skips retraining if the DB row count hasn't changed since the last run.

    Args:
        submitted_by: str

    Returns:
        dict - {
            "status": bool - whether the functional call was successful or not
            "message": str - message returned on each case
        }
    """
    model_name = "config/classifier.pkl"
    cache_file = "config/classifier_cache.txt"

    current_count = _get_db_row_count(submitted_by)

    # Check cache: if row count matches and model file exists, skip retraining
    if os.path.isfile(model_name) and os.path.isfile(cache_file):
        try:
            with open(cache_file, "r") as f:
                cached = f.read().strip().split(":")
                cached_user = cached[0]
                cached_count = int(cached[1])
            if cached_user == submitted_by and cached_count == current_count:
                return {"status": True, "message": "Model up to date (cache hit)"}
        except Exception:
            pass  # Cache read failed — retrain

    # Remove stale model
    if os.path.isfile(model_name):
        os.remove(model_name)

    try:
        labels, key_pts = get_train_data(submitted_by)
        
        if len(labels) == 0 or key_pts.empty:
            return {"status": False, "message": "No valid face mesh data found. Please ensure cases have clear face photos."}
        
        le = LabelEncoder()
        encoded_labels = le.fit_transform(labels)
        
        # Use at most 3 neighbors, but not more than the number of samples
        n_neighbors = min(len(labels), 3)
        if n_neighbors < 1:
            return {"status": False, "message": "Need at least one registered case for training."}
            
        classifier = KNeighborsClassifier(
            n_neighbors=n_neighbors, algorithm="ball_tree", weights="distance"
        )
        classifier.fit(key_pts, encoded_labels)

        with open(model_name, "wb") as file:
            pickle.dump((le, classifier), file)

        # Save cache metadata
        with open(cache_file, "w") as f:
            f.write(f"{submitted_by}:{current_count}")

        return {"status": True, "message": "Model Refreshed"}
    except Exception as e:
        traceback.print_exc()
        return {"status": False, "message": str(e)}
