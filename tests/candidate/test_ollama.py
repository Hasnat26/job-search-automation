from backend.candidate.extractor import normalize_missing, parse_profile_json


def test_json_object_parses():
    profile = parse_profile_json('{"full_name":"Test Candidate"}')
    assert normalize_missing(profile)["full_name"] == "Test Candidate"


def test_non_object_fails():
    try:
        parse_profile_json('[]')
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")
