from orchestrator import Orchestrator
import sys
def main():
     Orchestrator().orchestrate(sys.argv.pop(1))

main()