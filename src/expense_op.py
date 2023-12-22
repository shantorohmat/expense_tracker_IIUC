import os
import streamlit as st
import pandas as pd
x = []
y1 = False
y2 = False
y3 = False
expense_date  = "" 
category = "" 
amount = "" 
notes= ""
notesx= ""
amountx = "" 
document_upload = "" 
created_at = "" 
updated_at = "" 
notid = "" 
categoryx = ""

from src.db_ops import show_data, edit_data, delete_data

def insert_parameter(cursor,db):
    if 'flag' not in st.session_state:
        st.session_state.flag = 0
    

    global x
    st.sidebar.header('add or delete column')
    task = st.sidebar.selectbox('--------',
                                    ('Add column', 
                                     'Delete column'))

    if(task == "Add column"):
        # Streamlit Form
        st.title('Add Column to Database')

        # Form to get new column details
        new_column_name = st.text_input('Enter the new column name:')
        new_column_type = st.text_input('Enter the data type for the new column (e.g.,longtext, TEXT, INTEGER, double, VARCHAR(n)):')
        # x.append(new_column_name)
        # for i, element in enumerate(x, start=1):
        #     st.write(f" {element}")

        if st.button('Add Column'):
            # x = (new_column_name)
            # x.append(new_column_name)
            # for i, element in enumerate(x, start=1):
            #     st.write(f" {element}")
            
            
            # Use the ALTER TABLE statement to add the new column
            alter_query = f'''ALTER TABLE expense ADD COLUMN {new_column_name} {new_column_type}'''
                            ##AFTER document"
            # ALTER TABLE student_information ADD COLUMN new_column_name longtext;

            try:
                cursor.execute(alter_query)
                db.commit()
                st.success(f"Column '{new_column_name}' added successfully.")
                st.balloons()
            except:
                st.error("Error adding column")
                
    if(task == "Delete column"):
        st.title('Delete Column to Database')
        st.header('button for columns')
        cursor.execute('''SHOW COLUMNS FROM expense FROM ExpenseDB''')
        
        columns = [column[0] for column in cursor.fetchall()]
        
        if st.button('show Columns'):
            try:
                st.title('Columns for Table: expense')
                for column in columns:
                    st.write(column)
                    #st.success(f"Column '{new_column_name}' added successfully.")
                    st.balloons()
            except:
                st.error("Error adding column")

        # Streamlit Form
        st.title('Delete Column from Database')

        # Form to get the column name to be deleted
        column_to_delete = st.text_input('Enter the column name to be deleted:')

        if st.button('Delete Column'):
            # Use the ALTER TABLE statement to delete the column
            alter_query = f"ALTER TABLE expense DROP COLUMN {column_to_delete};"

            try:
                cursor.execute(alter_query)
                db.commit()
                st.success(f"Column '{column_to_delete}' deleted successfully.")
            except:
                st.error("Error deleting column: ")


def save_expense(cursor, db):
    
    if 'flag' not in st.session_state:
        st.session_state.flag = 0
    # global x
    st.header('💸 Expense Entry')
    
    with st.form(key='expense_submit_form', clear_on_submit=False):
        # cursor.execute('''SHOW COLUMNS FROM expense FROM ExpenseDB''')
        
        
    # Read data into a Pandas DataFrame
        #df = pd.read_sql_query("SELECT * FROM expense", db)
        # Execute query to retrieve table structure
        table_name = 'expense'
        cursor.execute(f"DESCRIBE {table_name}")
        columns_data = cursor.fetchall()
        # for column_data in columns_data:
        #     st.header("Columns and Data Types:")
        #     column_name, data_type = column_data[0], column_data[1]
        y1 = False
        y2 = False
        y3 = False
        global expense_date  
        global category
        global categoryx
        global amount 
        global amountx
        global category
        global document_upload
        global created_at
        global updated_at
        global notid
        global notes
        global notesx
    
        
        
        for column_data in columns_data:
            expense_dateZ  = "expense_date"
            categoryZ = "category"
            amountZ = "amount"
            

            
            column_name, data_type = column_data[0], column_data[1]
            # st.write(f"Column: {column_name}, Data Type: {data_type}")
            expense_category = ['Shopping', 'Snacks', 'Mobile Recharge', 
                            'Online Course', 'Subscription']
            # st.write("help")
            if data_type == b'int' and  column_name != "id":
               notid = st.number_input(f"Enter an {column_name} value:")
               
            elif data_type == b'timestamp' and column_name == "created_at":
               created_at = st.date_input(f"Enter an {column_name} value:")

            elif data_type == b'timestamp' and column_name == "updated_at":
               updated_at = st.date_input(f"Enter an {column_name} value:")
               
            elif data_type == b'timestamp' and column_name == "expense_date":
               expense_date = st.date_input(f"Enter an {column_name} value:")
            #    st.write(f"dfgff{category}")
               expense_dateZ = column_name
               y1 = True

            #    st.write(f"dff{column_name}")
            #    if column_name == "expense_date":
            #         expense_dateZ = column_name
            #         st.write(f"df545f {expense_dateZ}")
            #    else:
            #        st.write(f"dfgff{expense_dateZ}")
                   
                
            elif data_type == b'longtext' and column_name == "notes":
               notes = st.text_area(f"Enter an {column_name} value:")
            elif data_type == b'longtext' and column_name != "notes":
               notesx = st.text_area(f"Enter an {column_name} value:")
            # elif data_type == b'double' and column_name != "amount":
            #    column_name = st.text_input(f"Enter an {column_name} value:")

            elif data_type == b'double' and column_name == "amount":
               amount = st.text_input(f"Enter an {column_name}* value:")
            elif data_type == b'double' and column_name != "amount":
               amountx = st.text_input(f"Enter an {column_name}* value:")
            #    st.write(f"dfgff{amount}")
            #    amountZ = column_name
            #    y2 = True
            #    chr(data_type[0]) == 'v' & chr(data_type[1]) == 'a' & chr(data_type[2]) =='r':
            elif chr(data_type[0]) == 'v' and chr(data_type[1]) == 'a' and chr(data_type[2]) =='r':
                
                if column_name == "category":
                    # categoryZ = column_name
                    category = st.selectbox('Expense Category*', expense_category)
                    # st.write(f"dfdddddgff {category}")
                    y3 = True
                elif column_name == "documents":
                    document_upload = st.file_uploader('Upload Document', 
                                           type=['txt','pdf', 
                                                 'jpg', 'png', 'jpeg'], 
                                            accept_multiple_files=True)
                else:
                    categoryx = st.text_input(f"Enter an {column_name} value:")
            
        if st.form_submit_button(label='Submit'):
            if not(expense_date and category and amount):
                st.write('Please fill all the * fields')
            else:
                st.session_state.flag = 1
                st.success('Data Submitted Successfully')
            # st.write(f"ss {amount}")
            # table_name = 'expense'
            # cursor.execute(f"DESCRIBE {table_name}")
            # columns_data = cursor.fetchall()
            # for column_data in columns_data:
            #     column_name, data_type = column_data[0], column_data[1]
            #     st.write(f"Column: {column_name}, Data Type: {data_type}")
                
            # st.session_state.flag = 1
            # st.success('Data Submitted Successfully')
            # expense_dateZ = "kj"
                
            # if (amountZ and expense_dateZ and categoryZ  ):
            # if (y2):
            #     st.write(f"{amountZ}")
            #     st.write('Please fill all the * fields')
            # else:
            #     st.session_state.flag = 1
            #     st.success('Data Submitted Successfully')
                
                # expense_dateZ  = ""
                # categoryZ = ""
                # amountZ = ""
                # table_name = 'expense'
                # cursor.execute(f"DESCRIBE {table_name}")
                # columns_data = cursor.fetchall()
                # for column_data in columns_data:
                #     column_name, data_type = column_data[0], column_data[1]
                # if column_name == "expense_date":
                #     expense_dateZ = column_name
                # elif column_name == "category":
                #         categoryZ = column_name
                # elif column_name == "amount":
                #     amountZ = column_name
                    
           
         
            



        
    
        # st.title("Display Table Columns and Data Types in Streamlit")

        # Display DataFrame
        # st.dataframe(df)

        # Loop through columns and display column names and data types
        # st.header("Columns and Data Types:")
        # for column in df.columns:
        #     data_type = df[column].dtype
        #     st.write(f"Column: {column}, Data Type: {data_type}")

       
        # expense_category = ['Shopping', 'Snacks', 'Mobile Recharge', 
        #                     'Online Course', 'Subscription']
        # # expense_date = st.date_input('Expense Date*')
        # category = st.selectbox('Expense Category*', expense_category)
        # amount = st.text_input('Amount*')
        # notes = st.text_area('Notes')
        # if len(x) > 0:
        #     for i, element in enumerate(x, start=1):
        #         st.text_input(f" {element}")
                # st.form_submit_button("input")
        #     st.form_submit_button(label='sunbk')
        # x = st.text_area(f'{x}')
        # st.form_submit_button(label='sunbk')
        # document_upload = st.file_uploader('Upload Document', 
        #                                    type=['txt','pdf', 
        #                                          'jpg', 'png', 'jpeg'], 
        #                                     accept_multiple_files=True)
        # expense_reason = st.text_area('Expemse_reason')
        # Streamlit Form
        
        # if st.form_submit_button(label='Submit'):
            # expense_dateZ  = ""
            # categoryZ = ""
            # amountZ = ""
            # table_name = 'expense'
            # cursor.execute(f"DESCRIBE {table_name}")
            # columns_data = cursor.fetchall()
            # for column_data in columns_data:
            #     column_name, data_type = column_data[0], column_data[1]
            #     if column_name == "expense_date":
            #         expense_dateZ = column_name
            #     elif column_name == "category":
            #         categoryZ = column_name
            #     elif column_name == "amount":
            #         amountZ = column_name
            #         if (expense_dateZ and categoryZ and amountZ):
            #                     st.write('Please fill all the * fields')
            #         else:
            #             st.session_state.flag = 1
            #             st.success('Data Submitted Successfully')

                    

    if st.session_state.flag:
        # st.write(final_parameter_calculation)

        with st.form(key='final', clear_on_submit=True):
             # st.write(final_parameter_calculation)

            if st.form_submit_button('Are you Sure?'):
                # st.write(final_parameter_calculation)
                st.session_state.flag = 0
                # insert data into expense table
                
                # st.write(document_upload.read())
                # st.write(document_upload.name)
                # st.write(document_upload.getvalue())
                # file = open(document_upload.read(),'rb')
                all_documents = []
                for file in document_upload:
                    st.write(file.name)
                    # st.write(file.getvalue())
                    # st.write(file.read())
                    if file is not None:
                        # Get the file name and extract the extension
                        file_name = file.name
                        # st.write(file_name)
                        file_extension = os.path.splitext(file_name)[1]
                        dir_name = "./documents/expenses"
                        if not os.path.isdir(dir_name):
                            os.makedirs(dir_name)

                        file_url = dir_name + '/' + file_name
                        # file_url = dir_name + file_name
                        all_documents.append(file_url)

                        # Save the file in its original format
                        with open(file_url, "wb") as f:
                            f.write(file.read())
                        st.success("File has been successfully saved.")
                        # for i, element in enumerate(x, start=1):
                            # st.text_input(f" {element}")
                # table_name = 'expense'
                # cursor.execute(f"DESCRIBE {table_name}")
                # columns_data = cursor.fetchall()
                # for column_data in columns_data:
                #     if column_name == "expense_date":
                #         expense_date = column_name
                #     column_name, data_type = column_data[0], column_data[1]


                # if(notesx):
                #     query = '''Insert into expense (expense_date, category, amount, 
                #                                 notes, documents,notesx) 
                #         VALUES (%s, %s, %s, %s, %s, %s)
                #         '''
                # elif(categoryx):
                #     query = '''Insert into expense (expense_date, category, amount, 
                #                                 notes, documents,categoryx) 
                #         VALUES (%s, %s, %s, %s, %s, %s)
                #         '''
                # elif(amountx):
                #     query = '''Insert into expense (expense_date, category, amount, 
                #                                 notes, documents,amountx) 
                #         VALUES (%s, %s, %s, %s, %s, %s)'''
                # elif(amountx and categoryx):
                #     query = '''Insert into expense (expense_date, category, amount, 
                #                                 notes, documents,amountx,categoryx) 
                #         VALUES (%s, %s, %s, %s, %s, %s, %s)'''
                # elif(amountx and notesx):
                #     query = '''Insert into expense (expense_date, category, amount, 
                #                                 notes, documents,amountx,notesx) 
                #         VALUES (%s, %s, %s, %s, %s, %s, %s)'''
                # elif(categoryx and notesx):
                #     query = '''Insert into expense (expense_date, category, amount, 
                #                                 notes, documents,categoryx,notesx) 
                #         VALUES (%s, %s, %s, %s, %s, %s, %s)'''
                # elif(categoryx and notesx and amountx):
                #     query = '''Insert into expense (expense_date, category, amount, 
                #                                 notes, documents,categoryx,notesx,amountx) 
                #         VALUES (%s, %s, %s, %s, %s, %s, %s,%s)'''
                # else:
                query = '''Insert into expense (expense_date, category, amount, 
                                                notes, documents) 
                        VALUES (%s, %s, %s, %s,  %s)
                        '''
                # table_name = 'expense'
                # cursor.execute(f"DESCRIBE {table_name}")
                # columns_data = cursor.fetchall()
                # for column_data in columns_data:
                values = (expense_date, category, amount, notes, str(all_documents))
                # st.write(query, values)
                cursor.execute(query, values)
                db.commit()
                st.success("Expense Record Inserted Successfully!")
                st.balloons()

            else:
                st.write("Click above button If you are Sure")
    else:
        st.warning("Please fill up above form")

    if(notesx):
        df = pd.read_sql('''SELECT id, expense_date, category, 
                        amount, notes, documents,notesx FROM expense''', con=db)
    # elif(categoryx):
    #     df = pd.read_sql('''SELECT id, expense_date, category, 
    #                     amount, notes, documents, categoryx FROM expense''', con=db)
    elif(amountx):
        df = pd.read_sql('''SELECT id, expense_date, category, 
                        amount, notes, documents,amountx FROM expense''', con=db)
    elif(amountx and categoryx):
        df = pd.read_sql('''SELECT id, expense_date, category, 
                        amount, notes, documents,categoryx,amountx FROM expense''', con=db)
    elif(amountx and notesx):
        
        df = pd.read_sql('''SELECT id, expense_date, category, 
                        amount, notes, documents,notesx,amountx FROM expense''', con=db)
        
    elif(categoryx and notesx):
        df = pd.read_sql('''SELECT id, expense_date, category, 
                        amount, notes, documents,categoryx,notesx FROM expense''', con=db)
        
    elif(categoryx and notesx and amountx):
        df = pd.read_sql('''SELECT id, expense_date, category, 
                        amount, notes, documents,categoryx,notesx,amountx FROM expense''', con=db)
        
    else:
        df = pd.read_sql('''SELECT id, expense_date, category, 
                        amount, notes, documents FROM expense''', con=db)
        
    
    # st.dataframe(df)

    # select the columns you want the users to see
    columns = ['id',
               'expense_date',
                'category',
                'amount',
                'notes',
                ]   
    # st.dataframe(df)
    show_data(df, columns)
    edit_data(cursor, db, df, columns, 'Edit Expenses', 'expense')
    delete_data(cursor, db, df, columns, 'Delete Expenses', 'expense')


