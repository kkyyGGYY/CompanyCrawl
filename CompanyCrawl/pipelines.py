from .models.models import CompanyType
from w3lib.html import remove_tags

class CompanycrawlPipeline(object):
    def process_item(self, item, spider):
        return item


class ElasticSearchPipeline(object):
    # 写入数据到es中
    def process_item(self, item, spider):
        # 将item转换为es的数据

        # company = CompanyType()
        # company.company_name = item['company_name']
        # company.crn = item['crn']
        # company.organization_type = item['organization_type']
        # company.faren = item['faren']
        # company.registered_capital = item['registered_capital']
        # company.company_type = item['company_type']
        # company.registration_state = item['registration_state']
        # company.former_name = item['former_name']
        # company.searched_by = item['searched_by']
        # company.data_count = str(item['data_count'])
        # company.establishment_date = item['establishment_date']
        # company.abstract = item['abstract']

        # company.save()

        item.save_to_es()

        return item

    # def analyze_tokens(self, text):
    #     from .models.models import connections
    #     es = connections.get_connection(ArticleType._doc_type.using)
    #     index = ArticleType._doc_type.index
    #
    #     if not text:
    #         return []
    #     global used_words
    #     result = es.indices.analyze(index=index, analyzer='ik_max_word',
    #                                 params={'filter': ['lowercase']}, body=text)
    #
    #     words = set([r['token'] for r in result['tokens'] if len(r['token']) > 1])
    #
    #     new_words = words.difference(used_words)
    #     used_words.update(words)
    #     return new_words
    #
    # @classmethod
    # def from_settings(cls, settings):
    #     dbparms = dict(
    #         host=settings["MYSQL_HOST"],
    #         db=settings["MYSQL_DBNAME"],
    #         user=settings["MYSQL_USER"],
    #         passwd=settings["MYSQL_PASSWORD"],
    #         charset='utf8',
    #         cursorclass=MySQLdb.cursors.DictCursor,
    #         use_unicode=True,
    #     )
    #     dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
    #
    #     return cls(dbpool)
    #
    # def gen_suggests(self, title, tags):
    #     global used_words
    #     used_words = set()
    #     suggests = []
    #
    #     for item, weight in ((title, 10), (tags, 3)):
    #         item = self.analyze_tokens(item)
    #         if item:
    #             suggests.append({'input': list(item), 'weight': weight})
    #     return suggests
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     ext = cls()
    #     ext.settings = crawler.settings
    #     Article.init()
    #     return ext
    #
    #
    # def process_item(self, item, spider):
    #     article = Article()
    #     article.title = item["title"]
    #     article.create_date = item["create_date"]
    #     article.content = remove_tags(item["content"]).strip().replace("\r\n","").replace("\t","")
    #     article.front_image_url = item["front_image_url"]
    #     # article.front_image_path = item["front_image_path"]
    #     article.praise_nums = item["praise_nums"]
    #     article.comment_nums = item["comment_nums"]
    #     article.fav_nums = item["fav_nums"]
    #     article.url = item["url"]
    #     article.tags = item["tags"]
    #     article.id = item["url_object_id"]
    #
    #     title_suggest = self.gen_suggests(article.title, article.tags)
    #     article.title_suggest = title_suggest
    #
    #     article.save()
    #
    #     return item