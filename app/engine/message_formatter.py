from app.models.message import Message


class MessageFormatter:

    def anthropic(
        self,
        messages: list[Message],
    ):

        formatted = []

        for message in messages:

            formatted.append(
                {
                    "role": message.role.value,
                    "content": message.content,
                }
            )

        return formatted