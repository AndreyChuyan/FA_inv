from db.init import conn, curs, IntegrityError
from .model import Arm
from error import Missing, Duplicate

curs.execute("""create table if not exists arm(
                name text primary key,
                number text, 
                deparment text, 
                description text)""") #if not exist - избежать разрушения таблицы после создания
    
def row_to_model(row: tuple) -> Arm:
    return Arm(name=row[0], number=row[1], deparment=row[2], description=row[3])

def model_to_dict(arm: Arm) -> dict:
    return arm.model_dump() if arm else None

def get_all() -> list[Arm]:
    qry = "select * from arm"
    curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]

def get_one(name:str) -> Arm:
    qry = "select * from arm where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Arm {name} not found")

def create(arm: Arm) -> Arm:
    qry = """Insert into arm (name, number, deparment, description) 
        values (:name, :number, :deparment, :description)"""
    params = model_to_dict(arm)
    try:
        _ = curs.execute(qry,params)
        conn.commit()  # Добавлен коммит после выполнения запроса
    except IntegrityError:  
        raise Duplicate(msg=f"Arm {arm.name} already exists")
    return get_one(arm.name)
    
def modify(name: str, arm: Arm) -> Arm:
    qry = """
    update arm
        set name=:new_name,
            number=:number, 
            deparment=:deparment, 
            description=:description
        where name=:orig_name
    """
    params= model_to_dict(arm)
    params["orig_name"]= name
    params["new_name"] = arm.name
    curs.execute(qry, params)
    conn.commit()  # подтверждаем изменения в базе данных
    if curs.rowcount == 1:
        return get_one(arm.name)    
    else:
        raise Missing(msg=f"Arm {name} not found")
    
def delete(name: str) -> bool:
    qry = "Delete from arm where name= :name"
    params = {"name": name}
    res= curs.execute(qry,params)
    conn.commit()
    if curs.rowcount != 1:
        raise Missing(msg=f"Arm {name} not found")
    else:
        return True    # запись успешно удалена

