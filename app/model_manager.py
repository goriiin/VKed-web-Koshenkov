from django.core.paginator import Paginator

from app.models import Question, Tag, Answer


def index_news():
    return Question.objects.news()


def tag_news(tag):
    return Question.objects.filter(tags__tag_name=tag)


def hot_news():
    return Question.objects.hot()


def check_page(request):
    try:
        page = int(request.GET['page'])
        if page < 1:
            return 1
    except:
        return 1

    return page


def pagination(request, type_req, count=4, tag_name=None):
    page_num = check_page(request)

    if type_req == 'index':
        items = index_news()
    elif type_req == 'tag':
        items = tag_news(tag_name)
    elif type_req == 'hot':
        items = hot_news()

    paginator = Paginator(items, count)
    items = paginator.get_page(page_num)

    return {'questions': items,
            'paginator': paginator}


def this_question(request, question_id, count=4):
    page_num = check_page(request)
    try:
        question = Question.objects.get(pk=question_id)
    except:
        return {'page': -1}

    tags = question.tags.all()
    answers = Answer.objects.filter(question=question_id).order_by('-likes_count')

    paginator = Paginator(answers, count)
    answers = paginator.get_page(page_num)

    return {
        'question': question, 'tags': tags, 'answers': answers,
        'paginator': paginator, 'page': 0
    }
