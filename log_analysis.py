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

get_popular_articles()
get_popular_authors()
