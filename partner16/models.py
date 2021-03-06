from django.db import models

# Create your models here.
class LineUser(models.Model):
    line_id = models.CharField(max_length = 30)

    full_name = models.CharField(max_length = 30)

    nickname = models.CharField(max_length = 20)

    def __str__(self):
        return 'line_id: ' + self.line_id + ' | nickname: ' + self.nickname

# 現在是 KeyWord group 的概念
class Statement(models.Model):
    main_type = models.CharField(max_length = 20)

    sub_type = models.CharField(max_length = 20)

    enable = models.BooleanField(default = True)

    def __str__(self):
        keyWordList = self.keyword_set.all()
        return 'main_type: ' + self.main_type + ' | sub_type: ' \
                + self.sub_type + ' | keyWordList: ' + str(keyWordList)


class Reply(models.Model):
    main_type = models.CharField(max_length = 20)

    sub_type = models.CharField(max_length = 20)

    reply_text = models.CharField(max_length = 200)

    enable = models.BooleanField(default = True)

    def __str__(self):
        return 'main_type: ' + self.main_type + ' | sub_type: ' \
                + self.sub_type + ' | reply_text: ' + self.reply_text

class Communication(models.Model):
    statement = models.ManyToManyField(Statement, through='Statement_Flow')

    reply = models.ManyToManyField(Reply, through='Reply_Set')

    enable = models.BooleanField(default = True)

    def __str__(self):
        return 'id: ' + str(self.id) + ' | enable: ' + str(self.enable)

class KeyWord(models.Model):
    word = models.CharField(max_length = 50)

    count = models.IntegerField(default = 0)

    statement = models.ForeignKey(Statement, on_delete = models.CASCADE)

    def __str__(self):
        return self.word


# 自定義 Statement 與 Communication 多對多關聯
class Statement_Flow(models.Model):
    statement = models.ForeignKey(Statement, on_delete = models.CASCADE)

    communication = models.ForeignKey(Communication, on_delete = models.CASCADE)

    flow_order = models.IntegerField(default = 0)

    def __str__(self):
        return 'statement: ' + str(self.statement) + ' | flow_order: ' \
                + str(self.flow_order)

# 自定義 Reply 與 Communication 多對多關聯
class Reply_Set(models.Model):
    reply = models.ForeignKey(Reply, on_delete = models.CASCADE)

    communication = models.ForeignKey(Communication, on_delete = models.CASCADE)

    set_order = models.IntegerField(default = 0)

    def __str__(self):
        return 'reply: ' + str(self.reply) + ' | set_order: ' + \
                str(self.set_order)
