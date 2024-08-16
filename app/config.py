class Config:
    # scrapy_demo 就是之前旅游爬虫教程中建的数据库，如果不清楚，可以去看之前的教程
    # 视频：https://www.bilibili.com/video/BV1Vx4y147wQ
    # 博客：https://blog.csdn.net/roccreed?type=blog
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:12345678@localhost/scrapy_demo?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False