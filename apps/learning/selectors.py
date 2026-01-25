# ----------- IMPORTS ----------
from __future__ import annotations
from typing import Optional

from apps.learning.models import LearningProgress
from apps.accounts.models import User 

# ----------- SELECTORS -----------------

# ---- Selector 1: get the learning progress model for a particular language ------
def learning_progress_get(*, user: User, language_slug: str) -> Optional[LearningProgress]:
    """
    Fetches the learning progress record for a specific user and language.
    
    Args:
        user (User): The user instance whose progress is being retrieved.
        language_slug (str): The unique identifier for the programming language.
        
    Returns:
        Optional[LearningProgress]: The progress model instance if it exists, otherwise None.
    """
    return (
        LearningProgress.objects
        .filter(user=user, language_slug=language_slug)
        .first()
    )
