from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from datetime import datetime, timedelta
import json
import os
import subprocess
import webbrowser
from threading import Timer

app = Flask(__name__)

# ============================================================
# ПАЛИТРА ЦВЕТОВ (расширенная)
# ============================================================
palette = {
    # ===== РОЗОВЫЕ И ЯГОДНЫЕ ОТТЕНКИ =====
    "Ягодный розовый": "#c66f80",
    "Увядшая роза": "#b35a6c",
    "Пыльно-розовый": "#e8afba",
    "Зефирный розовый": "#f7d6db",
    "Лавандово-белый": "#fff0f5",
    "Пастельный брусничный": "#d99fa5",
    "Марсала": "#a0525a",
    "Нежная роза": "#fce4ec",
    "Пудровый розовый": "#f8d7da",
    "Кораллово-розовый": "#e8a8a8",
    "Розовый кварц": "#f6b8c0",
    "Тёплый розовый": "#f0c0c8",

    # ===== ЗЕЛЁНЫЕ И ОЛИВКОВЫЕ ОТТЕНКИ =====
    "Глубокий хвойный": "#3b5235",
    "Тёмно-зелёный (хаки)": "#4a6644",
    "Сухой шалфей": "#899464",
    "Оливково-зелёный": "#9faa74",
    "Светлый полынный": "#c5c99e",
    "Светло-оливковый": "#d7dab3",
    "Мятный": "#b8d0a3",
    "Шалфей": "#769455",
    "Лесной мох": "#5a7a4a",
    "Травяной": "#7a9a5a",
    "Мохнатый зелёный": "#8aaa6a",
    "Пастельный зелёный": "#c8e0c0",
    "Мятно-зелёный": "#b0d4b0",
    "Фисташковый": "#b8c99e",

    # ===== БЕЖЕВЫЕ И КРЕМОВЫЕ ОТТЕНКИ =====
    "Льняной": "#e2d7c5",
    "Кремовый": "#ece3d2",
    "Слоновая кость": "#f4efe3",
    "Тёплый бежевый": "#e8dcc8",
    "Песочный": "#ddd0b8",
    "Ванильный": "#f0e6d3",
    "Шампань": "#f5eddc",
    "Пергамент": "#e8ddc8",
    "Молочный": "#f5f0e8",

    # ===== СИНИЕ И ГОЛУБЫЕ ОТТЕНКИ =====
    "Небесно-голубой": "#b8d4e8",
    "Мягкий голубой": "#c8dce8",
    "Пыльный голубой": "#a8c0d0",
    "Лавандовый": "#c8c0d8",
    "Серо-голубой": "#b0bcc8",
    "Пастельный голубой": "#d0e0ec",
    "Морская волна": "#a0c8c8",

    # ===== ТЁПЛЫЕ И ЗЕМЛИСТЫЕ ОТТЕНКИ =====
    "Терракотовый": "#c4886a",
    "Кирпичный": "#b87060",
    "Карамельный": "#d4a880",
    "Медовый": "#e0b890",
    "Ореховый": "#b89878",
    "Пряничный": "#d4b090",
    "Тыквенный": "#e8b880",
}

# ============================================================
# ФАЙЛЫ ДЛЯ ХРАНЕНИЯ
# ============================================================
STUDENTS_FILE = 'students.json'
SCHEDULE_FILE = 'schedule.json'
HABITS_FILE = 'habits.json'
GOALS_FILE = 'goals.json'
EGE_FILE = 'ege.json'
EGE_PLANNER_FILE = 'ege_planner_data.json'
EGE_CALENDAR_FILE = 'ege_calendar.json'
TASKS_DAY_FILE = 'tasks_day.json'

# ============================================================
# ДАННЫЕ
# ============================================================
students = []
schedule = {}
habits = []
goals = []
ege_data = {}
tasks_day = {}

# Данные ЕГЭ-планера
ege_planner_data = {
    "subjects": {
        "math": {
            "name": "Профильная математика",
            "color": "#b35a6c",
            "icon": "📐",
            "tasks": [],
            "exams": [],
            "progress": 0
        },
        "russian": {
            "name": "Русский язык",
            "color": "#c66f80",
            "icon": "📖",
            "tasks": [],
            "exams": [],
            "progress": 0
        },
        "physics": {
            "name": "Физика",
            "color": "#4a6644",
            "icon": "⚡",
            "tasks": [],
            "exams": [],
            "progress": 0
        },
        "informatics": {
            "name": "Информатика",
            "color": "#899464",
            "icon": "💻",
            "tasks": [],
            "exams": [],
            "progress": 0
        }
    }
}

# Данные ЕГЭ-календаря
ege_calendar = {}

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekdays_ru = {
    "Monday": "Понедельник",
    "Tuesday": "Вторник",
    "Wednesday": "Среда",
    "Thursday": "Четверг",
    "Friday": "Пятница",
    "Saturday": "Суббота",
    "Sunday": "Воскресенье"
}

START_HOUR = 7
END_HOUR = 23


# ============================================================
# ФУНКЦИИ СОХРАНЕНИЯ/ЗАГРУЗКИ
# ============================================================
def save_students():
    with open(STUDENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(students, f, ensure_ascii=False, indent=2)


def load_students():
    global students
    if os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
            students = json.load(f)
    else:
        students = []


def save_schedule():
    with open(SCHEDULE_FILE, 'w', encoding='utf-8') as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)


def load_schedule():
    global schedule
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
            schedule = json.load(f)
    else:
        schedule = {}


def save_habits():
    with open(HABITS_FILE, 'w', encoding='utf-8') as f:
        json.dump(habits, f, ensure_ascii=False, indent=2)


def load_habits():
    global habits
    if os.path.exists(HABITS_FILE):
        with open(HABITS_FILE, 'r', encoding='utf-8') as f:
            habits = json.load(f)
    else:
        habits = []


def save_goals():
    with open(GOALS_FILE, 'w', encoding='utf-8') as f:
        json.dump(goals, f, ensure_ascii=False, indent=2)


def load_goals():
    global goals
    if os.path.exists(GOALS_FILE):
        with open(GOALS_FILE, 'r', encoding='utf-8') as f:
            goals = json.load(f)
    else:
        goals = []


def save_ege():
    with open(EGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(ege_data, f, ensure_ascii=False, indent=2)


def load_ege():
    global ege_data
    if os.path.exists(EGE_FILE):
        with open(EGE_FILE, 'r', encoding='utf-8') as f:
            ege_data = json.load(f)
    else:
        ege_data = {}


def save_ege_planner():
    with open(EGE_PLANNER_FILE, 'w', encoding='utf-8') as f:
        json.dump(ege_planner_data, f, ensure_ascii=False, indent=2)


def load_ege_planner():
    global ege_planner_data
    if os.path.exists(EGE_PLANNER_FILE):
        with open(EGE_PLANNER_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for subject in ege_planner_data["subjects"]:
                if subject in data.get("subjects", {}):
                    ege_planner_data["subjects"][subject].update(data["subjects"][subject])


def save_ege_calendar():
    with open(EGE_CALENDAR_FILE, 'w', encoding='utf-8') as f:
        json.dump(ege_calendar, f, ensure_ascii=False, indent=2)


def load_ege_calendar():
    global ege_calendar
    if os.path.exists(EGE_CALENDAR_FILE):
        with open(EGE_CALENDAR_FILE, 'r', encoding='utf-8') as f:
            ege_calendar = json.load(f)
    else:
        ege_calendar = {}


def save_tasks_day():
    with open(TASKS_DAY_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks_day, f, ensure_ascii=False, indent=2)


def load_tasks_day():
    global tasks_day
    if os.path.exists(TASKS_DAY_FILE):
        with open(TASKS_DAY_FILE, 'r', encoding='utf-8') as f:
            tasks_day = json.load(f)
    else:
        tasks_day = {}


# Загружаем данные
load_students()
load_schedule()
load_habits()
load_goals()
load_ege()
load_ege_planner()
load_ege_calendar()
load_tasks_day()


# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================
def get_week_dates(week_offset=0):
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week += timedelta(weeks=week_offset)
    week_dates = {}
    for i, day in enumerate(weekdays):
        current_date = start_of_week + timedelta(days=i)
        week_dates[day] = {
            "formatted": current_date.strftime("%d.%m.%Y"),
            "iso": current_date.strftime("%Y-%m-%d")
        }
    return week_dates


# Функция очистки старых дел (вызывать при каждом обращении)
def clean_old_tasks():
    global tasks_day
    today = datetime.now().date().isoformat()
    # Удаляем все дела, которые не относятся к сегодняшнему дню
    tasks_day = {today: tasks_day.get(today, [])}
    save_tasks_day()


# ============================================================
# ГЛАВНЫЙ МАРШРУТ
# ============================================================
@app.route("/")
def index():
    week_offset = int(request.args.get('week', 0))
    week_dates = get_week_dates(week_offset)
    current_date = datetime.now().date() + timedelta(weeks=week_offset)
    selected_date = current_date.isoformat()
    weekday_index = current_date.weekday()
    current_day_name = weekdays[weekday_index]
    date_formatted = week_dates[current_day_name]["formatted"]
    clean_old_tasks()

    week_schedule = {}
    for day, date_info in week_dates.items():
        date_iso = date_info["iso"]
        week_schedule[day] = schedule.get(date_iso, [])

    today_str = datetime.now().date().isoformat()

    return render_template("schedule.html",
                           schedule=week_schedule,
                           full_schedule=schedule,
                           weekdays=weekdays,
                           weekdays_ru=weekdays_ru,
                           students=students,
                           palette=palette,
                           start_hour=START_HOUR,
                           end_hour=END_HOUR,
                           week_offset=week_offset,
                           week_dates=week_dates,
                           selected_date=selected_date,
                           current_day_iso=selected_date,
                           date_formatted=date_formatted,
                           habits=habits,
                           goals=goals,
                           ege_data=ege_data,
                           tasks_day=tasks_day,
                           now_str=today_str)


# ============================================================
# ДОБАВЛЕНИЕ СОБЫТИЯ (главный календарь)
# ============================================================
@app.route("/add_event", methods=["POST"])
def add_event():
    day = request.form.get("day")
    student_name = request.form.get("student")
    comment = request.form.get("comment", "").strip()
    week_offset = request.form.get('week_offset', 0)

    if not day:
        return "Ошибка: дата не передана", 400

    student = next((s for s in students if s["name"] == student_name), None)
    if not student:
        return f"Ошибка: ученик '{student_name}' не найден", 400

    start = request.form.get("start")
    end = request.form.get("end")

    event = {
        "student": student["name"],
        "subject": student["subject"],
        "color": student["color"],
        "start": start,
        "end": end,
        "size": student.get("size", "medium"),
        "comment": comment,
        "date": day,
        "category": student.get("category", "Ученик")
    }

    if day not in schedule or not isinstance(schedule[day], list):
        schedule[day] = []

    schedule[day].append(event)
    save_schedule()

    print(f"✅ СОБЫТИЕ ДОБАВЛЕНО на {day}: {event['student']} {event['start']}-{event['end']}")

    return redirect(url_for("index", week=week_offset))


# ============================================================
# ОБНОВЛЕНИЕ СОБЫТИЯ (главный календарь)
# ============================================================
@app.route("/update_event", methods=["POST"])
def update_event():
    day = request.form.get("day")
    index = int(request.form.get("index"))
    new_start = request.form.get("start")
    new_end = request.form.get("end")
    comment = request.form.get("comment", "").strip()
    week_offset = request.form.get('week_offset', 0)

    if day in schedule and isinstance(schedule[day], list) and 0 <= index < len(schedule[day]):
        schedule[day][index]["start"] = new_start
        schedule[day][index]["end"] = new_end
        schedule[day][index]["comment"] = comment
        save_schedule()
        print(f"✏️ ОБНОВЛЕНО событие на {day}")

    return redirect(url_for("index", week=week_offset))


# ============================================================
# УДАЛЕНИЕ СОБЫТИЯ (главный календарь)
# ============================================================
@app.route("/delete_event", methods=["POST"])
def delete_event():
    day = request.form.get("day")
    index = int(request.form.get("index"))
    week_offset = request.form.get('week_offset', 0)

    if day in schedule and isinstance(schedule[day], list) and 0 <= index < len(schedule[day]):
        del schedule[day][index]
        if len(schedule[day]) == 0:
            del schedule[day]
        save_schedule()
        print(f"🗑️ УДАЛЕНО событие на {day}")

    return redirect(url_for("index", week=week_offset))


# ============================================================
# УПРАВЛЕНИЕ УЧЕНИКАМИ
# ============================================================
@app.route("/students", methods=["GET", "POST"])
def manage_students():
    if request.method == "POST":
        name = request.form.get("name")
        subject = request.form.get("subject")
        size = request.form.get("size", "medium")
        color = request.form.get("color")
        category = request.form.get("category", "Ученик")

        if name and subject and color:
            students.append({
                "name": name,
                "subject": subject,
                "size": size,
                "color": color,
                "category": category
            })
            save_students()
            print(f"✅ Добавлен ученик: {name}")
        return redirect(url_for("manage_students"))

    return render_template("students.html", students=students, palette=palette)


@app.route("/remove_student/<name>", methods=["POST"])
def remove_student(name):
    global students
    students = [s for s in students if s["name"] != name]
    save_students()
    return redirect(url_for("manage_students"))


# ============================================================
# ПРИВЫЧКИ
# ============================================================
@app.route("/habits", methods=["GET", "POST"])
def manage_habits():
    global habits
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            habits.append({"name": name, "dates": []})
            save_habits()
        return redirect(url_for("manage_habits"))
    return render_template("habits.html", habits=habits)


@app.route("/toggle_habit", methods=["POST"])
def toggle_habit():
    data = request.get_json()
    habit_id = data.get("habit_id")
    date = data.get("date")
    if 0 <= habit_id < len(habits):
        if date in habits[habit_id]["dates"]:
            habits[habit_id]["dates"].remove(date)
        else:
            habits[habit_id]["dates"].append(date)
        save_habits()
        return jsonify({"success": True})
    return jsonify({"success": False}), 404


@app.route("/delete_habit", methods=["POST"])
def delete_habit():
    data = request.get_json()
    habit_id = data.get("habit_id")
    if 0 <= habit_id < len(habits):
        habits.pop(habit_id)
        save_habits()
        return jsonify({"success": True})
    return jsonify({"success": False}), 404


# ============================================================
# ЦЕЛИ
# ============================================================
@app.route("/goals", methods=["GET", "POST"])
def manage_goals():
    global goals
    if request.method == "POST":
        title = request.form.get("title")
        target = request.form.get("target")
        if title and target:
            goals.append({
                "title": title,
                "target": float(target),
                "current": 0,
                "created_at": datetime.now().isoformat()
            })
            save_goals()
        return redirect(url_for("manage_goals"))
    return render_template("goals.html", goals=goals)


@app.route("/update_goal", methods=["POST"])
def update_goal():
    data = request.get_json()
    goal_id = data.get("goal_id")
    value = data.get("value")
    if 0 <= goal_id < len(goals):
        goals[goal_id]["current"] = float(value)
        save_goals()
        return jsonify({"success": True})
    return jsonify({"success": False}), 404


@app.route("/delete_goal", methods=["POST"])
def delete_goal():
    data = request.get_json()
    goal_id = data.get("goal_id")
    if 0 <= goal_id < len(goals):
        goals.pop(goal_id)
        save_goals()
        return jsonify({"success": True})
    return jsonify({"success": False}), 404


# ============================================================
# ДЕЛА НА ДЕНЬ
# ============================================================
@app.route("/add_day_task", methods=["POST"])
def add_day_task():
    clean_old_tasks()
    text = request.form.get("text", "").strip()
    today = datetime.now().date().isoformat()

    if text:
        if today not in tasks_day or not isinstance(tasks_day[today], list):
            tasks_day[today] = []

        tasks_day[today].append({
            "text": text,
            "done": False,
            "created_at": datetime.now().isoformat()
        })
        save_tasks_day()
        print(f"✅ ДЕЛО ДОБАВЛЕНО: {text}")

    return redirect(url_for("index"))


@app.route("/toggle_day_task", methods=["POST"])
def toggle_day_task():
    clean_old_tasks()
    data = request.get_json()
    task_index = data.get("task_index")
    today = datetime.now().date().isoformat()

    if today in tasks_day and isinstance(tasks_day[today], list) and 0 <= task_index < len(tasks_day[today]):
        tasks_day[today][task_index]["done"] = not tasks_day[today][task_index]["done"]
        save_tasks_day()
        return jsonify({"success": True, "done": tasks_day[today][task_index]["done"]})
    return jsonify({"success": False}), 404


@app.route("/delete_day_task", methods=["POST"])
def delete_day_task():
    clean_old_tasks()
    data = request.get_json()
    task_index = data.get("task_index")
    today = datetime.now().date().isoformat()

    if today in tasks_day and isinstance(tasks_day[today], list) and 0 <= task_index < len(tasks_day[today]):
        del tasks_day[today][task_index]
        save_tasks_day()
        return jsonify({"success": True})
    return jsonify({"success": False}), 404


# ============================================================
# ЕГЭ (старая версия)
# ============================================================
@app.route("/ege", methods=["GET", "POST"])
def manage_ege():
    global ege_data
    if request.method == "POST":
        subject = request.form.get("subject")
        task_number = request.form.get("task_number")
        confidence = request.form.get("confidence", 5)
        solved = request.form.get("solved", 0)
        topic = request.form.get("topic", "")

        if subject and task_number:
            if subject not in ege_data:
                ege_data[subject] = {}
            ege_data[subject][task_number] = {
                "confidence": int(confidence),
                "solved": int(solved),
                "topic": topic
            }
            save_ege()
        return redirect(url_for("manage_ege"))
    return render_template("ege.html", ege_data=ege_data)


@app.route("/update_ege", methods=["POST"])
def update_ege():
    data = request.get_json()
    subject = data.get("subject")
    task_number = data.get("task_number")
    field = data.get("field")
    value = data.get("value")

    if subject in ege_data and task_number in ege_data[subject]:
        if field == "confidence":
            ege_data[subject][task_number]["confidence"] = int(value)
        elif field == "solved":
            ege_data[subject][task_number]["solved"] += int(value)
        elif field == "topic":
            ege_data[subject][task_number]["topic"] = value
        save_ege()
        return jsonify({"success": True})
    return jsonify({"success": False}), 404


@app.route("/delete_ege_task", methods=["POST"])
def delete_ege_task():
    data = request.get_json()
    subject = data.get("subject")
    task_number = data.get("task_number")
    if subject in ege_data and task_number in ege_data[subject]:
        del ege_data[subject][task_number]
        save_ege()
        return jsonify({"success": True})
    return jsonify({"success": False}), 404


# ============================================================
# ЕГЭ ЦЕНТР (НОВАЯ СТРАНИЦА)
# ============================================================
@app.route("/ege_center")
def ege_center():
    return render_template("ege_center.html")


# ============================================================
# ЕГЭ ПЛАНЕР
# ============================================================
@app.route("/ege_planner")
def ege_planner():
    return render_template("ege_planner.html",
                           data=ege_planner_data,
                           palette=palette)


@app.route("/api/ege_planner/add_task", methods=["POST"])
def add_ege_task():
    data = request.get_json()
    subject = data.get("subject")
    date = data.get("date")
    time = data.get("time")
    note = data.get("note", "")
    topics = data.get("topics", [])

    if subject in ege_planner_data["subjects"]:
        ege_planner_data["subjects"][subject]["tasks"].append({
            "date": date,
            "time": time,
            "note": note,
            "topics": topics,
            "completed": False
        })
        save_ege_planner()
        return jsonify({"success": True})
    return jsonify({"success": False}), 400


@app.route("/api/ege_planner/add_exam", methods=["POST"])
def add_ege_exam():
    data = request.get_json()
    subject = data.get("subject")
    date = data.get("date")
    score = data.get("score", 0)
    max_score = data.get("max_score", 100)

    if subject in ege_planner_data["subjects"]:
        ege_planner_data["subjects"][subject]["exams"].append({
            "date": date,
            "score": score,
            "max_score": max_score
        })
        save_ege_planner()
        return jsonify({"success": True})
    return jsonify({"success": False}), 400


@app.route("/api/ege_planner/update_progress", methods=["POST"])
def update_ege_progress():
    data = request.get_json()
    subject = data.get("subject")
    progress = data.get("progress")

    if subject in ege_planner_data["subjects"]:
        ege_planner_data["subjects"][subject]["progress"] = progress
        save_ege_planner()
        return jsonify({"success": True})
    return jsonify({"success": False}), 400


@app.route("/api/ege_planner/toggle_task", methods=["POST"])
def toggle_ege_task():
    data = request.get_json()
    subject = data.get("subject")
    task_index = data.get("task_index")

    if subject in ege_planner_data["subjects"]:
        tasks = ege_planner_data["subjects"][subject]["tasks"]
        if 0 <= task_index < len(tasks):
            tasks[task_index]["completed"] = not tasks[task_index]["completed"]
            save_ege_planner()
            return jsonify({"success": True, "completed": tasks[task_index]["completed"]})
    return jsonify({"success": False}), 400


@app.route("/api/ege_planner/delete_task", methods=["POST"])
def delete_ege_task_planner():
    data = request.get_json()
    subject = data.get("subject")
    task_index = data.get("task_index")

    if subject in ege_planner_data["subjects"]:
        tasks = ege_planner_data["subjects"][subject]["tasks"]
        if 0 <= task_index < len(tasks):
            del tasks[task_index]
            save_ege_planner()
            return jsonify({"success": True})
    return jsonify({"success": False}), 400


# ============================================================
# ЕГЭ КАЛЕНДАРЬ
# ============================================================
@app.route("/ege_calendar")
def ege_calendar_page():
    return render_template("ege_calendar.html",
                           ege_calendar=ege_calendar,
                           students=students,
                           palette=palette)


@app.route("/add_ege_event", methods=["POST"])
def add_ege_event():
    day = request.form.get("day")
    student_name = request.form.get("student")
    comment = request.form.get("comment", "").strip()
    done = request.form.get("done") == "true"

    if not day:
        return "Ошибка: дата не передана", 400

    # Проверяем, что это ЕГЭ-предмет
    ege_subjects = ['математика', 'русский', 'физика', 'информатика']
    is_ege_subject = any(subj in student_name.lower() for subj in ege_subjects)
    if not is_ege_subject:
        return "Ошибка: можно добавлять только ЕГЭ-предметы", 400

    student = next((s for s in students if s["name"] == student_name), None)
    if not student:
        color_map = {
            'математика': '#b35a6c',
            'русский': '#c66f80',
            'физика': '#4a6644',
            'информатика': '#899464'
        }
        color = '#b35a6c'
        for subj, col in color_map.items():
            if subj in student_name.lower():
                color = col
                break
        student = {
            "name": student_name,
            "subject": student_name,
            "color": color,
            "size": "medium",
            "category": "ЕГЭ"
        }

    start = request.form.get("start")
    end = request.form.get("end")

    event = {
        "student": student["name"],
        "subject": student["subject"],
        "color": student["color"],
        "start": start,
        "end": end,
        "size": student.get("size", "medium"),
        "comment": comment,
        "date": day,
        "category": "ЕГЭ",
        "done": done
    }

    if day not in ege_calendar or not isinstance(ege_calendar[day], list):
        ege_calendar[day] = []

    ege_calendar[day].append(event)
    save_ege_calendar()

    print(f"✅ СОБЫТИЕ ДОБАВЛЕНО в ЕГЭ-календарь на {day}: {event['student']} {event['start']}-{event['end']}")

    return redirect(url_for("ege_calendar_page"))


@app.route("/update_ege_event", methods=["POST"])
def update_ege_event():
    day = request.form.get("day")
    index = int(request.form.get("index"))
    new_start = request.form.get("start")
    new_end = request.form.get("end")
    comment = request.form.get("comment", "").strip()
    done = request.form.get("edit_done") == "on"

    if day in ege_calendar and isinstance(ege_calendar[day], list) and 0 <= index < len(ege_calendar[day]):
        ege_calendar[day][index]["start"] = new_start
        ege_calendar[day][index]["end"] = new_end
        ege_calendar[day][index]["comment"] = comment
        ege_calendar[day][index]["done"] = done
        save_ege_calendar()
        print(f"✏️ ОБНОВЛЕНО событие в ЕГЭ-календаре на {day}")

    return redirect(url_for("ege_calendar_page"))


@app.route("/delete_ege_event", methods=["POST"])
def delete_ege_event():
    day = request.form.get("day")
    index = int(request.form.get("index"))

    if day in ege_calendar and isinstance(ege_calendar[day], list) and 0 <= index < len(ege_calendar[day]):
        del ege_calendar[day][index]
        if len(ege_calendar[day]) == 0:
            del ege_calendar[day]
        save_ege_calendar()
        print(f"🗑️ УДАЛЕНО событие из ЕГЭ-календаря на {day}")

    return redirect(url_for("ege_calendar_page"))


# ============================================================
# ЕГЭ ПРОБНИКИ
# ============================================================
@app.route("/ege_exams")
def ege_exams():
    return render_template("ege_exams.html")


# ============================================================
# РАБОТА С ПАПКАМИ ЕГЭ
# ============================================================
@app.route("/get_folder_contents", methods=["POST"])
def get_folder_contents():
    data = request.get_json()
    folder_path = data.get("folder")

    base_path = r"C:\Users\yarus\Desktop\ЕГЭ_Подготовка"
    full_path = os.path.join(base_path, folder_path)

    try:
        if not os.path.exists(full_path):
            return jsonify({"error": f"Папка не найдена: {folder_path}"})

        files = []
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            is_folder = os.path.isdir(item_path)

            size = ""
            if not is_folder:
                size_bytes = os.path.getsize(item_path)
                if size_bytes < 1024:
                    size = f"{size_bytes} B"
                elif size_bytes < 1024 * 1024:
                    size = f"{size_bytes / 1024:.1f} KB"
                else:
                    size = f"{size_bytes / (1024 * 1024):.1f} MB"

            files.append({
                "name": item,
                "isFolder": is_folder,
                "size": size
            })

        files.sort(key=lambda x: (not x["isFolder"], x["name"].lower()))
        return jsonify({"files": files})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/open_file", methods=["POST"])
def open_file():
    data = request.get_json()
    folder = data.get("folder")
    filename = data.get("filename")

    base_path = r"C:\Users\yarus\Desktop\ЕГЭ_Подготовка"
    full_path = os.path.join(base_path, folder, filename)

    try:
        if not os.path.exists(full_path):
            return jsonify({"error": f"Файл не найден: {filename}"}), 404

        os.startfile(full_path)
        return jsonify({"success": True, "path": full_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# 12-НЕДЕЛЬНЫЙ СПРИНТ
# ============================================================
@app.route("/sprint")
def sprint():
    return render_template("sprint.html")


# ============================================================
# ЗАПУСК
# ============================================================
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5003")


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=True, port=5003)