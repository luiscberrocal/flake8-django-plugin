from pathlib import Path

import pytest


@pytest.fixture(scope='session')
def fixture_folder() -> Path:
    folder = Path(__file__).parent / 'fixtures'
    return folder
