
class ExecuteStoredProcedure:
    @classmethod
    def ExecuteProcedure(cls, procedure_name, params, conn):

        cursor = conn.cursor()
        procedure_name = procedure_name
        param_markers = ", ".join(["?" for _ in params])
        sql_query = f"CALL {procedure_name} {param_markers}"
        cursor.execute(sql_query, params)
        data = cursor.fetchall()
        json_list = []
        for i in range(len(data[0].cursor_description)):
            x = {
                data[0].cursor_description[i][0]: [column[i] for column in data]
            }
            json_list.append(x)

        conn.commit()
        cursor.close()
        conn.close()
        return json_list
