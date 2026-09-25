from __future__ import annotations
import os

TEST_UNLOCK_VALUE = "YES_I_FROZE_CONFIG"


def ensure_split_allowed(split: str) -> None:
    """Prevent accidental tuning on the locked final SYNUR test split."""
    if split != "test":
        return
    if os.getenv("ESF_UNLOCK_TEST") != TEST_UNLOCK_VALUE:
        raise RuntimeError(
            "SYNUR TEST is locked. Freeze the final configuration in an ADR first, "
            f"then explicitly set ESF_UNLOCK_TEST={TEST_UNLOCK_VALUE!r} for the one final run."
        )
