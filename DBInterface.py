from sqlite3 import Error
import sqlite3

class DB:
    def __init__(self):
        pass

    def create_connection(self,db_file):
        """
        description: 
        ------------
        create a database connection to the SQLite database
        specified by the db_file
        
        args:
        ------------
        :param db_file: database file

        return:
        ------------
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect(db_file,check_same_thread=False)
            return conn
        except Error as e:
            print(e)

        return None
    # ---------------------------------------------------------------------------------------------
    def create_table(self,conn,create_table_sql):
        """
        description: 
        ------------
        create a table from the create_table_sql statement
        
        args:
        ------------
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement

        return:
        ------------
        """

        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    # ---------------------------------------------------------------------------------------------
    def create_tables(self,conn,dbname):
        """
        description: 
        ------------
        create a tables in database
        
        args:
        ------------

        :param conn: Connection object
        :param dbname: a database name
        return:
        ------------
        """
        sql_create_systems_table = """CREATE TABLE IF NOT EXISTS Systems (
                                        id	INTEGER PRIMARY KEY,
                                        host_name	TEXT NOT NULL,
                                        os_name	TEXT,
                                        os_architecture TEXT,
                                        os_version	TEXT,
                                        cpu_name  TEXT,
                                        cpu_cores TEXT,
                                        gpu	TEXT,
                                        bios_name TEXT,
                                        bios_version TEXT,
                                        bios_manufacturer TEXT
                                    );
                                    """
        sql_create_softwares_table = """ CREATE TABLE IF NOT EXISTS Softwares (
                                        id INTEGER PRIMARY KEY,
                                        system_id INTEGER,
                                        name TEXT NOT NULL,
                                        version TEXT,
                                        FOREIGN KEY (system_id) REFERENCES Systems (id)
                                    ); """
        sql_create_emails_table = """ CREATE TABLE IF NOT EXISTS Emails (
                                        id INTEGER PRIMARY KEY,
                                        link TEXT NOT NULL,
                                        receiver_email TEXT NOT NULL,
                                        date TEXT NOT NULL
                                    ); """
        if conn is not None:
            # create systems table
            self.create_table(conn,sql_create_systems_table)
            # create softwares table
            self.create_table(conn,sql_create_softwares_table)
            # create emails table
            self.create_table(conn,sql_create_emails_table)
            print('OK. tables created successfully\n'+'-'*50)
        else:
            print('Error! cannot create the database connection.\n'+'-'*50)
# ---------------------------------------------------------------------------------------------   
    def query_execution(self,conn,sql):
        """
        description: 
        ------------
        execute sql query on input db connection

        args:
        ------------
        :param conn: current connection to database
        :param sql: input sql query

        return:
        ------------
        :return ID: inserted ID
        """
        curser = conn.cursor()
        curser.execute(sql)
        rows = curser.fetchall()
        conn.commit()

        return rows
    # ---------------------------------------------------------------------------------------------

    def insert_softwares(self,conn,softwares):
        """
        description: 
        ------------        
        insert new software information

        args:
        ------------
        :param conn: current connection to database
        :param softwares : list like [[system_id,software1_name,version],[system_id,software2_name,version],...]
 
        return:
        ------------
        :return ID : inserted ID
        """
        try:
            curser = conn.cursor()
            curser.execute('''DELETE FROM Softwares WHERE system_id=?''',(str(softwares[0][2])))
            curser.executemany('''INSERT INTO Softwares(name,version,system_id) VALUES(?,?,?)''',softwares)
            conn.commit()
            return curser.lastrowid
        except Exception:
            print('Error in inserting data')
    # ---------------------------------------------------------------------------------------------
    def select_softwares_name(self,conn):
        """
        description: 
        ------------
        select softwares name

        args:
        ------------
        :param conn: current connection to database

        return:
        ------------
        :return row : fotwares name
        """
        curser = conn.cursor()
        curser.execute("SELECT name FROM softwares")
        rows = curser.fetchall()
        return rows
    # ------------------------------------------------------------------------------------------------
    def insert_system_info(self,conn,host_name,os_name,os_architecture,os_version,cpu_name,cpu_cores,gpu,bios_name,bios_version,bios_manufacturer):
        """
        description: 
        ------------        
        insert system information into database

        args:
        ------------
        :param host_name : system name
        :param os_name : system os name
        :param os_architecture : system os architecture
        :param os_version : system os version 
        :param cpu_name : system cpu name
        :param cpu_cores : system cpu cores
        :param gpu : system gpu name
        :param bios_name : system bios name
        :param bios_version : system bios version 
        :param bios_manufacturer : system bios manufacturer

        return:
        ------------
        :return ID : inserted ID
        """
        try:
            curser = conn.cursor()
            curser.execute('''SELECT DISTINCT id FROM Systems WHERE host_name = ?''',(host_name,))
            rows = curser.fetchall()
            if(len(rows)==0):
                curser.execute('''INSERT INTO Systems(host_name,os_name,os_architecture,os_version,cpu_name,cpu_cores,gpu,bios_name,bios_version,bios_manufacturer) VALUES(?,?,?,?,?,?,?,?,?,?)''',
                                        (host_name,os_name,os_architecture,os_version,cpu_name,cpu_cores,gpu,bios_name,bios_version,bios_manufacturer))
                conn.commit()
                return curser.lastrowid
            else:
                return rows[0][0]
        except Exception:
            print('Error in inserting data')
            return None
    # ------------------------------------------------------------------------------------------------
    def insert_emails(self,conn,emails):
        """
        description: 
        ------------        
        insert new email 

        args:
        ------------
        :param conn: current connection to database
        :param emails : list like [[exploit1_link,receiver_email,date],[exploit2_link,receiver_email,date],...]
 
        return:
        ------------
        :return ID : inserted ID
        """
        try:
            curser = conn.cursor()
            curser.executemany('''INSERT INTO Emails(link,receiver_email,date) VALUES(?,?,?)''',emails)
            conn.commit()
            return curser.lastrowid
        except Exception:
            print('Error in inserting data')
    # ---------------------------------------------------------------------------------------------
    def link_was_sent_to_email(self,conn,link,receiver_email):
        """
        description: 
        ------------
        return True if the given link was sent to the given email else return False

        args:
        ------------
        :param conn: current connection to database

        return:
        ------------
        :return True or False : 
        """
        try:
            curser = conn.cursor()
            curser.execute('''SELECT id FROM Emails WHERE link = ? and receiver_email = ?''',(link,receiver_email))
            rows = curser.fetchall()
            if len(rows)>0:
                return True
            else:
                return False
        except Exception:
            print('Error in selecting rows')
            return False
    # ---------------------------------------------------------------------------------------------
