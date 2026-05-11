"""Stegmotor: lagra och visa steg."""


def new_solution(summary):
    return {"sum": summary, "steps": [], "final": None}


def add_step(sol, title, expr="", calc="", result=None):
    sol["steps"].append({
        "id": len(sol["steps"]) + 1,
        "title": title,
        "expr": expr,
        "calc": calc,
        "result": result,
    })


def set_final(sol, final):
    sol["final"] = final


def render_step(step):
    parts = [f"Steg {step['id']}: {step['title']}"]
    if step.get("expr"):
        parts.append(step["expr"])
    if step.get("calc"):
        parts.append(step["calc"])
    if step.get("result") is not None:
        parts.append(f"Resultat: {step['result']}")
    return "\n".join(parts)
