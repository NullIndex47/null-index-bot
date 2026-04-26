# generator.py

import base64
import random
import secrets
import textwrap
from datetime import datetime, timezone

from config import (
    LEVELS,
    INTERVALS_HOURS,
    HEX_SIZES,
    EASY_MESSAGES,
    MEDIUM_MESSAGES,
    HARD_FRAGMENTS,
    DEEP_MESSAGES,
    VOID_MESSAGES,
)


def weighted_choice(items):
    names = [item.get("name", item.get("hours")) for item in items]
    weights = [item["weight"] for item in items]
    return random.choices(names, weights=weights, k=1)[0]


def choose_level():
    return weighted_choice(LEVELS)


def choose_next_interval_hours():
    return weighted_choice(INTERVALS_HOURS)


def make_title():
    # Formato tipo A858: 202604261947
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M")


def wrap_hex(hex_text, width=88):
    return "\n".join(textwrap.wrap(hex_text, width))


def noise_hex(bytes_amount):
    return secrets.token_hex(bytes_amount)


def choose_size(level):
    return secrets.choice(HEX_SIZES[level])


def to_hex(text):
    return text.encode("utf-8").hex()


def to_base64(text):
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def xor_text(text, key):
    output = []
    for i, char in enumerate(text):
        output.append(chr(ord(char) ^ ord(key[i % len(key)])))
    return "".join(output)


def make_noise():
    size = choose_size("NOISE")
    return noise_hex(size), None


def make_easy():
    message = secrets.choice(EASY_MESSAGES)
    size = choose_size("EASY")

    # Fácil: mensaje en hex al principio + ruido detrás.
    # Si alguien convierte de hex a texto, verá la frase y luego basura.
    payload = to_hex(message)
    padding = noise_hex(size)

    return payload + padding, message


def make_medium():
    message = secrets.choice(MEDIUM_MESSAGES)
    size = choose_size("MEDIUM")

    # Medio: texto -> base64 -> hex + ruido.
    encoded = to_hex(to_base64(message))
    padding = noise_hex(size)

    return encoded + padding, message


def make_hard():
    message = secrets.choice(HARD_FRAGMENTS)
    size = choose_size("HARD")

    # Difícil: fragmento -> base64 -> hex + ruido.
    encoded = to_hex(to_base64(message))
    padding = noise_hex(size)

    return encoded + padding, message


def make_deep():
    message = secrets.choice(DEEP_MESSAGES)
    size = choose_size("DEEP")

    # Muy difícil: XOR simple con clave interna + base64 + hex + ruido.
    # La clave NO se publica directamente.
    key = "nullindex"
    xored = xor_text(message, key)
    encoded = to_hex(to_base64(xored))
    padding = noise_hex(size)

    return encoded + padding, message


def make_void():
    # VOID: a veces no tiene mensaje real, a veces tiene uno brutal.
    has_message = secrets.choice([True, False, False])

    size = choose_size("VOID")

    if not has_message:
        return noise_hex(size), None

    message = secrets.choice(VOID_MESSAGES)

    # 100-300 rondas visuales. No todas son "cifrado militar";
    # son transformaciones internas para hacerlo muy difícil.
    rounds = secrets.choice(range(100, 301))
    data = message

    for i in range(rounds):
        if i % 4 == 0:
            data = to_base64(data)
        elif i % 4 == 1:
            data = data[::-1]
        elif i % 4 == 2:
            data = to_hex(data)
        else:
            data = to_base64(data)

    # Lo dejamos en hex final + ruido largo.
    if not all(c in "0123456789abcdef" for c in data.lower()):
        data = to_hex(data)

    padding = noise_hex(size)
    return data.lower() + padding, message


def generate_post():
    level = choose_level()

    if level == "NOISE":
        body_hex, hidden_message = make_noise()
    elif level == "EASY":
        body_hex, hidden_message = make_easy()
    elif level == "MEDIUM":
        body_hex, hidden_message = make_medium()
    elif level == "HARD":
        body_hex, hidden_message = make_hard()
    elif level == "DEEP":
        body_hex, hidden_message = make_deep()
    elif level == "VOID":
        body_hex, hidden_message = make_void()
    else:
        body_hex, hidden_message = make_noise()

    title = make_title()
    body = wrap_hex(body_hex, width=88)

    return {
        "title": title,
        "body": body,
        "level": level,
        "hidden_message": hidden_message,
    }
