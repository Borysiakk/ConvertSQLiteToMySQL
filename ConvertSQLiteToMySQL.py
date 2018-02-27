import sqlite3
import pymysql

class SqliteConventerMySql:
    __ConnectionSqlite = None
    __ConnectionMySql = None
    __CursorSqlite = None
    __CursorMySql = None

    def __init__(self,DateBaseName,user,password,host,DateBaseNameMySql):
        try:
            self.__ConnectionSqlite = sqlite3.Connection(DateBaseName)
            self.__CursorSqlite = self.__ConnectionSqlite.cursor()
        except sqlite3.Error:
            print("Error opening %s "%DateBaseNameMySql)

        try:
            self.__ConnectionMySql = pymysql.connect(host,user,password)
            self.__CursorMySql = self.__ConnectionMySql.cursor()
        except pymysql.Error:
            print("Error connect mysql")

        try:
            self.__CursorMySql.execute("CREATE DATABASE " + DateBaseNameMySql)
            self.__CursorMySql.execute("USE " + DateBaseNameMySql)
        except pymysql.MySQLError:
            print("There is already a database with this name")
        self.__main()




    def __getTabelesName(self):
        self.__CursorSqlite.execute("SELECT name FROM sqlite_master")
        return self.__CursorSqlite.fetchall()

    def __getColumnsName(self,TableName):
        self.__CursorSqlite.execute("PRAGMA table_info(" + TableName + ")")
        return self.__CursorSqlite.fetchall()
    
    def __getAttributeName(self,TableName):
        self.__CursorSqlite.execute("SELECT * FROM " + TableName)
        return self.__CursorSqlite.fetchall()

    def __main(self):
        NameTables = self.__getTabelesName()
        for nametable in NameTables:
            DataColumns = self.__getColumnsName(nametable[0])
            DataAttributes = self.__getAttributeName(nametable[0])
            CreateTable = "CREATE TABLE " + nametable[0] + " ("
            InsertTable = "INSERT INTO " + nametable[0] + " ("
            for columnname in DataColumns:
                CreateTable += columnname[1] + " " + columnname[2] + ","
                InsertTable += columnname[1] + ","
            CreateTable = CreateTable[0:len(CreateTable) - 1]
            InsertTable = InsertTable[0:len(InsertTable) - 1]
            CreateTable += ");"
            InsertTable += ") VALUES("
            InsertTable += "%s," * len(DataAttributes[0])
            InsertTable = InsertTable[0:len(InsertTable) - 1]
            InsertTable +=")"
            print(InsertTable)
            self.__CursorMySql.execute(CreateTable)
            self.__CursorMySql.executemany(InsertTable,DataAttributes)
            self.__ConnectionMySql.commit()

        self.__ConnectionSqlite.close()
        self.__ConnectionMySql.close()

                



test = SqliteConventerMySql("Test.db","root","","localhost","DateBaseName")
