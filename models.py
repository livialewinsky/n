"""Kompakta datastrukturer för TI-84."""


def new_func(family, params, label="f(x)"):
    return {"f": family, "p": params, "m": {"l": label}}


def new_problem(topic, subtopic, func, inputs):
    return {"t": topic, "s": subtopic, "fn": func, "in": inputs}
