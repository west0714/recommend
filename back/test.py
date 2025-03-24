import sqlite3
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from collections import defaultdict

#DB情報
dbname = "Llama3.db"
table_object = "object"
table_method = "method"
table_dataset = "dataset"

#DB接続
def db_conect():
    with sqlite3.connect(dbname) as conn:
        return conn
    
#model準備
def model_prepare():
    return SentenceTransformer("sentence-transformers/paraphrase-distilroberta-base-v1")
    
#クエリ処理
def search_faq(query, model, index, k):
  query_embedding = model.encode([query]) #質問文をベクトル化
  distances, indices = index.search(np.array(query_embedding), k) #Faissデータベースから類似している文のトップ3を取得．kはトップkまで取得する意味
  return indices[0]

#結果の取得
def get_faq_results(faq_ids):
  conn = db_conect()
  cur = conn.cursor()
  cur.execute("SELECT file,name FROM object WHERE id IN ({})".format(",".join("?" * len(faq_ids))), faq_ids)#結果をデータベースから取得
  return cur.fetchall() 

#取得した文と同じ論文の要素を読み込み
def load_data(id_lst,table):
  lst = [] #idと中身
  conn = db_conect()
  cur = conn.cursor()
  # プレースホルダをリストの要素数に応じて生成
  placeholders = ', '.join(['?'] * len(id_lst))
  data = f'SELECT file,name FROM {table} WHERE file IN ({placeholders})'
  cur.execute(data, id_lst)
  rows = cur.fetchall()
  for row in rows:
    lst.append(row)
  return lst

#論文IDで呼び出しやすいようにdict型に
def load_data_dict(lst):
  #detaset内で同じidをまとめる
  connect_item = []
  # 要素をまとめるための辞書を作成
  result = defaultdict(list)
  # データをループして辞書に追加
  for key, value in lst:
    result[key].append(value)
  # 辞書をリストに変換
  connect_item = [[key, values] for key, values in result.items()]
  #connect_itemをdict型に
  item_dict = {}
  for item in connect_item:
    item_dict[item[0]] = item[1]
  return item_dict

#recomend
def recomend(id_lst,objective_dict,dataset_dict,method_dict):
  rows = []
  for id in id_lst:
    objective = objective_dict[id]
    dataset = dataset_dict[id]
    method = method_dict[id]
    rows.append([id, objective, method, dataset])
  return rows


#実行部分
model = model_prepare()
loaded_index = faiss.read_index("index_file.index") #index読み込み
k = 3
query = "predict stock price"
indices = search_faq(query, model, loaded_index, k)
new_indices = [int(i) for i in indices]
results = get_faq_results(new_indices)

#print(results)

id_lst =[] #類似したもののid
objective_dict = {} #idとocjective
for i in results:
    id = i[0]
    content = i[1]
  #類似したもののidと中身をリストに保存
    objective_dict[id] = content
    id_lst.append(id)

#同じ論文の要素を取得
lst_dataset = load_data(id_lst,table_dataset)
lst_method = load_data(id_lst,table_method)


#論文IDで呼び出しやすいようにdict型に
dataset_dict = load_data_dict(lst_dataset)
method_dict = load_data_dict(lst_method)

#recomed
rows = recomend(id_lst,objective_dict,dataset_dict,method_dict)