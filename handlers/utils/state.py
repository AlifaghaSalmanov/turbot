async def finish_state(text, state):

    if text == "/filter_bitir":
        await state.finish()
        return True
    return False
