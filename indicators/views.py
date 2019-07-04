from datetime import datetime

import pytz

# Create your views here.
today = datetime.now().replace(tzinfo=pytz.UTC).date()

