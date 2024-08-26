import sqlite3
import os

SOURCE_DB="./source_db/inventory.db"
TARGET_DB="./target_db/inventory.db"



def export_data_from_source(source_db_path):
    if not os.path.isfile(source_db_path):
        raise FileNotFoundError(f"Source database file '{source_db_path}' not found.")
    
    conn_source = sqlite3.connect(source_db_path)
    cursor_source = conn_source.cursor()

    # Чтение всех данных из таблиц
    cursor_source.execute("SELECT * FROM worker")
    workers = cursor_source.fetchall()
    
    cursor_source.execute("SELECT * FROM arm")
    arms = cursor_source.fetchall()

    conn_source.close()
    return workers, arms

def import_data_to_target(target_db_path, workers, arms):
    conn_target = sqlite3.connect(target_db_path)
    cursor_target = conn_target.cursor()

    # Удаление id worker
    worker_ids = [worker[0] for worker in workers]
    cursor_target.executemany("DELETE FROM worker WHERE id = ?", [(worker_id,) for worker_id in worker_ids])

    # Удаление id arm
    arm_ids = [arm[0] for arm in arms]
    cursor_target.executemany("DELETE FROM arm WHERE id = ?", [(arm_id,) for arm_id in arm_ids])


    # Вставка данных в таблицы целевой базы данных
    cursor_target.executemany("INSERT INTO worker VALUES (?, ?, ?, ?, ?, ?, ?, ?)", workers)
    cursor_target.executemany("INSERT INTO arm VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", arms)

    conn_target.commit()
    conn_target.close()

if __name__ == "__main__":
    source_db_path = SOURCE_DB  # Путь к исходной базе данных
    target_db_path = TARGET_DB  # Путь к целевой базе данных

    # Экспортируем данные из исходной базы данных
    workers, arms = export_data_from_source(source_db_path)

    # Импортируем данные в целевую базу данных
    import_data_to_target(target_db_path, workers, arms)

    print("Данные успешно импортированы.")