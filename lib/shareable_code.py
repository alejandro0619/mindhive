from random import randint
def gen_shareable_code():
  code = randint(1000, 9999)
  return str(code)
