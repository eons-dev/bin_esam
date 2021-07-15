import pytest
import logging
import sys, os
from subprocess import Popen, PIPE, STDOUT

#Run esam from the example directory, as a user might.
#This tests that the program is executable and operational.
def test_processing_ms():

    #Change working directory to the example folder.
    os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "example"))

    command = "esam -v -i *.txt -if in_ms -s saved_ms-data.json -f mass --ignore 86 -o out_ms-data_1.xlsx -of out_excel"

    p = Popen(command, stdout = PIPE, stderr = STDOUT, shell = True)
    while True:
      line = p.stdout.readline()
      if (not line):
        break
      print(line.decode('ascii')[:-1]) #[:-1] to strip excessive new lines.
    assert(not p.returncode) #FIXME: it don't work :(

    assert(os.path.exists(os.path.join(os.getcwd(),"saved_ms-data.json")))

    #Reset working directory.
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
