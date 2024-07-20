import asyncio
import aiohttp
import json
import tiktoken
import logging

logger = logging.getLogger(__name__)

MESSAGE_STREAM_DELAY = 0.02  # second
MESSAGE_STREAM_RETRY_TIMEOUT = 15000  # milisecond
enc = tiktoken.get_encoding("cl100k_base")

def num_tokens_from_messages(messages):
    """Return the number of tokens used by a list of messages."""

    encoding = tiktoken.get_encoding("cl100k_base")

    num_tokens = 0
    for message in messages:
        num_tokens += 3
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


async def event_generator(request_url, request_header, request_json, request):
    print("进入event_generator")
    logger.info(f"{request_url}###{request_header}###{request_json}")
    one = True
    response_str = ""
    num_tokens = num_tokens_from_messages(request_json['messages'])
    async with aiohttp.ClientSession() as session:
        # 根据request_json中 engine来指定不同的request_url
        async with session.post(url=request_url, headers=request_header, json=request_json) as response:
            while True:
                if await request.is_disconnected():
                    logger.info("Request disconnected")
                    break

                if one:
                    yield {
                        "event": "start_message",
                        "retry": MESSAGE_STREAM_RETRY_TIMEOUT,
                        "data": f"{num_tokens}",
                    }
                    one = False
                line = await response.content.readline()
                line = line.decode('utf-8').strip()
                if "[DONE]" in line:
                    yield {
                        "event": "end_event",
                        "retry": MESSAGE_STREAM_RETRY_TIMEOUT,
                        "data": f"{len(enc.encode(response_str)) + 6}"
                    }
                    break
                # return line.decode('utf-8').strip()
                result = ""
                if line:
                    line_dict = json.loads(line[6:])
                    try:
                        delta = line_dict["choices"][0].get("delta")
                    except Exception as e:
                        logger.error(f"line_dict:{line_dict}")
                        logger.error(f"line:{line}")
                        logger.error(f"error:{e}")
                        continue
                    if delta:
                        result = delta.get("content")
                        if result:
                            response_str += result
                            yield {
                                "event": "new_message",
                                "retry": MESSAGE_STREAM_RETRY_TIMEOUT,
                                "data": f"{result}",
                            }

                await asyncio.sleep(MESSAGE_STREAM_DELAY)


async def call_api(request_url, request_header, request_json):
    async with aiohttp.ClientSession() as session:
        # 根据request_json中 engine来指定不同的request_url

        async with session.post(url=request_url, headers=request_header, json=request_json) as response:
            response = await response.json()
            logger.info(f"请求 json{request_json} ### Response data {response}")

            if response.get("error"):
                logger.info(f"请求错误 错误类型 {response['error']}")
                raise Exception(response["error"].get("message", "Something Unknown Error"))
            return response

async def parse_response(response: dict):
    completion_tokens = response["usage"]["completion_tokens"]
    prompt_tokens = response["usage"]["prompt_tokens"]
    total_tokens = response["usage"]["total_tokens"]
    try:
        messages = response["choices"][0]['message']["content"]
    except:
        messages = "Sorry, the content you entered contains harmful information and cannot be translated."
    return (prompt_tokens, completion_tokens, {
        "messages": messages,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens
    })
