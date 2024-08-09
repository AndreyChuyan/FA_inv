from .init import conn, curs, IntegrityError
from worker.model import Worker
from error import Missing, Duplicate

curs.execute("""create table if not exists worker(
                name text primary key,
                role text,
                password text,
                deparment text, 
                description text
                )""") #if not exist - избежать разрушения таблицы после создания

# def row_to_model(row: tuple) -> Worker:
#     (name, deparment, description) = row
#     return Worker(name, deparment, description)

def row_to_model(row: tuple) -> Worker:
    return Worker(name=row[0], role=row[1], password=row[2], deparment=row[3], description=row[4])

def model_to_dict(worker: Worker) -> dict:
    return worker.model_dump() if worker else None

def get_all() -> list[Worker]:
    qry = "select * from worker"
    curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]

def get_one(name:str) -> Worker:
    qry = "select * from worker where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Worker {name} not found")
    

def create(worker: Worker, table:str = "worker") -> Worker:
    """Добавление пользователя"""
    qry = f"""Insert into {table} (name, role, password, deparment, description) 
            values (:name, :role, :password, :deparment, :description)"""
    params = model_to_dict(worker)
    
    try:
        _ = curs.execute(qry,params)
        conn.commit()  # Добавлен коммит после выполнения запроса
    except IntegrityError:  
        raise Duplicate(msg=f"Worker {worker.name} already exists")
    return get_one(worker.name)
    
def modify(name: str, worker: Worker) -> Worker:
    qry = """
    update worker
        set name=:new_name,
            role=:role,
            password=:password,
            deparment=:deparment,
            description=:description
        where name=:orig_name
    """
    params = model_to_dict(worker)
    params["orig_name"] = name  # используем разные ключи для нового и старого значений name
    params["new_name"] = worker.name  # новое значение для имени
    curs.execute(qry, params)
    conn.commit()  # подтверждаем изменения в базе данных
    if curs.rowcount == 1:
        return get_one(worker.name)    
    else:
        raise Missing(msg=f"Worker {name} not found")
    
    
def delete(name: str) -> bool:
    qry = "delete from worker where name=:name"
    params = {"name": name}
    curs.execute(qry,params)
    conn.commit()
    if curs.rowcount != 1:
        raise Missing(msg=f"Worker {name} not found")
    else:
        return True    # запись успешно удалена