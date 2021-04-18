from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests import Session

retry_strategy = Retry(
    total=5,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = Session()
session.mount("https://", adapter)
session.mount("http://", adapter)
