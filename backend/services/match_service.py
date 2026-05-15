import json
import traceback
import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.neighbors import KNeighborsClassifier

from backend.database import db_queries


def get_public_cases_data(status="NF"):
    try:
        result = db_queries.fetch_public_cases(train_data=True, status=status)
        if not result:
            return pd.DataFrame()
            
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
            return pd.DataFrame()  # Return empty DataFrame if no valid face mesh records
        
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
        return df

    except Exception as e:
        traceback.print_exc()
        return pd.DataFrame()


def get_registered_cases_data(status="NF"):
    try:
        from backend.database.db_queries import engine, RegisteredCases
        from sqlmodel import Session, select

        with Session(engine) as session:
            result = session.exec(
                select(
                    RegisteredCases.id,
                    RegisteredCases.face_mesh,
                    RegisteredCases.status,
                )
            ).all()
            
            if not result:
                return pd.DataFrame()
                
            d1 = pd.DataFrame(result, columns=["label", "face_mesh", "status"])
            if status:
                d1 = d1[d1["status"] == status]
            
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
                return pd.DataFrame()  # Return empty DataFrame if no valid face mesh records
            
            # Expand face mesh into separate columns
            face_mesh_data = d1["face_mesh"].tolist()
            d2 = pd.DataFrame(face_mesh_data, index=d1.index).rename(
                columns=lambda x: "fm_{}".format(x + 1)
            )
            df = pd.concat([d1[["label", "status"]], d2], axis=1)
            
            # Ensure all columns except label and status are float
            for col in df.columns:
                if col not in ["label", "status"]:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
            
            # Drop rows with NaN values in face mesh columns
            df = df.dropna()
            return df
    except Exception as e:
        traceback.print_exc()
        return pd.DataFrame()


def match(distance_threshold=3):
    matched_images = defaultdict(list)
    match_details = []  # Store detailed match information
    
    public_cases_df = get_public_cases_data()
    registered_cases_df = get_registered_cases_data()

    if public_cases_df is None or registered_cases_df is None:
        return {"status": False, "message": "Couldn't connect to database"}
    
    if len(registered_cases_df) == 0:
        return {"status": False, "message": "No registered cases found. Please register at least one case with a clear face photo."}
    
    if len(public_cases_df) == 0:
        return {"status": False, "message": "No public submissions found. Please wait for public submissions or upload test submissions to match against registered cases."}

    # Store original labels before encoding
    original_reg_labels = registered_cases_df["label"].tolist()
    original_pub_labels = public_cases_df["label"].tolist()

    # Prepare training data - exclude label and status columns for features
    feature_cols = [col for col in registered_cases_df.columns if col not in ["label", "status"]]
    reg_features = registered_cases_df[feature_cols].values.astype(float)

    # Create simple numeric labels for KNN (0, 1, 2, ...)
    numeric_labels = list(range(len(reg_features)))

    # Train KNN classifier with numeric labels
    knn = KNeighborsClassifier(n_neighbors=1, algorithm="ball_tree", weights="distance")
    knn.fit(reg_features, numeric_labels)

    # Get additional case details for better matching display
    from backend.database.db_queries import engine, RegisteredCases, PublicSubmissions
    from sqlmodel import Session, select
    
    with Session(engine) as session:
        # Get registered case details
        reg_details = {}
        reg_cases = session.exec(select(RegisteredCases.id, RegisteredCases.name, RegisteredCases.last_seen, RegisteredCases.submitted_on)).all()
        for case_id, name, last_seen, submitted_on in reg_cases:
            reg_details[case_id] = {
                "name": name,
                "last_seen": last_seen,
                "submitted_on": submitted_on,
                "type": "Registered"
            }
        
        # Get public submission details
        pub_details = {}
        pub_cases = session.exec(select(PublicSubmissions.id, PublicSubmissions.location, PublicSubmissions.submitted_on, PublicSubmissions.mobile)).all()
        for sub_id, location, submitted_on, mobile in pub_cases:
            pub_details[sub_id] = {
                "location": location,
                "submitted_on": submitted_on,
                "mobile": mobile,
                "type": "Public"
            }

    # For each public submission, find the closest registered case
    for enum_idx, (df_idx, row) in enumerate(public_cases_df.iterrows()):
        pub_label = original_pub_labels[enum_idx]  # Use enumeration index, not df index
        # Extract features (exclude label column)
        face_encoding = row[feature_cols].values.astype(float)

        try:
            # Get distances to nearest neighbors
            closest_distances = knn.kneighbors([face_encoding])[0][0]
            closest_distance = np.min(closest_distances)

            # Check if distance meets threshold criteria (lower = better match)
            if closest_distance <= distance_threshold:
                # Get the index of the predicted registered case
                predicted_idx = knn.predict([face_encoding])[0]
                # Get the original UUID of the registered case
                reg_label = original_reg_labels[predicted_idx]
                
                # Store the match with distance for confidence scoring
                matched_images[reg_label].append((pub_label, float(closest_distance)))
                
                # Create detailed match information
                match_info = {
                    "registered_id": reg_label,
                    "public_id": pub_label,
                    "distance": float(closest_distance),
                    "confidence": max(0.0, min(100.0, (1.0 - closest_distance / distance_threshold) * 100)),
                    "registered_details": reg_details.get(reg_label, {}),
                    "public_details": pub_details.get(pub_label, {}),
                    "match_type": "Admin-Public Match"
                }
                match_details.append(match_info)
                
                print(f"MATCH FOUND: {reg_details.get(reg_label, {}).get('name', 'Unknown')} <-> {pub_details.get(pub_label, {}).get('location', 'Unknown')} (Distance: {closest_distance:.3f}, Confidence: {match_info['confidence']:.1f}%)")
                
        except Exception as e:
            print(f"Error matching public case {pub_label}: {e}")
            continue

    return {
        "status": True, 
        "result": matched_images,
        "details": match_details,
        "summary": {
            "total_matches": len(match_details),
            "registered_cases_count": len(registered_cases_df),
            "public_submissions_count": len(public_cases_df),
            "distance_threshold": distance_threshold
        }
    }
