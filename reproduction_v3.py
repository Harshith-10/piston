import requests
import json
import time

URL = "http://localhost:2000/api/v3/execute"

def test_python_batch():
    print("Testing Python Batch execution...")
    payload = {
        "language": "python",
        "version": "3.12.0", # Adjust version if needed, or query /runtimes
        "files": [
            {
                "name": "main.py",
                "content": "import sys\nprint(f'Hello {sys.stdin.read().strip()}!')"
            }
        ],
        "testcases": [
            {
                "id": "1",
                "input": "User",
                "expectedOutput": "Hello User!"
            },
            {
                "id": "2",
                "input": "World",
                "expectedOutput": "Hello World!"
            }
        ]
    }
    
    try:
        response = requests.post(URL, json=payload)
        response.raise_for_status()
        data = response.json()
        print("Response:", json.dumps(data, indent=2))
        
        # Validation
        passed = True
        for tc in data['testcases']:
            if not tc['passed']:
                print(f"Testcase {tc['id']} FAILED")
                passed = False
            else:
                print(f"Testcase {tc['id']} PASSED")
        
        if passed:
            print("Python Batch Test PASSED")
        else:
            print("Python Batch Test FAILED")

    except Exception as e:
        print(f"Test failed in request: {e}")
        if 'response' in locals():
            print(response.text)

def test_v2_regression():
    print("\nTesting v2 Regression...")
    url_v2 = "http://localhost:2000/api/v2/execute"
    payload = {
        "language": "python",
        "version": "3.12.0",
        "files": [
            {
                "name": "main.py",
                "content": "print('Hello v2')"
            }
        ]
    }
    
    try:
        response = requests.post(url_v2, json=payload)
        response.raise_for_status()
        data = response.json()
        
        if data['run']['stdout'].strip() == "Hello v2":
            print("v2 Regression Test PASSED")
        else:
            print(f"v2 Regression Test FAILED: {data['run']['stdout']}")
            
    except Exception as e:
        print(f"v2 Test failed: {e}")
        if 'response' in locals():
            print(response.text)

def waitForServer():
    print("Waiting for server to be ready...")
    for i in range(30):
        try:
            requests.get("http://localhost:2000/api/v2/runtimes")
            print("Server is ready!")
            return
        except:
            time.sleep(2)
            print(".", end="", flush=True)
    print("\nServer did not become ready in time.")
    exit(1)

def test_java_batch():
    print("\nTesting Java Batch execution...")
    payload = {
        "language": "java",
        "version": "15.0.2",
        "files": [
            {
                "name": "Main.java",
                "content": "import java.util.Scanner;\npublic class Main {\n    public static void main(String[] args) {\n        Scanner scanner = new Scanner(System.in);\n        if (scanner.hasNext()) {\n            System.out.println(\"Hello \" + scanner.next() + \"!\");\n        }\n    }\n}"
            }
        ],
        "testcases": [
            {
                "id": "1",
                "input": "JavaUser",
                "expectedOutput": "Hello JavaUser!"
            },
            {
                "id": "2",
                "input": "JavaWorld",
                "expectedOutput": "Hello JavaWorld!"
            }
        ]
    }
    
    try:
        response = requests.post(URL, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Check if compile stage exists and executed successfully
        if 'compile' in data:
            print("Compilation successful.")
        else:
            print("WARNING: No compile stage info returned (Java should be compiled).")

        passed = True
        for tc in data['testcases']:
            if not tc['passed']:
                print(f"Testcase {tc['id']} FAILED. Expected: {tc['expectedOutput']}, Got: {tc['actualOutput']}")
                passed = False
            else:
                print(f"Testcase {tc['id']} PASSED")
        
        if passed:
            print("Java Batch Test PASSED")
        else:
            print("Java Batch Test FAILED")

    except Exception as e:
        print(f"Java Test failed: {e}")
        if 'response' in locals():
            print(response.text)

if __name__ == "__main__":
    waitForServer()
    test_python_batch()
    test_java_batch()
    test_v2_regression()
