from django.shortcuts import render
from django.http import JsonResponse
from . import Eight_Puzzle_AStar as solver

def index(request):

    if request.method == 'GET' and 'init' in request.GET and 'goal' in request.GET:
        init = request.GET.get('init')
        goal = request.GET.get('goal')

        temp = init.split("\n")
        init = []
        for i in temp:
            init.append(i.split(","))
        for row in range(len(init)):
            for col in range(len(init)):
                init[row][col] = int(init[row][col])
        
        temp = goal.split("\n")
        goal = []
        for i in temp:
            goal.append(i.split(","))
        for row in range(len(goal)):
            for col in range(len(goal)):
                goal[row][col] = int(goal[row][col])

        p = solver.Puzzle(init, goal)
        result = p.solve()
        result = result.replace("\n", "<br>")
        result = result.replace("—————————————", "————————")
        result = result.replace("| ", "|&nbsp;&nbsp;&nbsp;")
        result = result.replace(" |", "&nbsp;&nbsp;&nbsp;|")

        return JsonResponse(
            {
                'result': result,
            },
            status = 200
        )

    return render(request, 'index.html')