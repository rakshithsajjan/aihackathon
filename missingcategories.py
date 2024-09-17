import pandas as pd
import openai
import json

df = pd.read_csv('data_usecase2.csv')


client = openai.OpenAI(api_key='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')

def categorize_and_respond(feedback):
### categorising the feedback
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that categorizes customer feedback and provides a response. For the category, use only these options: Current Account, Customer Support, Fixed Deposit, Loans, Online Banking, Savings Account. For the response, be brief and polite, either thanking them or apologizing and assuring them of action, as appropriate. Provide your output as a JSON object with 'category' and 'response' keys."},
            {"role": "user", "content": f"Categorize and respond to this feedback: {feedback}"}
        ],
        response_format={"type": "json_object"}
    )
    result = json.loads(response.choices[0].message.content)
    category = result['category']
    ai_response = result['response']

    return category, ai_response


df['Category-updated'] = ''
df['AI-Response'] = ''

for index, row in df.iterrows():
    category, ai_response = categorize_and_respond(row['Customer_Feedback'])
    df.at[index, 'Category-updated'] = category
    df.at[index, 'AI-Response'] = ai_response


df.to_csv('data_usecase2_updated.csv', index=False)

print("Processing complete. Updated CSV saved as 'data_usecase2_updated.csv'.")
