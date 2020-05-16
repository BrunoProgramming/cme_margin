import sys

from cme_margin.cme_margin import fib

if __name__ == "__main__":
    n = int(sys.argv[1])
    print(fib(n))
