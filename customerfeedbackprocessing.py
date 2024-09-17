import pandas as pd
import openai
import json

df = pd.read_csv('data_usecase2.csv')


client = openai.OpenAI(api_key'')

def categorize_and_respond(feedback):
### categorising the feedback
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that categorizes customer feedback, provides a response, analyzes sentiment, and extracts insights. For the category, use only these options: Current Account, Customer Support, Fixed Deposit, Loans, Online Banking, Savings Account. For the response, be brief and polite, either thanking them or apologizing and assuring them of action, as appropriate. Provide your output as a JSON object with 'category', 'response', 'sentiment', 'insights', and 'dissatisfaction_points' keys. The sentiment should be a number from 0 to 10, where 0 is extremely negative and 10 is extremely positive."},
            {"role": "user", "content": f"Analyze this feedback: {feedback}"}
        ],
        response_format={"type": "json_object"}
    )
    result = json.loads(response.choices[0].message.content)
    category = result['category']
    ai_response = result['response']
    sentiment = result['sentiment']
    insights = result['insights']
    dissatisfaction_points = result['dissatisfaction_points']
    print("Category:", category)
    print("AI Response:", ai_response)
    print("Sentiment:", sentiment)
    print("Insights:", insights)
    print("Dissatisfaction Points:", dissatisfaction_points)
    print("--------------------")

    return category, ai_response, sentiment, insights, dissatisfaction_points


df['Category-updated'] = ''
df['AI-Response'] = ''
df['Sentiment'] = ''
df['Insights'] = ''
df['Dissatisfaction_Points'] = ''
for index, row in df.iterrows():
    if index >= 50:
        break
    # Add a counter to track progress
    if index % 10 == 0:
        print(f"Processing feedback {index + 1} of {len(df)}")
    category, ai_response, sentiment, insights, dissatisfaction_points = categorize_and_respond(row['Customer_Feedback'])
    df.at[index, 'Category-updated'] = category
    df.at[index, 'AI-Response'] = ai_response
    df.at[index, 'Sentiment'] = sentiment
    df.at[index, 'Insights'] = insights
    df.at[index, 'Dissatisfaction_Points'] = dissatisfaction_points

df.to_csv('data_usecase2_updated.csv', index=False)

print("Processing complete. Updated CSV saved as 'data_usecase2_updated.csv'.")
