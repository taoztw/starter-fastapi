import asyncio
import string
import random


def generate_short_url(size=7) -> str:
    letters = string.ascii_letters + string.digits
    short_tag = "".join(random.choice(letters) for i in range(size))
    return short_tag


async def generate_num(size=6) -> str:
    return "".join(random.choices(string.digits, k=size))


if __name__ == "__main__":
    print(asyncio.run(generate_num(6)))
