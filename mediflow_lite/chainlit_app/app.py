import chainlit as cl
import requests
import json
from typing import Dict, List
import ollama  # Import the ollama library

API_BASE_URL = "http://localhost:8081/api/"
OLLAMA_API_URL = "http://localhost:11434"  # Replace with your Ollama API URL
OLLAMA_MODEL = "llama3.1"  # Replace with your specific model name

@cl.on_chat_start
async def start():
    cl.user_session.set("authenticated", False)
    await cl.Message(content="Welcome to MediFlow Lite! Please enter your username to log in.").send()

@cl.on_message
async def main(message: str):
    if not cl.user_session.get("authenticated"):
        await handle_authentication(message)
    else:
        await handle_command(message)

async def handle_authentication(message: str):
    try:
        response = requests.post(f"{API_BASE_URL}auth/login/", json={"username": message})
        response.raise_for_status()
        user_data = response.json()
        cl.user_session.set("authenticated", True)
        cl.user_session.set("username", user_data['username'])
        cl.user_session.set("user_id", user_data['id'])
        await cl.Message(f"Welcome, {user_data['username']}! How can I assist you today? You can ask about appointments, medical records, or general health advice.").send()
    except requests.RequestException as e:
        await cl.Message(f"Authentication failed. Error: {str(e)}").send()

async def handle_command(message: str):
    if "appointment" in message.lower():
        if "book" in message.lower() or "schedule" in message.lower():
            await book_appointment()
        else:
            appointments = get_appointments()
            await display_appointments(appointments)
    elif "medical record" in message.lower():
        records = get_medical_records()
        await display_medical_records(records)
    else:
        # If it's not about appointments or medical records, treat it as a health advice query
        await provide_health_advice(message)

async def book_appointment():
    doctors = get_doctors()
    elements = [
        cl.Select(
            id="doctor",
            label="Select a doctor",
            values=[{"label": f"Dr. {d['user']['username']} - {d['specialty']}", "value": str(d['id'])} for d in doctors],
            placeholder="Choose your doctor",
        ),
        cl.DateTimeInput(id="appointment_time", label="Select appointment date and time"),
        cl.Text(id="reason", label="Reason for appointment", placeholder="Brief description of your visit"),
    ]
    await cl.Message(content="Please provide the following details to book your appointment:", elements=elements).send()

    response = await cl.AskActionMessage(
        content="Confirm your appointment details:",
        actions=[
            cl.Action(name="confirm", value="confirm", label="Confirm Appointment"),
            cl.Action(name="cancel", value="cancel", label="Cancel"),
        ],
    ).send()

    if response.get("value") == "confirm":
        appointment_data = {
            "doctor": int(response['data']['doctor']),
            "date_time": response['data']['appointment_time'],
            "reason": response['data']['reason'],
            "patient": cl.user_session.get("user_id")  # Assuming you store user_id in the session
        }
        try:
            api_response = requests.post(f"{API_BASE_URL}appointments/", json=appointment_data)
            api_response.raise_for_status()
            await cl.Message("Your appointment has been booked successfully!").send()
        except requests.RequestException as e:
            await cl.Message(f"Failed to book appointment. Error: {str(e)}").send()
    else:
        await cl.Message("Appointment booking cancelled.").send()

async def display_appointments(appointments: List[Dict]):
    if not appointments:
        await cl.Message("You have no upcoming appointments.").send()
    else:
        message = "Your upcoming appointments:\n\n"
        for apt in appointments:
            message += f"- Date: {apt['date_time']}\n  Doctor: {apt['doctor']}\n  Reason: {apt['reason']}\n\n"
        await cl.Message(content=message).send()

async def display_medical_records(records: List[Dict]):
    if not records:
        await cl.Message("You have no medical records on file.").send()
    else:
        message = "Your medical records:\n\n"
        for record in records:
            message += f"- Date: {record['date']}\n  Doctor: {record['doctor']}\n  Notes: {record['notes']}\n\n"
        await cl.Message(content=message).send()

async def provide_health_advice(query: str):
    try:
        # Prepare the request payload
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": f"Provide health advice for: {query}",
            "max_tokens": 150  # Adjust as needed
        }

        # Send a request to the Ollama API
        response = requests.post(f"{OLLAMA_API_URL}/generate", json=payload)
        response.raise_for_status()  # Raise an error for bad responses

        # Extract the generated advice from the response
        advice = response.json().get("response", "No advice generated.")

        # Send the advice back to the user
        await cl.Message(content=f"Regarding your query about '{query}':\n\n{advice}").send()

    except requests.RequestException as e:
        error_message = f"I'm sorry, I couldn't process your request. Error: {str(e)}"
        await cl.Message(content=error_message).send()

def get_appointments() -> List[Dict]:
    try:
        response = requests.get(f"{API_BASE_URL}appointments/")
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching appointments: {e}")
        return []

def get_medical_records() -> List[Dict]:
    try:
        response = requests.get(f"{API_BASE_URL}medical-records/")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching medical records: {e}")
        return []

def get_doctors() -> List[Dict]:
    try:
        response = requests.get(f"{API_BASE_URL}doctors/")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching doctors: {e}")
        return []

if __name__ == "__main__":
    cl.run()