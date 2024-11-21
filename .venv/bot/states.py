from aiogram.fsm.state import State, StatesGroup

class Reg(StatesGroup):
    name = State()
    contact = State()
    location = State()
    age = State()
    photo = State()

