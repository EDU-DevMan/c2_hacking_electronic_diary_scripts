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


def get_user(FULL_NAME):
    try:
        return Schoolkid.objects.get(full_name=FULL_NAME)
    except Schoolkid.MultipleObjectsReturned:
        return Schoolkid.objects.filter(full_names=FULL_NAME).first()
    except Schoolkid.DoesNotExist:
        return False


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
        return False
    except AttributeError:
        return False


def get_lesson(FULL_NAME, TITLE):
    try:
        return Lesson.objects.filter(
            year_of_study=get_user(FULL_NAME).year_of_study,
            group_letter=get_user(FULL_NAME).group_letter,
            subject=get_subject(FULL_NAME, TITLE)).order_by('-date').first()
    except Lesson.DoesNotExist:
        return False
    except AttributeError:
        return False


def fix_marks(schoolkid):
    return Mark.objects.filter(schoolkid=schoolkid,
                               points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid):
    return Chastisement.objects.filter(
        schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject):

    if not Commendation.objects.filter(schoolkid=schoolkid,
                                       subject=subject).first():
        return Commendation.objects.create(
                text=random.choice(TEXTS),
                created=get_lesson(schoolkid.full_name, subject.title).date,
                schoolkid=schoolkid,
                subject=subject,
                teacher=get_lesson(schoolkid.full_name,
                                   subject.title).teacher,)


def main():
    FULL_NAME = input(str("Введити ФИО ученика:"))
    TITLE = input(str("Введите учебный предмет:"))

    schoolkid = get_user(FULL_NAME)
    subject = get_subject(FULL_NAME, TITLE)
    lesson = get_lesson(FULL_NAME, TITLE)

    if get_user(FULL_NAME):
        fix_marks(schoolkid)
        print("Плохие оценки удалены!")
        if subject:
            remove_chastisements(schoolkid)
            print("Плохие комментарии удалены!")
            if lesson:
                create_commendation(schoolkid, subject)
                print("К уроку добавлен положительный комментрий!")
            else:
                print("Урок не найден!")
        else:
            print(f'Учебный предмет {TITLE} не найден!')
    else:
        print(f'Ученик с именем {FULL_NAME} не найден!')


if __name__ == '__main__':
    main()