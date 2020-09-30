import sqlite3
import pandas as pd


class DB:

	def __init__(self):
		self.conn = sqlite3.connect('auto.db')
		self.cursor = self.conn.cursor()

	def csv2sql(self, filePath):
		df = pd.read_csv(filePath, encoding='utf-8')
		df.to_sql('auto_00', con=self.conn, if_exists='replace')


	def createAutoTable(self):
		self.cursor.execute('''
			create table if not exists auto(
				id integer primary key autoincrement,
				title varchar(128),
				price integer,
				bed integer,
				bath integer,
				area integer,
				start_dttm datetime default current_timestamp,
				end_dttm datetime default (datetime('2999-12-31 23:59:59'))
			);
			''')
		self.conn.commit()

		self.cursor.execute('''
			create view if not exists v_auto as
				select
						id,
						title,
						price,
						bed,
						bath,
						area
					from auto
					where current_timestamp between start_dttm and end_dttm
					;
				''')
		self.conn.commit()

	def createTableNewRows(self):
		self.cursor.execute('''
			create table auto_01 as 
				select
					t1.*
				from auto_00 t1
				left join v_auto t2
				on t1.title = t2.title
				where t2.title is null;
			''')

	def createTableUpdateRows(self):
		self.cursor.execute('''
			create table auto_02 as 
				select 
					t1.*
				from auto_00 t1
				inner join v_auto t2
				on t1.title = t2.title
				and (
					t1.price     <> t2.price
					or t1.bed    <> t2.bed
					or t1.bath   <> t2.bath
					or t1.area   <> t2.area
				);
			''')

	def createTableDeleteRows(self):
		self.cursor.execute('''
			create table auto_03 as 
				select
					t1.title
				from v_auto t1
				left join auto_00 t2
				on t1.title = t2.title
				where t2.title is null;
		''')

	def updateAutoTable(self):
		self.cursor.execute('''
			update auto
			set end_dttm = current_timestamp
			where title in (select title from auto_03)
			and end_dttm = datetime('2999-12-31 23:59:59');
		''')

		self.cursor.execute('''
			update auto
			set end_dttm = current_timestamp
			where title in (select title from auto_02)
			and end_dttm = datetime('2999-12-31 23:59:59');
		''')

		self.cursor.execute('''
			insert into auto (
				title,
				price,
				bed ,
				bath,
				area
			)
			select 
				title,
				price,
				bed ,
				bath,
				area
			from auto_02;
		''')

		self.cursor.execute('''
			insert into auto (
				title,
				price,
				bed ,
				bath,
				area
			)
			select 
				title,
				price,
				bed ,
				bath,
				area
			from auto_01;
		''')

		self.conn.commit()

	def deleteTmpTables(self):
		self.cursor.execute('''
			drop table if exists auto_00;
		''')
		self.cursor.execute('''
			drop table if exists auto_01;
		''')
		self.cursor.execute('''
			drop table if exists auto_02;
		''')
		self.cursor.execute('''
			drop table if exists auto_03;
		''')

db= DB()
db.deleteTmpTables()
db.csv2sql('clean_data.csv')
db.createAutoTable()
db.createTableNewRows()
db.createTableUpdateRows()
db.createTableDeleteRows()
db.updateAutoTable()