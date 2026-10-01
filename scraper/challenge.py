import re


CHALLENGE_PATTERNS = [
    r"cf-chl-",
    r"cloudflare",
    r"checking your browser",
    r"verify you are human",
    r"just a moment",
    r"attention required",
    r"security check",
]


def detect_challenge(
    title="",
    content="",
):

    text = f"{title} {content}".lower()

    for pattern in CHALLENGE_PATTERNS:

        if re.search(
            pattern,
            text,
        ):
            return True

    return False