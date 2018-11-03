#!/usr/bin/env python

import psycopg2
import datetime

def execute_query(query):
    #executes query and returns results

    try:
        db = psycopg2.connect("dbname=news")
        
        c = db.cursor()

        c.execute(query)
        
        data = c.fetchall()

        db.close()
        
        return data
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
def get_popular_articles():

    query = """select articles.title, dt.views
                 from (
                 select substring(path, 10) as title, count(*) as views
                 from log where path != '/' and status = '200 OK'
                 group by 1 order by views desc) as dt
                 join articles on
                 articles.slug = dt.title
                 order by dt.views desc
                 limit 3;"""
    
    data = execute_query(query)

    print("\nPrinting three most popular articles of all time\n")
    for title, views in data:
        print('"{}" - {} views'.format(title, views))


def get_popular_authors():

    query = """select authors.name, sum(dt.views) as views
                 from (
                 select substring(path, 10) as title, count(*) as views
                 from log where path != '/' and status = '200 OK'
                 group by 1
                 order by views desc) as dt
                 join articles on
                 articles.slug = dt.title
                 join authors on
                 articles.author = authors.id
                 group by authors.name
                 order by views desc;"""

    data = execute_query(query)

    print("\nPrinting most popular authors of all time\n")
    for author, views in data:
        print('"{}" - {} views'.format(author, views))


def get_errors_above_one():

    query = """select day,
                 to_char(percentageOfErrors, '999D9%') as percentOfErrors
                 from (
                 select day,
                 round( cast(float8((numberOfErrors/totalHits::float) * 100)
                 as numeric), 1)
                 as percentageOfErrors
                 from (
                 select date(time) as day,
                 sum(case when status = '404 NOT FOUND' then 1 else 0 end)
                 as numberOfErrors,
                 count(*) as totalHits
                 from log
                 group by day) as dt ) as ddt
                 where percentageOfErrors > 1;"""

    data = execute_query(query)

    print("\nPrinting days that had errors above 1 percent\n")
    for day,percent in data:
        day = day.strftime('%m/%d/%Y')
        print('{} - {} errors'.format(day, percent.lstrip()))


if __name__ == '__main__':
    get_popular_articles()
    get_popular_authors()
    get_errors_above_one()
