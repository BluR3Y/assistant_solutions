from classes.Process import Process
from methods import utils

SHEET_NAME = "Other"

def database_record_modifier(self):
    process_name = "Modify Database Records"
    def logic():
        # Retrieve all the tables in the database
        tables = self.db_manager.get_db_tables()

        while True:
            selected_table = input("Enter the name of the table whose records you wish to alter: ")
            if selected_table in tables:
                table_columns = self.db_manager.get_table_columns(selected_table)
                record_identifier = table_columns[0]
                selected_search_conditions = input(f"Input the name of the column in the '{selected_table}' table followed by the value in the selected column separated by a ':' and enclosed in double quotes, which will be used to filter records in the database. Ex: \"Discipline:Philosophy\": ")
                search_conditions = dict()
                for condition in utils.extract_quoted_strings(selected_search_conditions):
                    col, val = condition.split(':')
                    if col in table_columns:
                        search_conditions[col] = val
                    else:
                        print(f"The column '{col}' does not exist in the table '{selected_table}'.")
                        break
                
                search_result = self.db_manager.select_query(
                    selected_table,
                    [record_identifier],
                    (' AND '.join([f"{col}=?" for col in search_conditions.keys()])),
                    *search_conditions.values()
                )
                record_ids = [item[record_identifier] for item in search_result]
                print(f"Search returned {len(record_ids)} records.")
                
                if record_ids:
                    selected_alter_properties = input(f"Input the name of the column in the '{selected_table}' table that will be updated followed by the new value separated by a ':' and enclosed in double quites. Ex: \"Discipline:Philosophy\": ")
                    alter_properties = dict()
                    for prop in utils.extract_quoted_strings(selected_alter_properties):
                        col, val = prop.split(':')
                        if col in table_columns:
                            alter_properties[col] = val
                        else:
                            print(f"The column '{col}' does not exist in the table '{selected_table}'")
                            break

                    self.db_manager.update_query(
                        process_name,
                        selected_table,
                        alter_properties,
                        f"{record_identifier} IN ({','.join(['?' for _ in record_ids])})",
                        *record_ids
                    )
            else:
                print(f"Table '{selected_table}' does not exist in the database.")

            user_decision = input("Would you like to continue with another update operation (y)es/(n)o: ")
            if not user_decision.startswith('y'):
                break

    return Process(
        logic,
        process_name,
        "The database_record_modifier function provides an interactive tool for modifying records within a specified table in a connected database. It allows users to select a table, define search conditions, and update multiple records in a single operation. This function is designed for dynamic and secure interaction with the database, verifying that tables and columns exist before performing operations and using parameterized queries to avoid SQL injection risks. It encapsulates the entire process in a callable Process object, ready to be integrated into larger workflows or batch processes."
    )