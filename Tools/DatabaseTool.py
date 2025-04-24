from pgvector.psycopg2 import register_vector
import psycopg2
from openai import OpenAI
client = OpenAI()

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding
# conn = psycopg2.connect("dbname=ImgVec user=postgres password=root")
# cur = conn.cursor()
# register_vector(conn)

text = "hii"
print(len(get_embedding(text, model="text-embedding-3-small")))
