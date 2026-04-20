# Plan: Add Short Countdown (30s/60s/90s)

## TL;DR

> **Quick Summary**: Add a new row with 30s/60s/90s countdown options before the minute duration buttons.
> 
> **Deliverables**: 
> - Updated keyboard showing short countdowns first, then minutes
> - Handler updated to handle seconds-based timers
> 
> **Estimated Effort**: Short
> **Parallel Execution**: NO - sequential (2 tasks only)
> **Critical Path**: constants → keyboard → handler

---

## Context

### Original Request
User wants to add short countdown options (30secs, 60secs, 90secs) BEFORE the existing 15min/30min/45min row in the duration picker keyboard.

### Technical Analysis
- Current: `DURATIONS = [15, 30, 45, 60, 90, 120]` in constants.py
- Current: Keyboard builds "X min" buttons from DURATIONS
- Current: Handler parses `dur_{minutes}` callback data

### Scope
- IN: Add short countdown (30s/60s/90s), update keyboard order, handle seconds
- OUT: No other UI changes, no settings modification

---

## Work Objectives

### Core Objective
Users can pick quick 30/60/90 second countdowns from the same duration picker.

### Must Have
- [ ] Short countdown row appears FIRST (before minute rows)
- [ ] Buttons show "30 sec", "60 sec", "90 sec" (not "min")
- [ ] Timer runs for exact seconds specified

### Must NOT Have
- [ ] Don't mix seconds and minutes in same row
- [ ] Don't change existing minute durations

---

## Execution Strategy

```
Wave 1:
├── Task 1: Add SHORT_DURATIONS constant + update keyboard
└── Task 2: Update handler to handle seconds
```

---

## Tasks

- [ ] 1. Add SHORT_DURATIONS constant + update keyboard builder

  **What to do**:
  - Add `SHORT_DURATIONS = [30, 60, 90]` to constants.py
  - Import it in keyboards.py
  - Modify `duration_keyboard()` to build short row FIRST, then minute rows

  **References**:
  - `constants.py:14` - DURATIONS pattern to follow
  - `keyboards.py:35-44` - duration_keyboard() function
  
- [ ] 2. Update handler for seconds

  **What to do**:
  - Modify `cb_duration_selected()` to detect seconds vs minutes
  - Use `timedelta(seconds=...)` for short durations
  - Display shows "X sec" or "X min" appropriately

  **References**:
  - `handlers.py:143-178` - cb_duration_selected() callback handler
  - `constants.py:17` - DEFAULT_BREAK_DURATION (for reference pattern)

---

## Verification

- [ ] Bot shows 30 sec / 60 sec / 90 sec row FIRST
- [ ] Picking 30 sec runs 30 second timer, displays "30 sec" in status
- [ ] Original minute options still work (15/30/45/60/90/120 min)