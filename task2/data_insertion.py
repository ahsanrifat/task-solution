import asyncpg
import asyncio
import pandas as pd
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_database_connection(db_config):
    conn = None
    try:
        # Establish connection to PostgreSQL
        conn = await asyncpg.connect(**db_config)
        print("Database connection established.")
        yield conn
    except asyncpg.PostgresError as e:
        print(f"Database error: {e}")
        raise
    finally:
        if conn:
            await conn.close()
            print("Database connection closed.")

async def create_table_if_not_exists(conn, table_name):
    try:
        # Check if the table exists
        table_exists_query = f"""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = '{table_name}'
        );
        """
        table_exists = await conn.fetchval(table_exists_query)

        if not table_exists:
            # Create the table if it does not exist
            create_table_query = f"""
            CREATE TABLE {table_name} (
                col1 INTEGER,
                col2 INTEGER,
                col3 TEXT
            );
            """
            await conn.execute(create_table_query)
            print(f"Table '{table_name}' created.")
        else:
            print(f"Table '{table_name}' already exists.")
    except Exception as e:
        print(f"An error occurred while creating the table: {e}")

async def bulk_insert_data(conn, table_name, csv_file):
    try:
        # Read CSV data into a DataFrame
        df = pd.read_csv(csv_file)
        
        # Prepare the INSERT statement
        insert_query = f"""
        INSERT INTO {table_name} (col1, col2, col3)
        VALUES ($1, $2, $3)
        """
        
        # Prepare data for bulk insert
        data = df.to_records(index=False)
        
        # Perform the bulk insert
        await conn.executemany(insert_query, data)
        print(f"Data from '{csv_file}' bulk inserted into '{table_name}'.")
    except Exception as e:
        print(f"An error occurred during bulk insert: {e}")

async def main():
    db_config = {
        'user': 'admin',
        'password': 'password',
        'database': 'test_db',
        'host': 'localhost',
        'port': 5440
    }
    
    table_name = 'sample_table'
    csv_file = 'sample.csv'

    async with get_database_connection(db_config) as conn:
        await create_table_if_not_exists(conn, table_name)
        await bulk_insert_data(conn, table_name, csv_file)

# Run the asynchronous main function
asyncio.run(main())
