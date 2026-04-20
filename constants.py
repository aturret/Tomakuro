"""Constants for callback data, button labels, and config."""

# Bottom keyboard button labels (sent as text messages)
BTN_START_CLOCK = "Start Clock"
BTN_STATUS = "Status"
BTN_STOP = "Stop"
BTN_SETTINGS = "Settings"

# Callback data for inline buttons
CB_ADD_TIME = "add_time"
CB_CANCEL = "cancel_timer"

# Timer durations (minutes)
DURATIONS = [15, 30, 45, 60, 90, 120]

# Short countdown durations (seconds)
SHORT_DURATIONS = [30, 60, 90]
ADD_DURATIONS = [5, 10, 15, 30]

# Break time
DEFAULT_BREAK_DURATION = 5
BREAK_DURATIONS = [3, 5, 10, 15]
