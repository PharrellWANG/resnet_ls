def get_opts(my_argv):
  opts = {}  # Empty dictionary to store key-value pairs.
  while my_argv:  # While there are arguments left to parse...
    if my_argv[0][0] == '-':  # Found a "-name value" pair.
      opts[my_argv[0]] = my_argv[1]  # Add key and value to the dictionary.
    my_argv = my_argv[1:]  # Reduce the argument list by copying it starting from index 1.
  return opts
