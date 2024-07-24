class color:
   RED = '\033[91m'
   # ORANGE = 
   YELLOW = '\033[93m'
   GREEN = '\033[92m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   PURPLE = '\033[95m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def bolden(text):
   return color.BOLD + text + color.END

def stand_out(text):
   return '\n'+ text + '\n'

def print_wrapper(text, *args):
   for func in args:
      text = func(text)
   print(text)

def red(text):
   return color.RED + text + color.END

#def orange(text):


def yellow(text):
   return color.YELLOW + text + color.END