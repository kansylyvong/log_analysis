import psycopg2
import datetime


def get_popular_articles():

    db = psycopg2.connect("dbname=news")

    c = db.cursor()

    c.execute("""select articles.title, dt.views
                 from (
                 select substring(path, 10) as title, count(*) as views
                 from log where path != '/' and status = '200 OK'
                 group by 1 order by views desc limit 3 ) as dt
                 join articles on
                 articles.slug = dt.title
                 order by dt.views desc;""")

    data = c.fetchall()
    print("\nPrinting three most popular articles of all time\n")
    for datum in data:
        print("\"%s\" -- %s views" % (datum[0], datum[1]))
    db.close()


def get_popular_authors():

    db = psycopg2.connect("dbname=news")

    c = db.cursor()

    c.execute("""select authors.name, sum(dt.views) as views
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
                 order by views desc;""")

    data = c.fetchall()
    print("\nPrinting most popular authors of all time\n")
    for datum in data:
        print("\"%s\" -- %s views" % (datum[0], datum[1]))
    db.close()


def get_errors_above_one():

    db = psycopg2.connect("dbname=news")

    c = db.cursor()

    c.execute("""select day,
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
                 where percentageOfErrors > 1;""")

    data = c.fetchall()
    print("\nPrinting days that had errors above 1 percent\n")
    for datum in data:
        day = datum[0]
        day = day.strftime('%m/%d/%Y')
        print("%s -- %s errors" % (day, datum[1].lstrip()))
    db.close()


get_popular_articles()
get_popular_authors()
get_errors_above_one()
