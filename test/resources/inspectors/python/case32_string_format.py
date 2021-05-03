hello_world = "Hello, World!"
hello = "Hello"
world = "World"
some_list = [hello, world]
some_dict = {"hello": hello, "world": world}

# -----------------------------------------------------------------------------------

# Correct
print("{0}!".format(hello_world))

# Correct
print("{}!".format(hello_world))

# Correct
print("{0}, {1}!".format(hello, world))

# Correct
print("{0}, {1}!".format(*some_list))

# Correct
print("{1}, {0}!".format(world, hello))

# Correct
print("{1}, {0}!".format(*some_list))

# Correct
print("{}, {}!".format(hello, world))

# Correct
print("{}, {}!".format(*some_list))

# Correct
print("{hello}, {world}!".format(hello=hello, world=world))

# Correct
print("{hello}, {world}!".format(**some_dict))

# -----------------------------------------------------------------------------------

# Correct
print(str.format("{0}!", hello_world))

# Correct
print(str.format("{}!", hello_world))

# Correct
print(str.format("{0}, {1}!", hello, world))

# Correct
print(str.format("{0}, {1}!", *some_list))

# Correct
print(str.format("{1}, {0}!", world, hello))

# Correct
print(str.format("{1}, {0}!", *some_list))

# Correct
print(str.format("{}, {}!", hello, world))

# Correct
print(str.format("{}, {}!", *some_list))

# Correct
print(str.format("{hello}, {world}!", hello=hello, world=world))

# Correct
print(str.format("{hello}, {world}!", **some_dict))

# -----------------------------------------------------------------------------------

# Wrong: P-201
print("{0}, {1}!".format(hello))

# Wrong: P-201
print("{}, {}!".format(hello))

# Wrong: P-201
print(str.format("{0}, {1}!", hello))

# Wrong: P-201
print(str.format("{}, {}!", hello))

# -----------------------------------------------------------------------------------

# Wrong: P-202
print("{hello}, {world}!".format(hello=hello))

# Wrong: P-202
print(str.format("{hello}, {world}!", hello=hello))

# -----------------------------------------------------------------------------------

# Wrong: P-203
print("{0}!".format(**some_dict))

# Wrong: P-203
print("{}!".format(**some_dict))

# Wrong: P-203
print(str.format("{0}!", **some_dict))

# Wrong: P-203
print(str.format("{}!", **some_dict))

# -----------------------------------------------------------------------------------

# Wrong: P-204
print("{hello_world}!".format(*some_list))

# Wrong: P-204
print(str.format("{hello_world}!", *some_list))

# -----------------------------------------------------------------------------------

# Wrong: P-205
print("{}, {0}!".format(hello, world))

# Wrong: P-205
print(str.format("{}, {0}!", hello, world))

# -----------------------------------------------------------------------------------

# Wrong: P-301
print("{0}".format(hello_world, hello, world))

# Wrong: P-301
print("{}".format(hello_world, hello, world))

# Wrong: P-301
print(str.format("{0}", hello_world, hello, world))

# Wrong: P-301
print(str.format("{}", hello_world, hello, world))

# -----------------------------------------------------------------------------------

# Wrong: P-302
print("{hello_world}".format(hello_world=hello_world, hello=hello, world=world))

# Wrong: P-302
print(str.format("{hello_world}", hello_world=hello_world, hello=hello, world=world))
