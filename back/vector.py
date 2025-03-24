import faiss
import numpy as np
import sqlite3
from sentence_transformers import SentenceTransformer

#DB情報
dbname = "Llama3.db"
table_object = "object"
table_method = "method"
table_dataset = "dataset"

#DB接続
def db_conect():
    with sqlite3.connect(dbname) as conn:
        return conn

#データ読み込み
def insert_data():
  conn = db_conect()
  cur = conn.cursor()
  cur.execute("SELECT id,name FROM object")
  listtemp=cur.fetchall()
  faq_ids, faq_items = zip(*listtemp) #リストをIDとテキストに分ける
  return faq_ids, faq_items

#文章の埋め込みの作成
def compute_faq_embeddings(faq_questions, model):
  return np.array(model.encode(faq_questions)) #model.encodeで文字列をベクトル化する

#Faissインデックスの作成　Faissとはベクトル専用のデータベース
def create_faiss_index(model, embeddings, doc_ids):
  dimension = model.get_sentence_embedding_dimension() #ベクトルの次元を獲得
  index_flat = faiss.IndexFlatIP(dimension) #指定次元のベクトルを格納するFaissを整備.ベクトルの距離（コサイン）を計算できるよう初期化
  index = faiss.IndexIDMap(index_flat) #IDをベクトルに付与する（マッピング）
  index.add_with_ids(embeddings, doc_ids) #実際に文書のベクトルにIDを振ってデータベースに格納
  #indexをローカルに保存
  faiss.write_index(index, "index_file.index")
  print("succsess")

#＜実行部分＞
#modelの読み込み
model = SentenceTransformer("sentence-transformers/paraphrase-distilroberta-base-v1")

#データ読み込み、ベクトル化
faq_ids, faq_items = insert_data()
faq_embeddings = compute_faq_embeddings(faq_items, model) #各文をベクトル化

# Faissインデックスを作成
create_faiss_index(model, faq_embeddings, faq_ids) #Faissデータベースに文ベクトルを格納