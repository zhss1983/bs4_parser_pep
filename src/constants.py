from pathlib import Path

BASE_DIR = Path(__file__).parent
MAIN_DOC_URL = 'https://docs.python.org/3/'
MAIN_PEP_URL = 'https://peps.python.org/'
DT_FILE_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_LOG_FORMAT = '%d.%m.%Y %H:%M:%S'

PATTERN_PYTHON_VERSION_STATUS = (r'Python (?P<version>\d\.\d+) '
                                 r'\((?P<status>.*)\)|(All versions)()')
PATTERN_ZIP_A4 = r'^.+pdf-a4\.zip$'

EXPECTED_STATUS = {
    'A': ['Active', 'Accepted'],
    'D': ['Deferred'],
    'F': ['Final'],
    'P': ['Provisional'],
    'R': ['Rejected'],
    'S': ['Superseded'],
    'W': ['Withdrawn'],
    '': ['Draft', 'Active'],
}
