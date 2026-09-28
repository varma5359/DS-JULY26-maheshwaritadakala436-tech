import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
APP_PACKAGE_ROOT = PROJECT_ROOT / "logistics_delivery_analytics"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(APP_PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_PACKAGE_ROOT))

os.chdir(PROJECT_ROOT)

from logistics_delivery_analytics.app.streamlit_app import *  # noqa: F401,F403
