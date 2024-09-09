import logging

def handle_response(mysock):
    try:
        response_data = []
        while True:
            data = mysock.recv(512)
            if len(data) < 1:
                break
            response_data.append(data.decode())
        
        mysock.close()
        logging.info("Response received and socket closed.")
        return ''.join(response_data)
    except Exception as e:
        logging.error(f"Error handling response: {e}")
        raise