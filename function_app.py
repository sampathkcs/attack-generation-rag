import azure.functions as func
from openai import OpenAI
import pandas as pd
import json
import requests
import logging
from langchain_community.vectorstores import Chroma, FAISS
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.docstore.document import Document

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Helper function to generate cyber attack descriptions
def generate_cyber_attack_descriptions(example_attack, num_attacks):
    openai_api_key = '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'  # Replace with your actual key

    prompt = f'''Generate {num_attacks} realistic cyber attack descriptions for vehicles similar to the below example with at least 20 words :
    
Example:
{example_attack}

1.
'''

    # Request the generation of attack descriptions
    client = OpenAI(api_key = openai_api_key)
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",  # Adjust the model version as needed
        prompt=prompt,
        temperature=0.7,  # Adjust for creativity. Lower is more deterministic.
        max_tokens=150 * num_attacks,  # Adjust based on desired length of responses
        n=num_attacks,  # Number of responses (each with multiple attack descriptions)
        stop="2."  # Stops generating more text at each new line, to separate the attacks
    )
    
    # Extract and return the generated descriptions as a list
    # Splitting responses into individual attacks
    # print(response.choices[0].text)
    # print(type(response.choices))
    # generated_attacks = response["choices"]
    generated_attacks = [choice.text for choice in response.choices]
    print(len(generated_attacks))
    attacks = []
    for i, text in enumerate(generated_attacks):
        attacks.append({
                        "id":i,
                        "text":text
                      })
    return attacks  # Filtering out empty strings



pages = [Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 0}, page_content='Abuse of privileges by staff (insider attack)  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 1}, page_content='Unauthorized internet access to the server (enabled for example by backdoors, unpatched \nsystem software vulnerabilities, SQL attacks or other means)  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 2}, page_content='Unauthorized physical access to the server (conducted by for example USB sticks or other \nmedia connecting to the server)  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 3}, page_content='Attack on back -end server stops it functioning, for example it prevents it from interacting with \nvehicles and providing services they rely on  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 4}, page_content='Abuse of privileges by staff (in sider attack)  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 5}, page_content='Loss of information in the cloud. Sensitive data may be lost due to attacks or accidents when \ndata is stored by third -party cloud service providers  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 6}, page_content='Unauthorized internet access to the server (enabled for example by backdoors, unpatched \nsystem software vulnerabilities, SQL attacks or other means)  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 7}, page_content='Unauthorized physical access to the server (conducted for example by USB sticks or other \nmedia connecting to the server)  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 8}, page_content='Information breach by unintended sharing of data (e.g. admin errors)  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 9}, page_content='Spoofing of messages by impersonation (e.g. 802.11p V2X during platooning, GNSS \nmessages, etc.)  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 10}, page_content='Sybil attack (in order to spoof other vehicles as if there are many vehicles on the road)  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 11}, page_content='Communications channels permit code injection, for example tampered  software binary \nmight be injected into the communication stream  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 12}, page_content='Communications channels permit manipulate of vehicle held data/code  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 13}, page_content='Communications channels permit overwrite of vehicle held data/code  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 14}, page_content='Communications channels permit erasure of vehicle held data/code  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 15}, page_content='Communications channels permit introduction of data/code to the vehicle (write data code)  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 16}, page_content='Accepting information from an unreliable or untrusted source  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 17}, page_content='Man in the middle attack/ session hijacking  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 18}, page_content='Replay attack, for example an attack against a communication gateway allows the attacker \nto downgrade software of an ECU or firmware of the gateway  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 19}, page_content='Interception of information / interfering radiations / monitoring communications  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 20}, page_content='Gaining unauthorized ac cess to files or data  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 21}, page_content='Sending a large number of garbage data to vehicle information system, so that it is unable to \nprovide services in the normal manner  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 22}, page_content='Black hole attack, in order to disrupt communication between vehicles the attacker is able to \nblock messages between the vehicles  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 23}, page_content='An unprivileged user is able to gain privileged access, for example root access  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 24}, page_content='Virus embedded in communication media infects vehicle systems  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 25}, page_content='Malicious internal (e.g. CAN) messages  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 26}, page_content='Malicious V2X messages, e.g. infras tructure to vehicle or vehicle -vehicle messages (e.g. \nCAM, DENM)  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 27}, page_content='Malicious diagnostic messages  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 28}, page_content='Malicious proprietary messages (e.g. those normally sent from OEM or \ncomponent/system/function supplier)  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 29}, page_content='Compromise of over the air software update procedures. This includes fabricating the \nsystem update program or firmware  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 30}, page_content='Compromise of local/physical software update procedures. This includes fabricating the \nsystem update program or firmware  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 31}, page_content='The software is manipulated before the update process ( and is therefore corrupted), \nalthough the update process is intact  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 32}, page_content='Compromise of cryptographic keys of the software provider to allow invalid update  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 33}, page_content='Denial of Service attack against update server or network to prevent rollout of critical \nsoftware updat es and/or unlock of customer specific features  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 34}, page_content='Innocent victim (e.g. owner, operator or maintenance engineer) being tricked into taking an \naction to unintentionally load malware or enable an attack  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 35}, page_content='Defined security procedures are not followed  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 36}, page_content='Manipul ation of functions designed to remotely operate systems, such as remote key, \nimmobilizer, and charging pile  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 37}, page_content='Manipulation of vehicle telematics (e.g. manipulate temperature measurement of sensitive \ngoods, remotely unlock cargo doors)  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 38}, page_content='Interference with s hort range wireless systems or sensors  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 39}, page_content='Corrupted applications, or those with poor software security, used as a method to attack \nvehicle systems  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 40}, page_content='External interfaces such as USB or other ports used as a point of attack, for example \nthrough code injection  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 41}, page_content='Media infected with a virus connected to a vehicle system  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 42}, page_content='Diagnostic access (e.g. dongles in OBD port) used to facilitate an attack, e.g. manipulate \nvehicle parameters (directly or indirectly)  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 43}, page_content='Extraction of copyright or proprietary software from veh icle systems (product piracy)  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 44}, page_content='Unauthorized access to the owner ’s privacy information such as personal identity, payment \naccount information, address book information, location information, vehicle ’s electronic ID, \netc. \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 45}, page_content='Extraction of cryptographic keys  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 46}, page_content='Illegal/unauthorized changes to vehicle ’s electronic ID  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 47}, page_content='Identity fraud. For example, if a user wants to display another identity when communicating \nwith toll systems, manufacturer backend  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 48}, page_content='Action to circumvent monitoring systems (e.g. hacking/ tamperi ng/ blocking of messages \nsuch as ODR Tracker data, or number of runs)  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 49}, page_content='Data manipulation to falsify vehicle ’s driving data (e.g. mileage, driving speed, driving \ndirections, etc.)  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 50}, page_content='Unauthorized changes to system diagnostic data  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 51}, page_content='Unauthorized deletion/man ipulation of system event logs  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 52}, page_content='Introduce malicious software or malicious software activity  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 53}, page_content='Fabrication of software of the vehicle control system or information system  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 54}, page_content='Denial of service, for example this may be triggered on the internal network by flo oding a \nCAN bus, or by provoking faults on an ECU via a high rate of messaging  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 55}, page_content='Unauthorized access of falsify the configuration parameters of vehicle ’s key functions, such \nas brake data, airbag deployed threshold, etc.  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 56}, page_content='Unauthorized access of falsify th e charging parameters, such as charging voltage, charging \npower, battery temperature, etc.  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 57}, page_content='Combination of short encryption keys and long period of validity enables attacker to break \nencryption  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 58}, page_content='Insufficient use of cryptographic algorithms to protect sensitive systems  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 59}, page_content='Using already or soon to be deprecated cryptographic algorithms  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 60}, page_content='Hardware or software, engineered to enable an attack or fails to meet design criteria to stop \nan attack  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 61}, page_content='Software bugs. The presence of software bugs can be a ba sis for potential exploitable \nvulnerabilities. This is particularly true if software has not been tested to verify that known \nbad code/bugs is not present and reduce the risk of unknown bad code/bugs being present  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 62}, page_content='Using remainders from development (e.g. debug ports, JTAG ports, microprocessors, \ndevelopment certificates, developer passwords, …) can permit access to ECUs or permit \nattackers to gain higher privileges  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 63}, page_content='Superfluous internet ports left open, providing access to network systems  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 64}, page_content='Circumvent net work separation to gain control. Specific example is the use of unprotected \ngateways, or access points (such as truck -trailer gateways), to circumvent protections and \ngain access to other network segments to perform malicious acts, such as sending arbitrar y \nCAN bus messages  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 65}, page_content='Information breach. Personal data may be leaked when the car changes user (e.g. is sold or \nis used as hire vehicle with new hirers)  \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n '),
 Document(metadata={'source': 'temp_pdf_file.pdf', 'page': 66}, page_content='Manipulation of electronic hardware, e.g. unauthorized electronic hardware added to a \nvehicle to enab le "man -in-the-middle" attack  ')]

# Helper function to vector database
def load_vector_db():
    # pdf_file_path = 'Anex5 sce for mitigation spaces.pdf'
    pdf_url = "https://attackgeneration.blob.core.windows.net/data/Anex5%20sce%20for%20mitigation%20spaces.pdf?sp=r&st=2024-09-29T04:40:05Z&se=2024-09-29T12:40:05Z&spr=https&sv=2022-11-02&sr=b&sig=0UAf%2BOEfL8gA0reFqIgrHhRbzpTq6PsEOwaeBBQBiJs%3D"
    
    #file path
    # file_path = (
    #     pdf_file_path
    # )
    # logging.info('PDF loading...')
    # # Download the PDF
    # response = requests.get(pdf_url)
    # pdf_path = "temp_pdf_file.pdf"

    # with open(pdf_path, "wb") as f:
    #     f.write(response.content)

    # loader = PyPDFLoader(pdf_path)
    # pages = loader.load_and_split()
    # logging.info('PDF loaded')

    # save to disk
    try:
        #vector_store = Chroma.from_documents(documents=pages, embedding=FastEmbedEmbeddings(),persist_directory="attacks_vector_store_db")
        # vector_store = Chroma.from_documents(documents=pages, embedding=FastEmbedEmbeddings())
        vector_store = FAISS.from_documents(documents=pages, embedding=FastEmbedEmbeddings())
        logging.info('Vector DB loaded')
    except Exception as e:
        logging.error(f"Error while loading Vector DB: {e}")

    return vector_store



# routes for attack generation and mitigation
@app.route(route="attack_generation", methods=["POST"])
def attack_generation(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing request to generate cyber attacks.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid request body.", status_code=400)

    example_attack = req_body.get("example_attack")
    num_attacks = req_body.get("num_attacks", 3)

    if not example_attack:
        return func.HttpResponse("Missing 'example_attack' in request.", status_code=400)

    try:
        attack_descriptions = generate_cyber_attack_descriptions(example_attack, num_attacks)
        # wrap json
        attack_descriptions_json = json.dumps({"attacks": attack_descriptions})
        return func.HttpResponse(attack_descriptions_json, status_code=200, mimetype="application/json")
    except Exception as e:
        logging.error(f"Error generating attack descriptions: {e}")
        return func.HttpResponse(f"Error generating attacks: {str(e)}", status_code=500)




@app.route(route="retrieve_mitigation", methods=["POST"])
def retrieve_mitigation(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing request to retrieve mitigation actions.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid request body.", status_code=400)

    selected_attack = req_body.get("selected_attack")
    logging.info(f'Selected Attack: {selected_attack}')
    if not selected_attack:
        return func.HttpResponse("Missing 'selected_attack' in request.", status_code=400)

    # Load vector store and mitigation CSV
    vector_store = load_vector_db()
    retriever = vector_store.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 3, "score_threshold": 0.5})
    

    docs = retriever.invoke(selected_attack)
    csv_path = "https://attackgeneration.blob.core.windows.net/data/Mitigation.csv?sp=r&st=2024-10-02T03:22:32Z&se=2025-12-31T11:22:32Z&spr=https&sv=2022-11-02&sr=b&sig=LNCYq3QexNAvXXjgDiEfGf6SNgsdRLr1VZMc9oviEx8%3D"
    df = pd.read_csv(csv_path, header=2)

    # Process the attack descriptions and mitigation data
    most_similar = docs[0].page_content.strip().lower().replace(" ", "").replace('\n', '')
    logging.info(f'Most Similar Doc: {most_similar}')
    df['Threat_Description'] = df['Threat_Description'].str.strip().str.lower().str.replace(" ", "").str.replace('\n', '')

    matched_row = df[df['Threat_Description'] == most_similar]
    if not matched_row.empty:
        mitigation_measure = matched_row['Mitigation'].iloc[0]
        # wrap json
        mitigation_measure_json = json.dumps({"mitigation": mitigation_measure})
        return func.HttpResponse(mitigation_measure_json, status_code=200)
    else:
        return func.HttpResponse("No matching threat description found.", status_code=404)