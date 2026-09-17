from backend.evidence.service import apply_evidence_gate, normalize_evidence


def test_exact_snippet_is_verified():
    source = "PMP certified."
    evidence = normalize_evidence([{"field_name":"certifications","value":["PMP"],"raw_snippet":"PMP certified."}], source, "cv.txt")
    assert evidence[0].status == "VERIFIED"


def test_fake_snippet_is_not_verified():
    source = "Project Manager."
    evidence = normalize_evidence([{"field_name":"skills","value":["ABB 800xA"],"raw_snippet":"ABB 800xA expert"}], source, "cv.txt")
    assert evidence[0].status != "VERIFIED"


def test_gate_removes_unsupported_claim():
    profile = {"full_name":"John Doe", "skills":["ABB 800xA"]}
    evidence = normalize_evidence([], "John Doe", "cv.txt")
    gated, missing = apply_evidence_gate(profile, evidence)
    assert gated["skills"] == []
    assert "skills" in missing
