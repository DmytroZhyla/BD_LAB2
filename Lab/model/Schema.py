#!/usr/bin/env python3

from . import DynamicSearch
from .AutoSchema import *


class Library(Schema):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._dynamicsearch = {a.name: a for a in [DynamicSearch.BooksDynamicSearch(self), DynamicSearch.ReaderLoanDynamicSearch(self), DynamicSearch.ReaderDynamicSearch(self), ]}
		# self.reoverride()

	def reoverride(self):
		pass

	def reinit(self):
		# sql = f"""
		# 	SELECT table_name FROM information_schema.tables
		# 	WHERE table_schema = '{self}';
		# """
		with self.dbconn.cursor() as dbcursor:
			# dbcursor.execute(sql)
			for a in self.refresh_tables():  # tuple(dbcursor.fetchall()):
				q = f"""DROP TABLE IF EXISTS {a} CASCADE;"""
				# print(q)
				dbcursor.execute(q)

		tables = [
			f"""CREATE SCHEMA IF NOT EXISTS "{self}";""",
			f"""CREATE TABLE "{self}"."Author" (
				"id" bigserial PRIMARY KEY,
				"Full_name" character varying(255) NOT NULL,
				"Pseudonym" character varying(255) NOT NULL,
				"experience" bigint NOT NULL
			);
			""",
			f"""CREATE TABLE "{self}"."Reader" (
				"id" bigserial PRIMARY KEY,
				"Full_Name" character varying(255) NOT NULL,
				"Аge" bigint NOT NULL
			);
			""",
			f"""CREATE TABLE IF NOT EXISTS "{self}"."Books" (
				"id" bigserial PRIMARY KEY,
				"date_of_printing" timestamp with time zone NOT NULL,
				"Name" character varying(255) NOT NULL,
				"Author" bigint NOT NULL,
				"Reader_id" bigint NOT NULL,
				CONSTRAINT "Books_Author_fkey" FOREIGN KEY ("Author")
					REFERENCES "{self}"."Author"("id") MATCH SIMPLE
					ON UPDATE NO ACTION
					ON DELETE CASCADE
					NOT VALID,
				CONSTRAINT "Books_Reader_id_fkey" FOREIGN KEY ("Reader_id")
					REFERENCES "{self}"."Reader"("id") MATCH SIMPLE
					ON UPDATE NO ACTION
					ON DELETE CASCADE
					NOT VALID
			);
			""",
			f"""CREATE TABLE IF NOT EXISTS "{self}"."Library" (
				"id" bigserial PRIMARY KEY,
				"year_of_foundation" timestamp with time zone NOT NULL,
				"address" character varying(255) NOT NULL,
				"capacity" bigint NOT NULL,
				"Reader_id" bigint NOT NULL,
				CONSTRAINT "Library_Reader_id_fkey" FOREIGN KEY ("Reader_id")
					REFERENCES "{self}"."Reader"("id") MATCH SIMPLE
					ON UPDATE NO ACTION
					ON DELETE CASCADE
					NOT VALID
			);
			""",
			f"""CREATE TABLE IF NOT EXISTS "{self}"."LibraryBooks" (
				"id" bigserial PRIMARY KEY,
				"Library_id" bigint NOT NULL,
				"Book_id" bigint NOT NULL,
				CONSTRAINT "LibraryBooks_Library_id_fkey" FOREIGN KEY ("Library_id")
					REFERENCES "{self}"."Library"("id") MATCH SIMPLE
					ON UPDATE NO ACTION
					ON DELETE CASCADE
					NOT VALID,
				CONSTRAINT "LibraryBooks_Book_id_fkey" FOREIGN KEY ("Book_id")
					REFERENCES "{self}"."Books"("id") MATCH SIMPLE
					ON UPDATE NO ACTION
					ON DELETE CASCADE
					NOT VALID
			);
			""",
		]

		with self.dbconn.cursor() as dbcursor:
			for a in tables:
				# print(a)
				dbcursor.execute(a)

		self.dbconn.commit()

		tables = self.refresh_tables()
		# print(f"tables: {tables}")

	def randomFill(self):
		self.tables.Author.randomFill(1_000)
		self.tables.Reader.randomFill(1_000)
		self.tables.Books.randomFill(1_000)
		self.tables.Library.randomFill(1_000)
		self.tables.LibraryBooks.randomFill(1_000)


def _test():
	pass


if __name__ == "__main__":
	_test()
