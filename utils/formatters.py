def format_laws(laws: list) -> str:
    return "\n\n".join(
        f"📖 <b>{law[0]} ст.{law[1]}</b>\n"
        f"{law[2][:300]}...\n"
        f"<i>Источник: consultant.ru</i>"
        for law in laws[:3]  # Первые 3 результата
    )
