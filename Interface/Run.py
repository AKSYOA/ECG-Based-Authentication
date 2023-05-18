import numpy as np
from joblib import load

from App.Data_Preparation import filter_signal, segment_signal
from App.Feature_Extraction import extract_fiducial_features, extract_ac_dct_non_fiducial


def get_features_and_classifier(signal, feature_extraction_method_value):
    filtered_signal = filter_signal(signal)
    if feature_extraction_method_value == 1:  # Fiducial
        features = extract_fiducial_features(filtered_signal)
        clf = load('../Models/Fiducial.joblib')
    else:
        segments = segment_signal(filtered_signal)
        features = extract_ac_dct_non_fiducial(segments)
        clf = load('../Models/AC_DCT.joblib')
    return features, clf


def evaluate_authentication(predictions):
    unique, counts = np.unique(predictions, return_counts=True)
    half_length = len(predictions) / 2
    for value, count in zip(unique, counts):
        if count > half_length:
            return value
    return -1


def run(signal, feature_extraction_method_value):
    features, clf = get_features_and_classifier(signal, feature_extraction_method_value)
    predictions = clf.predict(features)
    authenticated_person_index = evaluate_authentication(predictions)
    return authenticated_person_index
