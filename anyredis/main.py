from anyio import (
    TASK_STATUS_IGNORED,
    create_task_group,
    create_tcp_listener,
    run,
    sleep,
)
from anyio.abc import ByteStream


async def some_task(num):
    print("Task", num, "running")
    await sleep(0.1)
    print("Task", num, "finished")


async def handler(stream: ByteStream):
    received = await stream.receive()
    print(received)
    print("HTTP/1.1 200 OK\r\n\r\n".encode("ascii"))
    await stream.send("HTTP/1.1 200 OK\r\nContent-Length: 1\r\n\r\n1".encode("ascii"))


async def some_service(port: int, *, task_status=TASK_STATUS_IGNORED):
    async with await create_tcp_listener(local_host="127.0.0.1", local_port=port) as listener:
        task_status.started()
        await listener.serve(handler)


async def main():
    print("Hello")
    async with create_task_group() as tg:
        for num in range(5):
            tg.start_soon(some_task, num, name=f"Task{num}")
        await tg.start(some_service, 8000)


if __name__ == "__main__":
    run(main)
