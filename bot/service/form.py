from aiogram.fsm.state import StatesGroup, State


class FormStates(StatesGroup):
    waiting_for_file = State()
