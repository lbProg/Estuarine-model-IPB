import sys

def progressbar(count, total):
  bar_length = 60
  filled_length = int(bar_length * count // total)
  percents = (100 * count // total)
  bar = '=' * filled_length + '-' * (bar_length - filled_length)
  
  sys.stdout.write(f'\r|{bar}| {percents}%')
  sys.stdout.flush()