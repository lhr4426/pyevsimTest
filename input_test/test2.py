import subprocess as sp

proc = sp.Popen(['dotnet', 'run', '--project', '/Users/hyerim_lee/Documents/gits/pyevsimTest/process_test'])

while proc.poll() is None :
    print("Running", end="\r")
print("\n")
print(proc.poll())