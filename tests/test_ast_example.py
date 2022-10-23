

def test_parse_code(fixture_folder):
    print(fixture_folder)
    filename = fixture_folder / 'patients_models.py'
    assert filename.exists()
