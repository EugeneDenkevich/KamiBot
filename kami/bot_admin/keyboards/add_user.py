from aiogram.filters.callback_data import CallbackData


class AddUserCallbackData(CallbackData, prefix="add_user"):  # type: ignore[call-arg]
    """Callback data for "Add user" button"""

    tg_id: str
    phone: str
