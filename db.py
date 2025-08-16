import sqlite3

DB_PATH = "marketing.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_info TEXT,
            perplexity_data TEXT,
            marketing_plan TEXT,
            strategy_selection TEXT,
            final_plan TEXT
        )
    """)
    conn.commit()
    conn.close()


def insert_plan(business_info, perplexity_data=None, marketing_plan=None, strategy_selection=None, final_plan=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO plans (business_info, perplexity_data, marketing_plan, strategy_selection, final_plan)
        VALUES (?, ?, ?, ?, ?)
    """, (business_info, perplexity_data, marketing_plan, strategy_selection, final_plan))
    conn.commit()
    plan_id = cur.lastrowid
    conn.close()
    return plan_id


def update_plan(plan_id, business_info=None, perplexity_data=None, marketing_plan=None, strategy_selection=None, final_plan=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if business_info is not None:
        cur.execute("UPDATE plans SET business_info = ? WHERE id = ?", (business_info, plan_id))
    if perplexity_data is not None:
        cur.execute("UPDATE plans SET perplexity_data = ? WHERE id = ?", (perplexity_data, plan_id))
    if marketing_plan is not None:
        cur.execute("UPDATE plans SET marketing_plan = ? WHERE id = ?", (marketing_plan, plan_id))
    if strategy_selection is not None:
        cur.execute("UPDATE plans SET strategy_selection = ? WHERE id = ?", (strategy_selection, plan_id))
    if final_plan is not None:
        cur.execute("UPDATE plans SET final_plan = ? WHERE id = ?", (final_plan, plan_id))

    conn.commit()
    conn.close()


def get_plan(plan_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM plans WHERE id = ?", (plan_id,))
    row = cur.fetchone()
    conn.close()
    return row



def delete_all_plans():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Delete all rows from table `plans`
    cur.execute("DELETE FROM plans;")

    conn.commit()
    conn.close()

    print("✅ All data deleted from `plans` table.")
