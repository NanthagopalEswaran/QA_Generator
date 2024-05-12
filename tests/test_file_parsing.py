import os

import pytest
from delayed_assert import assert_expectations, expect

from qa_generator.file_parser import File

# Get all files under the sample_files directory
sample_files_folder = os.path.join(os.path.dirname(__file__), "sample_files")
sample_files = [
    f
    for f in os.listdir(sample_files_folder)
    if os.path.isfile(os.path.join(sample_files_folder, f))
]
extensions = [f.split(".")[-1] for f in sample_files]


@pytest.mark.parametrize("file_name", sample_files, ids=extensions)
def test_file_parsing_different_formats(file_name):
    """Test file parsing with all supported file formats."""

    file_path = os.path.join(sample_files_folder, file_name)
    try:
        File(file_path)
    except Exception as e:
        expect(False, f"Failed to parse {file_name}: {e}")
    else:
        expect(True, f"Successfully parsed {file_name}")

    assert_expectations()
