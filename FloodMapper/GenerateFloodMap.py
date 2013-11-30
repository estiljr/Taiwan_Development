from subprocess import CalledProcessError, check_output

try:
    output = check_output(["ls", "non existent"])
except CalledProcessError as e:
    print(e.returncode)