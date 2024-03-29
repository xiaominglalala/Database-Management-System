### Table

import os
import csv
from sql_parser import *
from index_manipulation import *
from relations import *

def table_functions(sql_tokens, current_database):

    if current_database == None:
        print("You must choose the database! Please enter: USE YOUR_DATABASE")
        print("Replace 'YOUR_DATABASE' with your target database.")
        return None

    first_token = sql_tokens[0]
    second_token = sql_tokens[1]
    root_0 = os.path.join(os.getcwd(), "Database_System")
    root_1 = os.path.join(root_0, current_database)

    # Create table
    # CREATE TABLE EMPLOYEE (emp# SMALLINT NOT NULL, name CHAR(20) NOT NULL, salary DECIMAL(5,2) NULL, primary key (emp#));
    if first_token == "create" and second_token == "table":
        table_name = sql_tokens[2]

        # check if table name exists
        table_name_file = os.path.join(root_1, "table_name.csv")
        if os.path.exists(table_name_file):
            with open(os.path.join(root_1, "table_name.csv"), 'r')as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == table_name:
                        print("Woops! This table already exists!")
                        return None

        if table_name in ["rel-i-i-1000", "rel-i-1-1000", "rel-i-i-10000", "rel-i-1-10000", "rel-i-1-100000", "rel-i-i-100000"]:
            relation_function(table_name, current_database)
        else:

            # Get attribute_names and primary_key
            attribute_list = create_table_parse(sql_tokens)

            # for create table xx
            if not attribute_list:
                print("Error! Please enter a command with correct syntax!")
                return
            primary_key = []
            attribute_names = []
            for attribute in attribute_list:
                attribute = attribute.lstrip()
                # get the primary key
                reg = "primary\s*key.*\((.*)\)+"
                primary = re.compile(reg).findall(attribute)
                if len(primary) > 0:
                    primary = primary[0]
                    primary_key = primary.split(', ')
                # get attributes
                else:
                    attribute = attribute.split(' ')
                    attribute_names.append(attribute[0])
            #print(attribute_names)
            #print(primary_key)
            # 列数 Column Num
            col_num = len(attribute_names)



            # Save primary key:
            with open(os.path.join(root_1, "primary_key.csv"), 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([table_name, primary_key[0]])
            f.close()

            # Write attribute names
            with open(os.path.join(root_1, "%s.csv" % table_name), 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([i for i in attribute_names])
            f.close()

        # Write table name into table_name.csv
        # 用'a' 才能不覆盖写入; newline解决多空行
        with open(os.path.join(root_1, "table_name.csv"), 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([table_name])
        f.close()

        print("Create table successfully!")
        return

    # Drop table
    if first_token == "drop" and second_token == "table":
        table_name = sql_tokens[2]
        table_file = os.path.join(root_1, "%s.csv" % table_name)
        # print(table_file)

        # If table name doesn't exist
        if not os.path.exists(table_file):
            print("Woops! This table doesn't exist!")
            return None

        # Delete table name from table_name.csv
        flag = 0
        with open(os.path.join(root_1, "table_name.csv"), 'r')as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == table_name:
                    flag = 2
        f.close()
        if flag != 2:
            print("This table doesn't exist!")
            return

        # Delete table file
        if os.path.isfile(table_file):
            os.remove(table_file)

        # Delete table name
        lines = list()
        with open(os.path.join(root_1, "table_name.csv"), 'r')as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != table_name:
                    lines.append(row)
        f.close()

        # Use "w" to overwrite
        with open(os.path.join(root_1, "table_name.csv"), 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(lines)
        f.close()

        # Delete primary key
        if os.path.exists(os.path.join(root_1, "primary_key.csv")):
            lines = list()
            with open(os.path.join(root_1, "primary_key.csv"), 'r')as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] != table_name:
                        lines.append(row)
            f.close()

            # Use "w" to overwrite
            with open(os.path.join(root_1, "primary_key.csv"), 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(lines)
            f.close()

        # Drop Index
        if os.path.exists(os.path.join(root_1, "index.csv")):
            lines = list()
            drop_indexes=list()
            with open(os.path.join(root_1, "index.csv"), 'r')as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] != table_name:
                        lines.append(row)
                    else:
                        drop_indexes.append(row[1])
            f.close()

            # Use "w" to overwrite
            with open(os.path.join(root_1, "index.csv"), 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(lines)
            f.close()

            # Drop indexing structure
            for index in drop_indexes:
                index_file=os.path.join(root_1, table_name + '_' + index + ".pkl")
                try:
                    os.remove(index_file)
                except:
                    print('No such index in the database!')

        print("Table %s dropped successfully" % table_name.upper())
        return

    # Alter table
    if first_token == "alter" and second_token == "table":
        table_name = sql_tokens[2]
        # TODO
        return

    else:
     print("Error! Please enter a command with correct syntax!")
     return

#table_functions(['drop','table','play'],'play')
