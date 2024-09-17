import openai
import streamlit as st
import json



client = openai.OpenAI(api_key='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')


customer_service_teams = json.loads('''{
  "customer_service_teams": [
    {
      "team_name": "Debit Card Team",
      "responsibilities": [
        "Card activation",
        "PIN resets",
        "Lost card reporting",
        "Transaction disputes",
        "Card delivery issues"
      ]
    },
    {
      "team_name": "Credit Card Team",
      "responsibilities": [
        "Application processing",
        "Billing issues",
        "Rewards programs",
        "Credit limit adjustments",
        "Card upgrades"
      ]
    },
    {
      "team_name": "Loan Team",
      "responsibilities": [
        "Loan applications",
        "Disbursements",
        "Repayment issues",
        "Interest rate inquiries",
        "Loan account statements"
      ]
    },
    {
      "team_name": "Savings Account Team",
      "responsibilities": [
        "Account opening",
        "Balance inquiries",
        "Interest rate queries",
        "Minimum balance requirements",
        "Account statements"
      ]
    },
    {
      "team_name": "Current Account Team",
      "responsibilities": [
        "Account opening",
        "Overdraft facilities",
        "Transaction issues",
        "Cheque book requests",
        "Account management"
      ]
    },
    {
      "team_name": "Priority Account Team",
      "responsibilities": [
        "High-value customer queries",
        "Personalized services",
        "Priority transaction processing",
        "Exclusive offers management"
      ]
    },
    {
      "team_name": "Digital Banking Team",
      "responsibilities": [
        "Netbanking issues",
        "Mobile app support",
        "Online transaction problems",
        "Digital security concerns"
      ]
    },
    {
      "team_name": "Fixed Deposit (FD) Team",
      "responsibilities": [
        "FD account opening",
        "Interest rate inquiries",
        "Maturity processing",
        "Renewal requests"
      ]
    },
    {
      "team_name": "Technical Support Team",
      "responsibilities": [
        "Cross-service technical issues",
        "System downtime management",
        "App and website troubleshooting"
      ]
    },
    {
      "team_name": "Paperless Banking Team",
      "responsibilities": [
        "Digital transition support",
        "E-statement setup",
        "Paperless process inquiries"
      ]
    },
    {
      "team_name": "Customer Retention Team",
      "responsibilities": [
        "Churn risk assessment",
        "Customer satisfaction improvement",
        "Retention offer management"
      ]
    },
    {
      "team_name": "General Customer Service Team",
      "responsibilities": [
        "General inquiries",
        "Customer routing to specialized teams",
        "Basic account information"
      ]
    }
  ]
}''')

def get_chatbot_response(messages):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return response.choices[0].message.content

def route_complaint(complaint):
    prompt = f"""
given the following customer complaint or query:
"{complaint}"

and the following list of customer service teams and their responsibilities-
{json.dumps(customer_service_teams, indent=2)}

determine the most appropriate team to handle this complaint or query.Respond with only the team name.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a financial institution's complaint management assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def main():
    st.title("Complaint Management System")

    # chat history 
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a financial institution's complaint management assistant. Your task is to ask 3 questions to gather information about the user's complaint or query before routing it to the appropriate department."}
        ]
    if "question_count" not in st.session_state:
        st.session_state.question_count = 0

    # display chat history
    for message in st.session_state.messages[1:]:  # Skip the system message
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # input
    if prompt := st.chat_input("What's your complaint or question?"):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        

        with st.chat_message("user"):
            st.markdown(prompt)

        ##respo0nce
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                response = get_chatbot_response(st.session_state.messages)
                
                if st.session_state.question_count < 2:
                    st.session_state.question_count += 1
                    full_response = response
                else:
                    routed_team = route_complaint(" ".join([m["content"] for m in st.session_state.messages if m["role"] == "user"]))
                    full_response = f"Thank you for providing the information. Based on our AI analysis, your complaint has been routed to the {routed_team}."
                
            st.markdown(full_response)
        

        st.session_state.messages.append({"role": "assistant", "content": full_response})
#reset
        if st.session_state.question_count >= 3:
            st.session_state.question_count = 0
            st.session_state.messages = [st.session_state.messages[0]] 

if __name__ == "__main__":
    main()
