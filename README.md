# Demo for Messaging App with End-to-End Encryption

## Set up

## Set up

1. Create a virtual environment
2. Install the required packages: 

```bash
pip install -r requirements-project.txt
```

## Run the project

1. Run the server at port 8766:

```bash
python server.py
```

2. Generate the client's private and public keys:

```bash
python keygen.py <username>
```

3. Run the client:

  - Run in non-encrypted mode to test the hash-checking mode:

	```bash
	python client.py --no-encrypt --server-port=8766
	```

  - Run in encrypted mode:

	```bash
	python client.py --server-port=8766
	```

4. Test the man-in-the-middle attack:

  ```bash
  # Run the mitm script at port 8765
  python mitm.py

  # Run the client and point to port 8765
  python client.py --server-port=8765
  ```

## Demo


https://github.com/truonghm/encryption_chat_app/assets/10404416/0cdca4bf-b199-4cbf-ac4f-6f2e79180da3


