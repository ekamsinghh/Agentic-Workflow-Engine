from src.tools.registry import registry

@registry.tool()
def calculate_discount(price: float, percentage: float = 10.0) -> float:
  """Calculates the final price after applying a percentage discount."""
  return price - (price * (percentage / 100.0))

print(registry.get_schemas())
print(registry.execute("calculate_discount", price = 100.0, percentage = 15.0))
print(registry.execute("calculate_discount", rand = 100.0))