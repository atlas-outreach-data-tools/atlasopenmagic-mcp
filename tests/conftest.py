from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_atom() -> MagicMock:
    """Return a MagicMock that mimics the atlasopenmagic module."""
    atom = MagicMock()

    # Core module-level attributes
    atom.metadata.RELEASES_DESC = {
        "2024r-pp": "2024 research release for proton-proton collisions",
        "2020e-13tev": "2020 education release, 13 TeV",
    }
    atom.metadata.AVAILABLE_FIELDS = [
        "dataset_number",
        "physics_short",
        "cross_section_pb",
        "keywords",
    ]

    # Default return values for common functions
    atom.get_current_release.return_value = "2024r-pp"
    atom.available_datasets.return_value = ["301204", "301205"]
    atom.available_skims.return_value = ["noskim", "exactly4lep"]
    atom.available_keywords.return_value = ["top", "higgs", "dilepton"]
    atom.get_metadata_fields.return_value = [
        "cross_section_pb",
        "dataset_number",
        "keywords",
        "physics_short",
    ]
    atom.get_metadata.return_value = {
        "dataset_number": "301204",
        "physics_short": "zprime_ee",
        "cross_section_pb": 1.23,
    }
    atom.get_all_info.return_value = {
        "dataset_number": "301204",
        "physics_short": "zprime_ee",
        "cross_section_pb": 1.23,
        "file_list": ["https://opendata.cern.ch/file1.root"],
        "skims": [],
    }
    atom.get_urls.return_value = [
        "https://opendata.cern.ch/file1.root",
        "https://opendata.cern.ch/file2.root",
    ]
    atom.match_metadata.return_value = [
        ("301204", "zprime_ee"),
        ("301205", "zprime_mumu"),
    ]
    atom.get_weights.return_value = {
        "release_name": "2025r-evgen-13tev",
        "energy_level": "13TeV",
        "dataset_number": "306600",
        "weights": ["nominal", "muR2p0", "muF0p5"],
        "weight_count": 3,
    }
    atom.get_all_weights_for_release.return_value = {
        "release_name": "2025r-evgen-13tev",
        "energy_level": "13TeV",
        "datasets": {"306600": ["nominal", "muR2p0"], "306601": ["nominal"]},
    }

    return atom


@pytest.fixture
def mock_ctx(mock_atom: MagicMock) -> MagicMock:
    """Return a mock FastMCP Context with atlasopenmagic in lifespan context."""
    ctx: MagicMock = MagicMock()
    ctx.request_context.lifespan_context = {"atom": mock_atom}
    return ctx


def pytest_addoption(parser: Any) -> None:
    """Add command line options for test categories."""
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_collection_modifyitems(config: Any, items: Any) -> None:
    """Skip tests based on command line options."""
    if not config.getoption("--runslow"):
        skip_slow = pytest.mark.skip(reason="need --runslow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
