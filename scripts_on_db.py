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
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject=subject).order_by('-date').first()

    if not Commendation.objects.filter(schoolkid=schoolkid,
                                       subject=subject).first():
        return Commendation.objects.create(
            text=random.choice(TEXTS),
            created=lesson.date,
            schoolkid=schoolkid,
            subject=subject,
            teacher=lesson.teacher,)


def get_user(FULL_NAME):
    try:
        return Schoolkid.objects.get(full_name__contains=FULL_NAME)
    except Subject.MultipleObjectsReturned:
        Schoolkid.objects.filter(full_name__contains=FULL_NAME).first()
    except Schoolkid.DoesNotExist:
        return None


def get_subject(FULL_NAME, TITLE):
    try:
        return Subject.objects.get(
            year_of_study=get_user(FULL_NAME).year_of_study,
            title=TITLE)
    except Subject.MultipleObjectsReturned:
        return Subject.objects.filter(
            year_of_study=get_user(FULL_NAME).year_of_study,
            title=TITLE).first()
    except Subject.DoesNotExist:
        return None


def main():
    FULL_NAME = input(str("Введити ФИО ученика:"))
    TITLE = input(str("Введите учебный предмет:"))

    if get_user(FULL_NAME) is None:
        print(f'Ученик с именем "{FULL_NAME}" не найден.')
    elif get_subject(FULL_NAME, TITLE) is None:
        print(f'Учебный предмет "{TITLE}" не найден.')
    else:
        fix_marks(get_user(FULL_NAME))
        remove_chastisements(get_user(FULL_NAME))
        create_commendation(get_user(FULL_NAME),
                            get_subject(FULL_NAME, TITLE))
        print("""
Из журнала удалены двойки и тройки
Плохие комментарии от учителя удалены
Положительный комментарий к уроку добавлен
              """)


if __name__ == '__main__':
    main()
