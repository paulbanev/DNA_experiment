import argparse

parser = argparse.ArgumentParser(description="Run Fishbone DNA Hole Transport Simulation")
parser.add_argument('--length', type=int, required=True, help='Number of base-pairs')
parser.add_argument('--mode', choices=['HOMO', 'LUMO'], required=True, help='HOMO or LUMO calculation')
parser.add_argument('--disorder', type=int, default=0, help='Disorder type (0-10)')

args = parser.parse_args()

print(args.length, args.mode, args.disorder)
