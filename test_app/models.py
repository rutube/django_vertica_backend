# coding: utf-8

# $Id: $
from datetime import datetime
from decimal import Decimal
from django.db import models


class PlatformReport(models.Model):
    """ Данные отчетов по площадка.
    """
    date = models.DateField("Дата", default=datetime.now)
    platform_id = models.IntegerField(verbose_name="Площадка")
    video_id = models.CharField(verbose_name="Видео", max_length=32)
    video_views = models.PositiveIntegerField("Количество показов видео",
                                              default=0, db_index=True)
    adv_views = models.PositiveIntegerField("Количество показов рекламы",
                                            default=0, db_index=True)
    income = models.DecimalField("Заработок", max_digits=12, decimal_places=4,
                                 default=Decimal("0.0000"), db_index=True)
    approved = models.BooleanField("Отчет утвержден", default=False)

    class Meta:

        db_table = "reports_platformreport"
        verbose_name = "Отчет по площадке"
        verbose_name_plural = "Отчеты по площадкам"
        unique_together = ("date", "platform_id", "video_id")

    def __unicode__(self):
        return '[%s] pid=%s vid=%s' % (self.date, self.platform_id, self.video_id)
