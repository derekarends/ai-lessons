from typing import Annotated

from semantic_kernel.functions.kernel_function_decorator import kernel_function

class HoursPlugin:
    """A sample Business Hours Plugin."""
    name = "HoursPlugin"

    @kernel_function(description="Provides a list of business hours.")
    def get_all_hours(self) -> Annotated[str, "Returns the business hours."]:
        return """
        Monday: 9:00 AM - 5:00 PM
        Tuesday: 9:00 AM - 5:00 PM
        Wednesday: 9:00 AM - 5:00 PM
        Thursday: 9:00 AM - 5:00 PM
        Friday: 9:00 AM - 5:00 PM
        Saturday: Closed
        Sunday: Close
        """
    
    @kernel_function(description="Provides the hours of operation for a specific day.")
    def get_hours_for_specific_day(
        self, day: Annotated[str, "The name of the day."]
    ) -> Annotated[str, "Returns the hours of operation for the specified day."]:
      hours = {
          "monday": "9:00 AM - 5:00 PM",
          "tuesday": "9:00 AM - 5:00 PM",
          "wednesday": "9:00 AM - 5:00 PM",
          "thursday": "9:00 AM - 5:00 PM",
          "friday": "9:00 AM - 5:00 PM",
          "saturday": "Closed",
          "sunday": "Closed"
      }
      return hours.get(day.lower(), "Unable to find the hours for that day, please check the business hours and try again.")