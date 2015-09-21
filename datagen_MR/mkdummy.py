import sys
import subprocess
from subprocess import Popen, PIPE


files = int(sys.argv[1])
def run(cmd, output = False):
	if output == True:
		return Popen([cmd],stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True).communicate()[0].split('\n')[:-1]
	out = Popen([cmd], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True).communicate()


run('rm -rf ./dummy_files')
run('mkdir -p ./dummy_files')

[run('touch ./dummy_files/f_' + str(i)) for i in range(files)]
run('hadoop fs -rm -r -skipTrash /datagen/dummy_files/*')
run('hadoop fs -put ./dummy_files/* /datagen/dummy_files')
