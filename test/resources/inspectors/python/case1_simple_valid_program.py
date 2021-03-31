days = int(input())

cost_food_per_day = int(input())
cost_flight = int(input())
cost_night = int(input())

nights = days - 1
total_cost = days * cost_food_per_day + cost_night * nights + cost_flight * 2

print(total_cost)
