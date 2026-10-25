
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from test import RecommendationEngine


@pytest.fixture(scope="module")
def engine():
    return RecommendationEngine(model_dir=str(PROJECT_ROOT / "models"))


@pytest.mark.parametrize(
    "project_input, expected_domain, expected_type",
    [
        (
            {
                "project_title": "AI-Powered Breast Cancer Detection",
                "project_description": (
                    "Deep learning using CNNs to classify histopathology images."
                ),
                "research_domain": "Biomedical",
                "project_type": "Computational",
                "budget_range": "5L-20L",
                "duration_months": 12,
                "team_expertise": "ML, Data Analysis, Biology",
                "location": "Chennai, Tamil Nadu",
            },
            "Biomedical",
            "Computational",
        ),
        (
            {
                "project_title": "Smart Water Quality Monitoring System",
                "project_description": (
                    "IoT sensors monitor water quality with ML anomaly detection."
                ),
                "research_domain": "Environmental Science",
                "project_type": "Experimental",
                "budget_range": "1L-5L",
                "duration_months": 6,
                "team_expertise": "Embedded Systems, ML, Data Analysis",
                "location": "Chennai, Tamil Nadu",
            },
            "Environmental Science",
            "Experimental",
        ),
    ],
)
def test_recommendation_output(engine, project_input, expected_domain, expected_type):
    result = engine.predict(project_input)

    assert isinstance(result, dict)
    assert result["detected_domain"] == expected_domain
    assert result["detected_project_type"] == expected_type

    for key in (
        "recommended_equipment",
        "recommended_methodologies",
        "recommended_tools",
        "similar_project_ids",
        "execution_roadmap",
        "recommended_labs",
        "teachers",
        "confidence_score",
    ):
        assert key in result, f"Missing result field: {key}"

    assert isinstance(result["recommended_equipment"], list)
    assert isinstance(result["recommended_methodologies"], list)
    assert isinstance(result["recommended_tools"], list)
    assert 0 <= result["confidence_score"] <= 1

