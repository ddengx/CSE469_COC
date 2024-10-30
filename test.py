import subprocess
import pytest
import os

def test_7(): #Add before init
    command = [
        "python", "bchoc.py", "add",
        "-c", "96f8a16d-0ee0-4aab-a521-a5e18603ab3a",
        "-i", "639500777",
        "-g", "v3RQMNZ72xYR",
        "-p", "C67C"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, f"Command failed: {result.stderr}"

def test_9(): #add with one case_id and multiple item_id values and status of the added item is CHECKEDIN
    command = [
        "python", "bchoc.py", "add",
        "-c", "5392071e-33be-46f8-bcef-fa1871458b16",
        "-i", "910371498", "-i", "4258990830",
        "-i", "387371749", "-i", "2714951576",
        "-i", "1542751280", "-i", "3953079798",
        "-i", "1923752865", "-i", "2791599009",
        "-i", "150319388",
        "-g", "WIvRiPMJB74n",
        "-p", "C67C"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, f"Command failed: {result.stderr}"
    

def test_12(): # add with duplicate item_id given
    command = [
        "python", "bchoc.py", "add",
        "-c", "773adce6-d369-473c-9b0d-9f666547c408",
        "-i", "1749301816",
        "-g", "IbkdqkGYjH9H",
        "-p", "C67C"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, f"Command failed: {result.stderr}"


def test_13(): #checkout after add
    command = [
        "python", "bchoc.py", "add",
        "-c", "caeae3e4-7979-4017-ae9e-ac0e66b4c773",
        "-i", "2293809361",
        "-g", "2jaRPY9FZpl9",
        "-p", "C67C"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, f"Command failed: {result.stderr}"


def test_14(): #checkin after checkout after add 
    command = [
        "python", "bchoc.py", "add",
        "-c", "5073baa2-f560-4f33-9d89-7bccdc350082",
        "-i", "4199380210",
        "-g", "OcdiWkM4Jo7n",
        "-p", "C67C"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, f"Command failed: {result.stderr}"

def test_15(): #checkin after add
    command = [
        "python", "bchoc.py", "add",
        "-c", "e39c4819-b7a3-4b51-873f-cecbb00fbb23",
        "-i", "3821954945",
        "-g", "ztr1PWLqKSxi",
        "-p", "C67C"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, f"Command failed: {result.stderr}"

def test_16(): #checkin after checkin after checkout after add
    command = [
        "python", "bchoc.py", "add",
        "-c", "7be452d7-c491-4c57-ac5c-12dea222b0df",
        "-i", "402862220",
        "-g", "MezmOHB60kZ2",
        "-p", "C67C"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, f"Command failed: {result.stderr}"

def test_17(): #checkout before add
    command = [
        "python", "bchoc.py", "checkout",
        "-i", "2557457204",
        "-p", "E69E"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, f"Command failed: {result.stderr}"

def test_18(): #checkin nefore add
    command = [
        "python", "bchoc.py", "checkin",
        "-i", "3007959291",
        "-p", "A65A"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, f"Command failed: {result.stderr}"

def test_19(): #checkin after remove
    command = [
        "python", "bchoc.py", "add",
        "-c", "f1fb3bb5-c66a-4487-8f6a-31f41f9ad3a8",
        "-i", "787649745",
        "-g", "LewPUsGRjeTP",
        "-p", "C67C"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, f"Command failed: {result.stderr}"

def test_20(): #checkout after remove
    command = [
        "python", "bchoc.py", "add",
        "-c", "ce88b925-8444-4145-ab3e-5beb14717d0a",
        "-i", "4098351831",
        "-g", "0mv5iWihn7xN",
        "-p", "C67C"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, f"Command failed: {result.stderr}"

def test_24(): #remove after checkin
    command = [
        "python", "bchoc.py", "add",
        "-c", "71ac4e71-4edd-4604-a258-a932fdf248c3",
        "-i", "1952679836",
        "-g", "0fqylDFvlaCp",
        "-p", "C67C"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, f"Command failed: {result.stderr}"
