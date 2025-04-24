import requests

def send_command(command_text):

    print(command_text)

    server_url='https://giving-just-troll.ngrok-free.app/run_command'
    timeout=500

    headers = {'Content-Type': 'application/json'}
    payload = {'text': command_text.strip()}

    try:
        response = requests.post(server_url, json=payload, headers=headers, timeout=timeout)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return str(data)

        if 'output ' in data:
            return data['output']
        elif 'error ' in data:
            return data['error']
        else:
            return 'Unexpected response format.'

    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors (e.g., 400, 500)
        try:
            error_data = response.json()
            return 'error '+ error_data.get('error', str(http_err))
        except ValueError:
            # Response wasn't JSON
            return 'error '+ str(http_err)

    except requests.exceptions.Timeout:
        return 'error ' + 'Request timed out.'

    except requests.exceptions.RequestException as req_err:
        # Handle other request-related errors
        return 'error '+ str(req_err)
    

def saveCodeonServer(code:str):


    server_url='https://giving-just-troll.ngrok-free.app/save'
    timeout=500

    headers = {'Content-Type': 'application/json'}
    payload = {'text': code}
    response = requests.post(server_url, json=payload, headers=headers, timeout=timeout)
    
if __name__ == "__main__":
    user = input("Enter the command: ")

    print(send_command(user))
