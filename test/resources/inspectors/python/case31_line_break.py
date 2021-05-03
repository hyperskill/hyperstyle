# Wrong
from math import exp, \
    log

# Correct
from math import (
    sin,
    cos,
)


# Wrong
def do_something_wrong(x: float, y: float):
    if sin(x) == cos(y) \
            and exp(x) == log(y):
        print("Do not do that!")


print(do_something_wrong(1, 2))

# Wrong
wrong_string = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. " \
               + "Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, " \
               + "nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. " \
               + "Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, " \
               + "vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. " \
               + "Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. " \
               + "Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, " \
               + "porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, " \
               + "viverra quis, feugiat a,"
print(wrong_string)

# Correct
correct_string = ("Lorem ipsum dolor sit amet, consectetuer adipiscing elit. "
                  + "Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis "
                  + "parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, "
                  + "pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, "
                  + "aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, "
                  + "venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. "
                  + "Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. "
                  + "Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. "
                  + "Aliquam lorem ante, dapibus in, viverra quis, feugiat a,"
                  )
print(correct_string)

other_correct_string = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec euismod vitae libero ut consequat. 
    Fusce quis ultrices sem, vitae viverra mi. Praesent fermentum quam ac volutpat condimentum. 
    Proin mauris orci, molestie vel fermentum vel, consectetur vel metus. Quisque vitae mollis magna. 
    In hac habitasse platea dictumst. Pellentesque sed diam eget dolor ultricies faucibus id sed quam. 
    Nam risus erat, varius ut risus a, tincidunt vulputate magna. Etiam lacinia a eros non faucibus. 
    In facilisis tempor nisl, sit amet feugiat lacus viverra quis.
"""
print(other_correct_string)
