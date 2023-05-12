import openai
import json

# OpenAI API key
with open("setting.json") as f:
    data = json.load(f)
    openai.api_key = data["OpenAIKey"]


def generate_sql_query(search_type: str = None, query: str = None, selected_region: str = None):
    if query is None:
        return ''

    prompt = f"### HouseWebsite SQL tables, with their properties:" \
             f"#" \
             f"# post(pId, uId, title, city, district, address, name, phone, description, reviseDateTime)" \
             f"# house(hId, pId, type, twPing, floor, lived, bedRoom, livingRoom, restRoom, balcony)" \
             f"# houserent(hId, price, refrigerator, washingMachine, TV, airCondition, waterHeater, bed, closet, " \
             f"            paidTVChannel, internet, gas, sofa, deskChair, balcony, elevator, parkingSpace)" \
             f"# housesell(hId, ratioOfPubicArea, pricePerTwping, price, age, houseType, houseName)" \
             f"#" \
             f"### A query to {query}"

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message
