import argparse,os
import subprocess
from shutil import copy, copytree, rmtree

if __name__ == "__main__":

	my_parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
	my_parser.add_argument('--compiler',
						   help='specify the compiler, you want to use to compile')
	my_parser.add_argument('--target_platform',
						   help='specify the platform, you want to go build for')
	my_parser.add_argument("-run_tests", help="should tests be run", default="False")
	my_parser.add_argument("-download_godot", help="should tests be run", default="False")
	# Execute parse_args()
	args = my_parser.parse_args()

	try:
		res = subprocess.Popen(f"cd submodules/py4godot &&"
							   f"build.py --target_platform={args.target_platform} "
							   f"--compiler={args.compiler} -run_tests={args.run_tests} -download_godot={args.download_godot} " ,
							   shell=True)
		res.wait()
	except Exception as e:
		print(e)

	if os.path.exists(f"addons/{args.target_platform}"):
		rmtree(f"addons/{args.target_platform}")
	copytree(f"submodules/py4godot/build/addons/{args.target_platform}", f"addons/{args.target_platform}")
