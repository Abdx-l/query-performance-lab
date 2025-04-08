import argparse,json,os
from pathlib import Path
import psycopg
QUERIES=[
 "SELECT c.id,count(*) FROM customers c JOIN orders o ON c.id=o.customer_id JOIN items i ON i.order_id=o.id WHERE c.id<100 GROUP BY c.id",
 "SELECT customer_id,sum(total) FROM orders GROUP BY customer_id HAVING sum(total)>5000",
 "SELECT * FROM orders WHERE created_at BETWEEN '2025-03-01' AND '2025-03-07'",
 "SELECT * FROM customers WHERE lower(name) LIKE 'customer 12%'",
 "SELECT c.id FROM customers c WHERE EXISTS(SELECT 1 FROM orders o WHERE o.customer_id=c.id AND o.total>900)"
]
def seed(db,customers,orders):
 if customers<1 or orders<1:raise ValueError("positive sizes required")
 db.execute("DROP TABLE IF EXISTS items,orders,customers CASCADE")
 db.execute("CREATE TABLE customers(id integer PRIMARY KEY,name text NOT NULL)")
 db.execute("CREATE TABLE orders(id integer PRIMARY KEY,customer_id integer REFERENCES customers,created_at date,total numeric)")
 db.execute("CREATE TABLE items(id bigint PRIMARY KEY,order_id integer REFERENCES orders,quantity integer)")
 db.execute("INSERT INTO customers SELECT i,'Customer '||i FROM generate_series(1,%s) i",(customers,))
 db.execute("INSERT INTO orders SELECT i,1+(i*37 %% %s),date '2025-01-01'+(i %% 365),(i*13 %% 1000) FROM generate_series(1,%s) i",(customers,orders))
 db.execute("INSERT INTO items SELECT i,1+((i-1) %% %s),1+(i %% 5) FROM generate_series(1,%s) i",(orders,orders*5))
 db.execute("ANALYZE")
def benchmark(db,stage):
 Path("results").mkdir(exist_ok=True)
 for i,q in enumerate(QUERIES):
  plan=db.execute("EXPLAIN (ANALYZE,BUFFERS,FORMAT JSON) "+q).fetchone()[0]
  Path(f"results/{stage}-{i+1}.json").write_text(json.dumps(plan,indent=2))
  print(stage,i+1,plan[0]["Execution Time"],"ms")
def indexes(db):
 for q in ["CREATE INDEX orders_customer ON orders(customer_id) INCLUDE(total)","CREATE INDEX items_order ON items(order_id)","CREATE INDEX orders_date ON orders(created_at)","CREATE INDEX customer_prefix ON customers(lower(name) text_pattern_ops)","CREATE INDEX large_orders ON orders(customer_id) WHERE total>900"]:db.execute(q)
 db.execute("ANALYZE")
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--customers",type=int,default=10000);p.add_argument("--orders",type=int,default=100000);a=p.parse_args()
 with psycopg.connect(os.environ["DATABASE_URL"],autocommit=True) as db:
  seed(db,a.customers,a.orders);benchmark(db,"before");indexes(db);benchmark(db,"after")
