from typing import Annotated

from semantic_kernel.functions.kernel_function_decorator import kernel_function

class LegalPlugin:
    """A sample Legal Plugin."""

    name = "LegalPlugin"

    @kernel_function(description="Given a copy of the content it will determine if the content is legal.")
    def is_legal(
        self, content: Annotated[str, "The content to check."]
    ) -> Annotated[str, "Returns whether the content is legal, if it is not, it will say why."]:
        legal_words = ["guarantee", "warranty", "secure", "protected", "certified"]
        if any(word in content.lower() for word in legal_words):
            return f"The content is not legal because it contains {', '.join(legal_words)}."
        return "The content is legal."