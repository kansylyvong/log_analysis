import psycopg2

def get_popular_articles():
    db = psycopg2.connect("dbname=news")

    c = db.cursor()

    c.execute("select articles.title, dt.views from (select substring(path, 10) as title, count(*) as views from log where path != '/' and status = '200 OK' group by 1 order by views desc limit 3 ) as dt join articles on articles.slug = dt.title order by dt.views desc;")

    data = c.fetchall()
    print(data)
    db.close()

def get_popular_authors():
    db = psycopg2.connect("dbname=news")

    c = db.cursor()

    c.execute("select authors.name, dt.views from (select substring(path, 10) as title, count(*) as views from log where path != '/' and status = '200 OK' group by 1 order by views desc) as dt join articles on articles.slug = dt.title join authors on articles.author = authors.id order by dt.views desc;")

    data = c.fetchall()
    print(data)
    db.close()

def get_errors_above_one():
    db = psycopg2.connect("dbname=news")

    c = db.cursor()

    c.execute("select day, to_char(percentageOfErrors, '999D9%') as percentOfErrors  from ( select day, round( cast( float8 ((numberOfErrors/totalHits::float) * 100) as numeric), 1) as percentageOfErrors from ( select date(time) as day, sum(case when status = '404 NOT FOUND' then 1 else 0 end) as numberOfErrors, count(*) as totalHits from log group by day) as dt ) as ddt where percentageOfErrors > 1;")

    data = c.fetchall()
    print(data)
    db.close()


get_errors_above_one()
get_popular_articles()
get_popular_authors()
