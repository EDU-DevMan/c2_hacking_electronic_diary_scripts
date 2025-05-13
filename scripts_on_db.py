from datacenter.models import (Commendation, Mark,
                               Schoolkid, Subject,
                               Chastisement, Lesson)
import random


TEXTS = [
    "Молодец!",
    "Отлично!",
    "Хорошо!",
    "Гораздо лучше, чем я ожидал!",
    "Ты меня приятно удивил!",
    "Великолепно!",
    "Прекрасно!",
    "Ты меня очень обрадовал!",
    "Именно этого я давно ждал от тебя!",
    "Сказано здорово – просто и ясно!",
    "Ты, как всегда, точен!",
    "Очень хороший ответ!",
    "Талантливо!",
    "Ты сегодня прыгнул выше головы!",
    "Я поражен!",
    "Уже существенно лучше!",
    "Потрясающе!",
    "Замечательно!",
    "Прекрасное начало!",
    "Так держать!",
    "Ты на верном пути!",
    "Здорово!",
    "Это как раз то, что нужно!",
    "Я тобой горжусь!",
    "С каждым разом у тебя получается всё лучше!",
    "Мы с тобой не зря поработали!",
    "Я вижу, как ты стараешься!",
    "Ты растешь над собой!",
    "Ты многое сделал, я это вижу!",
    "Теперь у тебя точно все получится!",
    ]


def fix_marks(schoolkid):
    return Mark.objects.filter(schoolkid=schoolkid,
                               points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid):
    return Chastisement.objects.filter(
        schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject):
    created = Mark.objects.filter(
        schoolkid=schoolkid,
        subject=subject).order_by("-created").first().created

    teacher = Mark.objects.filter(
        schoolkid=schoolkid,
        subject=subject).order_by("-created").first().teacher

    if not Commendation.objects.filter(schoolkid=schoolkid,
                                       subject=subject).first():
        return Commendation.objects.create(
            text=random.choice(TEXTS),
            created=created,
            schoolkid=schoolkid,
            subject=subject,
            teacher=teacher,)


def main():
    FULL_NAME = input(str("Введити ФИО ученика:"))
    TITLE = input(str("Введите учебный предмет:"))

    try:
        schoolkid = Schoolkid.objects.get(full_name=FULL_NAME)
        subject = Subject.objects.get(
            year_of_study=schoolkid.year_of_study,
            title=TITLE)
        fix_marks(schoolkid.full_name)
        remove_chastisements(schoolkid.full_name)
        create_commendation(schoolkid, subject)
        print("""
Из журнала удалены двойки и тройки
Плохие комментарии от учителя удалены
Положительный комментарий к уроку добавлен""")

    except Schoolkid.DoesNotExist:
        print(f'Ученик с именем "{FULL_NAME}" не найден.')
    except Subject.DoesNotExist:
        print(f'Учебный предмет "{TITLE}" не найден.')


if __name__ == '__main__':
    main()
