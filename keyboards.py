"""Keyboard builders."""

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from constants import (
    BTN_SETTINGS,
    BTN_START_CLOCK,
    BTN_STATUS,
    BTN_STOP,
    CB_ADD_TIME,
    CB_CANCEL,
    ADD_DURATIONS,
    BREAK_DURATIONS,
    DURATIONS,
)


def main_reply_keyboard() -> ReplyKeyboardMarkup:
    """Persistent bottom keyboard."""
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(BTN_START_CLOCK), KeyboardButton(BTN_STATUS)],
            [KeyboardButton(BTN_STOP), KeyboardButton(BTN_SETTINGS)],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


def duration_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard for picking pomodoro duration."""
    rows = []
    for i in range(0, len(DURATIONS), 3):
        row = [
            InlineKeyboardButton(f"{d} min", callback_data=f"dur_{d}")
            for d in DURATIONS[i : i + 3]
        ]
        rows.append(row)
    return InlineKeyboardMarkup(rows)


def status_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard shown with timer status."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Add Time", callback_data=CB_ADD_TIME)],
        [InlineKeyboardButton("Cancel Clock", callback_data=CB_CANCEL)],
    ])


def add_time_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard for choosing how much time to add."""
    row = [
        InlineKeyboardButton(f"+{d} min", callback_data=f"addtime_{d}")
        for d in ADD_DURATIONS
    ]
    return InlineKeyboardMarkup([row])


def break_duration_keyboard(current: int) -> InlineKeyboardMarkup:
    """Inline keyboard for choosing break duration in settings."""
    rows = []
    for d in BREAK_DURATIONS:
        label = f"{'> ' if d == current else ''}{d} min"
        rows.append([InlineKeyboardButton(label, callback_data=f"break_{d}")])
    return InlineKeyboardMarkup(rows)
