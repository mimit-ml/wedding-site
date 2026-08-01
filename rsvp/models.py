from django.db import models

class RSVPResponse(models.Model):
    ATTENDANCE_CHOICES = [
        ('yes', 'Обязательно буду!'),
        ('no', 'К сожалению, не смогу'),
    ]

    name = models.CharField("Имя и фамилия", max_length=200)
    attendance = models.CharField("Присутствие", max_length=20, choices=ATTENDANCE_CHOICES)
    drinks = models.TextField("Напитки", blank=True, help_text="Выбранные напитки через запятую")
    created_at = models.DateTimeField("Дата заполнения", auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.get_attendance_display()}"

    class Meta:
        verbose_name = "Ответ гостя"
        verbose_name_plural = "Ответы гостей"
        ordering = ['-created_at']