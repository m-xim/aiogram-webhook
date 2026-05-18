import asyncio

from aiogram_webhook.logs import get_logger

logger = get_logger("tasks")


class TaskTracker:
    def __init__(self) -> None:
        self._tasks: set[asyncio.Task] = set()

    def spawn(self, coro) -> asyncio.Task:
        """
        Starts a coroutine in the background and tracks it.

        :param coro: Coroutine to be executed.
        :return: The created asyncio Task.
        """
        task = asyncio.create_task(coro)
        self._tasks.add(task)

        task.add_done_callback(self._on_task_done)
        return task

    def _on_task_done(self, task: asyncio.Task) -> None:
        """Callback to remove the task from the set and log unhandled exceptions."""
        self._tasks.discard(task)

        if not task.cancelled():
            exc = task.exception()
            if exc:
                logger.error("Unhandled exception in background task: %s", exc, exc_info=exc)

    async def close(self, timeout: float | None = 10.0) -> None:
        """
        Gracefully waits for all tracked tasks to complete.
        Cancels remaining tasks if the timeout is reached.

        :param timeout: Maximum time (in seconds) to wait before canceling.
        """
        if not self._tasks:
            return

        done, pending = await asyncio.wait(self._tasks, timeout=timeout, return_when=asyncio.ALL_COMPLETED)

        if pending:
            logger.warning("Timeout reached. Cancelling %s pending tasks.", len(pending))
            for task in pending:
                task.cancel()

            # Wait for cancellations to process
            await asyncio.gather(*pending, return_exceptions=True)
