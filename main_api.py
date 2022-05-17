from fastapi import FastAPI
from pydantic import BaseModel

from database_requests import cursor

from psycopg2.errors import UndefinedColumn


class Model(BaseModel):
    chat_id: int
    account: str
    profiles_column: str


app = FastAPI()


@app.post("/users/add/")
def insert_account_in_database_if_not_exists(
    # chat_id: int, account: str, profiles_column: str
    model: Model,
) -> bool:
    """insert in user_table user''s chat_id if not exists and insta/tiktok profiles if not exists. If exists return False, else return True. Account : profile which need to save, profiles_colum : name of column where account need to save, can be insta/tt accounts. Chat_id : user''s ID. download_count : count user''s download"""
    # sql_selecting = f"SELECT MAX(download_count) FROM user_table WHERE chat_id = {chat_id} AND {profiles_column} = '{account}'"
    sql_selecting = "SELECT MAX(download_count) FROM user_table WHERE chat_id = {chat_id} AND {profiles_column} = '{account}'".format(
        **model.dict()
    )
    execute_command = cursor.execute(sql_selecting)
    write_answer = cursor.fetchall()
    print(write_answer)
    for every_answer in write_answer[0]:
        if every_answer != None:
            download_count = every_answer + 1
        else:
            download_count = 1
    excepted_answer = [(download_count,)]
    if write_answer == excepted_answer:
        return False
    else:
        print("inserting")
        sql_inserting = "INSERT INTO user_table(chat_id, {profiles_column}, download_count) VALUES({chat_id}, '{account}', {download_count})".format(
            **model.dict(), download_count=download_count
        )
        inserting_command = cursor.execute(sql_inserting)
        return True


class AccountInfo(BaseModel):
    profiles_column: str
    download_count: int


@app.get("/users/{chat_id}/{profiles_column}")
def selecting_accounts_if_exists(chat_id: int, profiles_column: str):
    """Return user''s save profiles if exists, else return False"""
    # print(chat_id)
    # sql_selecting = f"SELECT {profiles_column} FROM user_table WHERE chat_id = {chat_id} and {profiles_column} != 'null' GROUP BY {profiles_column} ORDER BY MAX(download_count) DESC LIMIT 3"
    try:
        second_sql_selecting = f"SELECT {profiles_column}, MAX(download_count) FROM user_table WHERE chat_id = {chat_id} and {profiles_column} != 'null' GROUP BY {profiles_column} ORDER BY MAX(download_count) DESC LIMIT 3"
        execute_command = cursor.execute(second_sql_selecting)
    except UndefinedColumn:
        return None
        # pass
    # write_answer = dict(cursor.fetchall())
    write_answer = cursor.fetchall()
    all_response = []
    for account_count_name in write_answer:
        # all_response.append(
        #     {
        #         "account_name": list(account_count_name)[0],
        #         "download_count": list(account_count_name)[1],
        #     }
        # )
        all_response.append(
            AccountInfo(
                profiles_column=list(account_count_name)[0],
                download_count=list(account_count_name)[1],
            )
        )
    return all_response
    # return "ok"


# @app.get("/users/{chat_id}/{profiles_column}/download_count")
# def selecting_download_count_if_exists(chat_id: int, profiles_column):
#     sql_selecting = f"SELECT MAX(download_count) FROM user_table WHERE chat_id = {chat_id} and {profiles_column} != 'null' GROUP BY {profiles_column} ORDER BY MAX(download_count) DESC LIMIT 3"
#     # if not write_answer:
#     execute_command = cursor.execute(sql_selecting)
#     write_answer = cursor.fetchall()
#     return write_answer
