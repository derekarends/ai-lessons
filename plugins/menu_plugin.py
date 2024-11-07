from typing import Annotated

from semantic_kernel.functions.kernel_function_decorator import kernel_function

class MenuPlugin:
    """A sample Menu Plugin."""
    name = "MenuPlugin"

    @kernel_function(description="Provides a list of specials from the menu.")
    def get_specials(self) -> Annotated[str, "Returns the specials from the menu."]:
        return """
        Special Soup: Clam Chowder
        Special Salad: Cobb Salad
        Special Drink: Chai Tea
        """

    @kernel_function(description="Provides the price of the specials menu item.")
    def get_special_price(
        self, menu_item: Annotated[str, "The name of the menu item."]
    ) -> Annotated[str, "Returns the price of the menu item."]:
      menu_prices = {
          "clam chowder": "$4.99",
          "cobb salad": "$7.99",
          "chai tea": "$2.99"
      }
      return menu_prices.get(menu_item.lower(), "Unable to find that menu item, please check the specials and try again.")