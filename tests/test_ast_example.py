from flake8_django_plugin.ast_example import parse_models_file


def test_parse_code(fixture_folder):
    print(fixture_folder)
    filename = fixture_folder / 'patients_models.py'
    assert filename.exists()

    parse_models_file(filename)
