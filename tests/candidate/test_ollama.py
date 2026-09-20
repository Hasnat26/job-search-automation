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


def test_chunk_defaults_are_cpu_friendly():
    from backend.candidate.extractor import chunk_markdown

    chunks = chunk_markdown("x" * 5248)
    assert [len(chunk) for chunk in chunks] == [4000, 1448]


def test_deterministic_profile_uses_exact_evidence():
    from backend.candidate.extractor import extract_deterministic_profile

    profile = extract_deterministic_profile(
        "John Doe\nProject Manager\n10 years of experience in industrial automation.\nPMP certified.\nEmail: john.doe@example.com\n"
    )
    assert profile["full_name"] == "John Doe"
    assert profile["email"] == "john.doe@example.com"
    assert "PMP certified." in profile["certifications"]
    assert any(item["raw_snippet"] == "PMP certified." for item in profile["evidence"])
