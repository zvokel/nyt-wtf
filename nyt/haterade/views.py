
from django.shortcuts import render
import datetime

import pytz

eastern = pytz.timezone('US/Eastern')


from .models import Connections, SpellingBee, Wordle, LoggedRequest, Sudoku, Strands
from .cache import SpellingBeeCache, SudokuCache

# Create your views here.

from . import games

sb_cache = SpellingBeeCache(last_check=datetime.datetime(1970, 1, 1), date=datetime.date(1970, 1, 1), sb=SpellingBee(), first=True)
sudoku_cache = SudokuCache(last_check=datetime.datetime(1970, 1, 1), date=datetime.date(1970, 1, 1), sudoku=Sudoku(), first=True)


def log(request, endpoint):
    ip = None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')

    agent = request.META['HTTP_USER_AGENT']
    r = LoggedRequest(ip=ip, endpoint=endpoint, time=datetime.datetime.now(tz=eastern), agent=agent)
    r.save()


def index(request):

    log(request, 'i')
    return render(request, 'haterade/index.html', {})


def connections(request):
    eastern_time = datetime.datetime.now(tz=eastern)
    today = eastern_time.date()
    today_str = str(today)[0:10]

    try:
        c = Connections.objects.get(date=today)
    except:
        solution = games.get_connections(today_str)
        c = Connections(date=today, solution=solution)
        c.save()

    log(request, 'c')

    return render(request, 'haterade/connections.html', {'solution': c.solution, 'date': str(today)[0:10]})


def wordle(request):
    eastern_time = datetime.datetime.now(tz=eastern)
    today = eastern_time.date()
    today_str = str(today)[0:10]

    try:
        w = Wordle.objects.get(date=today)
    except:
        word = games.get_wordle(today_str)
        w = Wordle(date=today, word=word)
        w.save()

    log(request, 'w')

    return render(request, 'haterade/wordle.html', {'w': w, 'date': today_str})


def strands(request):

    eastern_time = datetime.datetime.now(tz=eastern)
    today = eastern_time.date()
    today_str = str(today)[0:10]

    try:
        s = Strands.objects.get(date=today)
        solution = s.solution
    except:
        solution = games.get_strands(today_str)
        s = Strands(date=today, solution=solution)
        s.save()

    return render(request, 'haterade/strands.html', {'strands': solution, 'date': today_str})


def spelling_bee(request):
    eastern_time = datetime.datetime.now(tz=eastern)
    today = eastern_time.date()

    if sb_cache.first:
        try:
            sbo = SpellingBee.objects.latest('date')
            if sbo is not None:
                sb_cache.sb = sbo
                sb_cache.date = sbo.date
        except:
            pass

    if today == sb_cache.date:
        # if we're looking for a date that's already cached, we're all set
        sb = sb_cache.sb
        date = sb_cache.date
    elif (sb_cache.last_check is None) or (datetime.datetime.now() - sb_cache.last_check > datetime.timedelta(hours=1)):
        # only check the times website once an hour
        words, date = games.get_spelling_bee()
        sb_cache.last_check = datetime.datetime.now()

        if sb_cache.date != date:
            # it's a new one, save it to db
            sb = SpellingBee(date=date, words=words)
            sb.save()

            # and to the cache
            sb_cache.sb = sb
            sb_cache.date = date
        else:
            # it's old, use the cached version
            sb = sb_cache.sb
    else:
        # use the cache!
        sb = sb_cache.sb
        date = sb_cache.date

    log(request, 'b')

    return render(request, 'haterade/spellingbee.html', {'sb': sb, 'date': str(date)[0:10]})


def sudoku(request):
    eastern_time = datetime.datetime.now(tz=eastern)
    today = eastern_time.date()


    if sudoku_cache.first:
        try:
            sdo = Sudoku.objects.latest('date')
            if sdo is not None:
                sudoku_cache.sb = sdo
                sudoku_cache.date = sdo.date
        except:
            pass

    if today == sudoku_cache.date:
        # if we're looking for a date that's already cached, we're all set
        sudoku = sudoku_cache.sudoku
        date = sudoku_cache.date

    elif (sudoku_cache.last_check is None) or (datetime.datetime.now() - sudoku_cache.last_check > datetime.timedelta(hours=1)):
        # only check the times website once an hour
        boards, date = games.get_sudoku()
        sudoku_cache.last_check = datetime.datetime.now()

        if sb_cache.date != date:
            # it's a new one, save it to db
            sudoku = Sudoku(date=date, boards=boards)
            sudoku.save()

            # and to the cache
            sudoku_cache.sudoku = sudoku
            sudoku_cache.date = date

        else:
            # it's old, use the cached version
            sudoku = sudoku_cache.sudoku

    else:
        # use the cache!
        sudoku = sudoku_cache.sudoku
        date = sudoku_cache.date

    boards = sudoku.boards
    results = {}

    for difficulty in ['easy', 'medium', 'hard']:
        solution = boards[difficulty]['puzzle_data']['solution']
        puzzle = boards[difficulty]['puzzle_data']['puzzle']
        results[difficulty] = []
        for i in range(len(solution)):
            results[difficulty].append({
                'number': solution[i],
                'given': solution[i] == puzzle[i]
            })

    log(request, 'k')

    return render(request, 'haterade/sudoku.html', {'sudoku': results, 'date': str(date)[0:10]})
