import json
import os
import time
from math import ceil
from neo4j import GraphDatabase


NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "goods_info.json")

BATCH_SIZE_NODE = 5000
BATCH_SIZE_REL = 5000


def clean_text(x):
    if x is None:
        return ""
    return str(x).strip().replace(" ", "")


def read_data():
    concept_goods = set()
    concept_brands = set()
    rels_goods = set()
    rels_brand = set()
    goods_attrdict = {}

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        for line_id, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            data = json.loads(line)

            first_class = clean_text(data.get("first_class", ""))
            second_class = clean_text(data.get("second_class", ""))
            third_class = clean_text(data.get("third_class", ""))

            attrs = data.get("attrs", {}) or {}

            if first_class:
                concept_goods.add(first_class)
            if second_class:
                concept_goods.add(second_class)
            if third_class:
                concept_goods.add(third_class)

            if first_class and second_class:
                rels_goods.add((second_class, first_class))

            if second_class and third_class:
                rels_goods.add((third_class, second_class))

            if "品牌" in attrs and third_class:
                brands = attrs["品牌"].split(";")
                for brand in brands:
                    brand = clean_text(brand)
                    if brand:
                        concept_brands.add(brand)
                        rels_brand.add((brand, third_class))

            if third_class:
                goods_attrdict[third_class] = {
                    k: v for k, v in attrs.items() if k != "品牌"
                }

    return concept_goods, concept_brands, rels_goods, rels_brand, goods_attrdict


def print_progress(title, current, total, start_time):
    percent = current / total * 100 if total else 100
    elapsed = time.time() - start_time
    speed = current / elapsed if elapsed > 0 else 0
    left = total - current
    eta = left / speed if speed > 0 else 0

    print(
        f"\r{title}: {current}/{total} "
        f"({percent:.2f}%) | 已用 {elapsed:.1f}s | 预计剩余 {eta:.1f}s",
        end="",
        flush=True
    )


def run_batches(session, title, query, rows, batch_size):
    total = len(rows)
    if total == 0:
        print(f"{title}: 无数据")
        return

    start_time = time.time()
    batch_count = ceil(total / batch_size)

    for batch_id in range(batch_count):
        start = batch_id * batch_size
        end = min(start + batch_size, total)
        batch = rows[start:end]

        session.run(query, rows=batch).consume()

        print_progress(title, end, total, start_time)

    print()


def main():
    concept_goods, concept_brands, rels_goods, rels_brand, goods_attrdict = read_data()

    print("读取数据完成")
    print("商品概念数量：", len(concept_goods))
    print("品牌数量：", len(concept_brands))
    print("商品上下位关系数量：", len(rels_goods))
    print("品牌销售关系数量：", len(rels_brand))

    goods_rows = [
        {
            "name": name,
            "props": goods_attrdict.get(name, {})
        }
        for name in concept_goods
    ]

    brand_rows = [
        {
            "name": name
        }
        for name in concept_brands
    ]

    goods_rel_rows = [
        {
            "child": child,
            "parent": parent
        }
        for child, parent in rels_goods
    ]

    brand_rel_rows = [
        {
            "brand": brand,
            "product": product
        }
        for brand, product in rels_brand
    ]

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD)
    )

    driver.verify_connectivity()
    print("Neo4j 连接成功")

    with driver.session(database="neo4j") as session:
        print("正在创建唯一约束...")
        session.run(
            "CREATE CONSTRAINT product_name IF NOT EXISTS "
            "FOR (n:Product) REQUIRE n.name IS UNIQUE"
        ).consume()

        session.run(
            "CREATE CONSTRAINT brand_name IF NOT EXISTS "
            "FOR (n:Brand) REQUIRE n.name IS UNIQUE"
        ).consume()

        session.run("CALL db.awaitIndexes()").consume()

        product_query = """
        UNWIND $rows AS row
        MERGE (n:Product {name: row.name})
        SET n += row.props
        """

        brand_query = """
        UNWIND $rows AS row
        MERGE (n:Brand {name: row.name})
        """

        goods_rel_query = """
        UNWIND $rows AS row
        MATCH (a:Product {name: row.child})
        MATCH (b:Product {name: row.parent})
        MERGE (a)-[r:is_a]->(b)
        SET r.name = "属于"
        """

        brand_rel_query = """
        UNWIND $rows AS row
        MATCH (a:Brand {name: row.brand})
        MATCH (b:Product {name: row.product})
        MERGE (a)-[r:sales]->(b)
        SET r.name = "销售"
        """

        run_batches(
            session,
            "创建商品节点 Product",
            product_query,
            goods_rows,
            BATCH_SIZE_NODE
        )

        run_batches(
            session,
            "创建品牌节点 Brand",
            brand_query,
            brand_rows,
            BATCH_SIZE_NODE
        )

        run_batches(
            session,
            "创建商品上下位关系 is_a",
            goods_rel_query,
            goods_rel_rows,
            BATCH_SIZE_REL
        )

        run_batches(
            session,
            "创建品牌销售关系 sales",
            brand_rel_query,
            brand_rel_rows,
            BATCH_SIZE_REL
        )

    driver.close()

    print("导入完成")
    print("商品概念数量：", len(concept_goods))
    print("品牌数量：", len(concept_brands))
    print("商品上下位关系数量：", len(rels_goods))
    print("品牌销售关系数量：", len(rels_brand))


if __name__ == "__main__":
    main()