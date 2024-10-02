import requests
import json

# Azure Function URLs (replace with your actual local or deployed function URLs)
generate_attack_url = "https://attack-generation.azurewebsites.net/api/attack_generation?code=10q-BOc6xTrwZuI3Z8gRX14qUHlk5mW0wouXFfM8aIGfAzFuRrz_5w%3D%3D"  # Adjust based on your local setup
retrieve_mitigation_url = "https://attack-generation.azurewebsites.net/api/retrieve_mitigation?code=10q-BOc6xTrwZuI3Z8gRX14qUHlk5mW0wouXFfM8aIGfAzFuRrz_5w%3D%3D"  # Adjust based on your local setup

# Test data for generating cyber attacks
example_attack = "Attacker uses the OBD port and Local Diagnostics Write Function to Modify Existing ECU Firmware to alter vehicle configuration"
num_attacks = 5

# Prepare the JSON payload for generating cyber attacks
generate_attack_payload = {
    "example_attack": example_attack,
    "num_attacks": num_attacks
}

# Test generating cyber attacks
def test_generate_attacks():
    print("Testing generate_attacks function...")

    try:
        response = requests.post(generate_attack_url, json=generate_attack_payload)
        if response.status_code == 200:
            print("Success! Generated cyber attacks:")
            print(response.json())
            print(type(response.json()))
            attacks = response.json()["attacks"]
            print(len(attacks))
        else:
            print(f"Failed with status code {response.status_code}.")
            print(response.text)
    except Exception as e:
        print(f"Error during request: {e}")




# Test data for retrieving mitigation actions
attacks_list = [{'id': 0, 'text': "A hacker gains access to a vehicle's on-board computer system through a compromised mobile app and is able to remotely control various functions, including the steering and braking systems.\n\n"}, 
                {'id': 1, 'text': "\nAttacker exploits weaknesses in the vehicle's wireless communication system to remotely access and manipulate critical systems, causing the vehicle to malfunction.\n\n"}, 
                {'id': 2, 'text': "Attackers exploit a vulnerability in the vehicle's keyless entry system to remotely unlock and start the vehicle without authorization.\n\n"}, 
                {'id': 3, 'text': "Attacker exploits the wireless communication system to gain remote access to the vehicle's infotainment system and manipulate navigation settings.\n\n"}, 
                {'id': 4, 'text': "An attacker gains access to a vehicle's Bluetooth system and uses it to remotely disable the brakes and steering controls.\n\n"}]

selected_attack = attacks_list[0]["text"]

# Prepare the JSON payload for retrieving mitigation actions
retrieve_mitigation_payload = {
    "selected_attack": selected_attack
}



# Test retrieving mitigation actions
def test_retrieve_mitigation():
    print("Testing retrieve_mitigation function...")

    try:
        response = requests.post(retrieve_mitigation_url, json=retrieve_mitigation_payload)
        if response.status_code == 200:
            print("Success! Retrieved mitigation action:")
            response = response.json()
            print(response)
            print(type(response))
        elif response.status_code == 404:
            print("No matching threat description found.")
        else:
            print(f"Failed with status code {response.status_code}.")
            print(response.text)
    except Exception as e:
        print(f"Error during request: {e}")

# Run tests
if __name__ == "__main__":
    test_generate_attacks()
    test_retrieve_mitigation()
