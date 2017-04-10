from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.template import loader
from django.views import generic
from var_dump import var_dump

from .models import Quest, Question, Choise
from .forms import get_form


DATA_FORM = [
    {
        "name": "firstname",
        "label": "First Name",
        "type": "text",
        "max_length": 25,
        "required": 1
    },
    {
        "name": "lastname",
        "label": "Last Name",
        "type": "text",
        "max_length": 25,
        "required": 1
    },
    {
        "name": "smallcv",
        "label": "Small CV",
        "type": "textarea",
        "help_text": "Please insert a small CV"
    },
    {
        "name": "age",
        "label": "Age",
        "type": "integer",
        "max_value": 200,
        "min_value": 0
    },
    {
        "name": "marital_status",
        "label": "Marital Status",
        "type": "radio",
        "choices": [
            {"name": "Single", "value":"single"},
            {"name": "Married", "value":"married"},
            {"name": "Divorced", "value":"divorced"},
            {"name": "Widower", "value":"widower"}
        ]
    },
    {
        "name": "occupation",
        "label": "Occupation",
        "type": "select",
        "choices": [
            {"name": "Farmer", "value":"farmer"},
            {"name": "Engineer", "value":"engineer"},
            {"name": "Teacher", "value":"teacher"},
            {"name": "Office Clerk", "value":"office_clerk"},
            {"name": "Merchant", "value":"merchant"},
            {"name": "Unemployed", "value":"unemployed"},
            {"name": "Retired", "value":"retired"},
            {"name": "Other", "value":"other"}
        ]
    },
    {
        "name": "internet",
        "label": "Internet Access",
        "type": "checkbox"
    }
]



# Create your views here.
class IndexView(generic.ListView):
    template_name = 'quest/index.html'
    context_object_name = 'quest_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Quest.objects.all()

@csrf_exempt
def questions(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    questions = get_list_or_404(Question, quest=quest)
    choises = get_list_or_404(Choise, question__in=questions)

    data_form = []

    for index, q in enumerate(questions):
        questions[index].choises = [x for x in choises if x.question_id == q.id]

    var_dump(questions)

    for q in questions:
        data = {
            "name": "choise-{}".format(q.id),
            "label": q.question_text,
            "type": q.choise_type.type,
            "required": 1
        }

        chs = []

        if q.choises:
            for c in q.choises:
                chs.append({"name": c.choice_text, "value": c.id})

        data['choices'] = chs
        data_form.append(data)

    form_class = get_form(data_form)

    rdata = {}

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            rdata = form.cleaned_data
            var_dump(rdata)
    else:
        form = form_class()

    # var_dump(questions[0])
    # var_dump(data_form)

    return render(
        request=request,
        template_name="quest/questions.html",
        context={'questions': questions, "quest": quest, "form": form, "data": rdata}
    )
