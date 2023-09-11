from typing import Dict, Union, Tuple

from flask import Response

API_Response = Union[Response, Tuple[Dict[str, str], int]]
