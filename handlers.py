"""Handlers for the pomodoro timer bot."""

import datetime

from telegram import Update
from telegram.ext import ContextTypes

from constants import DEFAULT_BREAK_DURATION
from keyboards import (
    add_time_keyboard,
    break_duration_keyboard,
    duration_keyboard,
    main_reply_keyboard,
    status_keyboard,
)


# ===== Helpers =====


def _format_timedelta(td: datetime.timedelta) -> str:
    total_seconds = int(td.total_seconds())
    if total_seconds < 0:
        return "0 min 0 sec"
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes}m {seconds}s"
    return f"{minutes} min {seconds} sec"


def _has_active_timer(context: ContextTypes.DEFAULT_TYPE) -> bool:
    return context.user_data.get("active", False)


def _is_on_break(context: ContextTypes.DEFAULT_TYPE) -> bool:
    return context.user_data.get("on_break", False)


def _remove_jobs(context: ContextTypes.DEFAULT_TYPE, name: str) -> None:
    for job in context.job_queue.get_jobs_by_name(name):
        job.schedule_removal()


def _get_break_duration(context: ContextTypes.DEFAULT_TYPE) -> int:
    return context.user_data.get("break_duration", DEFAULT_BREAK_DURATION)


# ===== /start =====


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Tomakuro\nYour pomodoro timer.",
        reply_markup=main_reply_keyboard(),
    )


# ===== Bottom keyboard handlers =====


async def handle_start_clock(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if _has_active_timer(context):
        await update.message.reply_text(
            "You already have a running clock.\nCheck status or stop it first.",
        )
        return

    if _is_on_break(context):
        user_id = update.effective_user.id
        _remove_jobs(context, f"break_{user_id}")
        context.user_data["on_break"] = False

    await update.message.reply_text(
        "Pick a duration:",
        reply_markup=duration_keyboard(),
    )


async def handle_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if _is_on_break(context):
        now = datetime.datetime.now()
        break_finish: datetime.datetime = context.user_data["break_finish"]
        remaining = break_finish - now
        await update.message.reply_text(
            f"On Break\n\n"
            f"Remaining: {_format_timedelta(remaining)}\n"
            f"Break ends at: {break_finish.strftime('%H:%M:%S')}",
        )
        return

    if not _has_active_timer(context):
        await update.message.reply_text("No active clock.")
        return

    now = datetime.datetime.now()
    start_time: datetime.datetime = context.user_data["start"]
    finish_time: datetime.datetime = context.user_data["finish"]
    duration: int = context.user_data["duration"]
    duration_unit: str = context.user_data.get("duration_unit", "min")
    elapsed = now - start_time
    remaining = finish_time - now

    await update.message.reply_text(
        f"Clock Status\n\n"
        f"Duration: {duration} {duration_unit}\n"
        f"Started: {start_time.strftime('%H:%M:%S')}\n"
        f"Elapsed: {_format_timedelta(elapsed)}\n"
        f"Remaining: {_format_timedelta(remaining)}\n"
        f"Finishes at: {finish_time.strftime('%H:%M:%S')}",
        reply_markup=status_keyboard(),
    )


async def handle_stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    if _is_on_break(context):
        _remove_jobs(context, f"break_{user_id}")
        context.user_data["on_break"] = False
        await update.message.reply_text("Break cancelled.")
        return

    if not _has_active_timer(context):
        await update.message.reply_text("No active clock to stop.")
        return

    _remove_jobs(context, f"pomodoro_{user_id}")
    context.user_data["active"] = False
    await update.message.reply_text("Clock stopped.")


async def handle_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    current = _get_break_duration(context)
    await update.message.reply_text(
        f"Settings\n\nBreak duration: {current} min\n\nSelect a new break duration:",
        reply_markup=break_duration_keyboard(current),
    )


# ===== Inline callback handlers =====


async def cb_duration_selected(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    await query.answer()

    if _has_active_timer(context):
        await query.edit_message_text("You already have a running clock.")
        return

    # Handle both sec_* (seconds) and dur_* (minutes) callbacks
    data = query.data
    prefix, value = data.split("_")
    duration = int(value)

    if prefix == "sec":
        delta = datetime.timedelta(seconds=duration)
        unit = "sec"
    else:
        delta = datetime.timedelta(minutes=duration)
        unit = "min"

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    now = datetime.datetime.now()
    finish = now + delta

    context.user_data["active"] = True
    context.user_data["start"] = now
    context.user_data["duration"] = duration
    context.user_data["duration_unit"] = unit
    context.user_data["finish"] = finish
    context.user_data["chat_id"] = chat_id

    _remove_jobs(context, f"pomodoro_{user_id}")
    context.job_queue.run_once(
        timer_finished,
        when=delta,
        chat_id=chat_id,
        name=f"pomodoro_{user_id}",
        data={"user_id": user_id, "duration": duration, "duration_unit": unit},
    )

    await query.edit_message_text(
        f"Clock started!\n\n"
        f"Duration: {duration} {unit}\n"
        f"Started: {now.strftime('%H:%M:%S')}\n"
        f"Finishes at: {finish.strftime('%H:%M:%S')}",
        reply_markup=status_keyboard(),
    )


async def cb_add_time_pressed(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    await query.answer()

    if not _has_active_timer(context):
        await query.edit_message_text("No active clock.")
        return

    await query.edit_message_text(
        "How much time to add?",
        reply_markup=add_time_keyboard(),
    )


async def cb_add_time_selected(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    await query.answer()

    if not _has_active_timer(context):
        await query.edit_message_text("No active clock.")
        return

    extra = int(query.data.split("_")[1])
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    context.user_data["duration"] += extra
    context.user_data["finish"] += datetime.timedelta(minutes=extra)
    new_finish: datetime.datetime = context.user_data["finish"]

    _remove_jobs(context, f"pomodoro_{user_id}")
    remaining = new_finish - datetime.datetime.now()
    if remaining.total_seconds() > 0:
        context.job_queue.run_once(
            timer_finished,
            when=remaining,
            chat_id=chat_id,
            name=f"pomodoro_{user_id}",
            data={"user_id": user_id, "duration": context.user_data["duration"]},
        )

    await query.edit_message_text(
        f"+{extra} min added.\nNew finish time: {new_finish.strftime('%H:%M:%S')}",
        reply_markup=status_keyboard(),
    )


async def cb_cancel_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    _remove_jobs(context, f"pomodoro_{user_id}")
    context.user_data["active"] = False

    await query.edit_message_text("Clock cancelled.")


async def cb_break_duration_selected(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    await query.answer()

    new_duration = int(query.data.split("_")[1])
    context.user_data["break_duration"] = new_duration

    await query.edit_message_text(f"Break duration set to {new_duration} min.")


# ===== Job queue callbacks =====


async def timer_finished(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    user_id = job.data["user_id"]
    duration = job.data["duration"]
    duration_unit = job.data.get("duration_unit", "min")

    user_data = context.application.user_data.get(user_id, {})
    user_data["active"] = False

    break_duration = user_data.get("break_duration", DEFAULT_BREAK_DURATION)

    await context.bot.send_message(
        chat_id=job.chat_id,
        text=(
            f"Time's up! {duration} {duration_unit} completed.\n"
            f"Great work! Starting a {break_duration} min break..."
        ),
    )

    # Start break
    now = datetime.datetime.now()
    user_data["on_break"] = True
    user_data["break_finish"] = now + datetime.timedelta(minutes=break_duration)

    _remove_jobs(context, f"break_{user_id}")
    context.job_queue.run_once(
        break_finished,
        when=datetime.timedelta(minutes=break_duration),
        chat_id=job.chat_id,
        name=f"break_{user_id}",
        data={"user_id": user_id, "break_duration": break_duration},
    )


async def break_finished(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    user_id = job.data["user_id"]
    break_duration = job.data["break_duration"]

    user_data = context.application.user_data.get(user_id, {})
    user_data["on_break"] = False

    await context.bot.send_message(
        chat_id=job.chat_id,
        text=(f"Break over! ({break_duration} min)\nReady for another pomodoro?"),
    )
